from datetime import timedelta

import pandas as pd

from Rapportering.DSN.constants import (
    VALID_STUDY_COLUMNS,
    VALID_SERIES_COLUMNS,
    EXAM_GROUPING_RULES_BY_MODALITY,
    EXAM_GROUPING_TYPE_PROTOCOL_CODE,
    EXAM_GROUPING_TYPE_STUDY_DESCRIPTION,
    EXAM_GROUPING_TYPE_PROCEDURE_CODE,
    EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL,
    OUTPUT_COL_EXAM,
    OUTPUT_COL_WEIGTH_CATEGORY,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    WEIGHT_CATEGORY_0_5,
    WEIGHT_CATEGORY_5_15,
    WEIGHT_CATEGORY_15_30,
    WEIGHT_CATEGORY_30_50,
    WEIGHT_CATEGORY_50_70,
    WEIGHT_CATEGORY_70_90,
)


def format_data(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    data = _sanity_check_patient_bmi(data)
    data = _filter_for_size_and_weight_date_intervals_relative_study_datetime(data)

    if modality == MODALITY_CT:
        return _format_ct_data(data)

    if modality == MODALITY_DX:
        return _format_dx_data(data)


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

    data = _categorize_by_weight_and_age(data)

    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_DX)

    summery_data = data.groupby(by=[OUTPUT_COL_EXAM, OUTPUT_COL_WEIGTH_CATEGORY, VALID_STUDY_COLUMNS.Machine]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="count"),
        DAP=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="median")
    )

    return data


def _filter_for_size_and_weight_date_intervals_relative_study_datetime(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, "SizeDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsSizeDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])
    data.loc[:, "WeightDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsWeightDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])

    data["KeepRow"] = True
    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == "Y") &  # Filters for patients that are at least 1 years old
        ((data["SizeDateDiff"] > timedelta(days=365)) | (data["WeightDateDiff"] > timedelta(days=365))),
         "KeepRow"
    ] = False

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAgeUnit] != "Y") &  # Filters for patients that are below 1 year
        ((data["SizeDateDiff"] > timedelta(days=30)) | (data["WeightDateDiff"] > timedelta(days=30))),
        "KeepRow"
    ] = False

    # Keep only rows where "KeepRow" is True
    data = data[data["KeepRow"]]

    # Drop the "KeepRow" column as it is no longer needed
    data = data.drop(columns=["KeepRow"])

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

def _categorize_by_weight_and_age(data: pd.DataFrame) -> pd.DataFrame:
    """Categories the data by weight intervalls for DSN reports

    Parameters
    ----------
    data
        the REMbox data to be categorized into weight intervals

    Returns
    -------
    The original dataframe with an additional column containing the weight interval
    """
    data.loc[:, OUTPUT_COL_WEIGTH_CATEGORY] = [None] * len(data)

    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] < 5.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_0_5
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 5.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 15.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_5_15
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 15.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 30.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_15_30
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 30.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 50.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_30_50
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 50.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 70.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_50_70
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 70.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 90.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_70_90    

    return data


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
