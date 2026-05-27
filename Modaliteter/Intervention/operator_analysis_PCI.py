import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Operator follow up at the PCI-labs

    Analysis of system use. Both on study and series level. <br>
    Import the operator name translation list ("operators_202X") to <i>rvbrtg/Data/input_data</i>.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import from REMbox
    """)
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
    import math
    from plotly.subplots import make_subplots
    import numpy as np

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
    COL_NORM_FL_DAP = "normalisedFluoroDAP"
    COL_NORM_ACQ_DAP = "normalisedAcqDAP"
    COL_NORM_FL_RP = "normalisedFluoroRP"
    COL_NORM_ACQ_RP = "normalisedAcqRP"
    return (
        COL_NORM_ACQ_DAP,
        COL_NORM_ACQ_RP,
        COL_NORM_FL_DAP,
        COL_NORM_FL_RP,
        COL_OPERATOR_NAME,
        Path,
        REMboxDataQuery,
        go,
        make_subplots,
        math,
        np,
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
            #machine_types=["XASTAT"], # Mobile C-arm-XAMOB or is optional
            machines=["U110", "S08", "S08_2025", "L3"] # "U105", "U106", "U104", "U601", "U602" "Arytmi 1", "Arytmi 2"
        )

        rembox.filter_options.patient_age_interval_include_nulls = True

        rembox.filter_options.study_time_interval_start_date = "2025-01-01T00:00:00Z"
        rembox.filter_options.study_time_interval_end_date = "2025-12-10T00:00:00Z"


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
    mo.md(r"""
    ## Management of dataframes
    """)
    return


@app.cell
def _(series_data, study_data):
    study = study_data.copy() #Create copy of dataframe on study-level
    series = series_data.copy() #Create copy of dataframe on series-level
    return series, study


@app.cell
def _(study, valid_study_columns):
    # Convert to Europe/Stockholm timezone
    study[valid_study_columns.StudyDateTime] = study[valid_study_columns.StudyDateTime].dt.tz_convert('Europe/Stockholm')
    # Convert ProcedureCode from object to integer.
    # Use nullable integer dtype so missing / non-numeric values are preserved as <NA>.
    #study[valid_study_columns.ProcedureCode] = pd.to_numeric(
    #    study[valid_study_columns.ProcedureCode], errors="coerce"
    #).astype("Int64")
    study.head()
    return


@app.cell
def _(mo, px, study, valid_study_columns):
    fig_test = mo.ui.plotly(px.scatter(study, x=valid_study_columns.StudyDateTime, y=valid_study_columns.DoseAreaProductTotal, color=valid_study_columns.ProcedureCodeMeaning))
    fig_test
    return


@app.cell
def _(mo, px, study, valid_study_columns):
    #removals_procedures = study[valid_study_columns.StudyDescription].value_counts().reset_index()
    #removals_procedures = removals_procedures[removals_procedures['count'] > 10] # Threshold for number of procedures to get included in further analysis
    #removals_procedures

    #procedures_filtered = study[study[valid_study_columns.ProcedureCode].isin(removals_procedures[valid_study_columns.StudyDescription])]
    #filtered_df.head()

    fig_procedures_filtered = mo.ui.plotly(px.box(study, x=valid_study_columns.ProcedureCode, y=valid_study_columns.DoseAreaProductTotal, points='all', color=valid_study_columns.Machine, height=600))
    #fig.update_layout(width=1000, height=600)


    fig_procedures_filtered
    return


@app.cell
def _(go, make_subplots, mo, np, study, valid_study_columns):
    # Åldersfiltrerat urval
    kids_study = study[study[valid_study_columns.PatientAge] > 18]

    procedure = kids_study[kids_study[valid_study_columns.ProcedureCode] == "53100"]

    # Ej åldersfiltrerad
    #procedure = study[study[valid_study_columns.ProcedureCode] == "41200"]

    # Mean DAP for this procedure
    mean_dap = procedure[valid_study_columns.DoseAreaProductTotal].mean()

    # Create a color map for machines
    machines = np.sort(procedure[valid_study_columns.Machine].unique())
    color_map = {machine: f"hsl({i * 360 / len(machines)}, 70%, 50%)" for i, machine in enumerate(machines)}

    # Create 1x2 subplots: left = time, right = patient age
    fig_procedure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            "DoseAreaProductTotal vs StudyDateTime",
            "DoseAreaProductTotal vs PatientAge",
        ],
    )

    # Scatter: StudyDateTime vs DAP (colored by Machine)
    for machine in machines:
        machine_data = procedure[procedure[valid_study_columns.Machine] == machine]
        fig_procedure.add_trace(
            go.Scatter(
                x=machine_data[valid_study_columns.StudyDateTime],
                y=machine_data[valid_study_columns.DoseAreaProductTotal],
                mode="markers",
                name=str(machine),
                marker=dict(color=color_map[machine], size=8),
            ),
            row=1,
            col=1,
        )

    # Mean line on the first subplot (use datetime min/max extents)
    if not procedure.empty:
        dt_min = procedure[valid_study_columns.StudyDateTime].min()
        dt_max = procedure[valid_study_columns.StudyDateTime].max()
        fig_procedure.add_trace(
            go.Scatter(
                x=[dt_min, dt_max],
                y=[mean_dap, mean_dap],
                mode="lines",
                name="Mean DAP",
                line=dict(color="red", dash="dash"),
                showlegend=True,
            ),
            row=1,
            col=1,
        )

    # Scatter: PatientAge vs DAP (colored by Machine)
    for machine in machines:
        machine_data = procedure[procedure[valid_study_columns.Machine] == machine]
        fig_procedure.add_trace(
            go.Scatter(
                x=machine_data[valid_study_columns.PatientAge],
                y=machine_data[valid_study_columns.DoseAreaProductTotal],
                mode="markers",
                name=str(machine),
                marker=dict(color=color_map[machine], size=8),
                showlegend=False,  # avoid duplicate legend entries
            ),
            row=1,
            col=2,
        )

    # Mean line on the second subplot (use age min/max extents, handle NaNs)
    if not procedure.empty:
        age_series = procedure[valid_study_columns.PatientAge].dropna()
        if not age_series.empty:
            age_min = age_series.min()
            age_max = age_series.max()
            fig_procedure.add_trace(
                go.Scatter(
                    x=[age_min, age_max],
                    y=[mean_dap, mean_dap],
                    mode="lines",
                    name="Mean DAP",
                    line=dict(color="red", dash="dash"),
                    showlegend=False,  # already shown for first mean line
                ),
                row=1,
                col=2,
            )

    # Layout tweaks
    fig_procedure.update_xaxes(title_text="StudyDateTime", row=1, col=1)
    fig_procedure.update_xaxes(title_text="PatientAge (years)", row=1, col=2)
    fig_procedure.update_yaxes(title_text="DoseAreaProductTotal", row=1, col=1)
    fig_procedure.update_yaxes(title_text="DoseAreaProductTotal", row=1, col=2)

    fig_procedure.update_layout(
        height=600,
        width=1500,
        title_text=f"Procedure { '53100' } — DoseAreaProductTotal by date and patient age",
    )

    # Wrap with marimo UI helper
    fig_procedure = mo.ui.plotly(fig_procedure)
    fig_procedure
    return


@app.cell
def _(
    COL_NORM_ACQ_DAP,
    COL_NORM_ACQ_RP,
    COL_NORM_FL_DAP,
    COL_NORM_FL_RP,
    study,
    valid_study_columns,
):
    study[COL_NORM_FL_DAP] = study[valid_study_columns.FluoroDoseAreaProductTotal] / study[valid_study_columns.TotalFluoroTime]
    study[COL_NORM_ACQ_DAP] = study[valid_study_columns.AcquisitionDoseAreaProductTotal] / study[valid_study_columns.TotalAcquisitionTime]
    study[COL_NORM_FL_RP] = study[valid_study_columns.FluoroDoseRPTotal] / study[valid_study_columns.TotalFluoroTime]
    study[COL_NORM_ACQ_RP] = study[valid_study_columns.AcquisitionDoseRPTotal] / study[valid_study_columns.TotalAcquisitionTime]
    return


@app.cell
def _(study):
    number = study['patientDbId'].count()
    patients = study['patientDbId'].nunique()
    print("In the dataset there are", number, "procedures distributed over", patients, "patients.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add operator names
    """)
    return


