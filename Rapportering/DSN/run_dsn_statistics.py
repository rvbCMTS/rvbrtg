import logging
import time
from datetime import datetime
from math import floor

# import user

from rich.console import Console



from Rapportering.DSN.constants import MODALITY_LIST
from Rapportering.DSN.fetch_data import get_modality_data_for_year
from Rapportering.DSN.format_data  import format_data
from Rapportering.DSN.save_formatted_data import save_formatted_data
from Rapportering.DSN.plot_data import plot_data

rprint = Console(soft_wrap=True).print


class CustomRichHandler(logging.Handler):
    LEVEL_MAPPING = {
        logging.DEBUG: "[blue]DEBUG   [/blue]",
        logging.INFO: "[green]INFO    [/green]",
        logging.WARNING: "[yellow]WARNING [/yellow]",
        logging.ERROR: "[red]ERROR   [/red]",
        logging.CRITICAL: "[bold red]CRITICAL[/bold red]",
    }

    def emit(self, record):
        msg = self.format(record)
        rprint(msg)

    def format(self, record):
        levelname = self.LEVEL_MAPPING.get(record.levelno, str(record.levelno))

        file_name_line = (
            f"[link file://{record.filename}#{record.lineno}]"
            f"{record.filename}:{record.lineno}"
            f"[/link file://{record.filename}#{record.lineno}]")

        record.levelname = levelname
        record.filename = file_name_line
        return super().format(record)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[CustomRichHandler()]
)
logger = logging.getLogger("yearly_statistics")


def main(year: int = 0):
    def _valid_year(year: int) -> bool:
        return year > 2020 and year <= datetime.now().year

    while not _valid_year(year):
        year = int(input("Enter year: "))

    logger.info(f"Skapar statistikrapporter för {year}")

    start_time = time.time_ns()
    for modality in MODALITY_LIST:
        logger.info(f"Skapar rapporter för {modality}")

        logger.info("Hämtar data från REMbox")
        study_data = get_modality_data_for_year(year=year, modality=modality)
        logger.info(f"Hämtade {len(study_data)} study rader")

        logger.info(f"Formaterar data för att stoppa in i rapporterna")
        formatted_data = format_data(data=study_data, modality=modality)
        logger.info(f"Data för {modality} formaterad")

        logger.info(f"Plottar formaterad data för {modality}")
        plot_data(data=formatted_data, modality=modality)

        logger.info(f"Sparar formaterad data för {modality}")
        save_formatted_data(data=formatted_data, modality=modality)
        logger.info(f"Rapporter skapade för {modality}")

    total_time = (time.time_ns() - start_time) / 1000000000
    total_minutes = floor(total_time / 60)
    total_seconds = round(total_time - (60 * total_minutes))
    logger.info(f"Rapporter skapade. Tid för rapportskapande: {total_minutes} min {total_seconds} s")

if __name__ == "__main__":
    main()
