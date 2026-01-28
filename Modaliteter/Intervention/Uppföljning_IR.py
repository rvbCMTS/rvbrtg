import marimo

__generated_with = "0.17.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Importer av paket och data från REMbox""")
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
        datetime,
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
            machines=["U104"]#, "U601", "U602", "Arytmi1", "Arytmi2", "Arytmi2_2024"]        # INR, IR1, IR2, PCI1, PCI2, Morran, Mumin
        )

        #rembox.filter_options.set_exclusive_tags() om jag vill ange filter där man bortser från ett visst kriterie

        rembox.filter_options.patient_age_interval_include_nulls = True

        rembox.filter_options.study_time_interval_start_date = "2025-01-01T00:00:00Z"
        rembox.filter_options.study_time_interval_end_date = "2025-10-29T00:00:00Z"

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
    #study_data.to_csv("C:/Users/chgr09/GIT/rvbrtg/Data/output_data/XA_study_2023.csv")
    #series_data.to_csv("C:/Users/chgr09/GIT/rvbrtg/Data/output_data/XA_series_2023.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Kontroller av data och hantering av dataframes""")
    return


@app.cell
def _(series_data, study_data):
    study = study_data.copy() #skapa kopia av dataframe på study-nivå för att kunna behålla orginalet
    series = series_data.copy() #skapa kopia av dataframe på serie-nivå för att kunna behålla orginalet

    #Ta bort undersökningar från testpatient U105 som har PatientId = LO_sgY+/xUXOYtGGM1+o+JXSO9IQy9LaYFpsPIl/UAWtP0=
    #Ta bort undersökningar från testpatient U106 som har PatientId = LO_9a9c67eb_5dc1_43ed_8008_858c4683e27d
    return series, study


@app.cell
def _(series, study):
    exams = study['patientDbId'].count()
    patients = study['patientDbId'].nunique()
    print(exams, 'undersökningar/ingrepp fördelat på', patients, 'patienter')
    series_1 = series[(series['xrayFilterMaterial'] == 'Copper') | (series['xrayFilterMaterial'] == 'Copper or Copper compound')]
    print(len(series_1), 'antal irradiation events')
    return (series_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Addering av events för att få med båda planen. Viktigt för Biplan""")
    return


@app.cell
def _(series_1):
    plane_A_doses = series_1[series_1['acquisitionPlaneSeries'] == 'Plane A'].groupby(['studyInstanceUID', 'irradiationEventType']).agg({'doseAreaProduct': 'sum', 'doseRP': 'sum', 'irradiationDuration': 'sum'}).reset_index().round(3)
    plane_A_doses.rename(columns={'doseAreaProduct': 'doseAreaProductPlaneA', 'doseRP': 'doseRpPlaneA', 'irradiationDuration': 'irradiationDurationPlaneA'}, inplace=True)
    plane_B_doses = series_1[series_1['acquisitionPlaneSeries'] == 'Plane B'].groupby(['studyInstanceUID', 'irradiationEventType']).agg({'doseAreaProduct': 'sum', 'doseRP': 'sum', 'irradiationDuration': 'sum'}).reset_index().round(3)
    plane_B_doses.rename(columns={'doseAreaProduct': 'doseAreaProductPlaneB', 'doseRP': 'doseRpPlaneB', 'irradiationDuration': 'irradiationDurationPlaneB'}, inplace=True)
    Plane_A_and_B_doses = plane_A_doses.merge(plane_B_doses, on=['studyInstanceUID', 'irradiationEventType'], how='left')
    Plane_A_and_B_doses.head()
    return


@app.cell
def _(series_1, study):
    rotational_acquisition_plane_a = series_1[series_1['irradiationEventType'] == 'Rotational Acquisition']
    rotational_dap_plane_a = rotational_acquisition_plane_a.groupby('studyInstanceUID')['doseAreaProduct'].sum().reset_index()
    rotational_dap_plane_a.rename(columns={'doseAreaProduct': 'accumulatedRotationalDapPlaneA'}, inplace=True)
    study_1 = study.merge(rotational_dap_plane_a, on='studyInstanceUID', how='left')
    study_1['accumulatedRotationalDapPlaneA'] = study_1['accumulatedRotationalDapPlaneA'].fillna(0)
    study_1.head()
    return (study_1,)


@app.cell
def _(study_1):
    study_1['acquisitionDoseAreaProductTotalminusRotational'] = study_1['acquisitionDoseAreaProductTotal'] - study_1['accumulatedRotationalDapPlaneA']
    study_1['normalisedFluoroDap'] = study_1['fluoroDoseAreaProductTotal'] / study_1['totalFluoroTime']
    study_1['normalisedAcqDap'] = study_1['acquisitionDoseAreaProductTotal'] / study_1['totalAcquisitionTime']
    study_1['normalisedFluoroRP'] = study_1['fluoroDoseRPTotal'] / study_1['totalFluoroTime']
    study_1['normalisedAcqRP'] = study_1['acquisitionDoseRPTotal'] / study_1['totalAcquisitionTime']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Lägg till operatörsnamn""")
    return


