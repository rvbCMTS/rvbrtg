import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Importer av paket och data från REMbox
    """)
    return


@app.cell
def _():
    import pandas as pd 
    import math
    import hvplot.pandas #noqa #plotpaket
    from datetime import datetime
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    from rembox_integration_tools import REMboxDataQuery
    from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
    from pathlib import Path

    # om plotly önskas så skrivs följande hvplot.extension("plotly")
    hvplot.extension("bokeh")

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
        REMboxDataQuery,
        go,
        make_subplots,
        math,
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
            machines=["U110", "S08", "S08_2025", "L3"] # Umeå, Skellefteå, Lycksele
        )

        #rembox.filter_options.set_exclusive_tags() om jag vill ange filter där man bortser från ett visst kriterie

        rembox.filter_options.patient_age_interval_include_nulls = True

        rembox.filter_options.study_time_interval_start_date = "2025-01-01T00:00:00Z"
        rembox.filter_options.study_time_interval_end_date = "2025-12-31T00:00:00Z"

        rembox.deanonymize_performing_physician = True

        rembox.add_columns(
            columns=[
                valid_study_columns.StudyDateTime,
                valid_study_columns.AccessionNumber,
                valid_study_columns.AcquisitionDoseAreaProductTotal,
                valid_study_columns.AcquisitionDoseRPTotal,
                valid_study_columns.AcquisitionPlane,
                #valid_study_columns.CalibrationDate,
                #valid_study_columns.CalibrationFactor,
                #valid_study_columns.CalibrationProtocol,
                #valid_study_columns.CalibrationResponsibleParty,
                #valid_study_columns.CalibrationUncertainty,
                valid_study_columns.City,
                valid_study_columns.ConvFluoroClassifier,
                valid_study_columns.DoseAreaProductTotal,
                valid_study_columns.DoseMeasurementDevice,
                valid_study_columns.DoseRPTotal,
                valid_study_columns.FluoroDoseAreaProductTotal,
                valid_study_columns.FluoroDoseRPTotal,
                valid_study_columns.HasIntent,
                #valid_study_columns.HalfValueLayer,
                valid_study_columns.Hospital,
                valid_study_columns.Id,
                valid_study_columns.Machine,
                #valid_study_columns.MeanBodyThickness,
                #valid_study_columns.MaximumBodyThickness,
                #valid_study_columns.MinimumBodyThickness,
                valid_study_columns.PatientAge,
                valid_study_columns.PatientAgeUnit,
                valid_study_columns.PatientDbId,
                valid_study_columns.PatientId,
                #valid_study_columns.PatientModel,
                #valid_study_columns.PatientsBodyMassIndex,
                #valid_study_columns.PatientsName,
                valid_study_columns.PatientsSex,
                valid_study_columns.PatientsSize,
                valid_study_columns.PatientsSizeDate,
                valid_study_columns.PatientsSizeSource,
                valid_study_columns.PatientsWeight,
                valid_study_columns.PatientsWeightDate,
                valid_study_columns.PatientsWeightSource,
                #valid_study_columns.PerformingPhysicianIdentificationSequence,
                valid_study_columns.PSD, # ------------------------------------------------------PSD?
                valid_study_columns.PerformingPhysicianName,
                #valid_study_columns.PregnancyStatus,
                valid_study_columns.ProcedureCode,
                valid_study_columns.ProcedureCodeMeaning,
                valid_study_columns.ProcedureReported,
                valid_study_columns.ProtocolCode,
                valid_study_columns.ProtocolCodeMeaning,
                #valid_study_columns.ReferenceAuthority,
                #valid_study_columns.ReferencedSopInstanceUid,
                valid_study_columns.ReferencePointDefinition,
                #valid_study_columns.ReferencePointDefinitionCode,
                valid_study_columns.ReferringPhysicianIdentificationSequence,
                valid_study_columns.ReferringPhysiciansName,
                #valid_study_columns.RequestedProcedureCode,
                #valid_study_columns.RequestedProcedureCodeMeaning,
                valid_study_columns.ScopeOfAccumulation,
                valid_study_columns.SoftwareVersions,
                #valid_study_columns.StartOfXrayIrradiation,
                #valid_study_columns.StudyDateTime, --------- La denna överst
                valid_study_columns.StudyDescription,
                valid_study_columns.StudyId,
                valid_study_columns.StudyInstanceUID,
                valid_study_columns.TotalAcquisitionTime,
                valid_study_columns.TotalFluoroTime,
                valid_study_columns.TotalNumberOfIrradiationEvents,
                valid_study_columns.TotalNumberOfRadiographicFrames,
                valid_series_columns.AcquisitionPlaneSeries,
                valid_series_columns.AcquisitionProtocol,
                #valid_series_columns.AcquisitionType,
                #valid_series_columns.ApplicationName, #--------------------------------------Här finns protokollnamn för Azurion
                #valid_series_columns.AnatomicalStructure,
                #valid_series_columns.AnodeTargetMaterial,
                valid_series_columns.AverageXrayTubeCurrent,
                valid_series_columns.CollimatedFieldArea,
                valid_series_columns.CollimatedFieldHeight,
                valid_series_columns.CollimatedFieldWidth,
                #valid_series_columns.ColumnAngulation,
                #valid_series_columns.CrdrMechanicalConfiguration,
                valid_series_columns.DateTimeStarted,
                #valid_series_columns.DerivedEffectiveDiameter,
                #valid_series_columns.DeviationIndex,
                valid_series_columns.DistanceSourceToDetector,
                valid_series_columns.DistanceSourceToIsocenter,
                valid_series_columns.DistanceSourceToReferencePoint,
                #valid_series_columns.DistanceSourceToTablePlane,
                valid_series_columns.DoseAreaProduct,
                valid_series_columns.DoseRP,
                #valid_series_columns.EffectiveDose,
                #valid_series_columns.EffectiveDoseConversionFactor,
                #valid_series_columns.EntranceExposureAtRP,
                #valid_series_columns.ExposedRange,
                valid_series_columns.Exposure,
                #valid_series_columns.ExposureIndex,
                #valid_series_columns.ExposureTime,
                #valid_series_columns.ExposureTimePerRotation,
                valid_series_columns.FluoroMode,
                #valid_series_columns.FluoroFlavour, # -------------------------------------------- Här finns pulsrat för Azurion
                #valid_series_columns.FrameOfReferenceUID,
                #valid_series_columns.IdentificationOfTheXraySource,
                #valid_series_columns.ImageView,
                #valid_series_columns.ImageViewModifier,
                valid_series_columns.IrradiationDuration,
                #valid_series_columns.IrradiationEventLabel,
                valid_series_columns.IrradiationEventType,
                valid_series_columns.IrradiationEventUID,
                valid_series_columns.kVp,
                #valid_series_columns.LabelType,
                #valid_series_columns.Laterality,
                #valid_series_columns.MaximumXrayTubeCurrent,
                #valid_series_columns.MeasurementMethodDose,
                #valid_series_columns.NominalCollimationWidth,
                #valid_series_columns.NominalTotalCollimationWidth,
                valid_series_columns.NumberOfPulses,
                #valid_series_columns.NumberOfXraySources,
                valid_series_columns.PatientEquivalentThickness,
                valid_series_columns.PatientOrientation,
                valid_series_columns.PatientOrientationModifier,
                valid_series_columns.PatientTableRelationship,
                valid_series_columns.PositionerPrimaryAngle,
                #valid_series_columns.PositionerPrimaryEndAngle,
                valid_series_columns.PositionerSecondaryAngle,
                #valid_series_columns.PositionerSecondaryEndAngle,
                #valid_series_columns.ProcedureContext,
                #valid_series_columns.ProjectionEponymousName,
                valid_series_columns.PulseRate,
                valid_series_columns.PulseWidth,
                #valid_series_columns.ReconstructionAlgortihm,
                valid_series_columns.ReferencePointDefinitionText,
                valid_series_columns.SpotSize,
                valid_series_columns.TableCradleTiltAngle,
                valid_series_columns.TableHeadTiltAngle,
                #valid_series_columns.TableHeightEndPosition,
                valid_series_columns.TableHeightPosition,
                valid_series_columns.TableHorizontalRotationAngle,
                #valid_series_columns.TableLateralEndPosition,
                valid_series_columns.TableLateralPosition,
                #valid_series_columns.TableLongitudinalEndPosition,
                valid_series_columns.TableLongitudinalPosition,
                #valid_series_columns.TargetExposureIndex,
                valid_series_columns.TargetRegion,
                #valid_series_columns.WaterEquivalentDiameter,
                #valid_series_columns.WedMeasurementMethod,
                #valid_series_columns.XrayFilterAluminumEquivalent,
                valid_series_columns.XrayFilterMaterial,
                valid_series_columns.XrayFilterThicknessMaximum,
                valid_series_columns.XrayFilterThicknessMinimum,
                valid_series_columns.XrayFilterType,
                #valid_series_columns.XrayGrid,
                #valid_series_columns.XrayGridAspectRatio,
                #valid_series_columns.XrayGridFocalDistance,
                #valid_series_columns.XrayGridPitch,
                #valid_series_columns.XrayModulationType,
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
    #study_data.to_csv("C:/Users/chgr09/GIT/rvbrtg/Data/output_data/XA_study_2025.csv")
    #series_data.to_csv("C:/Users/chgr09/GIT/rvbrtg/Data/output_data/XA_series_2025.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kontroller av data och hantering av dataframes
    """)
    return


