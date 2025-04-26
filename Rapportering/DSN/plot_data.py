import logging
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from Rapportering.DSN.constants import (
    VALID_STUDY_COLUMNS,
    OUTPUT_COL_EXAM,
    OUTPUT_COL_WEIGTH_CATEGORY,
    MODALITY_DX, MODALITY_MG, VALID_SERIES_COLUMNS, MG_COL_PROJECTION, MG_PROJ_LMLO, MG_PROJ_RMLO, MG_PROJ_LML,
    MG_PROJ_RML, MG_PROJ_LCC, MG_PROJ_RCC, COL_MARKER_LINE_WIDTH
)

logger = logging.getLogger("yearly_statistics")


def plot_data(data: pd.DataFrame, modality: str) -> None:
  

    if modality == MODALITY_DX:
        for exam_name in data[OUTPUT_COL_EXAM].unique().tolist():
            _plot_data_dx(dataframe = data, exam_name = exam_name)
    elif modality == MODALITY_MG:
        _plot_data_mg(data = data)

    else:
        logger.info(f"Modality {modality} not implemented.")
        


def _plot_data_dx(dataframe: pd.DataFrame, exam_name: str) -> None:

    if dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name)].empty:
        return

    fig_scatter = px.scatter(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name)],
                    x=VALID_STUDY_COLUMNS.PatientsWeight,
                    y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                    size=VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames,
                    color=VALID_STUDY_COLUMNS.Machine,
                    title=f"{exam_name}",
                    hover_data={
                            VALID_STUDY_COLUMNS.Machine: True,
                            VALID_STUDY_COLUMNS.PatientsWeight: True,
                            VALID_STUDY_COLUMNS.DoseAreaProductTotal: True,
                            VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames: True,
                    },
    )
    
    fig_violin = px.violin(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name)],
                        x=OUTPUT_COL_WEIGTH_CATEGORY,
                        y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                        color=VALID_STUDY_COLUMNS.Machine,
                        box=True,
                        points="all",
                        title=f"{exam_name}",
    )

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Scatter Plot", "Violin Plot"))
    
    for trace in fig_scatter['data']:
        fig.add_trace(trace, row=1, col=1)

    for trace in fig_violin['data']:
        fig.add_trace(trace, row=1, col=2)

    fig.update_layout(title_text=f"{exam_name}")
    fig.update_layout(violinmode='group')

    fig.update_xaxes(title_text="Patient Weight [kg]", row=1, col=1)
    fig.update_yaxes(title_text="Dose Area Product [Gy*cm^2]", row=1, col=1)
    fig.update_xaxes(title_text="Patient Weight Category", row=1, col=2)
    fig.update_yaxes(title_text="Dose Area Product [Gy*cm^2]", row=1, col=2)

    fig.show()


def _plot_data_mg(data: pd.DataFrame) -> None:
    try:
        study_descriptions = sorted(data[OUTPUT_COL_EXAM].unique().tolist())

        data[COL_MARKER_LINE_WIDTH] = 0
        data.loc[
            data[VALID_SERIES_COLUMNS.CompressionThickness].astype(float).isnotnull() &
            data[VALID_SERIES_COLUMNS.CompressionForce].astype(float).isnotnull(),
            COL_MARKER_LINE_WIDTH
        ] = 4

        machines = sorted(data[VALID_STUDY_COLUMNS.Machine].unique().tolist())


        for study_description in study_descriptions:
            fig = make_subplots(
                rows=3, cols=4,
                subplot_titles=(
                    MG_PROJ_LMLO, MG_PROJ_RMLO, MG_PROJ_LMLO, MG_PROJ_RMLO,
                    MG_PROJ_LML, MG_PROJ_RML, MG_PROJ_LML, MG_PROJ_RML,
                    MG_PROJ_LCC, MG_PROJ_RCC, MG_PROJ_LCC, MG_PROJ_RCC,
                )
            )
            for ind, machine in enumerate(machines):
                tmp_df = data[(data[OUTPUT_COL_EXAM] == study_description) & (data[VALID_STUDY_COLUMNS.Machine] == machine)]
                _get_mg_plot_row_for_projections(
                    tmp_df=tmp_df, left_proj=MG_PROJ_LMLO, right_proj=MG_PROJ_RMLO, row=1, ind=ind, fig=fig)
                _get_mg_plot_row_for_projections(
                    tmp_df=tmp_df, left_proj=MG_PROJ_LML, right_proj=MG_PROJ_RML, row=2, ind=ind, fig=fig)
                _get_mg_plot_row_for_projections(
                    tmp_df=tmp_df, left_proj=MG_PROJ_LCC, right_proj=MG_PROJ_RCC, row=3, ind=ind, fig=fig)

            fig.update_layout(title_text=f"{study_description}")

    except Exception as e:
        logger.error("Failed to create mammography plots", exc_info=True)


