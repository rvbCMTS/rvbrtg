

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Import from REMbox
        """
    )
    return


@app.cell
def _():
    import pandas as pd 
    import plotly.express as px
    from pathlib import Path
    from datetime import datetime
    from rembox_integration_tools import REMboxDataQuery
    from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
    from pathlib import Path

    CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
    CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"
    TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token" #Var finns access token
    API_URI = "https://rembox.vll.se/api" #Var finns API:t
    ORIGIN_URI = "https://rembox.vll.se" #Vilken URL

    rembox = REMboxDataQuery(
        client_id_environment_variable=CLIENT_ID_ENV_VAR,
        client_secret_environment_variable=CLIENT_PWD_ENV_VAR,
        token_uri=TOKEN_URI,
        api_uri=API_URI,
        origin_uri=ORIGIN_URI,
        verify_ssl_cert=False
    )

    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()
    return (
        Path,
        REMboxDataQuery,
        pd,
        px,
        rembox,
        valid_series_columns,
        valid_study_columns,
    )


@app.cell
def _(REMboxDataQuery, pd, rembox, valid_series_columns, valid_study_columns):
    rembox.reset_filter_options()
    def get_data_from_fluoro(rembox: REMboxDataQuery) -> tuple[pd.DataFrame, pd.DataFrame]:


        rembox.filter_options.set_inclusive_tags(
            machine_types=["XASTAT"],     # CT-CT, Fluoroscopic-XASTAT, Mobile C-arm-XAMOB, Conventional-DX, Mammography-MG, Intraoral-IO, Panoramic-PX, Dental Cone Beam CT-DCBCT, PET-PET, PET/CT-PETCT, SPECT-SPECT, SPECT/CT-SPECTCT, Nuclear Medicine-NM, Mobile X-ray-DXMOB, Conventional with fluoro-DXXA
            machines=["U105", "U106", "U104", "U601", "U602", "Arytmi 1", "Arytmi 2"]        # INR, IR 1+2, PCI 1+2, Arytmi 1+2
        )

        rembox.filter_options.patient_age_interval_include_nulls = True

        rembox.filter_options.study_time_interval_start_date = "2024-01-01T00:00:00Z"
        rembox.filter_options.study_time_interval_end_date = "2025-06-27T00:00:00Z"


        rembox.add_columns(
            columns=[
                valid_study_columns.AccessionNumber,
                valid_study_columns.AcquisitionDoseAreaProductTotal,
                valid_study_columns.AcquisitionDoseRPTotal,
                valid_study_columns.AcquisitionPlane,
                valid_study_columns.DoseAreaProductTotal,
                valid_study_columns.DoseRPTotal,
                valid_study_columns.FluoroDoseAreaProductTotal,
                valid_study_columns.FluoroDoseRPTotal,
                valid_study_columns.Id,
                valid_study_columns.Machine,
                valid_study_columns.PatientAge,
                valid_study_columns.PatientAgeUnit,
                valid_study_columns.PatientDbId,
                valid_study_columns.PatientId,
                valid_study_columns.PatientsSex,
                valid_study_columns.PatientsSize,
                valid_study_columns.PatientsSizeDate,
                valid_study_columns.PatientsWeight,
                valid_study_columns.PatientsWeightDate,
                valid_study_columns.PerformingPhysicianName,
                valid_study_columns.ProcedureCode,
                valid_study_columns.ProcedureCodeMeaning,
                valid_study_columns.ProcedureReported,
                valid_study_columns.ProtocolCode,
                valid_study_columns.ProtocolCodeMeaning,
                valid_study_columns.SoftwareVersions,
                valid_study_columns.StudyDateTime,
                valid_study_columns.StudyDescription,
                valid_study_columns.StudyId,
                valid_study_columns.StudyInstanceUID,
                valid_study_columns.TotalAcquisitionTime,
                valid_study_columns.TotalFluoroTime,
                valid_study_columns.TotalNumberOfIrradiationEvents,
                valid_study_columns.TotalNumberOfRadiographicFrames,
                valid_series_columns.AcquisitionPlaneSeries,
                valid_series_columns.AcquisitionProtocol,
                valid_series_columns.AcquisitionType,
                valid_series_columns.AverageXrayTubeCurrent,
                valid_series_columns.CollimatedFieldArea,
                valid_series_columns.CollimatedFieldHeight,
                valid_series_columns.CollimatedFieldWidth,
                valid_series_columns.DateTimeStarted,
                valid_series_columns.DistanceSourceToDetector,
                valid_series_columns.DistanceSourceToIsocenter,
                valid_series_columns.DistanceSourceToReferencePoint,
                valid_series_columns.DistanceSourceToTablePlane,
                valid_series_columns.DoseAreaProduct,
                valid_series_columns.DoseRP,
                valid_series_columns.Exposure,
                valid_series_columns.ExposureTime,
                valid_series_columns.FluoroMode,
                valid_series_columns.IrradiationDuration,
                valid_series_columns.IrradiationEventLabel,
                valid_series_columns.IrradiationEventType,
                valid_series_columns.IrradiationEventUID,
                valid_series_columns.kVp,
                valid_series_columns.NumberOfPulses,
                valid_series_columns.PatientEquivalentThickness,
                valid_series_columns.PatientTableRelationship,
                valid_series_columns.PositionerPrimaryAngle,
                #valid_series_columns.PositionerPrimaryEndAngle,
                valid_series_columns.PositionerSecondaryAngle,
                #valid_series_columns.PositionerSecondaryEndAngle,
                valid_series_columns.PulseRate,
                valid_series_columns.PulseWidth,
                valid_series_columns.SpotSize,
                valid_series_columns.TableHeightPosition,
                valid_series_columns.TableLateralPosition,
                valid_series_columns.TableLongitudinalPosition,
                valid_series_columns.XrayFilterMaterial,
                valid_series_columns.XrayFilterThicknessMaximum,
                valid_series_columns.XrayTubeCurrent
            ]
        )

        return rembox.run_query()
    return (get_data_from_fluoro,)


@app.cell
def _(get_data_from_fluoro, rembox):
    #Hämta data från REMbox
    study_data, series_data = get_data_from_fluoro(rembox=rembox)
    return series_data, study_data


@app.cell
def _():
    #Export av data till csv
    #study_data.to_csv(Path(__file__).parent.parent.parent / "Data/output_data/XA_study_2026.csv")
    #series_data.to_csv(Path(__file__).parent.parent.parent / "Data/output_data/XA_series_2026.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Management of dataframes""")
    return


