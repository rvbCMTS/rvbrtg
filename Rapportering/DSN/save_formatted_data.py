import logging
from pathlib import Path

from openpyxl import load_workbook
import pandas as pd

from Rapportering.DSN.constants import (
    REPORT_TEMPLATE_PATH_PER_MODALITY,
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA,
    REPORT_OUTPUT_DIR, EXAM_GROUPING_RULES_BY_MODALITY,
    EXAM_GROUPING_TYPE_PROCEDURE_CODE, EXAM_GROUPING_TYPE_PROTOCOL_CODE,
    OUTPUT_COL_EXAM, VALID_SERIES_COLUMNS, VALID_STUDY_COLUMNS)

logger = logging.getLogger("yearly_statistics")


def save_formatted_data(data: pd.DataFrame, modality: str) -> None:
    report_template = REPORT_TEMPLATE_PATH_PER_MODALITY[modality]
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Sparar rapporter i {REPORT_OUTPUT_DIR.absolute()}")

    for exam_name in data[OUTPUT_COL_EXAM].unique().tolist():
        logger.debug(f"Skapar rapport för {modality} kopplade till undersökning {exam_name}")

        _create_report_main(template_path=report_template, data=data, exam_name=exam_name, modality=modality)

    return


def _create_report_main(template_path: Path, data: pd.DataFrame, modality:str,  exam_name:str):
    output_path: Path = REPORT_OUTPUT_DIR / f"{modality} - {exam_name}{template_path.suffix}"

    report_template = load_workbook(template_path)
    sheet = report_template.active
    sheet_exams = {exam: row for row in range(3, 50) if (exam := sheet.cell(row=row, column=1).value)}
    tmp_data = data[data[OUTPUT_COL_EXAM] == exam_name].reset_index()

    if len(tmp_data) < 20:
        return


    tmp_data['CTDIdiff'] = (tmp_data[VALID_SERIES_COLUMNS.MeanCTDIvol] - tmp_data.loc[:, VALID_SERIES_COLUMNS.MeanCTDIvol].mean()).abs()
    tmp_data.sort_values('CTDIdiff', inplace=True, ignore_index=True)

    for row_ind in range(20):
        sheet.cell(row=row_ind + 3, column=1).value = tmp_data[VALID_SERIES_COLUMNS.MeanCTDIvol][row_ind]
        sheet.cell(row=row_ind + 3, column=2).value = tmp_data[VALID_SERIES_COLUMNS.DlPv][row_ind]
        sheet.cell(row=row_ind + 3, column=3).value = tmp_data[VALID_SERIES_COLUMNS.SizeSpecificDoseEstimation][row_ind]
        sheet.cell(row=row_ind + 3, column=4).value = tmp_data[VALID_STUDY_COLUMNS.PatientAge][row_ind]
        sheet.cell(row=row_ind + 3, column=5).value = tmp_data[VALID_STUDY_COLUMNS.PatientsSex][row_ind]
        sheet.cell(row=row_ind + 3, column=6).value = tmp_data[VALID_STUDY_COLUMNS.PatientsSize][row_ind]
        sheet.cell(row=row_ind + 3, column=7).value = tmp_data[VALID_STUDY_COLUMNS.PatientsWeight][row_ind]
        sheet.cell(row=row_ind + 3, column=8).value = tmp_data[VALID_STUDY_COLUMNS.Machine][row_ind]
        sheet.cell(row=row_ind + 3, column=9).value = tmp_data[VALID_SERIES_COLUMNS.AcquisitionProtocol][row_ind]

    report_template.save(output_path)
    report_template.close()