import datetime

import pandas as pd
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn


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

valid_study_columns = StudyColumn()
valid_series_columns = SeriesColumn()


def get_data_from_REMbox(rembox: REMboxDataQuery) -> tuple[pd.DataFrame, pd.DataFrame]:
    rembox.filter_options.set_inclusive_tags(
        machine_types=["DX"],
    )

    current_datetime = datetime.datetime.now(datetime.UTC)
    start_time = current_datetime - datetime.timedelta(days=7)

    # about four month data
    rembox.filter_options.study_time_interval_start_date = f"{start_time.strftime('%Y-%m-%d')}T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = f"{current_datetime.strftime('%Y-%m-%d')}T23:59:59Z"

    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.AccessionNumber,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            valid_study_columns.DoseAreaProductTotal,
            valid_study_columns.TotalNumberOfIrradiationEvents,
            valid_study_columns.TotalNumberOfRadiographicFrames,
        ]
    )

    return rembox.run_query()


def main(analysis_rule=None):
    study, _ = get_data_from_REMbox(rembox=rembox)

    result = study[valid_study_columns.DoseAreaProductTotal].min()
    triggering_studies = study[study[valid_study_columns.DoseAreaProductTotal] <= 1]

    plot_markers = ["circle", "square", "diamond", "cross", "x", "triangle", "pentagon", "hexagram", "star",
                    "hourglass", "bowtie", "asterisk"]

    plot_traces = [{
        "traceName": machine,
        "x": study[study[valid_study_columns.Machine] == machine][valid_study_columns.StudyDateTime].tolist(),
        "y": study[study[valid_study_columns.Machine] == machine][valid_study_columns.DoseAreaProductTotal].tolist(),
        "tolerance": None,
        "plotMarker": f"{plot_markers[ind // len(plot_markers)]}-open"
    } for ind, machine in enumerate(study[valid_study_columns.Machine].unique())]

    for ind, machine in enumerate(triggering_studies[valid_study_columns.Machine].unique()):
        output = {
            "analysisResult": {
                "analysisRuleId": "00000000-0000-0000-0000-000000000000",  # Ersätts med ID från jobbets meddelande
                "resultWithinTolerance": result <= 0,
                "analysisResultJson": {
                    "analysisResultType": "string",
                    "accessionNumber": study[valid_study_columns.AccessionNumber][
                        (study[valid_study_columns.Machine] == machine) & (
                                    study[valid_study_columns.DoseAreaProductTotal] <= 1)].values[0],
                    "studyInstanceUid": study[valid_study_columns.StudyInstanceUID][
                        (study[valid_study_columns.Machine] == machine) & (
                                    study[valid_study_columns.DoseAreaProductTotal] <= 1)].values[0],
                    "analysisDateTime": "0001-01-01T00:00:00Z",
                    "analysisResultValue": machine,
                    "withinTolerance": False,
                    "analysisResultPlotTraces": plot_traces,
                    "plotType": "scatter"
                }
            },
            "sendNotification": ind == 0,
            "notificationMessage": f"{machine} har DAP-värde som indikerar trasig DAP-mätare"
        }

        rembox.post_analysis_result(output)


if __name__ == "__main__":
    main()
