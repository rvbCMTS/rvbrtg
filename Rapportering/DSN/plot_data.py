import pandas as pd

import plotly.express as px

from Rapportering.DSN.constants import (
    VALID_STUDY_COLUMNS,
    OUTPUT_COL_EXAM,
    OUTPUT_COL_WEIGTH_CATEGORY,
    MODALITY_DX
)

def plot_data(data: pd.DataFrame, modality: str) -> None:

    for exam_name in data[OUTPUT_COL_EXAM].unique().tolist():

        if modality == MODALITY_DX:
            _plot_child_data(dataframe = data, exam_name = exam_name)
            _plot_adult_data(dataframe = data, exam_name = exam_name)
        


def _plot_child_data(dataframe: pd.DataFrame, exam_name: str) -> None:
    fig = px.scatter(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name) & (dataframe[VALID_STUDY_COLUMNS.PatientAge] < 16)],
                     x=VALID_STUDY_COLUMNS.PatientsWeight,
                     y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                     size=VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames,
                     color=VALID_STUDY_COLUMNS.Machine,
                     title=f"{exam_name} - Barn",
                     hover_data={
                             VALID_STUDY_COLUMNS.Machine: True,
                             VALID_STUDY_COLUMNS.PatientsWeight: True,
                             VALID_STUDY_COLUMNS.DoseAreaProductTotal: True,
                             VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames: True,
                     },
    )
    fig.show()


    fig_violin = px.violin(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name) & (dataframe[VALID_STUDY_COLUMNS.PatientAge] < 16)],
                           x=OUTPUT_COL_WEIGTH_CATEGORY,
                           y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                           color=VALID_STUDY_COLUMNS.Machine,
                           box=True,
                           points="all",
                           title=f"{exam_name} - Barn",
    )
    fig_violin.show()    

def _plot_adult_data(dataframe: pd.DataFrame, exam_name: str) -> None:
    fig = px.scatter(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name) & (dataframe[VALID_STUDY_COLUMNS.PatientAge] > 16)],
                     x=VALID_STUDY_COLUMNS.PatientsWeight,
                     y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                     size=VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames,
                     color=VALID_STUDY_COLUMNS.Machine,
                     title=f"{exam_name} - Vuxen",
                     hover_data={
                             VALID_STUDY_COLUMNS.Machine: True,
                             VALID_STUDY_COLUMNS.PatientsWeight: True,
                             VALID_STUDY_COLUMNS.DoseAreaProductTotal: True,
                             VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames: True,
                     },
    )
    fig.show()

    fig_violin = px.violin(data_frame=dataframe[(dataframe[OUTPUT_COL_EXAM] == exam_name) & (dataframe[VALID_STUDY_COLUMNS.PatientAge] > 16)],
                           x=OUTPUT_COL_WEIGTH_CATEGORY,
                           y=VALID_STUDY_COLUMNS.DoseAreaProductTotal,
                           color=VALID_STUDY_COLUMNS.Machine,
                           box=True,
                           points="all",
                           title=f"{exam_name} - Vuxen",
    )
    fig_violin.show()