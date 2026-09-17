from datetime import time
from pathlib import Path
import pandas as pd
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
from typing import Dict, List

CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"
TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

MODALITY_MG: str = "MG"

MG_COL_PROJECTION = "Projection"
MG_COL_REJECT = "Reject"
MG_COL_TIME_OF_DAY = "TimeOfDay"
MG_COL_ANONYMOUS_USER_ID = "AnonymousUserId"

MG_PROJ_LPMLO = "LPMLO"
MG_PROJ_LNMLO = "LNMLO"
MG_PROJ_RPMLO = "RPMLO"
MG_PROJ_RNMLO = "RNMLO"
MG_PROJ_LPML = "LPML"
MG_PROJ_LNML = "LNML"
MG_PROJ_RPML = "RPML"
MG_PROJ_RNML = "RNML"
MG_PROJ_LCC = "LCC"
MG_PROJ_RCC = "RCC"

OUTPUT_CSV_PATH = Path("LocalOnly\\Mammografi screening omtag\\")
USER_DATA_PATH = Path("LocalOnly\\Mammografi screening omtag\\MammoPontus.xlsx")

VALID_STUDY_COLUMNS = StudyColumn()
VALID_SERIES_COLUMNS = SeriesColumn()


def get_data_from_REMbox(procedures: List[str],
                         study_descriptions: List[str]) -> pd.DataFrame:

    rembox = REMboxDataQuery(
    client_id_environment_variable=CLIENT_ID_ENV_VAR,
    client_secret_environment_variable=CLIENT_PWD_ENV_VAR,
    token_uri=TOKEN_URI,
    api_uri=API_URI,
    origin_uri=ORIGIN_URI,
    verify_ssl_cert=False
    )

    rembox.reset_filter_options()

    # All mammografi
    rembox.filter_options.set_inclusive_tags(machine_types=[MODALITY_MG])

    if procedures:
        rembox.filter_options.set_inclusive_tags(procedures=procedures)

    if study_descriptions:
        rembox.filter_options.set_inclusive_tags(study_descriptions=study_descriptions)

    # 2026 time period
    rembox.filter_options.study_time_interval_start_date = "2026-01-01T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = "2026-08-31T00:00:00Z"


    rembox.add_columns(
        columns=[
            VALID_STUDY_COLUMNS.Hospital,
            VALID_STUDY_COLUMNS.StudyDateTime,
            VALID_STUDY_COLUMNS.Machine,
            VALID_STUDY_COLUMNS.StudyDescription,
            VALID_STUDY_COLUMNS.AccessionNumber,
            VALID_STUDY_COLUMNS.PatientAge,
            VALID_STUDY_COLUMNS.PatientAgeUnit,
            VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
            VALID_STUDY_COLUMNS.PatientDbId,
            VALID_STUDY_COLUMNS.PatientsSex,
            VALID_STUDY_COLUMNS.ProcedureCode,
            VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
            VALID_SERIES_COLUMNS.kVp,
            VALID_SERIES_COLUMNS.CompressionThickness,
            VALID_SERIES_COLUMNS.PositionerPrimaryAngle,
            VALID_SERIES_COLUMNS.Exposure,
            VALID_SERIES_COLUMNS.Laterality,
            VALID_SERIES_COLUMNS.AverageGlandularDose,
        ]
    )
    study_data, series_data = rembox.run_query()

    # Merge study and series
    data = series_data.merge(study_data, on=['studyInstanceUID'], how="left")

    # clean accession number after merge to avoid duplicates
    data = data.drop(columns=["accessionNumber_x"])
    data = data.rename(columns={"accessionNumber_y": VALID_STUDY_COLUMNS.AccessionNumber})

    return data




def save(data_collection: Dict):
    for projection, df in data_collection.items():
        df.to_csv(OUTPUT_CSV_PATH.with_name(projection).with_suffix(".csv"), sep=";", decimal=",")

def _determine_mg_projection(data: pd.DataFrame) -> pd.DataFrame:
    data[MG_COL_PROJECTION] = pd.Series(dtype="str")
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-65, -40)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = MG_PROJ_RNMLO
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(40, 65)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = MG_PROJ_RPMLO
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-65, -40)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = MG_PROJ_LNMLO
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(40, 65)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = MG_PROJ_LPMLO

    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-95, -85)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = MG_PROJ_RNML
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(85, 95)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = MG_PROJ_RPML
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-95, -85)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = MG_PROJ_LNML
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(85, 95)
        & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = MG_PROJ_LPML

    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-5, 5) &
        data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = MG_PROJ_RCC
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-5, 5) &
        data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = MG_PROJ_LCC

    return data

