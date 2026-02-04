from typing import Optional

import numpy as np
import pandas as pd

from Rapportering.Arsstatistik.constants import (
    AGE_SEX_CATEGORY_JUNIOR_MALE,
    AGE_SEX_CATEGORY_JUNIOR_FEMALE,
    AGE_SEX_CATEGORY_ADULT_MALE_16_40,
    AGE_SEX_CATEGORY_ADULT_FEMALE_16_40,
    AGE_SEX_CATEGORY_ADULT_MALE_41_65,
    AGE_SEX_CATEGORY_ADULT_FEMALE_41_65,
    AGE_SEX_CATEGORY_ADULT_MALE_66plus,
    AGE_SEX_CATEGORY_ADULT_FEMALE_66plus,
    AGE_SEX_CATEGORY_DOSE_BOY,
    AGE_SEX_CATEGORY_DOSE_GIRL,
    AGE_SEX_CATEGORY_DOSE_MALE,
    AGE_SEX_CATEGORY_DOSE_FEMALE,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    OUTPUT_COL_AGE_SEX_CATEGORY,
    OUTPUT_COL_AGE_SEX_CATEGORY_DOSE,
    VALID_STUDY_COLUMNS,
    OUTPUT_COL_EXAM,
    EXAM_GROUPING_RULES_BY_MODALITY,
    EXAM_GROUPING_TYPE_PROTOCOL_CODE,
    EXAM_GROUPING_TYPE_STUDY_DESCRIPTION,
    EXAM_GROUPING_TYPE_PROCEDURE_CODE,
    MODALITY_DX_MACHINE_GENERAL,
    MODALITY_DX_MACHINE_MOBILE,
    MODALITY_XA_MACHINE_DIAGNOSTIC,
    MODALITY_XA_MACHINE_TREATMENT,
    MISC_CATEGORY_GROUP_STATIONARY_DX,
    MISC_CATEGORY_GROUP_MOBILE_XA,
    MISC_CATEGORY_GROUP_MOBILE_DX_REF2,
    MISC_CATEGORY_GROUP_MOBILE_DX_REF,
    MISC_CATEGORY_GROUP_MOBILE_DX_VAL2,
    MISC_CATEGORY_GROUP_MOBILE_DX_VAL,
    MISC_CATEGORY_GROUP_MOBILE_DX_REF3,
    MISC_CATEGORY_GROUP_MOBILE_DX_VAL3,
    MISC_CATEGORY_GROUP_MG,
    MISC_CATEGORY_GROUP_STATIONARY_XA_DIAGNOSTIC,
    MISC_CATEGORY_GROUP_STATIONARY_XA_TREATMENT,
    MODALITY_XA_MACHINE_MOBILE,

)


def format_data(data: pd.DataFrame, modality: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    if modality == MODALITY_CT:
        return _format_ct_data(data)

    if modality == MODALITY_DX:
        return _format_dx_data(data)

    if modality == MODALITY_MG:
        return _format_mg_data(data)

    if modality == MODALITY_XA:
        return _format_xa_data(data)

    raise NotImplementedError(f"Modality {modality} not implemented")


def _format_ct_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_CT)

    # TODO: Kolla om DT behöver justeras för specialla fall.
    data_number = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc="count"),
    )
    data_number = data_number.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])
    output_number = data_number.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal"])

    data_dose = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]).agg(
        dose_mean=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc="mean"),
        dose_median=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc="median"),
        dose_Q1=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc=lambda x: np.percentile(x, 25)),
        dose_Q3=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc=lambda x: np.percentile(x, 75)),
    )
    data_dose = data_dose.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY_DOSE])
    output_dose = data_dose.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY_DOSE,
                                  values=["dose_mean", "dose_median", "dose_Q1", "dose_Q3"])

    return output_number, output_dose


def _format_dx_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data.loc[data[VALID_STUDY_COLUMNS.Hospital] == "Södra Lappland", [VALID_STUDY_COLUMNS.Hospital]] = "Lycksele"

    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_DX)

    #Categorize into miscellaneous categories for exams not fitting anywhere else
    data.loc[
        (data[OUTPUT_COL_EXAM] == "") & (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_DX_MACHINE_GENERAL),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_STATIONARY_DX

    data.loc[
        (data[OUTPUT_COL_EXAM] == "") & (data[VALID_STUDY_COLUMNS.Machine].isin(MODALITY_XA_MACHINE_MOBILE)),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_MOBILE_XA
    
    data.loc[
        (data[OUTPUT_COL_EXAM] == MISC_CATEGORY_GROUP_MOBILE_DX_REF) &
        (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_DX_MACHINE_MOBILE),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_MOBILE_DX_VAL
    
    data.loc[
        (data[OUTPUT_COL_EXAM] == MISC_CATEGORY_GROUP_MOBILE_DX_REF2) &
        (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_DX_MACHINE_MOBILE),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_MOBILE_DX_VAL2
    
    data.loc[
        (data[OUTPUT_COL_EXAM] == MISC_CATEGORY_GROUP_MOBILE_DX_REF3) &
        (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_DX_MACHINE_MOBILE),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_MOBILE_DX_VAL3

    data_number = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="count"),
    )
    data_number = data_number.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])
    output_number = data_number.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal"])

    data_dose = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]).agg(
        dose_mean=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="mean"),
        dose_median=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="median"),
        dose_Q1=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc=lambda x: np.percentile(x, 25)),
        dose_Q3=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc=lambda x: np.percentile(x, 75)),
    )
    data_dose = data_dose.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY_DOSE])
    output_dose = data_dose.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY_DOSE, values=["dose_mean", "dose_median", "dose_Q1", "dose_Q3"])

    return output_number, output_dose


