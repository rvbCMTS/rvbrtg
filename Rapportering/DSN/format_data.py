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
    OUTPUT_COL_AGE_CATEGORY,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    WEIGHT_CATEGORY_0_5,
    WEIGHT_CATEGORY_5_15,
    WEIGHT_CATEGORY_15_30,
    WEIGHT_CATEGORY_30_50,
    WEIGHT_CATEGORY_50_70,
    WEIGHT_CATEGORY_60_90,
    AGE_CATEGORY_0_1,
    AGE_CATEGORY_1_6,
    AGE_CATEGORY_6_16,
    CHILD_EXAM_PREFIX, MG_COL_PROJECTION
)
from Rapportering.DSN.plot_data import plot_data


def format_data(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    data = _sanity_check_patient_bmi(data=data, modality=modality)
    data = _filter_for_size_and_weight_date_intervals_relative_study_datetime(data=data, modality=modality)

    if modality == MODALITY_CT:
        return _format_ct_data(data)

    if modality == MODALITY_DX:
        return _format_dx_data(data)
    
    if modality == MODALITY_XA:
        return _format_xa_data(data)

    if modality == MODALITY_MG:
        return _format_mg_data(data)

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

    data = _categorize_by_weight(data)

    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_DX)
 
    data = _filter_for_number_of_examinations_needed_for_DSN_report(data)

    return data

def _format_mg_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data[VALID_SERIES_COLUMNS.AverageGlandularDose] > 0]  # Remove negative and zero AGD values
    data = _determine_mg_projection(data=data)
    data[VALID_SERIES_COLUMNS.AverageGlandularDose] *= 0.1  # Convert from N to daN
    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_MG)

    plot_data(data=data, modality=MODALITY_MG)

    data = data[
        data[VALID_SERIES_COLUMNS.CompressionForce].astype(float).isnotnull() &
        data[VALID_SERIES_COLUMNS.CompressionThickness].astype(float).isnotnull()
    ]  # Remove rows that is missing either CompressionForce or CompressionThickness
    return data


def _format_xa_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data[VALID_STUDY_COLUMNS.DoseAreaProductTotal] > 0]  # Remove negative and zero DAP values

    data[VALID_STUDY_COLUMNS.TotalFluoroTime] = data[VALID_STUDY_COLUMNS.TotalFluoroTime] / 60  # Convert fluoro time to minutes
    data[VALID_STUDY_COLUMNS.TotalFluoroTime] = data[VALID_STUDY_COLUMNS.TotalFluoroTime].round(2)  # Round fluoro time to 2 decimal places
    
    data = _categorize_by_weight(data)

    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_XA)
 
    data = _filter_for_number_of_examinations_needed_for_DSN_report(data)

    return data

def _filter_for_size_and_weight_date_intervals_relative_study_datetime(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    if modality == MODALITY_MG:
        return data

    data.loc[:, "SizeDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsSizeDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])
    data.loc[:, "WeightDateDiff"] = abs(data[VALID_STUDY_COLUMNS.PatientsWeightDate] - data[VALID_STUDY_COLUMNS.StudyDateTime])

    data.loc[:, "KeepRow"] = True
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

def _sanity_check_patient_bmi(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    """Throws away data for patients with an unreasonable value for the BMI

    Parameters
    ----------
    data
        the REMbox data to be sanitized

    Returns
    -------
    A copy of the original dataframe with added column for BMI and rows with unreasonable values dropped
    """
    if modality == MODALITY_MG:
        return data

    data["BMI"] = data[VALID_STUDY_COLUMNS.PatientsWeight] / ((data[VALID_STUDY_COLUMNS.PatientsSize] / 100) ** 2)

    return data[(data.BMI > 10) & (data.BMI < 35.0)]

def _categorize_by_weight(data: pd.DataFrame) -> pd.DataFrame:
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
    data.loc[(data[VALID_STUDY_COLUMNS.PatientsWeight] >= 60.0) &
             (data[VALID_STUDY_COLUMNS.PatientsWeight] < 90.0) &
             (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) &
             (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), OUTPUT_COL_WEIGTH_CATEGORY] = WEIGHT_CATEGORY_60_90    

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
            if CHILD_EXAM_PREFIX in exam_name:
                data.loc[(data[grouping_column].isin(exam_group_values)) & 
                         (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
                         (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), [OUTPUT_COL_EXAM]] = exam_name
            else:
                data.loc[(data[grouping_column].isin(exam_group_values)) & 
                         (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) &
                         (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), [OUTPUT_COL_EXAM]] = exam_name

    return data.dropna(subset=[OUTPUT_COL_EXAM, VALID_STUDY_COLUMNS.PatientsSize, VALID_STUDY_COLUMNS.PatientsWeight])


def _filter_for_number_of_examinations_needed_for_DSN_report(data: pd.DataFrame) -> pd.DataFrame:
    """Filter for number of examinations neeeded for DSN report: 20 for adults and 10 for children.

    Parameters
    ----------
    data
        the REMbox data to be filtered
 

    Returns
    -------
    A filtered version of the REMbox data
    """

    filtered_data = data.groupby(by=[OUTPUT_COL_EXAM, OUTPUT_COL_WEIGTH_CATEGORY, VALID_STUDY_COLUMNS.Machine]).filter(
        lambda x: x[VALID_STUDY_COLUMNS.DoseAreaProductTotal].count() > 10
        if x[VALID_STUDY_COLUMNS.PatientAge].max() < 16
        else x[VALID_STUDY_COLUMNS.DoseAreaProductTotal].count() > 20
    )

    return filtered_data


def _determine_mg_projection(data: pd.DataFrame) -> pd.DataFrame:
    data[MG_COL_PROJECTION] = None
    data.loc[
        (
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-65, -40) |
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(40, 65)
        ) & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = "RMLO"
    data.loc[
        (
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-65, -40) |
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(40, 65)
        ) & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = "LMLO"
    data.loc[
        (
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-95, -85) |
            data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(85, 95)
        ) & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = "RML"
    data.loc[
        (
                data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-95, -85) |
                data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(85, 95)
        ) & data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = "LML"
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-5, 5) &
        data[VALID_SERIES_COLUMNS.Laterality].str.contains("Right"),
        MG_COL_PROJECTION
    ] = "RCC"
    data.loc[
        data[VALID_SERIES_COLUMNS.PositionerPrimaryAngle].between(-5, 5) &
        data[VALID_SERIES_COLUMNS.Laterality].str.contains("Left"),
        MG_COL_PROJECTION
    ] = "LCC"

    return data
