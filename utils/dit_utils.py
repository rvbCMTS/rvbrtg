import dicom_image_tools as dit
import numpy as np
from dicom_image_tools.helpers.point import Point


def _calculate_image_lims_exclude_cornerbox(image_array):

    mins = []
    maxs = []

    xlims = [10, 25]
    ylims = [9, 24]

    if len(image_array.shape) == 2:
        image_array = image_array.astype("float")
        image_array[xlims[0] : xlims[1], ylims[0] : ylims[1]] = np.nan

        return [np.nanmin(image_array), np.nanmax(image_array)]

    for i in range(image_array.shape[0]):
        sub_array = image_array[i, :, :]
        sub_array = sub_array.astype("float")

        sub_array[
            xlims[0] : xlims[1],
            ylims[0] : ylims[1],
        ] = np.nan

        mins.append(np.nanmin(sub_array))
        maxs.append(np.nanmax(sub_array))

    lims = [
        min(mins),
        max(maxs),
    ]
    return lims


def _get_first_key(
    data_dict,
):
    return list(data_dict.keys())[0]


def _rotate_dicom_image_data(
    data,
):
    for item in data:
        data[item].Series[0] = _rotate_imagevolumes(data[item].Series[0])


def _rotate_imagevolumes(
    Series,
):
    for i in range(len(Series.CompleteMetadata)):
        # fetch matrix rotation angle
        rot_angle = Series.CompleteMetadata[i].FieldOfViewRotation
        # calcualte corresponding number of 90 deg rotations
        rot_number_int = int(rot_angle / 90)
        # rotate to 0
        for j in range(rot_number_int):
            Series.ImageVolume[i] = np.rot90(Series.ImageVolume[i])
    return Series


def _load_dicom_image_data(
    data,
    sort_on_acquisition_time=False,
):
    for study in data:
        for serie in data[study].Series:
            serie.import_image()
            if sort_on_acquisition_time:
                serie.sort_images_on_acquisition_time()


def _fetch_roi_trace(
    roi,
):
    # helper function for tracing our the (x, y) coordinates of DIT ROIs
    x_trace = []
    y_trace = []

    for corner in [
        roi.UpperLeft,
        roi.UpperRight,
        roi.LowerRight,
        roi.LowerLeft,
        roi.UpperLeft,
    ]:
        x_trace.append(corner.x)
        y_trace.append(corner.y)

    return (x_trace, y_trace)


def _find_images_lims(
    ImageVolumes,
):
    min_vals = []
    max_vals = []

    for i in range(len(ImageVolumes)):
        min_vals.append(ImageVolumes[i].min())
        max_vals.append(ImageVolumes[i].max())

    lims = [np.min(min_vals), np.max(max_vals)]

    return lims


def _get_image_center(
    image: np.ndarray,
):
    return Point(x=np.divide(image.shape[1], 2), y=np.divide(image.shape[0], 2))