@app.cell
def _(COL_OPERATOR_NAME, Path, pd, study, valid_study_columns):
    # Translation from pseudo-operators to operators
    names_data_path = Path(__file__).parent.parent.parent / "Data/input_data/operators_2025.xlsx"
    names = pd.read_excel(names_data_path)
    # Format to fit study-dataframe
    names.columns = [valid_study_columns.PerformingPhysicianName, COL_OPERATOR_NAME]
    # Merge with study
    study_names = study.merge(names, on=[valid_study_columns.PerformingPhysicianName], how='left')
    print(study_names[COL_OPERATOR_NAME])
    return (study_names,)


@app.cell
def _(COL_OPERATOR_NAME, mo, px, study_names, valid_study_columns):
    fig_overview = mo.ui.plotly(px.scatter(
            study_names,
            x=valid_study_columns.StudyDateTime,
            y=valid_study_columns.DoseRPTotal,
            color=valid_study_columns.ProcedureCodeMeaning,
            custom_data=[valid_study_columns.AccessionNumber, valid_study_columns.AcquisitionPlane, valid_study_columns.Machine, valid_study_columns.DoseAreaProductTotal, valid_study_columns.FluoroDoseAreaProductTotal, valid_study_columns.AcquisitionDoseAreaProductTotal, valid_study_columns.ProcedureCodeMeaning, COL_OPERATOR_NAME],
            title='Dose in Reference Point for each procedure',
            width=1200, 
            height=600
        ))
        # Set hovertemplate to show full datetime with hours, minutes, seconds
    #fig_overview.update_traces(
    #    hovertemplate=
    #    "StudyDateTime: %{x|%Y-%m-%d %H:%M:%S}<br>" +
    #    "DoseRPTotal: <b>%{y:.1f}</b><br>" +
    #    "<b>Operator: %{customdata[7]}</b><br>" +
    #    "Machine: %{customdata[2]}<br>" +
    #    "DAPtot: %{customdata[3]}<br>" +
    #    "FlDAPtot: %{customdata[4]}<br>" +
    #    "AcqDAPtot: %{customdata[5]}<br>" +
    #    "ProcedureCode: %{customdata[6]}<br>" +
    #    "AccessionNumber: %{customdata[0]}<br>" +
    #    "AcquisitionPlane: %{customdata[1]}"
    #)
    fig_overview
    return


