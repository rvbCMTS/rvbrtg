import pandas as pd

from Rapportering.Arsstatistik.constants import REPORT_TEMPLATE_PATH_PER_MODALITY


def save_formatted_data(data: pd.DataFrame, modality: str) -> None:
    report_template = REPORT_TEMPLATE_PATH_PER_MODALITY[modality]
    # TODO: läs in mallen, fyll på med data och skriv ut mallen

    for hospital in data.index.get_level_values(0).unique().tolist():
        test = 1


    test = 1
    return
