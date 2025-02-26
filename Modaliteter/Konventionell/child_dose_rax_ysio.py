from datetime import timedelta

import pandas as pd
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
from typing import Dict, List

CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"
TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

rembox = REMboxDataQuery(
    client_id_environment_variable=CLIENT_ID_ENV_VAR,
    client_secret_environment_variable=CLIENT_PWD_ENV_VAR,
    token_uri=TOKEN_URI,
    api_uri=API_URI,
    origin_uri=ORIGIN_URI,
    verify_ssl_cert=False
)


def get_data_from_REMbox(rembox: REMboxDataQuery,
                         procedures: List[str],
                         protocol: str,
                         study_descriptions: List[str]) -> pd.DataFrame:
    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()

    rembox.reset_filter_options()

    # Rax at NUS
    rembox.filter_options.set_inclusive_tags(machine_types=['DX'])

    if procedures:
        rembox.filter_options.set_inclusive_tags(procedures=procedures)

    if study_descriptions:
        rembox.filter_options.set_inclusive_tags(study_descriptions=study_descriptions)

    # exclude Acquisition protocols - positionsgenmomlysning
    rembox.filter_options.set_exclusive_tags(
        acquisition_protocols=['CP_Positioning', 'CP_Barn buk', 'Småskelett', 'Position Skellefteå']
    )

    # 2024 time period
    rembox.filter_options.study_time_interval_start_date = "2023-01-01T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = "2023-12-31T00:00:00Z"


    # age below 16 years
    rembox.filter_options.patient_age_interval_start_unit = 'Y'
    rembox.filter_options.patient_age_interval_end_value = 16
    rembox.filter_options.patient_age_interval_include_nulls = False

    # only patient with weigth data
    rembox.filter_options.patient_weight_in_kilograms_include_nulls = False

    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.AccessionNumber,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            valid_study_columns.StudyDescription,
            valid_study_columns.PatientAge,
            valid_study_columns.PatientsWeight,
            valid_study_columns.PatientsWeightDate,
            valid_study_columns.PatientsSize,
            valid_study_columns.DoseAreaProductTotal,
            valid_series_columns.AcquisitionProtocol,
            valid_series_columns.DoseAreaProduct,
            valid_series_columns.ExposureIndex,
            valid_series_columns.kVp,
            valid_series_columns.DistanceSourceToDetector,
            valid_series_columns.XrayFilterThicknessMaximum,
            valid_series_columns.Exposure,
            valid_series_columns.DistanceSourceToDetector,
            valid_series_columns.CollimatedFieldArea,
        ]
    )
    study_data, series_data = rembox.run_query()

    # Merge study and series
    data = series_data.merge(study_data, on=['studyInstanceUID'], how="left")

    # Remove zero DAP
    data = data[data['doseAreaProduct'] != 0]

    # Only protocol string in acquisition protocol
    data = data[data['acquisitionProtocol'].str.contains(protocol, case=False)]

    # calculate BMI
    data['bmi'] = 10000*data['patientsWeight'] / (data['patientsSize']*data['patientsSize'])

    # time between examination and weigth less than 1 year
    data = data[(data['studyDateTime'] - data['patientsWeightDate']) < timedelta(days=365)]

    # add system
    def _system_name(row):
         rax = ['L2', 'S01', 'S02', 'U204', 'U207', 'U208']
         ysio = ['LVILM', 'LTARNA', 'L4', 'S04', 'U205', 'U206']
         mira = ['L10', 'S12', 'U220', 'U221', 'U222']
         if row['machine'] in rax:
             val = 'Multitom Rax'
         elif row['machine'] in ysio:
             val = 'Ysio Max'
         elif row['machine'] in mira:
             val = 'Mira Max'
         else:
             val = ""

         return val

    data['system'] = data.apply(_system_name, axis=1)

    #  detector
    def _detector_type(row):
          if 'T ' in row['acquisitionProtocol']:
              val = 'T'
          elif 'D ' in row['acquisitionProtocol']:
              val = 'X'
          elif 'H ' in row['acquisitionProtocol']:
              val = 'H'
          elif 'L ' in row['acquisitionProtocol']:
              val = 'L'
          elif 'W' in row['acquisitionProtocol']:
              val = 'W'
          else:
              val = 'X'

          return val

    data['detector'] = data.apply(_detector_type, axis=1)


    return data


