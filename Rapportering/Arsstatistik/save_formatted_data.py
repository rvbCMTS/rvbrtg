import logging
from pathlib import Path

from openpyxl import load_workbook
import pandas as pd

from Rapportering.Arsstatistik.constants import REPORT_TEMPLATE_PATH_PER_MODALITY, OUTPUT_COL_EXAM, MODALITY_CT, \
    REPORT_OUTPUT_DIR, MODALITY_DX, MODALITY_MG, MODALITY_XA, EXAM_GROUPING_RULES_BY_MODALITY, \
    EXAM_GROUPING_TYPE_PROCEDURE_CODE, EXAM_GROUPING_TYPE_PROTOCOL_CODE

logger = logging.getLogger("yearly_statistics")


def save_formatted_data(data: pd.DataFrame, modality: str) -> None:
    report_template = REPORT_TEMPLATE_PATH_PER_MODALITY[modality]
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Sparar rapporter i {REPORT_OUTPUT_DIR.absolute()}")

    for hospital in data.index.get_level_values(0).unique().tolist():
        logger.debug(f"Skapar rapport för {modality} kopplade till {hospital}")
        if modality == MODALITY_CT:
            _create_report_file_ct(template_path=report_template, data=data, hospital=hospital)
            continue
        if modality == MODALITY_DX:
            _create_report_file_dx(template_path=report_template, data=data, hospital=hospital)
            continue
        if modality == MODALITY_MG:
            _create_report_file_mg(template_path=report_template, data=data, hospital=hospital)
            continue
        if modality == MODALITY_XA:
            _create_report_file_xa(template_path=report_template, data=data, hospital=hospital)
            continue
        raise NotImplementedError(f"Report creation not implemented for {modality=}")

    return


def _create_report_main(template_path: Path, data: pd.DataFrame, hospital: str, dose_column_name: str, exam_codes: dict[str, list[str]], modality: str = "Inte mammo"):
    output_path: Path = REPORT_OUTPUT_DIR / f"{template_path.stem.split(' ')[0]} {hospital} DosReg{template_path.suffix}"

    report_template = load_workbook(template_path)
    sheet = report_template.active
    sheet_exams = {exam: row for row in range(3, 20) if (exam := sheet.cell(row=row, column=1).value)}

    for exam, row in sheet_exams.items():
        if (hospital, exam) not in data.index:
            logger.warning(f"Ingen {exam} undersökning hittades kopplad till {hospital}")
            continue

        df_row = data.loc[(hospital, exam)]
        if not len(df_row):
            print(f"Hittade inte {exam} från template bland undersökningarna")
            continue

        sheet.cell(row=row, column=2).value = ", ".join(codes) if (codes := exam_codes.get(exam)) is not None else ""
        sheet.cell(row=row, column=3).value = df_row["Antal"]["Kvinnor"]
        sheet.cell(row=row, column=4).value = df_row[dose_column_name]["Kvinnor"]

        if modality == MODALITY_MG:
            continue

        sheet.cell(row=row, column=5).value = df_row["Antal"]["Män"]
        sheet.cell(row=row, column=6).value = df_row[dose_column_name]["Män"]
        sheet.cell(row=row, column=7).value = df_row["Antal"]["Flickor"]
        sheet.cell(row=row, column=8).value = df_row[dose_column_name]["Flickor"]
        sheet.cell(row=row, column=9).value = df_row["Antal"]["Pojkar"]
        sheet.cell(row=row, column=10).value = df_row[dose_column_name]["Pojkar"]

    report_template.save(output_path)
    report_template.close()


def _get_exam_codes_for_modality(modality: str) -> dict[str, list[str]]:
    procedure_codes = EXAM_GROUPING_RULES_BY_MODALITY[modality].get(EXAM_GROUPING_TYPE_PROCEDURE_CODE)
    protocol_codes = EXAM_GROUPING_RULES_BY_MODALITY[modality].get(EXAM_GROUPING_TYPE_PROTOCOL_CODE)

    if not procedure_codes and not protocol_codes:
        return {}

    if procedure_codes and protocol_codes:
        output = {key: val + protocol_codes[key] for key, val in procedure_codes.items() if key in list(protocol_codes.keys())}
        if any(only_protocol_code_keys := [key for key in list(protocol_codes.keys()) if key not in list(procedure_codes.keys())]):
            output = output | {key: protocol_codes[key] for key in only_protocol_code_keys}
        return output

    if procedure_codes:
        return procedure_codes

    return procedure_codes


def _create_report_file_ct(template_path: Path, data: pd.DataFrame, hospital: str) -> None:
    exam_codes = _get_exam_codes_for_modality(modality=MODALITY_CT)
    _create_report_main(template_path=template_path, data=data, hospital=hospital, dose_column_name="DLP", exam_codes=exam_codes)


def _create_report_file_dx(template_path: Path, data: pd.DataFrame, hospital: str) -> None:
    exam_codes = _get_exam_codes_for_modality(modality=MODALITY_DX)
    _create_report_main(template_path=template_path, data=data, hospital=hospital, dose_column_name="DAP", exam_codes=exam_codes)


def _create_report_file_mg(template_path: Path, data: pd.DataFrame, hospital: str) -> None:
    exam_codes = _get_exam_codes_for_modality(modality=MODALITY_MG)
    _create_report_main(
        template_path=template_path,
        data=data,
        hospital=hospital,
        dose_column_name="AGD",
        exam_codes=exam_codes,
        modality=MODALITY_MG
    )


def _create_report_file_xa(template_path: Path, data: pd.DataFrame, hospital: str) -> None:
    exam_codes = _get_exam_codes_for_modality(modality=MODALITY_XA)
    _create_report_main(template_path=template_path, data=data, hospital=hospital, dose_column_name="DAP", exam_codes=exam_codes)