@app.cell
def _(series_data, study_data):
    study = study_data.copy() #skapa kopia av dataframe på study-nivå för att kunna behålla orginalet
    series = series_data.copy() #skapa kopia av dataframe på serie-nivå för att kunna behålla orginalet

    #TODO: Fixa detta för aktuella testpatienter.
    #Ta bort undersökningar från testpatient U105 som har PatientId = LO_sgY+/xUXOYtGGM1+o+JXSO9IQy9LaYFpsPIl/UAWtP0=
    #Ta bort undersökningar från testpatient U106 som har PatientId = LO_9a9c67eb_5dc1_43ed_8008_858c4683e27d
    return series, study


@app.cell
def _(study):
    study.head()
    return


@app.cell
def _(series, study):
    exams = study['patientDbId'].count()
    patients = study['patientDbId'].nunique()
    print(exams, 'undersökningar/ingrepp fördelat på', patients, 'patienter')
    series_no_duplicates = series[(series['xrayFilterMaterial'] == 'Copper') | (series['xrayFilterMaterial'] == 'Copper or Copper compound')]
    print(len(series_no_duplicates), 'antal irradiation events')
    return


@app.cell
def _(study):
    study['normalisedFluoroDap'] = study['fluoroDoseAreaProductTotal'] / study['totalFluoroTime']
    study['normalisedAcqDap'] = study['acquisitionDoseAreaProductTotal'] / study['totalAcquisitionTime']
    study['normalisedFluoroRP'] = study['fluoroDoseRPTotal'] / study['totalFluoroTime']
    study['normalisedAcqRP'] = study['acquisitionDoseRPTotal'] / study['totalAcquisitionTime']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lägg till operatörsnamn
    """)
    return


@app.cell
def _(pd, study):
    names_data_path = 'C:/Projekt/GIT/rvbrtg/Data/input_data/operators_2025.xlsx'
    names = pd.read_excel(names_data_path)
    # Rename according to the file's columns: PseudoValue -> performingPhysicianName, OriginalValue -> operatorName
    names.columns = ['performingPhysicianName', 'operatorName']
    # Build mapping and add operatorName column without reassigning the study dataframe
    operator_dict = names.set_index('performingPhysicianName')['operatorName'].to_dict()
    study['operatorName'] = study['performingPhysicianName'].map(operator_dict)
    return


@app.cell
def _():
    #study.to_csv('C:/Projekt/GIT/rvbrtg/Data/output_data/Operators_missing_GML_2025.csv')
    return


@app.cell
def _(px, study):
    fig_all = px.scatter(study, x='studyDateTime', y='doseAreaProductTotal', color='machine')
    fig_all.show()
    return


@app.cell
def _(px, series):
    fig_kVp = px.scatter(series[series['kVp'] > 0], x='dateTimeStarted', y='kVp', color='acquisitionProtocol', hover_data=['accessionNumber'])
    fig_kVp.show()

    #TODO: Gör analysen mer detaljerad för att urskilja vilka protokoll som systematiskt har högre kVp och undersök om sysemet maxas ut. Kanske plotta någon slags medel-kVp?
    return


@app.cell
def _(study):
    procedure_dap = study.groupby(
        ['procedureCode', 'procedureCodeMeaning', 'machine', 'acquisitionPlane']
        ).agg(
            {'doseAreaProductTotal': ['sum', 'median'],
            'fluoroDoseAreaProductTotal': 'median',
            'totalFluoroTime': 'median',
            'normalisedFluoroDap': 'median',
            'procedureCode': 'count'}
            ).reset_index().round(3)
    procedure_dap
    return


@app.cell
def _(study):
    procedure_dap_operator = study.groupby(
        ['procedureCode', 'procedureCodeMeaning', 'machine', 'acquisitionPlane', 'operatorName']
        ).agg({'doseAreaProductTotal': ['count', 'median'], 
        'fluoroDoseAreaProductTotal': 'median', 
        'totalFluoroTime': 'median', 
        'normalisedFluoroDap': 'median'}
        ).reset_index().round(3)
    procedure_dap_operator
    return


@app.cell
def _(study):
    removals_procCode = study['procedureCodeMeaning'].value_counts().reset_index()
    removals_procCode = removals_procCode[removals_procCode['count'] > 10]
    filtered_procCode = study[study['procedureCodeMeaning'].isin(removals_procCode['procedureCodeMeaning'])]
    filtered_procedure_dap = filtered_procCode[filtered_procCode['machine'] == 'U110'].groupby(
        ['procedureCode', 'procedureCodeMeaning', 'machine']
        ).agg({'doseAreaProductTotal': ['count', 'median'], 
        'acquisitionDoseAreaProductTotal': 'median', 
        'fluoroDoseAreaProductTotal': 'median', 
        'totalFluoroTime': 'median', 
        'normalisedFluoroDap': 'median'}
        ).reset_index().round(3)
    filtered_procedure_dap
    return


@app.cell
def _(px, study):
    fig_procCode_dap = px.box(study, x='procedureCodeMeaning', y='doseAreaProductTotal', color='machine')
    fig_procCode_dap.update_layout(height=1000)
    fig_procCode_dap.show()
    return


@app.cell
def _(go, make_subplots, math, study):
    study_U110 = study[study['machine'] == 'U110']
    removals_procCode_U110 = study_U110['procedureCodeMeaning'].value_counts().reset_index()
    removals_procCode_U110 = removals_procCode_U110[removals_procCode_U110['count'] > 10]
    filtered_procCode_U110 = study_U110[study_U110['procedureCodeMeaning'].isin(removals_procCode_U110['procedureCodeMeaning'])]
    unique_procedure_codes_U110 = filtered_procCode_U110['procedureCode'].unique()
    num_procedures = len(unique_procedure_codes_U110)
    grid_size = math.ceil(math.sqrt(num_procedures))
    median_dap = filtered_procCode_U110.groupby('procedureCode')['doseAreaProductTotal'].median()
    fig_procCode_U110 = make_subplots(rows=grid_size, cols=grid_size, specs=[[{'type': 'domain'} for _ in range(grid_size)] for _ in range(grid_size)], subplot_titles=[f'ProcedureCode {code}<br>Median DAP: {median_dap[code]:.2f}' if code in median_dap else f'ProcedureCode {code}' for code in unique_procedure_codes_U110])
    for idx, code in enumerate(unique_procedure_codes_U110):
        row = idx // grid_size + 1
        col = idx % grid_size + 1
        procedure_data = filtered_procCode_U110[filtered_procCode_U110['procedureCode'] == code]
        acquisition_dap = procedure_data['acquisitionDoseAreaProductTotal'].median()
        fluoro_dap = procedure_data['fluoroDoseAreaProductTotal'].median()
        values = [acquisition_dap, fluoro_dap]
        labels = ['Acquisition DAP', 'Fluoro DAP']
        fig_procCode_U110.add_trace(go.Pie(labels=labels, values=values, name=f'ProcedureCode {code}'), row=row, col=col)
    fig_procCode_U110.update_layout(height=300 * grid_size, width=300 * grid_size, title_text='Median DAP Distribution for All ProcedureCodes', showlegend=True)
    fig_procCode_U110.show()
    return


@app.cell
def _(study):
    median_KAP_studytype = study.groupby(['procedureCode', 'procedureCodeMeaning', 'operatorName', 'machine']
    ).agg({'doseAreaProductTotal': ['min', 'median', 'max'], 
    'normalisedFluoroDap': 'median',
    'procedureCode': 'count'}
    ).reset_index().round(3)
    median_KAP_studytype
    return


@app.cell
def _(px, study):
    removals_procCode_all = study['procedureCodeMeaning'].value_counts().reset_index()
    removals_procCode_all = removals_procCode_all[removals_procCode_all['count'] > 20]
    removals = removals_procCode_all
    filtered_procCode_all = study[study['procedureCodeMeaning'].isin(removals['procedureCodeMeaning'])]
    fig_procCode_all = px.box(filtered_procCode_all, x='procedureCodeMeaning', y='doseAreaProductTotal', color='machine', points='all')
    fig_procCode_all.update_layout(height=1000)
    fig_procCode_all.show()
    return


@app.cell
def _(px, series):
    fig_fluoro = px.box(series[series.irradiationEventType == 'Fluoroscopy'], x='acquisitionProtocol', y='doseAreaProduct')
    fig_fluoro.show()
    return


@app.cell
def _(px, study):
    fig_operator = px.box(study, x='protocolCodeMeaning', y='doseAreaProductTotal', color='operatorName')
    fig_operator.show()
    return


@app.cell
def _(series):
    export = series[series.accessionNumber == 'SERUMEXXX']
    export.to_excel('C:/Users/chgr09/GIT/rvbrtg/Data/output_data/XXX.xlsx')
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
