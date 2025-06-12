import datetime

import pandas as pd
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import SeriesColumn, StudyColumn

import Rapportering.Arsstatistik.Rembox_arstatistik_ct.src.constants as con


def get_study_and_series_data(year):
    rembox = REMboxDataQuery(
        client_id_environment_variable=con.CLIENT_ID_ENV_VAR,
        client_secret_environment_variable=con.CLIENT_PWD_ENV_VAR,
        token_uri=con.TOKEN_URI,
        api_uri=con.API_URI,
        origin_uri=con.ORIGIN_URI,
    )

    # Hämtar CT-data
    study_data, series_data = get_data_from_ct(rembox=rembox, year=year)

    return study_data, series_data


def get_data_from_ct(rembox: REMboxDataQuery, year) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()

    rembox.filter_options.set_inclusive_tags(
        machine_types=["CT"],
        # machines=["U209", "U211", "U213, L11, L5, S06 ,S07"]
    )

    rembox.filter_options.patient_age_interval_include_nulls = True

    # Om inget år har angetts, välj föregående år
    if year == -9999:
        year = datetime.date.today().year - 1

    # filter time interval
    rembox.filter_options.study_time_interval_start_date = "{}-01-01T00:00:00Z".format(year)
    rembox.filter_options.study_time_interval_end_date = "{}-12-31T00:00:00Z".format(year)

    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            valid_study_columns.AccessionNumber,
            valid_study_columns.StudyDescription,
            valid_study_columns.PatientAge,
            valid_study_columns.PatientsWeight,
            valid_study_columns.TotalNumberOfIrradiationEvents,
            valid_study_columns.PerformingPhysicianName,
            valid_study_columns.PerformingPhysicianIdentificationSequence,
            valid_study_columns.PatientDbId,
            valid_study_columns.DlpTotal,
            valid_series_columns.MeanCTDIvol,
            valid_study_columns.PatientsSex,
            valid_series_columns.AcquisitionProtocol,
            valid_series_columns.DateTimeStarted,
            valid_study_columns.ProcedureCode,
            valid_study_columns.ProcedureCodeMeaning,
            valid_study_columns.RequestedProcedureCodeMeaning,
        ]
    )

    return rembox.run_query()


def get_report_df():
    report_df = pd.read_excel("src/CT Mall årsredovisning DosReg.xlsx", header=[0, 1])
    report_df.columns = [".".join(column) for column in report_df.columns.values]
    report_df.rename(
        columns={
            "Undersökning.Unnamed: 0_level_1": "Undersökning",
            "Undersökningskod(er).Unnamed: 1_level_1": "Undersökningskod(er)",
        },
        inplace=True,
    )

    for procedure in con.procedure_codes_dict:
        code = con.procedure_codes_dict[procedure]
        code_as_str = ", ".join(code)

        report_df.loc[report_df["Undersökning"] == procedure, "Undersökningskod(er)"] = code_as_str

    return report_df


def get_performing_physician(study_data):
    # add column with name of performing physician

    # Översättningstabell från pseudo-operatörer till operatörer
    names_data_path = "input_data/Operatörer_2022.xlsx"

    names = pd.read_excel(names_data_path)

    # Ändra kolumn för att kunna göra en join
    names.columns = ["OperatorName", "performingPhysicianName"]

    # Joina dataframes för att få in operatörsnamn
    data_names = pd.merge(study_data, names, how="left", on=["performingPhysicianName"])

    # Print för att kolla så att det funkade
    print(data_names.OperatorName)