@app.cell
def _(study, valid_study_columns):
    # Operator stats per procedure code

    procedure_stats = (study.groupby([valid_study_columns.ProcedureCode, valid_study_columns.ProcedureCodeMeaning, valid_study_columns.Machine])
                        .agg({valid_study_columns.ProcedureCode: 'count', valid_study_columns.DoseAreaProductTotal: ['median', 'mean', 'std'], valid_study_columns.TotalFluoroTime: 'median'}
                             ).reset_index().round(3))
    procedure_stats
    return


@app.cell
def _(COL_OPERATOR_NAME, mo, px, study_names, valid_study_columns):
    # Analysis of reason to differences per procedure type
    # Projection angle, fluoro-mode, pulse frequency, collimation

    removals = study_names[valid_study_columns.ProcedureCode].value_counts().reset_index()
    removals = removals[removals['count'] > 22] # Threshold for number of procedures to get included in further analysis
    removals

    study_names_count_filtered = study_names[study_names[valid_study_columns.ProcedureCode].isin(removals[valid_study_columns.ProcedureCode])]
    #filtered_df.head()

    fig_filtered_procedures = mo.ui.plotly(px.box(study_names_count_filtered, x=valid_study_columns.ProcedureCodeMeaning, y=valid_study_columns.DoseAreaProductTotal, points='all', color=COL_OPERATOR_NAME, height=600))
    #fig.update_layout(width=1000, height=600)
    fig_filtered_procedures
    return (study_names_count_filtered,)


@app.cell
def _(series, study_names_count_filtered):
    # Ta bort alla dubletter där 1mm Al-filter visas istället för Cu-filter 
    # TODO: Gör separata kolumner för Al och Cu-filter så det inte blir dubbla rader.

    series_Cu_filtered = series[(series['xrayFilterMaterial'] == 'Copper') | (series['xrayFilterMaterial'] == 'Copper or Copper compound')]


    # Merge study and series on 'studyInstanceUID'
    merged_study_series = study_names_count_filtered.merge(series_Cu_filtered, on='studyInstanceUID', how='inner')

    # Display the first rows of the merged DataFrame
    merged_study_series.head()
    return (merged_study_series,)


@app.cell
def _(merged_study_series, px, valid_series_columns, valid_study_columns):
    fig_filtered_projections = px.scatter(merged_study_series, x=valid_series_columns.PositionerPrimaryAngle, y=valid_series_columns.PositionerSecondaryAngle, color=valid_study_columns.ProcedureCodeMeaning)
    fig_filtered_projections.show()
    return


@app.cell
def _(
    go,
    make_subplots,
    math,
    merged_study_series,
    valid_series_columns,
    valid_study_columns,
):


    # Get unique procedureCode values
    unique_procedure_codes = merged_study_series[valid_study_columns.ProcedureCode].unique()

    # Calculate the number of rows and columns for a symmetric layout
    num_procedures = len(unique_procedure_codes)
    grid_size = math.ceil(math.sqrt(num_procedures))  # Number of rows and columns


    # Create a subplot layout with a symmetric grid 
    fig_filtered_procedure_projections = make_subplots(
        rows=grid_size,
        cols=grid_size,
        specs=[[{'type': 'xy'} for _ in range(grid_size)] for _ in range(grid_size)],
        subplot_titles=[
            f"ProcedureCode {code}"
            for code in unique_procedure_codes
        ]
    )

    # Loop through each procedureCode and create a scatter plots
    for idx, code in enumerate(unique_procedure_codes):
        # Calculate the row and column index
        row = (idx // grid_size) + 1
        col = (idx % grid_size) + 1

        # Filter the data for the current procedureCode
        procedure_data = merged_study_series[(merged_study_series[valid_study_columns.ProcedureCode] == code)]


        # Add the scatterplot to the subplot
        fig_filtered_procedure_projections.add_trace(
            go.Scatter(x=procedure_data[valid_series_columns.PositionerPrimaryAngle], y=procedure_data[valid_series_columns.PositionerSecondaryAngle], mode='markers', name=f"ProcedureCode {code}"),# TODO: add operator as colors. Or make slider instead of subplots.
            row=row,
            col=col
        )

    # Update layout
    fig_filtered_procedure_projections.update_layout(
        height=300 * grid_size,  # Adjust height based on the grid size
        width=300 * grid_size,   # Adjust width based on the grid size
        title_text="Median DAP Distribution for All ProcedureCodes",
        showlegend=True  # Disable global legend for cleaner layout
    )

    # Show the figure
    fig_filtered_procedure_projections.show()
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
