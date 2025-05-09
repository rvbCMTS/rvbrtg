import pandas as pd
from rembox_integration_tools import REMboxDataQuery

from Rapportering.Arsstatistik.constants import (
    API_URI,
    COLUMN_SELECTION_PER_MODALITY,
    CLIENT_ID_ENV_VAR,
    CLIENT_PWD_ENV_VAR,
    MODALITY_FILTER_SELECTION_PER_MODALITY,
    ORIGIN_URI,
    TOKEN_URI,
)


def get_modality_data_for_year(year: int, modality: str) -> pd.DataFrame:
    rembox = REMboxDataQuery(
        client_id_environment_variable=CLIENT_ID_ENV_VAR,
        client_secret_environment_variable=CLIENT_PWD_ENV_VAR,
        token_uri=TOKEN_URI,
        api_uri=API_URI,
        origin_uri=ORIGIN_URI,
        verify_ssl_cert=False
    )

    rembox.filter_options.set_inclusive_tags(
        machine_types=MODALITY_FILTER_SELECTION_PER_MODALITY[modality]
    )

    rembox.filter_options.patient_age_interval_include_nulls = True

    rembox.filter_options.study_time_interval_start_date = "{}-01-01T00:00:00Z".format(year)
    rembox.filter_options.study_time_interval_end_date = "{}-12-31T00:00:00Z".format(year)

    rembox.add_columns(columns=COLUMN_SELECTION_PER_MODALITY[modality])

    study_data, _ = rembox.run_query()

    return study_data