@app.cell
def _(pd, study_1):
    names_data_path = 'C:/Projekt/GIT/rvbrtg/Data/input_data/operators_2025.xlsx'
    names = pd.read_excel(names_data_path)
    names.columns = ['performingPhysicianName', 'operatorName']
    study_2 = study_1.merge(names, on=['performingPhysicianName'], how='left')
    return (study_2,)


@app.cell
def _():
    #study_2[(study_2['machine'] == 'U105') | (study_2['machine'] == 'U106')].to_csv('C:/Projekt/GIT/rvbrtg/Data/output_data/Operators_missing_IR_2025.csv')
    return


@app.cell
def _(study_2):
    study_2[(study_2['machine'] == 'U105') | (study_2['machine'] == 'U106')].head()
    return


@app.cell
def _(px, study_2):
    _fig = px.scatter(study_2, x='studyDateTime', y='doseRPTotal', color='machine')
    _fig.show()
    return


@app.cell
def _(series_1):
    series_1[series_1['irradiationEventType'] == 'Rotational Acquisition'].head()
    return


@app.cell
def _(px, series_1):
    _fig = px.scatter(series_1[series_1['kVp'] > 0], x='dateTimeStarted', y='kVp', color='acquisitionProtocol', hover_data=['accessionNumber'])
    _fig.show()
    return


@app.cell
def _(study_2):
    _procedure_dap = study_2.groupby(['procedureCode', 'procedureCodeMeaning', 'machine', 'acquisitionPlane']).agg({'doseAreaProductTotal': ['sum', 'median'], 'fluoroDoseAreaProductTotal': 'median', 'totalFluoroTime': 'median', 'normalisedFluoroDap': 'median', 'procedureCode': 'count'}).reset_index().round(3)
    _procedure_dap.head()
    return


@app.cell
def _(study_2):
    _procedure_dap = study_2.groupby(['procedureCode', 'procedureCodeMeaning', 'machine', 'acquisitionPlane', 'operatorName']).agg({'doseAreaProductTotal': ['count', 'median'], 'acquisitionDoseAreaProductTotal': 'median', 'acquisitionDoseAreaProductTotalminusRotational': 'median', 'accumulatedRotationalDapPlaneA': 'median', 'fluoroDoseAreaProductTotal': 'median', 'totalFluoroTime': 'median', 'normalisedFluoroDap': 'median'}).reset_index().round(3)
    _procedure_dap.head()
    return


@app.cell
def _(study_2):
    _removals = study_2['procedureCodeMeaning'].value_counts().reset_index()
    _removals = _removals[_removals['count'] > 10]
    _removals
    _filtered_df = study_2[study_2['procedureCodeMeaning'].isin(_removals['procedureCodeMeaning'])]
    _procedure_dap = _filtered_df[_filtered_df['machine'] == 'U105'].groupby(['procedureCode', 'procedureCodeMeaning', 'machine']).agg({'doseAreaProductTotal': ['count', 'median'], 'acquisitionDoseAreaProductTotal': 'median', 'acquisitionDoseAreaProductTotalminusRotational': 'median', 'accumulatedRotationalDapPlaneA': 'median', 'fluoroDoseAreaProductTotal': 'median', 'totalFluoroTime': 'median', 'normalisedFluoroDap': 'median'}).reset_index().round(3)
    _procedure_dap.head()
    return


