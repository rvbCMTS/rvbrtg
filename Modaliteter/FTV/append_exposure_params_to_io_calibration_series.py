import datetime as dt
import sys
from pathlib import Path
from typing import List

path_to_repo = Path(__file__).parents[2]
sys.path.append(str(path_to_repo))


import shutil
from pathlib import Path
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pydicom
from analys_private_sprid_ej import create_calibration_plot

from utils.plot_utils import export_flatfield_image
from utils.intraoral_utils import _fetch_latest_dose_measurement


def _append_exposure_params_to_io_calibration_series(
    path_clinics_raw: Path,
    path_clinics_parsed: Path,
    exp_times: List[int],
    ma: int,
    run_tanqa_offline=False,
    export_flatfield_images=True,
    append_dose_measurements=True,
) -> None:
    dose_dict = dict()
    # select clinic from user input
    clinics_list = []
    for item in path_clinics_raw.iterdir():
        if item.name in [
            "dosmätningar",
            "raw_folder.txt",
            "klinik_namn",
        ]:
            continue
        clinics_list.append(item)

    print("\nselect clinic by index:\n")
    for i in range(len(clinics_list)):
        print(i, clinics_list[i].name)

    selected_clinic_index = input("\n")
    selected_clinic = clinics_list[int(selected_clinic_index)]
    # select measurement lab from user input
    labs_list = []
    for item in selected_clinic.iterdir():
        labs_list.append(item)

    print("\nselect lab by index:\n")
    for i in range(len(labs_list)):
        print(i, labs_list[i].name)

    selected_lab_index = input("\n")
    selected_lab = labs_list[int(selected_lab_index)]

    # get list of dose measurements
    if append_dose_measurements:
        dose_measurements = []
        for dose_measurement in (path_clinics_raw / "dosmätningar").iterdir():
            if "Date" in dose_measurement.name:
                continue
            dose_measurements.append(dose_measurement)

        # copy dosemeasurements to parsed folder
        for src in (path_clinics_raw / "dosmätningar").iterdir():
            dest = path_clinics_parsed / "dosmätningar" / src.name
            shutil.copyfile(src, dest)

    print(f"parsing clinic: {selected_clinic.name}")
    print(f"parsing lab: {selected_lab.name}")

    for x_ray_tube in selected_lab.iterdir():
        print(f"parsing x-ray tube: {x_ray_tube.name}")

        calib_path = x_ray_tube / "Kalibrering"

        sensor_id_list = []
        for sensor in calib_path.iterdir():
            if str(sensor.name) in ["sensorid_mall"]:
                continue

            sensor_id_list.append(str(sensor.name))
            print(f"parsing sensor: {sensor.name}")

            for kv in sensor.iterdir():
                if str(kv.name) in "readme.txt":
                    continue

                path_res_folder = path_clinics_parsed / f"{selected_clinic.name}_parsed"
                sub_path = Path(*kv.parts[7:])

                dcm_res_path = path_res_folder / sub_path
                dcm_res_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                if export_flatfield_images:
                    plots_path = (
                        path_res_folder / selected_lab / x_ray_tube.name / "Kalibrering" / sensor.name / kv.name
                    )
                    plots_path.mkdir(exist_ok=True)

                dcm_files = []  # for DICOM files
                acq_times = []  # for acquisition times (for sorting)

                for dcm_file in tqdm(kv.iterdir()):
                    if ".dcm" in str(dcm_file.name):
                        dcm_files.append(pydicom.dcmread(dcm_file))

                for i in range(len(dcm_files)):
                    acq_times.append(int(dcm_files[i].AcquisitionTime))

                sort_order = np.argsort(acq_times)

                for i in range(len(dcm_files)):
                    folder_kilovoltage = int(kv.name[:2])
                    dcm_files[sort_order[i]].ExposureTime = exp_times[i]
                    dcm_files[sort_order[i]].KVP = folder_kilovoltage
                    dcm_files[sort_order[i]].XRayTubeCurrent = ma

                    if append_dose_measurements:
                        dose = _fetch_latest_dose_measurement(
                            dcm_file=dcm_files[sort_order[i]], dose_measurements=dose_measurements, lab=selected_lab
                        )

                        dcm_files[sort_order[i]].EntranceDoseInmGy = dose[kv.name.lower()][i]

                    parsed_file_name = f"{kv.name}_{ma}ma_{exp_times[i]}ms.dcm"

                    dcm_files[sort_order[i]].save_as(dcm_res_path / parsed_file_name)

                    if export_flatfield_images:
                        export_flatfield_image(
                            file=dcm_files[sort_order[i]], file_name=parsed_file_name, dcm_res_path=dcm_res_path
                        )

        if run_tanqa_offline:
            create_calibration_plot(
                main_folder=path_clinics_parsed,
                output_dir=path_res_folder.parent / "plots" / path_res_folder.name,
                sensor_ids=sensor_id_list,
            )

        print("parsing completed")


path_clinics_raw = Path(r"V:\Enhetsytor\5-1-1-3. Strålningsfysik\Radiologi\FTV\Nya sensorer 2022 raw")


path_clinics_parsed = (
    Path("C:/")
    / "Users"
    / "maxh01"
    / "OneDrive - Region Västerbotten"
    / "Strålningsfysik - Dokument"
    / "Radiologi"
    / "Modaliteter"
    / "FTV"
    / "Nya sensorer 2022"
    / "Nya sensorer 2022 parsed"
)

exp_times = [20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250]
ma = 7


_append_exposure_params_to_io_calibration_series(
    path_clinics_raw=path_clinics_raw,
    path_clinics_parsed=path_clinics_parsed,
    exp_times=exp_times,
    ma=ma,
    run_tanqa_offline=False,
    export_flatfield_images=True,
    append_dose_measurements=True,
)
