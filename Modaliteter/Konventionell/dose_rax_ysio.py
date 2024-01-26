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
    origin_uri=ORIGIN_URI
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

    # 2022 time period
    rembox.filter_options.study_time_interval_start_date = "2022-01-01T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = "2022-12-31T00:00:00Z"

    # age from 16 years
    rembox.filter_options.patient_age_interval_start_unit = 'Y'
    rembox.filter_options.patient_age_interval_start_value = 16
    rembox.filter_options.patient_age_interval_include_nulls = False

    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            valid_study_columns.StudyDescription,
            valid_study_columns.PatientAge,
            valid_study_columns.TotalNumberOfIrradiationEvents,
            valid_study_columns.TotalNumberOfRadiographicFrames,
            valid_series_columns.AcquisitionProtocol,
            valid_series_columns.DoseAreaProduct,
            valid_series_columns.ExposureIndex,
            valid_series_columns.kVp,
            valid_series_columns.DistanceSourceToDetector,
            valid_series_columns.XrayFilterThicknessMaximum,
            valid_series_columns.Exposure,
        ]
    )
    study_data, series_data = rembox.run_query()

    # Merge study and series
    data = series_data.merge(study_data, on=['studyInstanceUID'], how="left")

    # Remove zero DAP
    data = data[data['doseAreaProduct'] != 0]

    # Only protocol string in acquisition protocol
    data = data[data['acquisitionProtocol'].str.contains(protocol, case=False)]

    return data


def group_data(data: pd.DataFrame) -> pd.DataFrame:
    agg_data = data.groupby("machine").agg({"doseAreaProduct": ['median', 'count'],
                                            "exposure": ["median"],
                                            "exposureIndex": ["median"],
                                            "patientAge": ["median"],
                                            "kVp": "median",
                                            "distanceSourceToDetector": "median",
                                            "xrayFilterThicknessMaximum": "median"})

    return agg_data


def save(data_collection: Dict):
    for projection, dataframe in data_collection.items():
        dataframe.to_csv(f"C:\\slask\\rax_ysio\\{projection}.csv", sep=";", decimal=",")


def projection(dataframe: pd.DataFrame, filtertag: str) -> pd.DataFrame:
    filtered_dataframe = dataframe[dataframe['acquisitionProtocol'].str.contains(filtertag, case=False)]

    return filtered_dataframe


def evaluate():
    pelvis = get_data_from_REMbox(rembox=rembox,
                                  procedures=["62600 Bäcken"],
                                  protocol="Bäcken",
                                  study_descriptions=[])


    chest = get_data_from_REMbox(rembox=rembox,
                                 procedures=[],
                                 protocol="Lung",
                                 study_descriptions=["Lungor", "Lungor, liggande", "Lunga-buk nyfödd"])



    hip = get_data_from_REMbox(rembox=rembox,
                               procedures=["63900 Höftled"],
                               protocol="Höftled",
                               study_descriptions=[])

    lumbar_spine = get_data_from_REMbox(rembox=rembox,
                                        procedures=["62300 Ländrygg", "62331 Ländrygg", "62332 Ländrygg"],
                                        protocol="Ländrygg",
                                        study_descriptions=[])


    # projections
    pelvis_frontal = pelvis[~pelvis['acquisitionProtocol'].str.contains("vrid", case=False)]
    pelvis_vridning = projection(dataframe=pelvis, filtertag="vrid")

    hip_frontal = projection(dataframe=hip, filtertag="frontal")
    hip_sida = projection(dataframe=hip, filtertag="sida")
    hip_vridning = projection(dataframe=hip, filtertag="vrid")

    lumbar_spine_frontal = projection(dataframe=lumbar_spine, filtertag="frontal")
    lumbar_spine_sida = projection(dataframe=lumbar_spine, filtertag="sida")
    lumbar_spine_vridning = projection(dataframe=lumbar_spine, filtertag="vrid")

    chest_frontal = projection(dataframe=chest, filtertag="frontal")
    chest_laying_frontal = projection(dataframe=chest_frontal, filtertag="D ")
    chest_frontal = chest_frontal[~chest_frontal['acquisitionProtocol'].str.contains("D ", case=False)]

    chest_sida = projection(dataframe=chest, filtertag="sida")
    chest_laying_sida = projection(dataframe=chest_sida, filtertag="D ")
    chest_sida = chest_sida[~chest_sida['acquisitionProtocol'].str.contains("D ", case=False)]

    data_collection = {
        "pelvis_frontal": group_data(pelvis_frontal),
        "pelvis_vridning": group_data(pelvis_vridning),
        "hip_frontal": group_data(hip_frontal),
        "hip_sida": group_data(hip_sida),
        "hip_vridning": group_data(hip_vridning),
        "lumbar_spine_frontal": group_data(lumbar_spine_frontal),
        "lumbar_spine_sida": group_data(lumbar_spine_sida),
        "lumbar_spine_vridning": group_data(lumbar_spine_vridning),
        "chest_frontal": group_data(chest_frontal),
        "chest_laying_frontal": group_data(chest_laying_frontal),
        "chest_sida": group_data(chest_sida),
        "chest_laying_sida": group_data(chest_laying_sida),
    }

    save(data_collection)



if __name__ == '__main__':
    evaluate()
