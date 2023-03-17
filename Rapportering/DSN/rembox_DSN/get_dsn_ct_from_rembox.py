from Rapportering.DSN.rembox_DSN.src.get_from_rembox import *
from src import save_as


def main():
    # Hämta remboxdata för CT, hämta från ett år tillbaka i tiden, kasta rader utan vikt och längd
    study_data, series_data = get_study_and_series_data()

    # Dela upp datat på undersökning, maskin och patientgrupper (små barn, barn och vuxna)
    # Varje k
    study_data_dict = get_study_data_dictionary(study_data)

    # kontrollera om krav på antalet patienter uppfylls, annars ta bort "gruppen"
    report_summary, report_summary_2, report_dict = get_study_data_report(
        study_data_dict=study_data_dict
    )

    # skapa rapport med CTDIvol, DLP, ålder, man/kvinna, längd och vikt.
    # Ålder ska rapporteras i månader upp till 48 månader och vuxna ska väga mellan 60-90 kg

    # Sortera på patient

    print("Följande måste rapporteras till SSM")
    print(report_summary)
    print("Följande ska inte rapporteras till SSM")
    print(report_summary_2)
    save_as.excel_files(report_summary, report_dict)
    print("End of script")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
