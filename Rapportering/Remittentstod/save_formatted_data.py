import logging
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg") # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Rapportering.Remittentstod.constants import (
    MODALITY_DX,
    REPORT_OUTPUT_DIR,
    OUTPUT_COL_EXAM,
    VALID_STUDY_COLUMNS,
    OUTPUT_COL_EFFECTIVE_DOSE,
    OUTPUT_COL_BODY_PART)

logger = logging.getLogger("referral_dose_calculation")


def save_formatted_data(data: pd.DataFrame, modality: str) -> None:
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Sparar rapporter i {REPORT_OUTPUT_DIR.absolute()}")

    _create_report_main(data=data, modality=modality)
    _create_report_summery_statistics(data=data, modality=modality)

    return


def _create_report_main(data: pd.DataFrame, modality:str):
    for exam_name in data[OUTPUT_COL_EXAM].unique().tolist():
        logger.debug(f"Skapar rapport för undersökning {exam_name}")
        tmp_data = data[(data[OUTPUT_COL_EXAM] == exam_name)].reset_index()

        if modality not in [MODALITY_DX]:
            raise NotImplementedError(f"Modality '{modality}' not implemented.")
        
        output_path: Path = REPORT_OUTPUT_DIR / f"{modality} - {exam_name}.pdf"
        if output_path.exists():
            try:
                output_path.unlink()
            except Exception:
                logger.error(f"Kunde inte ta bort befintlig rapportfil: {output_path}")
                
        with PdfPages(output_path) as pdf:
            try:
                if modality == MODALITY_DX:
                    _create_report_dx(pdf=pdf, data=tmp_data, exam_name=exam_name, modality=modality)
            except Exception:
                logger.error(f"Kunde inte skapa rapport för {modality} - {exam_name}")


def _create_report_summery_statistics(data: pd.DataFrame, modality: str):
    agg_data = _calculate_statistics(data=data, modality=modality)
    output_path: Path = REPORT_OUTPUT_DIR / f"Sammanfattning statistik.csv"

    agg_data.to_csv(output_path, sep=";", decimal=",", encoding="latin-1")

    return


def _create_report_dx(pdf, data: pd.DataFrame, exam_name: str, modality: str):
    # Plot a histogram of effective dose and calculate basic statistics
    agg_data = _calculate_statistics(data=data, modality=modality)

    fig, ax = plt.subplots(1, 1, sharey=True, tight_layout=True)
    ax.hist(data[OUTPUT_COL_EFFECTIVE_DOSE], bins=round(len(data) ** (1/2)))

    plt.text(data[OUTPUT_COL_EFFECTIVE_DOSE].max()*0.4,
             ax.get_yticks()[1],
             f"Body part (DAP -> mSv):\n {data[OUTPUT_COL_BODY_PART].unique().tolist()}\n" +
             f"Study description:\n {data[VALID_STUDY_COLUMNS.StudyDescription].unique().tolist()}\n" +
             f"Machine:\n {_list_to_multiline_string(data[VALID_STUDY_COLUMNS.Machine].unique().tolist())}\n\n" +
             f"Antal undersökningar: {agg_data['Antal'].values[0]}\n" +
             f"Medelvärde: {agg_data['Dose_mean'].values[0]:.2f} mSv\n" +
             f"Median: {agg_data['Dose_median'].values[0]:.2f} mSv\n" +
             f"95-percentil: {agg_data['Dose_95'].values[0]:.2f} mSv"
    )

    ax.set_ylabel("Antal undersökningar")
    ax.set_xlabel("Effektiv dos (mSv)")
    ax.set_title(f"Histogram över effektiv dos för {exam_name}")

    pdf.savefig(fig)
    plt.close(fig)


def _list_to_multiline_string(lst, per_line=5, sep=", "):
    chunks = [sep.join(map(str, lst[i:i+per_line])) for i in range(0, len(lst), per_line)]
    return "\n".join(chunks)


def _calculate_statistics(data: pd.DataFrame, modality: str):
    if modality == MODALITY_DX:
        agg_data = data.groupby(by=OUTPUT_COL_EXAM).agg(
                    Antal=pd.NamedAgg(column=OUTPUT_COL_EFFECTIVE_DOSE, aggfunc="count"),
                    Dose_mean=pd.NamedAgg(column=OUTPUT_COL_EFFECTIVE_DOSE, aggfunc="mean"),
                    Dose_median=pd.NamedAgg(column=OUTPUT_COL_EFFECTIVE_DOSE, aggfunc="median"),
                    Dose_95=pd.NamedAgg(column=OUTPUT_COL_EFFECTIVE_DOSE, aggfunc=lambda x: x.quantile(0.95))
        )
    return agg_data