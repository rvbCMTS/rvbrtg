import pandas as pd


def save_as_excel_file(report_dict, year):
    # TODO: fixa så att data skrivs in i mallen från SSM så att det går att ladda upp direkt på dosreg
    file_name = r'C:\Users\torbj\GIT\rvbrtg\Data/rembox_CT-data_årsstatistik_{}.xlsx'.format(year)
    writer = pd.ExcelWriter(file_name)

    for hospital in report_dict:

        report_dict[hospital].to_excel(writer, sheet_name=hospital)

    writer.close()

    print("\nData for {} saved as excel-file!".format(year))

