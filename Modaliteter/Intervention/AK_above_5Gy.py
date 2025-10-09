

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Evaluate the need for patient follow up due to high skin doses from fluoroscopic procedures

        Local follow-up limit is 5000 mGy air-kerma from a single procedure or accumulated during 6 months for the same patient. <br>
        Import the operator name translation list ("operators_202X") to <i>rvbrtg/Data/input_data</i>.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Import from REMbox""")
    return


@app.cell
def _():
    import pandas as pd 
    import plotly.express as px
    import plotly.graph_objects as go
    from pathlib import Path
    from datetime import datetime
    from rembox_integration_tools import REMboxDataQuery
    from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
    from pathlib import Path

    CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
    CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"
    TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
    API_URI = "https://rembox.vll.se/api"
    ORIGIN_URI = "https://rembox.vll.se"

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

    COL_OPERATOR_NAME = "operatorName"
    COL_RP_6M = "doseRPTotal_6m_sum"
    return (
        COL_OPERATOR_NAME,
        COL_RP_6M,
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
            machine_types=["XASTAT"], # Mobile C-arm-XAMOB or is optional
            machines=["U105", "U106", "U104", "U601", "U602", "Arytmi 1", "Arytmi 2"] # INR, IR 1+2, PCI 1+2, Arytmi 1+2
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
    #Fetch data from REMbox
    study_data, series_data = get_data_from_fluoro(rembox=rembox)
    return series_data, study_data


@app.cell
def _():
    #Export to csv
    #study_data.to_csv(Path(__file__).parent.parent.parent / "Data/output_data/XA_study_202X.csv")
    #series_data.to_csv(Path(__file__).parent.parent.parent / "Data/output_data/XA_series_202X.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Management of dataframes""")
    return


@app.cell
def _(series_data, study_data):
    study = study_data.copy() #Create copy of dataframe on study-level
    series = series_data.copy() #Create copy of dataframe on series-level
    return (study,)


@app.cell
def _(study, valid_study_columns):
    # Convert to Europe/Stockholm timezone
    study[valid_study_columns.StudyDateTime] = study[valid_study_columns.StudyDateTime].dt.tz_convert('Europe/Stockholm')
    return


@app.cell
def _(px, study, valid_study_columns):
    fig = px.scatter(
            study,
            x=valid_study_columns.StudyDateTime,
            y=valid_study_columns.DoseRPTotal,
            color=valid_study_columns.Machine,
            custom_data=[valid_study_columns.AccessionNumber, valid_study_columns.AcquisitionPlane, valid_study_columns.Machine],
            title='Dose in Reference point'
        )
        # Set hovertemplate to show full datetime with hours, minutes, seconds
    fig.update_traces(
        hovertemplate=
            "studyDateTime: %{x|%Y-%m-%d %H:%M:%S}<br>" +
            "doseRPTotal: <b>%{y:.1f}</b><br>" +
            "machine: %{customdata[2]}<br>" +
            "accessionNumber: %{customdata[0]}<br>" +
            "acquisitionPlane: %{customdata[1]}"
    )
    fig.show()
    return


@app.cell
def _(study):
    number = study['patientDbId'].count()
    patients = study['patientDbId'].nunique()
    print("In the dataset there are", number, "procedures distributed over", patients, "patients.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Add operator names""")
    return


@app.cell
def _(COL_OPERATOR_NAME, Path, __file__, pd, study, valid_study_columns):
    # Translation from pseudo-operators to operators
    names_data_path = Path(__file__).parent.parent.parent / "Data/input_data/operators_2025.xlsx"
    names = pd.read_excel(names_data_path)
    # Format to fit study-dataframe
    names.columns = [valid_study_columns.PerformingPhysicianName, COL_OPERATOR_NAME]
    # Merge with study
    study_names = study.merge(names, on=[valid_study_columns.PerformingPhysicianName], how='left')
    print(study_names[COL_OPERATOR_NAME])
    return (study_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Studies with air-kerma above 5Gy""")
    return


@app.cell
def _(COL_OPERATOR_NAME, study_names, valid_study_columns):
    study_5Gy = study_names[study_names[valid_study_columns.DoseRPTotal] > 5000]
    study_5Gy[[valid_study_columns.AccessionNumber, valid_study_columns.StudyDateTime, valid_study_columns.PatientDbId, valid_study_columns.StudyDescription, valid_study_columns.Machine, valid_study_columns.DoseRPTotal, valid_study_columns.AcquisitionPlane, COL_OPERATOR_NAME]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Accumulated doses during the past 6 months above 5Gy 
        **Note:** Only reoccuring patients during the dataframe time interval. To include more procedures the time interval must be increased.
        """
    )
    return


@app.cell
def _(COL_OPERATOR_NAME, COL_RP_6M, study_names, valid_study_columns):
    # Exclude rows with 'Plane B' in acquisitionPlane
    study_names_filtered = study_names[study_names[valid_study_columns.AcquisitionPlane] != 'Plane B']

    # Find patientIds that occur more than once
    duplicate_patients = study_names_filtered[valid_study_columns.PatientDbId].value_counts()
    duplicate_patients = duplicate_patients[duplicate_patients > 1].index

    # Filter only those patients
    df_duplicates = study_names_filtered[study_names_filtered[valid_study_columns.PatientDbId].isin(duplicate_patients)].copy()

    # Sort by patientId and studyDateTime
    df_duplicates = df_duplicates.sort_values([valid_study_columns.PatientDbId, valid_study_columns.StudyDateTime])

    # For each patient, calculate rolling 6-month sum of doseRPTotal
    def rolling_6m_sum(df):
        df = df.set_index(valid_study_columns.StudyDateTime)
        # Rolling window of 183 days (~6 months), right-closed
        df[COL_RP_6M] = df[valid_study_columns.DoseRPTotal].rolling('183D', min_periods=1).sum()
        return df.reset_index()

    result = (
        df_duplicates
        .groupby(valid_study_columns.PatientId, group_keys=False)
        .apply(rolling_6m_sum, include_groups=False)
    )

    # View the results
    result_5Gy_6M = result[result[COL_RP_6M] > 5000]
    result_5Gy_6M[[valid_study_columns.AccessionNumber, valid_study_columns.StudyDateTime, valid_study_columns.PatientDbId, valid_study_columns.StudyDescription, valid_study_columns.Machine, valid_study_columns.DoseRPTotal, valid_study_columns.AcquisitionPlane, COL_OPERATOR_NAME]]
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