@app.cell
def _(px, study_2):
    _fig = px.box(study_2, x='procedureCodeMeaning', y='doseAreaProductTotal', color='machine')
    _fig.update_layout(height=1000)
    _fig.show()
    return


@app.cell
def _(go, make_subplots, math, study_2):
    study_U105 = study_2[study_2['machine'] == 'U105']
    _removals = study_U105['procedureCodeMeaning'].value_counts().reset_index()
    _removals = _removals[_removals['count'] > 10]
    _filtered_df = study_U105[study_U105['procedureCodeMeaning'].isin(_removals['procedureCodeMeaning'])]
    unique_procedure_codes = _filtered_df['procedureCode'].unique()
    num_procedures = len(unique_procedure_codes)
    grid_size = math.ceil(math.sqrt(num_procedures))
    median_dap = _filtered_df.groupby('procedureCode')['doseAreaProductTotal'].median()
    _fig = make_subplots(rows=grid_size, cols=grid_size, specs=[[{'type': 'domain'} for _ in range(grid_size)] for _ in range(grid_size)], subplot_titles=[f'ProcedureCode {code}<br>Median DAP: {median_dap[code]:.2f}' if code in median_dap else f'ProcedureCode {code}' for code in unique_procedure_codes])
    for idx, code in enumerate(unique_procedure_codes):
        row = idx // grid_size + 1
        col = idx % grid_size + 1
        procedure_data = _filtered_df[_filtered_df['procedureCode'] == code]
        acquisition_dap = procedure_data['acquisitionDoseAreaProductTotalminusRotational'].median()
        fluoro_dap = procedure_data['fluoroDoseAreaProductTotal'].median()
        rotational_dap = procedure_data['accumulatedRotationalDapPlaneA'].median()
        values = [acquisition_dap, fluoro_dap, rotational_dap]
        labels = ['Acquisition DAP', 'Fluoro DAP', 'Rotational DAP']
        _fig.add_trace(go.Pie(labels=labels, values=values, name=f'ProcedureCode {code}'), row=row, col=col)
    _fig.update_layout(height=300 * grid_size, width=300 * grid_size, title_text='Median DAP Distribution for All ProcedureCodes', showlegend=True)
    _fig.show()
    return


@app.cell
def _(study_2):
    median_KAP_studytype = study_2.groupby(['procedureCode', 'procedureCodeMeaning', 'operatorName', 'machine']).agg({'doseAreaProductTotal': ['min', 'median', 'max'], 'normalisedFluoroDap': 'median', 'procedureCode': 'count'}).reset_index().round(3)
    median_KAP_studytype
    return


@app.cell
def _(px, study_2):
    _removals = study_2['procedureCodeMeaning'].value_counts().reset_index()
    _removals = _removals[_removals['count'] > 20]
    _removals
    _filtered_df = study_2[study_2['procedureCodeMeaning'].isin(_removals['procedureCodeMeaning'])]
    _fig = px.box(_filtered_df, x='procedureCodeMeaning', y='doseAreaProductTotal', color='machine', points='all')
    _fig.update_layout(height=1000)
    _fig.show()
    return


@app.cell
def _(px, series_1):
    _fig = px.box(series_1[series_1.irradiationEventType == 'Fluoroscopy'], x='acquisitionProtocol', y='doseAreaProduct')
    _fig.show()
    return


@app.cell
def _(px, study_2):
    _fig = px.box(study_2[study_2['acquisitionPlane'] == 'Plane A'], x='protocolCodeMeaning', y='doseAreaProductTotal', color='operatorName')
    _fig.show()
    return


@app.cell
def _(series_1):
    total_doseRP_study_and_plane = series_1.groupby(['studyInstanceUID', 'accessionNumber', 'acquisitionPlaneSeries']).sum('doseRP').reset_index()
    total_doseRP_study_and_plane.head()
    return


