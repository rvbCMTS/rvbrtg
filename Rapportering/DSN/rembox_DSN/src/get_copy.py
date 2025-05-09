import datetime
from datetime import date

import pandas as pd
import src.constants as con
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import SeriesColumn, StudyColumn
from src import get


def study_and_series_data():
    rembox = REMboxDataQuery(
        client_id_environment_variable=con.CLIENT_ID_ENV_VAR,
        client_secret_environment_variable=con.CLIENT_PWD_ENV_VAR,
        token_uri=con.TOKEN_URI,
        api_uri=con.API_URI,
        origin_uri=con.ORIGIN_URI,
    )

    # Hämtar CT-data
    study_data, series_data = get.data_from_ct(rembox=rembox)

    # TODO: ta bort det här när SizeSpecificDoseEstimation kan hämtas automatiskt istället
    # Lägger till kolumnen SizeSpecificDoseEstimation i series_data eftersom den av någon anledning inte skapas
    # automatiskt i get.data_from_ct
    series_data["SizeSpecificDoseEstimation"] = ""

    # Ta bort onödiga kolumner i series_data
    series_data = series_data.loc[:, ["studyInstanceUID", "meanCTDIvol", "SizeSpecificDoseEstimation"]]
    # Sortera series_data på meanCTDIvol från hög till låg dos
    series_data.sort_values(by="meanCTDIvol", ascending=False, inplace=True)
    # För varje study, spara serien med högst meanCTDIvol och kasta resten
    series_data.drop_duplicates("studyInstanceUID", keep="first", inplace=True)

    # lägg till 'meanCTDIvol' i study_data genom att slå ihop study_data och series_data
    # För ihopslagningen används 'studyInstanceUID' som nyckel/index
    study_data = study_data.merge(series_data, on="studyInstanceUID", how="left")

    # Ta bort rader som saknar uppgifter om patientens vikt, längd eller ålder
    study_data = study_data.dropna(subset=["patientsWeight"])
    study_data = study_data.dropna(subset=["patientsSize"])
    study_data = study_data.dropna(subset=["patientAge"])

    return study_data, series_data


def data_from_ct(rembox: REMboxDataQuery) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()

    rembox.filter_options.set_inclusive_tags(
        machine_types=["CT"],
        # machines=["U209", "U211", "U213, L11, L5, S06 ,S07"]
    )

    rembox.filter_options.patient_age_interval_include_nulls = True

    current_date = datetime.date.today()
    previous_year = current_date - datetime.timedelta(days=365)

    # filter time interval
    rembox.filter_options.study_time_interval_start_date = "{}T00:00:00Z".format(previous_year)
    rembox.filter_options.study_time_interval_end_date = "{}T00:00:00Z".format(current_date)

    # TODO: av någon anledning hämtas inte kolumnen SizeSpecificDoseEstimation till series_data.
    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            # valid_study_columns.AccessionNumber,
            valid_study_columns.StudyDescription,
            valid_study_columns.PatientAge,
            valid_study_columns.PatientsWeight,
            # valid_study_columns.TotalNumberOfIrradiationEvents,
            # valid_study_columns.PerformingPhysicianName,
            # valid_study_columns.PerformingPhysicianIdentificationSequence,
            valid_study_columns.PatientDbId,
            valid_study_columns.PatientsSize,
            valid_study_columns.DlpTotal,
            valid_study_columns.PatientsSex,
            valid_study_columns.ProcedureCode,
            valid_study_columns.ProcedureCodeMeaning,
            valid_series_columns.MeanCTDIvol,
            valid_series_columns.AcquisitionProtocol,
            valid_series_columns.DateTimeStarted,
            valid_series_columns.SizeSpecificDoseEstimation
            # valid_study_columns.RequestedProcedureCodeMeaning,
        ]
    )

    return rembox.run_query()


