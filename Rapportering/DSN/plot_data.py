import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots

from Rapportering.DSN.constants import (
    VALID_STUDY_COLUMNS,
    OUTPUT_COL_EXAM,
    OUTPUT_COL_WEIGTH_CATEGORY,
    MODALITY_DX
)

def plot_data(data: pd.DataFrame, modality: str) -> None:

    for exam_name in data[OUTPUT_COL_EXAM].unique().tolist():

        if modality == MODALITY_DX:
            _plot_data_dx(dataframe = data, exam_name = exam_name)
        


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


