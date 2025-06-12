from Rapportering.Arsstatistik.Rembox_arstatistik_ct.src.get import *
from Rapportering.Arsstatistik.Rembox_arstatistik_ct.src.save_as import *


def get_ct_dose_statistics_for_year(year: int = -9999):
    """
    Det här scriptet hämtar årsstatistik för angivet år och skriver ut en excel-fil som kan laddas upp på dosreg.
    Om inget år anges så hämtas statistik för föregående år.

    Året anges längst ner i det här scriptet (rad 32)
    """

    # Hämta data från rembox
    study_data, series_data = get_study_and_series_data(year)

    # Läser in rapport-mallen, formaterar kolumnnamn och lägger till undersökningskoder
    report_df = get_report_df()

    # Sortera på ålder och kön, och filtrera ut vuxna patienter mellan 60 och 90 kg
    study_data_dict = get_study_data_dict(study_data=study_data)

    # Hämta en dictionary innehållandes dataframes med årsstatistik för varje sjukhus i regionen
    report_dict = get_report_dict(study_data_dictionary=study_data_dict, report_dataframe=report_df)

    # Skriv ut en rapport för varje sjukhus
    save_as_excel_file(report_dict=report_dict, year=year)

    print("End of script")


if __name__ == "__main__":
    get_ct_dose_statistics_for_year(year=2022)