def format_for_export(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['region'] = 'Region Västerbotten'
    dataframe['aec_dose'] = ''
    dataframe['aec_dominant'] = ''
    dataframe['grid'] = ''

    export_list = ['region',
                   'examination',
                   'system',
                   'machine',
                   'projection',
                   'acquisitionProtocol',
                   'detector',
                   'kVp',
                   'exposure',
                   'aec_dose',
                   'aec_dominant',
                   'grid',
                   'distanceSourceToDetector',
                   'xrayFilterThicknessMaximum',
                   'doseAreaProduct',
                   'doseAreaProductTotal',
                   'exposureIndex',
                   'patientAge',
                   'patientsWeight']

    export_dataframe = dataframe[export_list]

    return export_dataframe


def save(data_collection: Dict):
    for projection, dataframe in data_collection.items():
        dataframe = format_for_export(dataframe)
        dataframe.to_csv(f"C:\\slask\\rax_ysio\\{projection}.csv", sep=";", decimal=",")


def include_projection(dataframe: pd.DataFrame, filtertag: str) -> pd.DataFrame:
    filtered_dataframe = dataframe[dataframe['acquisitionProtocol'].str.contains(filtertag, case=False)]

    return filtered_dataframe


def exclude_projection(dataframe: pd.DataFrame, filtertag: str) -> pd.DataFrame:
    filtered_dataframe = dataframe[~dataframe['acquisitionProtocol'].str.contains(filtertag, case=False)]

    return filtered_dataframe


def evaluate():
    hip = get_data_from_REMbox(rembox=rembox,
                               procedures=[],
                               protocol="Höftled",
                               study_descriptions=[])
    hip['examination'] = 'Höftleder'

    buk = get_data_from_REMbox(rembox=rembox,
                               procedures=[],
                               protocol="Buk",
                               study_descriptions=[])
    buk['examination'] = 'Buköversikt'
    buk = exclude_projection(dataframe=buk, filtertag="Lunga/buk")

    chest = get_data_from_REMbox(rembox=rembox,
                                 procedures=[],
                                 protocol="Lung",
                                 study_descriptions=[])
    chest['examination'] = 'Lungor - stående'
    chest = exclude_projection(dataframe=chest, filtertag="buk")
    chest = chest[~chest['detector'].str.contains('X')]

    lunga_buk = get_data_from_REMbox(rembox=rembox,
                                 procedures=[],
                                 protocol="Lunga/buk",
                                 study_descriptions=[])
    lunga_buk['examination'] = 'Lunga-buk'

    chest_laying = get_data_from_REMbox(rembox=rembox,
                                 procedures=[],
                                 protocol="",
                                 study_descriptions=["Lungor, liggande"])
    chest_laying = chest_laying[~chest_laying['detector'].str.contains('L')]
    chest_laying = chest_laying[~chest_laying['detector'].str.contains('W')]
    chest_laying = exclude_projection(dataframe=chest_laying, filtertag="buk")
    chest_laying['examination'] = 'Lungor - liggande'


    # projections
    hip_pelvis = include_projection(dataframe=hip, filtertag="höftleder")
    hip_pelvis.loc[:, 'projection'] = 'Bäcken'

    hip_frontal = include_projection(dataframe=hip, filtertag="frontal")
    hip_frontal = exclude_projection(dataframe=hip_frontal, filtertag="höftleder")
    hip_frontal.loc[:, 'projection'] = 'Höft frontal'

    hip_sida = include_projection(dataframe=hip, filtertag="sida")
    hip_sida.loc[:, 'projection'] = 'Höft axial'

    hip_lauenstein = include_projection(dataframe=hip, filtertag="lauenstein")
    hip_lauenstein.loc[:, 'projection'] = 'Höft Lauenstein'

    buk_sida = include_projection(dataframe=buk, filtertag='sida')
    buk_sida = pd.concat([buk_sida, include_projection(dataframe=buk, filtertag='upp')])
    buk_sida.loc[:, 'projection'] = 'Buk sida'

    buk_frontal = exclude_projection(dataframe=buk, filtertag="sida")
    buk_frontal = exclude_projection(dataframe=buk_frontal, filtertag="GML")
    buk_frontal = exclude_projection(dataframe=buk_frontal, filtertag="upp")
    buk_frontal.loc[:, 'projection'] = 'Buk frontal'

    chest_frontal = include_projection(dataframe=chest, filtertag="frontal")
    chest_frontal.loc[:, 'projection'] = 'Lungor frontal stående'
    chest_sida = include_projection(dataframe=chest, filtertag="sida")
    chest_sida.loc[:, 'projection'] = 'Lungor sida stående'

    lunga_buk_frontal = include_projection(dataframe=lunga_buk, filtertag="frontal")
    lunga_buk_frontal.loc[:, 'projection'] = 'Lunga-buk frontal'
    lunga_buk_sida = include_projection(dataframe=lunga_buk, filtertag="sida")
    lunga_buk_sida.loc[:, 'projection'] = 'Lunga-buk sida'

    chest_laying_frontal = include_projection(dataframe=chest_laying, filtertag="frontal")
    chest_laying_frontal.loc[:, 'projection'] = 'Lungor frontal liggande'
    chest_laying_sida = include_projection(dataframe=chest_laying, filtertag="sida")
    chest_laying_sida.loc[:, 'projection'] = 'Lungor sida liggande'

    data_collection = {
        "hip_frontal": hip_frontal,
        "hip_sida": hip_sida,
        "hip_pelvis": hip_pelvis,
        "hip_lauenstein": hip_lauenstein,
        "buk_frontal": buk_frontal,
        "buk_sida": buk_sida,
        "chest_frontal": chest_frontal,
        "chest_sida": chest_sida,
        "lunga_buk_frontal": lunga_buk_frontal,
        "lunga_buk_sida": lunga_buk_sida,
        "chest_laying_frontal": chest_laying_frontal,
        "chest_laying_sida": chest_laying_sida
    }

    save(data_collection)



if __name__ == '__main__':
    evaluate()