@app.cell
def _(series_data, study_data):
    study = study_data.copy() #skapa kopia av dataframe på study-nivå för att kunna behålla orginalet
    series = series_data.copy() #skapa kopia av dataframe på serie-nivå för att kunna behålla orginalet
    return series, study


@app.cell
def _(pd, series, study):
    # Ensure studyDateTime and dateTimeStarted is in datetime format
    study['studyDateTime'] = pd.to_datetime(study['studyDateTime'])
    series['dateTimeStarted'] = pd.to_datetime(series['dateTimeStarted'])
    # Add two hours
    study['studyDateTime'] = study['studyDateTime'] + pd.DateOffset(hours=2)
    series['dateTimeStarted'] = series['dateTimeStarted'] + pd.DateOffset(hours=2)
    return


@app.cell
def _(px, study):
    fig = px.scatter(study, x='studyDateTime', y='doseRPTotal', color='machine', hover_data=['accessionNumber', 'doseRPTotal', 'acquisitionPlane'], title='Dose in Reference point')
    fig.show()
    return


@app.cell
def _(study):
    antal = study['patientDbId'].count()
    patienter = study['patientDbId'].nunique()
    print("In the dataset there are", antal, "procedures distributed over", patienter, "patients.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Lägg till operatörsnamn
        """
    )
    return


@app.cell
def _(Path, __file__, pd):
    # Översättningstabell från pseudo-operatörer till operatörer
    names_data_path = Path(__file__).parent.parent.parent / "Data/input_data/operators_2025.xlsx"
    names = pd.read_excel(names_data_path)
    #Formattera så det passar befintlig dataframe
    names.columns = ["performingPhysicianName", "OperatorName"]
    #names.head()
    return (names,)


@app.cell
def _(names, study):
    study_names = study.merge(names, on=['performingPhysicianName'], how='left')
    #print(study_names.OperatorName)
    return (study_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Undersökningar som överstigit 5Gy
        """
    )
    return


@app.cell
def _(study_names):
    study_5Gy = study_names[study_names['doseRPTotal'] > 5000]
    study_5Gy[['accessionNumber', 'studyDateTime', 'patientDbId', 'studyDescription', 'machine', 'doseRPTotal', 'acquisitionPlane', 'OperatorName']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Accumulerade doser över 6 månader som överstigit 
        **Note:** Only reoccuring patients during the dataframe time interval
        """
    )
    return


@app.cell
def _(study_names):
    # Exclude rows with 'Plane B' in acquisitionPlane
    study_names_filtered = study_names[study_names['acquisitionPlane'] != 'Plane B']

    # Find patientIds that occur more than once
    duplicate_patients = study_names_filtered['patientDbId'].value_counts()
    duplicate_patients = duplicate_patients[duplicate_patients > 1].index

    # Filter only those patients
    df_duplicates = study_names_filtered[study_names_filtered['patientDbId'].isin(duplicate_patients)].copy()

    # Sort by patientId and studyDateTime
    df_duplicates = df_duplicates.sort_values(['patientDbId', 'studyDateTime'])

    # For each patient, calculate rolling 6-month sum of doseRPTotal
    def rolling_6m_sum(df):
        df = df.set_index('studyDateTime')
        # Rolling window of 183 days (~6 months), right-closed
        df['doseRPTotal_6m_sum'] = df['doseRPTotal'].rolling('183D', min_periods=1).sum()
        return df.reset_index()

    result = (
        df_duplicates
        .groupby('patientId', group_keys=False)
        .apply(rolling_6m_sum, include_groups=False)
    )

    # View the results
    result_5Gy = result[result['doseRPTotal_6m_sum'] > 5000]
    result_5Gy[['accessionNumber', 'studyDateTime', 'patientDbId', 'studyDescription', 'machine', 'doseRPTotal', 'doseRPTotal_6m_sum', 'acquisitionPlane', 'OperatorName']]
    return


@app.cell
def _():
    # Detailed analysis of single patients
    #study_names[study_names['patientDbId'] == #Insert PatientDbId here]
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
