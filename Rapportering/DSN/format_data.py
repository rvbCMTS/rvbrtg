from datetime import timedelta

import pandas as pd

from Rapportering.DSN.constants import (
    VALID_STUDY_COLUMNS, EXAM_GROUPING_RULES_BY_MODALITY, EXAM_GROUPING_TYPE_PROTOCOL_CODE,
    EXAM_GROUPING_TYPE_STUDY_DESCRIPTION, EXAM_GROUPING_TYPE_PROCEDURE_CODE, VALID_SERIES_COLUMNS, OUTPUT_COL_EXAM,
    EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL, MODALITY_CT,
)


def format_data(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    data = _sanity_check_patient_bmi(data)

    if modality == MODALITY_CT:
        return _format_ct_data(data)

    raise  NotImplementedError(f"Modality {modality} not implemented.")


def _format_ct_data(data: pd.DataFrame) -> pd.DataFrame:
    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_CT)

    return data[[
        VALID_SERIES_COLUMNS.MeanCTDIvol,
        VALID_SERIES_COLUMNS.DlPv,
        VALID_SERIES_COLUMNS.SizeSpecificDoseEstimation,
        VALID_STUDY_COLUMNS.PatientAge,
        VALID_STUDY_COLUMNS.PatientsSex,
        VALID_STUDY_COLUMNS.PatientsSize,
        VALID_STUDY_COLUMNS.PatientsWeight,
        VALID_SERIES_COLUMNS.AcquisitionProtocol,
        VALID_STUDY_COLUMNS.Machine,
        OUTPUT_COL_EXAM
    ]]


def _format_dx_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data[VALID_STUDY_COLUMNS.DoseAreaProductTotal] > 0]  # Remove data where DAP meter broken


def _filter_for_size_and_weight_date_intervals_relative_study_datetime(data: pd.DataFrame) -> pd.DataFrame:
    data["SizeDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsSizeDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])
    data["WeightDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsWeightDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])

    data["KeepRow"] = True
    data.KeepRow[
        (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == "Y") &  # Filters for patients that are at least 1 years old
        ((data["SizeDateDiff"] > timedelta(days=365)) | (data["WeightDateDiff"] > timedelta(days=365)))
    ] = False

    data.KeepRow[
        (data[VALID_STUDY_COLUMNS.PatientAgeUnit] != "Y") &  # Filters for patients that are below 1 year
        ((data["SizeDateDiff"] > timedelta(days=30)) | (data["WeightDateDiff"] > timedelta(days=30)))
    ] = False

    return data

def _sanity_check_patient_bmi(data: pd.DataFrame) -> pd.DataFrame:
    """Throws away data for patients with an unreasonable value for the BMI

    Parameters
    ----------
    data
        the REMbox data to be sanitized

    Returns
    -------
    A copy of the original dataframe with added column for BMI and rows with unreasonable values dropped
    """
    data["BMI"] = data[VALID_STUDY_COLUMNS.PatientsWeight] / ((data[VALID_STUDY_COLUMNS.PatientsSize] / 100) ** 2)

    return data[(data.BMI > 10) & (data.BMI < 35.0)]


def _categorize_exams_according_to_ssm(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    """Adds a column with the SSM specified exam name and populates it according to the rule setup in the
    EXAM_GROUPING_RULES_BY_MODALITY dictionary in the constants.

    Parameters
    ----------
    data
        the REMbox data to be categorized into SSM specified exam names
    modality
        the modality to which the exams belong. (Used for selecting grouping rules)

    Returns
    -------
    A copy of the original dataframe with an additional column containing the SSM specified exam name where the rows
    that could not be matched to an SSM specified exam dropped.
    """
    exam_grouping_rules = EXAM_GROUPING_RULES_BY_MODALITY[modality]

    data.reset_index(drop=True)
    data.loc[:, OUTPUT_COL_EXAM] = None

    for exam_grouping_type, exam_group in exam_grouping_rules.items():
        if exam_grouping_type == EXAM_GROUPING_TYPE_STUDY_DESCRIPTION:
            grouping_column = VALID_STUDY_COLUMNS.StudyDescription
        elif exam_grouping_type == EXAM_GROUPING_TYPE_PROTOCOL_CODE:
            grouping_column = VALID_STUDY_COLUMNS.ProtocolCode
        elif exam_grouping_type == EXAM_GROUPING_TYPE_PROCEDURE_CODE:
            grouping_column = VALID_STUDY_COLUMNS.ProcedureCode
        elif exam_grouping_type == EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL:
            grouping_column = VALID_SERIES_COLUMNS.AcquisitionProtocol
        else:
            raise ValueError("Invalid exam grouping type")

        for exam_name, exam_group_values in exam_group.items():
            if not exam_group_values:
                continue
            data.loc[data[grouping_column].isin(exam_group_values), [OUTPUT_COL_EXAM]] = exam_name

    return data.dropna(subset=[OUTPUT_COL_EXAM, VALID_STUDY_COLUMNS.PatientsSize, VALID_STUDY_COLUMNS.PatientsWeight])