def _determine_time_of_day(data: pd.DataFrame) -> pd.DataFrame:
    data[VALID_STUDY_COLUMNS.StudyDateTime] = pd.to_datetime(data[VALID_STUDY_COLUMNS.StudyDateTime])
    data[VALID_STUDY_COLUMNS.StudyDateTime] = data[VALID_STUDY_COLUMNS.StudyDateTime].dt.tz_convert('Europe/Stockholm')

    data[MG_COL_TIME_OF_DAY] = pd.Series(dtype="str")
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(6, 8),
        MG_COL_TIME_OF_DAY
    ] = "06-08"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(8, 10),
        MG_COL_TIME_OF_DAY
    ] = "08-10"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(10, 12),
        MG_COL_TIME_OF_DAY
    ] = "10-12"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(12, 14),
        MG_COL_TIME_OF_DAY
    ] = "12-14"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(14, 16),
        MG_COL_TIME_OF_DAY
    ] = "14-16"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(16, 18),
        MG_COL_TIME_OF_DAY
    ] = "16-18"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(0, 6),
        MG_COL_TIME_OF_DAY
    ] = "Övrig tid"
    data.loc[
        data[VALID_STUDY_COLUMNS.StudyDateTime].dt.hour.between(18, 24),
        MG_COL_TIME_OF_DAY
    ] = "Övrig tid"

    return data

def _read_user_data_from_xlsx(file_path: Path) -> pd.DataFrame:
    data = pd.read_excel(file_path, sheet_name="Sheet0", engine="openpyxl")
    data = data.rename(columns={"Accession Number": VALID_STUDY_COLUMNS.AccessionNumber})
    return data

def _make_anonymous_users(data: pd.DataFrame) -> pd.DataFrame:
    # Create a mapping of unique PatientDbId to anonymous IDs
    unique_ids = data["ID Check User"].unique()
    anon_mapping = {original_id: f"RSSK_{i+1}" for i, original_id in enumerate(unique_ids)}

    # Replace the original PatientDbId with the anonymous IDs
    data[MG_COL_ANONYMOUS_USER_ID] = data["ID Check User"].map(anon_mapping)

    return data

       
if __name__ == '__main__':
    rembox_data = get_data_from_REMbox(procedures=["66200 Mammografi", "66258 SCR Tekniskt omtag"],
                               study_descriptions=["Prime klin mammo"])

    user_data = _read_user_data_from_xlsx(USER_DATA_PATH)
    data = rembox_data.merge(user_data, on=[VALID_STUDY_COLUMNS.AccessionNumber], how="left")

    data = _determine_mg_projection(data)
    data[MG_COL_REJECT] = data.duplicated(subset=[VALID_STUDY_COLUMNS.AccessionNumber, MG_COL_PROJECTION], keep='first')
    
    data = _make_anonymous_users(data)
    data = _determine_time_of_day(data)


    data_per_month = pd.pivot_table(
        data,
        index=data[VALID_STUDY_COLUMNS.StudyDateTime].dt.to_period("M"),
        columns=VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
        aggfunc="size",
        fill_value=0
    )

    dose_per_month = (
        data.pivot_table(
            index=data[VALID_STUDY_COLUMNS.StudyDateTime].dt.to_period("M"),
            columns=MG_COL_REJECT,
            values=VALID_SERIES_COLUMNS.AverageGlandularDose,
            aggfunc="sum",
            fill_value=0
        )
        .rename(columns={
            False: "NonRejectDose",
            True: "RejectDose"
        })
    )

    rejects_per_month = pd.pivot_table(
        data,
        index=data[VALID_STUDY_COLUMNS.StudyDateTime].dt.to_period("M"),
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

    rejects_per_projection = pd.pivot_table(
        data,
        index=MG_COL_PROJECTION,
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

    rejects_per_machine = pd.pivot_table(
        data,
        index=VALID_STUDY_COLUMNS.Machine,
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

    rejects_per_user = pd.pivot_table(
        data,
        index=MG_COL_ANONYMOUS_USER_ID,
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

    rejects_per_time_of_day = pd.pivot_table(
        data,
        index=MG_COL_TIME_OF_DAY,
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

    rejects_per_compression_thickness = pd.pivot_table(
        data,
        index=VALID_SERIES_COLUMNS.CompressionThickness,
        columns=MG_COL_REJECT,
        aggfunc="size",
        fill_value=0
    )

data_to_save = {
    "data_per_month": data_per_month,
    "dose_per_month": dose_per_month,
    "rejects_per_month": rejects_per_month,
    "rejects_per_projection": rejects_per_projection,
    "rejects_per_machine": rejects_per_machine,
    "rejects_per_user": rejects_per_user,
    "rejects_per_time_of_day": rejects_per_time_of_day,
    "rejects_per_compression_thickness": rejects_per_compression_thickness
}

save(data_to_save)

