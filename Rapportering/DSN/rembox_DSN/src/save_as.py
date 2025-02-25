import pandas as pd

import Rapportering.DSN.rembox_DSN.src.constants as con


def excel_files(summary_dict, dict_of_reports):
    keylist = list(dict_of_reports.keys())

    # TODO: kontrollera om det finns två rapporter för olika patientgrupper och slå ihop dem

    for report in dict_of_reports:
        report_df = dict_of_reports[report].loc[
            :,
            [
                "meanCTDIvol",
                "dlpTotal",
                "SizeSpecificDoseEstimation",
                "patientAge",
                "patientsSex",
                "patientsSize",
                "patientsWeight",
            ],
        ]

        # Hämtar rätt kolumnnamn enligt mallen från SSM
        report_df.columns = con.report_template_columns

        # Formaterar om innehållet
        report_df["Man/kvinna"] = report_df["Man/kvinna"].str.replace("M", "Man")
        report_df["Man/kvinna"] = report_df["Man/kvinna"].str.replace("F", "Kvinna")

        # TODO: ålder för young_kids ska rapporteras i månader inte år

        file_name = r"C:\Users\torbj\GIT\rvbrtg\Data/DSN_{}_{}_({}).xlsx".format(report[2], report[1], report[0])

        writer = pd.ExcelWriter(file_name)

        report_df.to_excel(excel_writer=writer)

        writer.close()

    print("reports have been saved as excel-files")