@app.cell
def _(go, study_AB):
    _removals = study_AB['procedureCodeMeaning'].value_counts().reset_index()
    _removals = _removals[_removals['count'] > 10]
    _removals
    filtered_df_planes = study_AB[study_AB['procedureCodeMeaning'].isin(_removals['procedureCodeMeaning'])]
    _fig = go.Figure()
    for machine in study_AB['machine'].unique():
        machine_data = study_AB[study_AB['machine'] == machine]
        _fig.add_trace(go.Box(y=machine_data['doseAreaProduct_A'], x=machine_data['procedureCodeMeaning'], name=f'PlaneA - {machine}'))
        _fig.add_trace(go.Box(y=machine_data['doseAreaProduct_B'], x=machine_data['procedureCodeMeaning'], name=f'PlaneB - {machine}'))
    _fig.update_layout(boxmode='group')
    _fig.show()
    return


@app.cell
def _(px, study_AB):
    _fig = px.scatter(study_AB, x='studyDateTime', y='doseAreaProduct_A', color='machine')
    _fig.show()
    return


@app.cell
def _(study_names_planes):
    #Filtrera fram alla ingrepp där summerade doseRP från study_names_planes överstiger 5 Gy

    study_5Gy_names = study_names_planes[study_names_planes.doseRP > 5000]

    # Kika på innehåll i dataframe
    study_5Gy_names[["accessionNumber","studyDateTime","studyDescription","machine","doseRPTotal","acquisitionPlaneSeries","doseRP","OperatorName"]]
    return


@app.cell
def _(series_data):
    _test = series_data[series_data.accessionNumber == 'SERUME0007751954']
    _test.to_excel('C:/Users/chgr09/GIT/rvbrtg/Data/output_data/Binjure.xlsx')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Undersökningar som överstigit 5Gy""")
    return


@app.cell
def _(study_2):
    study_5Gy = study_2[study_2.doseRPTotal > 5000]
    study_5Gy
    return (study_5Gy,)


@app.cell
def _(study_5Gy):
    # Skriv till Excel
    study_5Gy.to_excel("output_data/Över_5Gy.xlsx")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Multiplar. Tester nedan.""")
    return


@app.cell
def _(study_2):
    multiple = study_2.groupby('patientDbId', as_index=False)['doseRPTotal'].nunique()
    multiple
    return


@app.cell
def _(study_data):
    _test = study_data.groupby(['patientDbId'])['doseRPTotal'].sum().reset_index()
    _test.drop(_test[_test['doseRPTotal'] < 5000].index, inplace=True)
    _test
    return


@app.cell
def _(study_data):
    top_pat = study_data[study_data.patientDbId == 84305]
    top_pat
    return


@app.cell
def _(datetime, pd):
    def loop_analysis(data: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        analysis_data = data[data.studyDateTime >= start_date & data.studyDateTime <= end_date]
        _test = analysis_data.groupby(['patientDbId', 'acquisitionPlaneSeries']).sum('doseRP').reset_index()
        _test = _test[['patientDbId', 'acquisitionPlaneSeries', 'doseRP', 'studyDateTime']]
        return _test[_test.doseRP > 5000]
    return (loop_analysis,)


@app.cell
def _(datetime, loop_analysis, pd, study_2):
    from dateutil.relativedelta import relativedelta
    new_study_data = study_2.copy()
    new_study_data.studyDateTime = pd.to_datetime(new_study_data.studyDateTime, infer_datetime_format=True)
    new_study_data['studyDate'] = pd.to_datetime(new_study_data.studyDateTime.dt.date)
    for end_date in sorted(new_study_data.studyDate.unique().tolist()):
        sd = pd.to_datetime(datetime.fromtimestamp(end_date / 1000000000.0) - relativedelta(months=3))
        resultat = loop_analysis(new_study_data, start_date=sd, end_date=end_date)
    _test = new_study_data.groupby(['patientDbId', 'acquisitionPlaneSeries', pd.Grouper(key='studyDateTime', freq='12M')]).sum('doseRP').reset_index()
    _test = _test[['patientDbId', 'acquisitionPlaneSeries', 'doseRP', 'studyDateTime']]
    study_data_5Gy = _test[_test.doseRP > 5000]
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