def study_data_dictionary(study_data):
    # Vuxna patienter: 16+ och (för all diagnoser utom hjärna) kroppsvikt 60-90 kg
    study_data_adults = study_data.copy()
    study_data_adults = study_data_adults[study_data_adults["patientAge"] >= 16]
    study_data_adults = study_data_adults[
        (study_data_adults["procedureCode"] != "Hjärna utan kontrast")
        & (study_data_adults["patientsWeight"] >= 60)
        & (study_data_adults["patientsWeight"] <= 90)
    ]

    # barn 4-15 år
    study_data_kids = study_data.copy()
    study_data_kids = study_data_kids[(study_data_kids["patientAge"] < 16) & (study_data_kids["patientAge"] >= 4)]

    study_data_young_kids = study_data.copy()
    study_data_young_kids = study_data_young_kids[study_data_young_kids["patientAge"] < 4]

    study_data_dict = {
        "adults": study_data_adults,
        "kids": study_data_kids,
        "young_kids": study_data_young_kids,
    }

    return study_data_dict


def study_data_report(study_data_dict, series_data):
    # Initialiserar report_dict som är en dictionary som kommer innehålla en DataFrame med undersökningar för
    # varje kombination av maskin, patiengrupp och undersökningstyp som ska rapporteras till SSM
    report_dict = {}

    # Initialiserar list_of_temp_dicts som kommer användas för att lagra en sammanfattning av varje DataFrame i
    # report_dict
    list_of_temp_dicts = []
    list_of_temp_dicts2 = []

    # för varje patientgrupp (adult, kids, young kids)
    for patient_group in study_data_dict:
        print(patient_group)

        # skapa en kopia av den DataFrame som innehåller datat för relevant patientgrupp
        study_data = study_data_dict[patient_group]

        # om patientgruppen är 'adults' så sätts count_criteria till 100 och annars till 50
        count_criteria = get.count_criteria(patient_group=patient_group)

        # Hämta relevanta undersökningskoder för patientgruppen
        procedure_codes = get.procedure_codes_dict(patient_group)

        # för varje relevant undersökning i patientgruppen
        for procedure in procedure_codes:
            # skapa en DataFrame som endast innehåller den undersökningen
            code = str(procedure_codes[procedure])
            procedure_study_data = study_data[study_data["procedureCode"] == code]

            # för varje maskin
            for machine in con.machines_in_region:
                # skapa en DataFrame som endast innehåller undersökningar från den maskinen
                procedure_study_data_on_machine = procedure_study_data[procedure_study_data["machine"] == machine]
                # räkna antal undersökningar i DataFrame
                study_count = procedure_study_data_on_machine["patientDbId"].count()

                # om antalet undersökningar i DataFrame överstiger count_criteria
                if study_count >= count_criteria:
                    report_dict[(patient_group, procedure, machine)] = procedure_study_data_on_machine

                    # skapa en dict med patiengrupp, undersökning, labb och antal undersökningar och lägg till i
                    temp_dict = {
                        "patientGroup": patient_group,
                        "procedure": procedure,
                        "machine": machine,
                        "count": study_count,
                    }

                    list_of_temp_dicts.append(temp_dict)
                else:
                    # skapa en dict med patiengrupp, undersökning, labb och antal undersökningar och lägg till i
                    temp_dict = {
                        "patientGroup": patient_group,
                        "procedure": procedure,
                        "machine": machine,
                        "count": study_count,
                    }

                    list_of_temp_dicts2.append(temp_dict)

    summary_df = pd.DataFrame.from_records(list_of_temp_dicts)
    summary_df2 = pd.DataFrame.from_records(list_of_temp_dicts2)
    return summary_df, summary_df2, report_dict


def count_criteria(patient_group):
    if patient_group == "adults":
        return 100
    else:
        return 50


def procedure_codes_dict(patient_group):
    if patient_group == "adults":
        return con.procedure_codes_adults
    elif patient_group == "kids":
        return con.procedure_codes_kids
    else:
        return con.procedure_codes_young_kids
