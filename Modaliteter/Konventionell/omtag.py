import pandas as pd
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
from typing import Dict, List
from collections import Counter


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
    verify_ssl_cert=False,
)


def get_data_from_REMbox(rembox: REMboxDataQuery) -> pd.DataFrame:

    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()

    rembox.reset_filter_options()

    rembox.filter_options.set_inclusive_tags(machine_types=['DX'],
                                             machines=['U204', 'U207', 'U208', 'L2', 'S01', 'S02'])


    rembox.filter_options.study_time_interval_start_date = "2024-01-01T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = "2024-06-30T00:00:00Z"


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
            valid_series_columns.IrradiationEventUID,
            valid_series_columns.DateTimeStarted,
            valid_series_columns.DoseAreaProduct,
            valid_series_columns.ExposureIndex,
            valid_series_columns.kVp,
            valid_series_columns.DistanceSourceToDetector,
            valid_series_columns.XrayFilterThicknessMaximum,
            valid_series_columns.Exposure,
            valid_series_columns.NumberOfPulses
        ]
    )
    study_data, series_data = rembox.run_query()

    # Merge study and series
    data = series_data.merge(study_data, on=['studyInstanceUID'], how="left")

    # Remove zero DAP
    data = data[data['doseAreaProduct'] != 0]


    return data


def repeat_analysis(data: pd.DataFrame) -> pd.DataFrame:
    summery_data = data.groupby(['studyInstanceUID']).agg(
            acquisition_count=('acquisitionProtocol', 'count'),
            unique_acquisition_count=('acquisitionProtocol', lambda x: len(set(x.values))),
            acquisition_list=('acquisitionProtocol', lambda x: list(x.values)),
            study_description=('studyDescription', 'first'),
        ).reset_index()
    
    summery_data['repeat_count'] = (
        summery_data['acquisition_count'] - summery_data['unique_acquisition_count']
    )

    summery_data['repeat_rate'] = summery_data['repeat_count'] / summery_data['acquisition_count'] * 100

    summery_data['repeat_acquisition_name'] = summery_data.apply(
        lambda row: [item for item, count in Counter(row['acquisition_list']).items() if count > 1],
        axis=1
    )

    # TODO: calcualte extra DAP for repeat acquisition
    
    return summery_data

def fluoroscopy_analysis(data: pd.DataFrame) -> pd.DataFrame:
    summery_data = data.groupby(['studyInstanceUID']).agg(
            acquisition_count=('acquisitionProtocol', 'count'),
            total_number_of_pulses=('numberOfPulses', 'sum'),
            median_number_of_pulses=('numberOfPulses', 'median'),
            acquisition_list=('acquisitionProtocol', lambda x: list(x.values)),
        ).reset_index()

    return summery_data


def evaluate():
    data = get_data_from_REMbox(rembox=rembox)

    position_fluoroscopy = [
        "CP_Positioning",
        "CP_Barn buk",
        "Småskelett",
        "Position Skellefteå",
        'CP_Vuxen esofagus',
        "CP_Shunt",
        'CP_antiiso',
    ]
    radiographic_frame = data[~data['acquisitionProtocol'].isin(position_fluoroscopy)]
    fluoroscopy = data[data['acquisitionProtocol'].isin(position_fluoroscopy)]

    repeat_data = repeat_analysis(data=radiographic_frame)
    fluoroscopy_data = fluoroscopy_analysis(data=fluoroscopy)

    combined_data = repeat_data.merge(fluoroscopy_data, on='studyInstanceUID', how='outer', suffixes=('_repeat', '_fluoroscopy'))
    combined_data['use_of_fluoroscopy'] = combined_data['total_number_of_pulses'] > 0 

    
    study_description_kpi = combined_data.groupby(['study_description', 'use_of_fluoroscopy']).agg(
        repeat_count_mean=('repeat_count', lambda x: x[x>0].mean()),
        examns_with_no_repeat=('repeat_count', lambda x: len(x[x == 0])),
        total_radiographic_frame=('acquisition_count_repeat', 'sum'),
        total_repeat_frame=('repeat_count', 'sum'),
        total_exams=('studyInstanceUID', 'count'),
    ).reset_index()

    study_description_kpi['success_rate'] = study_description_kpi['examns_with_no_repeat'] / study_description_kpi['total_exams'] * 100
    study_description_kpi['repeat_rate'] = study_description_kpi['total_repeat_frame'] / study_description_kpi['total_radiographic_frame'] * 100


                            



if __name__ == '__main__':
    evaluate()