from datetime import timedelta

import pandas as pd

from Rapportering.Remittentstod.constants import (
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
    OUTPUT_COL_EFFECTIVE_DOSE,
    OUTPUT_COL_BODY_PART,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    CHILD_EXAM_PREFIX,
    BODY_PART_GIVEN_STUDY_DESCRIPTION,
    EFFECTIVE_DOSE_PER_UNIT_DAP,
    PATIENT_SIZE_PER_AGE
)

from Rapportering.DSN.plot_data import plot_data


def format_data(data: pd.DataFrame, modality: str) -> pd.DataFrame:

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
   return 



def _format_dx_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data[VALID_STUDY_COLUMNS.DoseAreaProductTotal] > 0]  # Remove data where DAP meter broken

    data = _calculate_effective_dose_given_dap(data)

    data = _categorize_exams_according_to_ssm(data, modality=MODALITY_DX)
 
    return data

def _format_mg_data(data: pd.DataFrame) -> pd.DataFrame:

    return


def _format_xa_data(data: pd.DataFrame) -> pd.DataFrame:

    return

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
    data[OUTPUT_COL_EXAM] = pd.Series(dtype="str")

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

            if modality == MODALITY_MG:
                data.loc[data[grouping_column].isin(exam_group_values), [OUTPUT_COL_EXAM]] = exam_name

            data.loc[((data[grouping_column].isin(exam_group_values)) & 
                         (data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
                         (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y')) |
                         ((data[grouping_column].isin(exam_group_values)) & 
                          data[VALID_STUDY_COLUMNS.PatientAgeUnit].isin(['D', 'M'])), [OUTPUT_COL_EXAM]] = f"{CHILD_EXAM_PREFIX}{exam_name}"

            data.loc[(data[grouping_column].isin(exam_group_values)) & 
                         (data[VALID_STUDY_COLUMNS.PatientAge] >= 16) &
                         (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y'), [OUTPUT_COL_EXAM]] = exam_name

    data = data.dropna(subset=[OUTPUT_COL_EXAM])

    return data

def _calculate_effective_dose_given_dap(data: pd.DataFrame) -> pd.DataFrame:
    # Build a DataFrame with one row per (body part, study description), including the effective dose per unit DAP.
    rows = []
    for body_part, study_list in BODY_PART_GIVEN_STUDY_DESCRIPTION.items():
        dose = EFFECTIVE_DOSE_PER_UNIT_DAP.get(body_part)
        for study in study_list:
            rows.append({
                OUTPUT_COL_BODY_PART: body_part,
                VALID_STUDY_COLUMNS.StudyDescription: study,
                "EffectiveDosePerUnitDAP": dose,
            })
    effective_dose_per_unit_dap_body_part_study = pd.DataFrame(rows)

    data = pd.merge(data,
                    effective_dose_per_unit_dap_body_part_study,
                    how="left",
                    on=VALID_STUDY_COLUMNS.StudyDescription)
    
    # Build a Dataframe for patient age and patient size
    rows = []
    for patient_age, patient_size in PATIENT_SIZE_PER_AGE.items():
        rows.append({
            VALID_STUDY_COLUMNS.PatientAge: patient_age,
            "DAPFieldAreaPatientSizeCompensation": (PATIENT_SIZE_PER_AGE[15] / patient_size)**2,
        })
    patient_size_per_age = pd.DataFrame(rows)

    data = pd.merge(data,
                    patient_size_per_age,
                    how="left",
                    on=VALID_STUDY_COLUMNS.PatientAge)
    
    data.loc[((data[VALID_STUDY_COLUMNS.PatientAge] >= 16) &
                    (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y')), [OUTPUT_COL_EFFECTIVE_DOSE]] = data[VALID_STUDY_COLUMNS.DoseAreaProductTotal] * data['EffectiveDosePerUnitDAP']
    
    data.loc[((data[VALID_STUDY_COLUMNS.PatientAge] < 16) &
              (data[VALID_STUDY_COLUMNS.PatientAgeUnit] == 'Y')) |
              (data[VALID_STUDY_COLUMNS.PatientAgeUnit].isin(['D', 'M'])), [OUTPUT_COL_EFFECTIVE_DOSE]] = data[VALID_STUDY_COLUMNS.DoseAreaProductTotal] * data['EffectiveDosePerUnitDAP'] * data['DAPFieldAreaPatientSizeCompensation']
 
    return data