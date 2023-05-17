from pathlib import Path

import dicom_image_tools as dit
import numpy as np
import pandas as pd
from check_cbct_stack_axial_alignment import check_cbct_stack_axial_alignment
from parse_vendor_specific_cbct_info import get_serie_ssm_data_from_morita_dicom_files


def select_axial_series(series, alignment_limit=0.9):

    alignments = []
    nr_images = []
    for serie in data[selected_study].Series:
        axial_alignment = check_cbct_stack_axial_alignment(
            serie.CompleteMetadata[-1], mode="calc_alignment"
        )
        alignments.append(np.round(axial_alignment, 2))
        nr_images.append(len(serie.CompleteMetadata))

    print(f"{alignments}")
    print(f"{nr_images}")

    alignments, nr_images, series = (
        np.asarray(alignments),
        np.asarray(nr_images),
        np.asarray(series),
    )

    # sorts out stacks with axial alignment < alignment_limit
    sort_mask = alignments > alignment_limit
    nr_images, alignments, series = (
        nr_images[sort_mask],
        alignments[sort_mask],
        series[sort_mask],
    )

    return series.tolist(), alignments.tolist()


def select_from_several_axial_series(axial_series_info):
    if len(axial_series_info) == 1:
        return axial_series_info[0]

    # several axial series:
    stack_heights = [info["stack_height"] for info in axial_series_info]

    # index of stack with largest height
    idx_largest_height = stack_heights.index(max(stack_heights))

    return axial_series_info[idx_largest_height]


# folder
folder = Path(r"F:\Max\U922_mod")
procedure_dicts = []

for pat in folder.iterdir():
    # print(pat.name)
    print(pat.name.split(" ")[0])

    data = dit.import_dicom_from_folder(folder=pat)
    studies = [study for study in data.keys()]

    if len(studies) > 1:
        raise NotImplementedError

    selected_study = studies[0]
    # remove all non CT series
    data[selected_study].Series = [
        item
        for item in data[selected_study].Series
        if isinstance(item, dit.dicom_handlers.ct.CtSeries)
    ]

    # remove Sectra Reconstructions
    data[selected_study].Series = [
        item
        for item in data[selected_study].Series
        if item.SeriesDescription != "Sectra Reconstruction"
    ]

    # load image volumes
    [serie.import_image_volume() for serie in data[selected_study].Series]

    # select only axial stacks
    axial_series, alignments = select_axial_series(data[selected_study].Series)

    # get series info (for SSM stats for all axial stacks)
    axial_series_info = [
        get_serie_ssm_data_from_morita_dicom_files(axial_series[i], alignments[i])
        for i in range(len(axial_series))
    ]

    # select only one
    axial_serie_info = select_from_several_axial_series(axial_series_info)

    procedure_dicts.append(axial_serie_info)

res = pd.DataFrame(procedure_dicts)
res.to_csv('U923_mod.csv')