def get_uniques_and_registered_weight_fraction(study_data):
    """
    This function takes a DataFrame as input, prints the number of studies and unique patients in the DataFrame,
    and the fraction of studies/patients with a registered weight.
    """
    print("Antal studier: ", study_data["patientDbId"].count())
    print("Antal patienter: ", study_data["patientDbId"].nunique())

    fraction = study_data["patientsWeight"].isna().sum() / study_data["patientDbId"].count() * 100
    print(
        "Antal studier utan registrerad vikt: ",
        study_data["patientsWeight"].isna().sum(),
        " [{:.1f} %]".format(fraction),
    )

    study_data2 = study_data.dropna(subset=["patientsWeight"])
    fraction2 = (
        (study_data["patientDbId"].nunique() - study_data2["patientDbId"].nunique())
        / study_data["patientDbId"].nunique()
        * 100
    )

    print(
        "Antal patienter utan registrerad vikt: ",
        (study_data["patientDbId"].nunique() - study_data2["patientDbId"].nunique()),
        " [{:.1f} %]".format(fraction2),
    )


def get_studies_and_dlp(report_df, study_data, patient_group_studies, patient_group_dlp):
    for procedure in con.procedure_codes_dict:
        # filtrera på undersökningskoden
        study_data_filtered = study_data[study_data["procedureCode"].isin(con.procedure_codes_dict[procedure])]

        code = con.procedure_codes_dict[procedure]
        code_as_str = ", ".join(code)

        number_of_studies = study_data_filtered["patientDbId"].count()
        mean_dlp = study_data_filtered["dlpTotal"].mean()

        report_df.loc[report_df["Undersökningskod(er)"] == code_as_str, patient_group_studies] = number_of_studies
        report_df.loc[report_df["Undersökningskod(er)"] == code_as_str, patient_group_dlp] = mean_dlp

        """
        print(
            f"Undersökning: {procedure:<20} kod: ",
            con.procedure_codes_dict[procedure],
            " - Antal: ",
            number_of_studies,
            " Medel DLP: {:.0f} mGy*cm".format(mean_dlp),
        )
        """

    return report_df


def get_study_data_dict(study_data):
    # Ta bort rader utan vikt
    study_data = study_data.dropna(subset=["patientsWeight"])

    # Filtrera baserat på ålder
    study_data_kids = study_data.copy()
    study_data_kids = study_data_kids[study_data_kids["patientAge"] < 16]

    study_data_adults = study_data.copy()
    study_data_adults = study_data_adults[study_data_adults["patientAge"] >= 16]
    # För vuxna patienter, filtrera ut patienter över 60 kg och under 90 kg

    study_data_adults = study_data_adults[
        (study_data_adults["patientsWeight"] >= 60) & (study_data_adults["patientsWeight"] <= 90)
    ]

    # Filtrera baserat på kön
    study_data_kids_male = study_data_kids[study_data_kids["patientsSex"] == "M"]
    study_data_kids_female = study_data_kids[study_data_kids["patientsSex"] == "F"]

    study_data_adults_male = study_data_adults[study_data_adults["patientsSex"] == "M"]
    study_data_adults_female = study_data_adults[study_data_adults["patientsSex"] == "F"]

    dict_with_study_data = {
        "girl": study_data_kids_female,
        "boy": study_data_kids_male,
        "male": study_data_adults_male,
        "female": study_data_adults_female,
    }

    return dict_with_study_data


def get_report_dict(study_data_dictionary, report_dataframe):
    # Skapa en tom dictionary för att lagra rapporterna
    report_dictionary = {}
    print("Collecting data for:")
    # För varje sjukhus i regionen
    for hospital in con.machines_at_hospital:
        print(hospital)
        # För varje patient-grupp
        for patient_group in study_data_dictionary:
            study_data_at_hospital = study_data_dictionary[patient_group][
                study_data_dictionary[patient_group]["machine"].isin(con.machines_at_hospital[hospital])
            ]

            # Hämta antal studier och medeldos för varje undersökningskod
            report_dataframe = get_studies_and_dlp(
                report_df=report_dataframe,
                study_data=study_data_at_hospital,
                patient_group_studies=con.patient_group["{}-studies".format(patient_group)],
                patient_group_dlp=con.patient_group["{}-dlp".format(patient_group)],
            )

        # De individuella rapporterna för varje sjukhus samlas i en dict
        report_dictionary[hospital] = report_dataframe.copy()

    return report_dictionary
