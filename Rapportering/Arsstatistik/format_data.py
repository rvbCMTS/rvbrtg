import numpy as np
import pandas as pd

from Rapportering.Arsstatistik.constants import (
    AGE_SEX_CATEGORY_JUNIOR_MALE,
    AGE_SEX_CATEGORY_JUNIOR_FEMALE,
    AGE_SEX_CATEGORY_ADULT_MALE,
    AGE_SEX_CATEGORY_ADULT_FEMALE,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    OUTPUT_COL_AGE_SEX_CATEGORY,
    VALID_STUDY_COLUMNS, OUTPUT_COL_EXAM, EXAM_GROUPING_RULES_BY_MODALITY, EXAM_GROUPING_TYPE_PROTOCOL_CODE,
    EXAM_GROUPING_TYPE_STUDY_DESCRIPTION, EXAM_GROUPING_TYPE_PROCEDURE_CODE,
)


def format_data(data: pd.DataFrame, modality: str) -> pd.DataFrame:
    if modality == MODALITY_CT:
        return _format_ct_data(data)

    if modality == MODALITY_DX:
        return _format_dx_data(data)

    if modality == MODALITY_MG:
        return _format_mg_data(data)

    if modality == MODALITY_XA:
        return _format_xa_data(data)

    raise NotImplementedError(f"Modality {modality} not implemented")


def _format_ct_data(data: pd.DataFrame) -> pd.DataFrame:
    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_CT)

    data = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc="count"),
        DLP=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DlpTotal, aggfunc="mean")
    )
    data = data.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])

    output = data.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal", "DLP"])

    return output


def _format_dx_data(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[data[VALID_STUDY_COLUMNS.Hospital] == "Södra Lappland", [VALID_STUDY_COLUMNS.Hospital]] = "Lycksele"

    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_DX)

    data = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="count"),
        DAP=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="mean")
    )

    data = data.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])

    output = data.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal", "DAP"])

    return output


def _format_mg_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data[VALID_STUDY_COLUMNS.PatientsSex] == "F"]
    data.loc[:, OUTPUT_COL_AGE_SEX_CATEGORY] = AGE_SEX_CATEGORY_ADULT_FEMALE

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_MG)

    data = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc="count"),
        AGD=pd.NamedAgg(column=VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts, aggfunc="mean")
    )

    return data


def _format_xa_data(data: pd.DataFrame) -> pd.DataFrame:
    data = _categorize_by_age_and_sex(data)

    data = _categorize_exams_according_to_ssm(data=data, modality=MODALITY_XA)

    data = data.groupby(by=[VALID_STUDY_COLUMNS.Hospital, OUTPUT_COL_EXAM, OUTPUT_COL_AGE_SEX_CATEGORY]).agg(
        Antal=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="count"),
        DAP=pd.NamedAgg(column=VALID_STUDY_COLUMNS.DoseAreaProductTotal, aggfunc="mean")
    )

    data = data.reset_index(level=[OUTPUT_COL_AGE_SEX_CATEGORY])

    output = data.pivot(columns=OUTPUT_COL_AGE_SEX_CATEGORY, values=["Antal", "DAP"])

    return output


def _categorize_by_age_and_sex(data: pd.DataFrame) -> pd.DataFrame:
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
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_JUNIOR_MALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] < 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_JUNIOR_FEMALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "M"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_MALE

    data.loc[
        (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) & (data[VALID_STUDY_COLUMNS.PatientsSex] == "F"),
        [OUTPUT_COL_AGE_SEX_CATEGORY]
    ] = AGE_SEX_CATEGORY_ADULT_FEMALE

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

    data.loc[:, OUTPUT_COL_EXAM] = [None] * len(data)

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
