from pathlib import Path
from dicom_image_tools import import_dicom_from_folder, SquareRoi


def evaluate(base_dir):
    studies = import_dicom_from_folder(folder=base_dir)

    for study in studies.items():
        projection_serie = study[1].Series[0]
        projection_serie.import_image()

        image_crop_upper_left = projection_serie.CompleteMetadata[0][0x0025, 0x101A].value
        print(projection_serie.CompleteMetadata[0][0x0008, 0x0020].value)

        roi = SquareRoi(center={"x": 1430 - image_crop_upper_left[0],
                                "y": 1420 - image_crop_upper_left[1],
                                "z": 0},
                        height=515,
                        width=515,
                        pixel_size=projection_serie.VoxelData[0],
                        roi_size_in_pixels=True)
        projection_serie.show_image(rois=[roi],
                                    colour_map='grey')




if __name__ == '__main__':
    evaluate(
        base_dir=Path("C:\\slask\\Gonadskydd\\HELRYGG\\Urval")
    )
