from pathlib import Path
from dicom_image_tools import import_dicom_from_folder, SquareRoi
from dicom_image_tools.plotting.plotly import get_image_and_roi_traces_and_layout
from plotly.subplots import make_subplots
from typing import List


def determine_roi_depending_on_examination(series_description: str,
                                           image_crop_upper_left: List[int],
                                           voxel_data) -> List[SquareRoi]:
    roi = []
    if "benlängd" in series_description.lower():
        # two side dominants
        roi = [
            SquareRoi(center={"x": 1718 + 186 - image_crop_upper_left[0],
                              "y": 840 - image_crop_upper_left[1],
                              "z": 0},
                      height=408,
                      width=534,
                      pixel_size=voxel_data,
                      roi_size_in_pixels=True),

            SquareRoi(center={"x": 1794 + 186 - image_crop_upper_left[0],
                              "y": 1146 - image_crop_upper_left[1],
                              "z": 0},
                      height=192,
                      width=380,
                      pixel_size=voxel_data,
                      roi_size_in_pixels=True),

            SquareRoi(center={"x": 748 + 186 - image_crop_upper_left[0],
                              "y": 840 - image_crop_upper_left[1],
                              "z": 0},
                      height=408,
                      width=534,
                      pixel_size=voxel_data,
                      roi_size_in_pixels=True),

            SquareRoi(center={"x": 672 + 186 - image_crop_upper_left[0],
                              "y": 1146 - image_crop_upper_left[1],
                              "z": 0},
                      height=192,
                      width=380,
                      pixel_size=voxel_data,
                      roi_size_in_pixels=True)
        ]
    if "benvinkel" in series_description.lower():
        roi = [
            SquareRoi(center={"x": 1430 - image_crop_upper_left[0],
                              "y": 1420 - image_crop_upper_left[1],
                              "z": 0},
                      height=530,
                      width=530,
                      pixel_size=voxel_data,
                      roi_size_in_pixels=True)
        ]
    return roi


def evaluate(base_dir):
    studies = import_dicom_from_folder(folder=base_dir)
    for _, study in studies.items():
        all_images_and_roi_traces = []
        for serie in study.Series:
            # no stiched or composed images
            image_type = serie.CompleteMetadata[0][0x0008, 0x0008].value
            if "PRIMARY" in image_type:
                serie.import_image()
                roi = determine_roi_depending_on_examination(
                    series_description=serie.SeriesDescription,
                    image_crop_upper_left=serie.CompleteMetadata[0][0x0025, 0x101A].value,
                    voxel_data=serie.VoxelData[0])
                image_and_roi_traces = (
                    [get_image_and_roi_traces_and_layout(image,
                                                         x_scale=1,
                                                         y_scale=1,
                                                         colour_map="grey",
                                                         colour_bar=False,
                                                         rois=roi)
                     for image in serie.ImageVolume])

        all_images_and_roi_traces += image_and_roi_traces

        fig = make_subplots(rows=1, cols=len(all_images_and_roi_traces))

        for index, sub_plot in enumerate(all_images_and_roi_traces):
            for trace in sub_plot[0]:
                fig.add_trace(trace, row=1, col=index+1)
            fig.update_xaxes(all_images_and_roi_traces[0][1]['xaxis'], row=1, col=index+1)
            fig.update_yaxes(all_images_and_roi_traces[0][1]['yaxis'], row=1, col=index+1)

        fig.update_layout(all_images_and_roi_traces[0][1],
                          title=serie.CompleteMetadata[0][0x0008, 0x0020].value)
        fig.show()


if __name__ == '__main__':
    evaluate(
        base_dir=Path("C:\\slask\\Gonadskydd\\Långa ben")
    )
