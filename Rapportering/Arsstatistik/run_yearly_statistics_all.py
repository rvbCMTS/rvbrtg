from datetime import datetime

from rich.progress import track

from Rapportering.Arsstatistik.fetch_data import get_modality_data_for_year
from Rapportering.Arsstatistik.constants import MODALITY_LIST
from Rapportering.Arsstatistik.format_data import format_data
from Rapportering.Arsstatistik.save_formatted_data import save_formatted_data


def main(year: int = 0):
    def _valid_year(year: int) -> bool:
        return year > 2020 and year < datetime.now().year

    while not _valid_year(year):
        year = int(input("Enter year: "))

    # TODO: Kör statistiksammaställning för varje modalitet
    for modality in track(MODALITY_LIST, description="Creating report per modality..."):
        study_data = get_modality_data_for_year(year=year, modality=modality)
        formatted_data = format_data(data=study_data, modality=modality)
        save_formatted_data(data=formatted_data, modality=modality)


if __name__ == "__main__":
    main()