def _format_mg_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = data[data[VALID_STUDY_COLUMNS.PatientsSex] == "F"]
    data = data.reset_index(drop=True)
    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_MG)

    # Övrigt kategorisering för MG
    data.loc[
        (data[OUTPUT_COL_EXAM] == ""),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_MG

    data_number = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc="count"),
    )
    data_number = data_number.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])
    output_number = data_number.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal"])

    data_dose = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]).agg(
        dose_mean=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc="mean"),
        dose_median=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc="median"),
        dose_Q1=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc=lambda x: np.percentile(x, 25)),
        dose_Q3=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc=lambda x: np.percentile(x, 75)),
    )
    data_dose = data_dose.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY_DOSE])
    output_dose = data_dose.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY_DOSE, values=["dose_mean", "dose_median", "dose_Q1", "dose_Q3"])
    # TODO: Dosvärden ska delas för antal bröst. Använd Laterality om möjligt för att avgöra hur många bröst som undersökts.

    return output_number, output_dose


def _format_xa_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = _categorize_by_age_and_sex(data, modality=MODALITY_XA)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_XA)


    # Categorize into preset miscellaneous category
    data.loc[
        (data[OUTPUT_COL_EXAM] == "") & (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_XA_MACHINE_DIAGNOSTIC),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_STATIONARY_XA_DIAGNOSTIC
    
    data.loc[
        (data[OUTPUT_COL_EXAM] == "") & (data[VALID_STUDY_COLUMNS.Machine].isin==MODALITY_XA_MACHINE_TREATMENT),
        OUTPUT_COL_EXAM] = MISC_CATEGORY_GROUP_STATIONARY_XA_TREATMENT

    data_number = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="count"),
    )
    data_number = data_number.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])
    output_number = data_number.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal"])

    data_dose = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]).agg(
        dose_mean=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="mean"),
        dose_median=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="median"),
        dose_Q1=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc=lambda x: np.percentile(x, 25)),
        dose_Q3=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc=lambda x: np.percentile(x, 75)),
    )
    data_dose = data_dose.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY_DOSE])
    output_dose = data_dose.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY_DOSE, values=["dose_mean", "dose_median", "dose_Q1", "dose_Q3"])

    return output_number, output_dose


def _categorize_by_age_and_sex(data: pd.DataFrame, modality: Optional[str] = None) -> pd.DataFrame:
    """

    Parameters
    ----------
    data
        the REMbox data to be categorized into SSM specified age and sex categories

    Returns
    -------
    The original dataframe with an additional column containing the age and sex classification
    """
    data[OUTPUT_COL_AGE_SEX_CATEGORY] = [None] * len(data)

    data.loc[
        (~data[VALID_STUDY_COLUMNS.PatientAge].isna()) & (data[VALID_STUDY_COLUMNS.PatientAgeUnit] != "Y"),
        [VALID_STUDY_COLUMNS.PatientAge]
    ] = 0

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_JUNIOR_MALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_JUNIOR_FEMALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientAge] < 41) &
        (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_MALE_16_40

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientAge] < 41) &
        (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_FEMALE_16_40

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 41) & (data[VALID_STUDY_COLUMNS.PatientAge] < 66) &
        (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_MALE_41_65

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 41) & (data[VALID_STUDY_COLUMNS.PatientAge] < 66) &
        (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_FEMALE_41_65

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 66) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_MALE_66plus

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 66) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_FEMALE_66plus

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]
    ] = AGE_SEX_CATEGORY_DOSE_FEMALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]
    ] = AGE_SEX_CATEGORY_DOSE_MALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]
    ] = AGE_SEX_CATEGORY_DOSE_GIRL

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY_DOSE]
    ] = AGE_SEX_CATEGORY_DOSE_BOY

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
        else:
            raise ValueError("Invalid exam grouping type")

        for exam_name, exam_group_values in exam_group.items():
            if not exam_group_values:
                continue
            data.loc[data[grouping_column].isin(exam_group_values), [OUTPUT_COL_EXAM]] = exam_name

    return data.dropna(subset=[OUTPUT_COL_EXAM])