def _get_mg_plot_row_for_projections(tmp_df: pd.DataFrame, left_proj: str, right_proj: str, row: int, ind: int, fig):
    symbols = [
        "circle-open", "diamond-open", "square-open", "triangle-up-open", "cross-open", "x-open",
        "pentagon-open", "hexagon2-open"
    ]
    colors = [
        "blue", "red", "yellow", "magenta", "cyan", "mediumpurple", "MediumPurple"
    ]

    fig.add_trace(
        go.Scatter(
            x=tmp_df[VALID_SERIES_COLUMNS.CompressionThickness][tmp_df[MG_COL_PROJECTION] == left_proj],
            y=tmp_df[VALID_SERIES_COLUMNS.AverageGlandularDose][tmp_df[MG_COL_PROJECTION] == left_proj],
            mode="markers",
            marker=dict(
                line=dict(
                    width=tmp_df[COL_MARKER_LINE_WIDTH][tmp_df[MG_COL_PROJECTION] == left_proj]
                ),
                symbol=symbols[ind],
                color=colors[ind]
            )
        ), row=row, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=tmp_df[VALID_SERIES_COLUMNS.CompressionThickness][tmp_df[MG_COL_PROJECTION] == right_proj],
            y=tmp_df[VALID_SERIES_COLUMNS.AverageGlandularDose][tmp_df[MG_COL_PROJECTION] == right_proj],
            mode="markers",
            marker=dict(
                line=dict(
                    width=tmp_df[COL_MARKER_LINE_WIDTH][tmp_df[MG_COL_PROJECTION] == right_proj]
                ),
                symbol=symbols[ind],
                color=colors[ind]
            )
        ), row=row, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=tmp_df[VALID_SERIES_COLUMNS.CompressionForce][tmp_df[MG_COL_PROJECTION] == left_proj],
            y=tmp_df[VALID_SERIES_COLUMNS.AverageGlandularDose][tmp_df[MG_COL_PROJECTION] == left_proj],
            mode="markers",
            marker=dict(
                line=dict(
                    width=tmp_df[COL_MARKER_LINE_WIDTH][tmp_df[MG_COL_PROJECTION] == left_proj]
                ),
                symbol=symbols[ind],
                color=colors[ind]
            )
        ), row=row, col=3
    )
    fig.add_trace(
        go.Scatter(
            x=tmp_df[VALID_SERIES_COLUMNS.CompressionForce][tmp_df[MG_COL_PROJECTION] == right_proj],
            y=tmp_df[VALID_SERIES_COLUMNS.AverageGlandularDose][tmp_df[MG_COL_PROJECTION] == right_proj],
            mode="markers",
            marker=dict(
                line=dict(
                    width=tmp_df[COL_MARKER_LINE_WIDTH][tmp_df[MG_COL_PROJECTION] == right_proj]
                ),
                symbol=symbols[ind],
                color=colors[ind]
            )
        ), row=row, col=4
    )

