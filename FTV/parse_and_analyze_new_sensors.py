import sys
from pathlib import Path
from typing import List

import numpy as np
import pydicom

sys.path.append("..")
import shutil

import pandas as pd
from analys_private_sprid_ej import create_calibration_plot


def parse_onepix_data_for_new_clinic(
    path_clinics_raw: Path,
    path_clinics_parsed: Path,
    exp_times: List[int],
    ma: int,
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
    
    
    # fetch measurement date
    for tube_id in selected_lab.iterdir():
        for sensor_path in (tube_id / "Kalibrering").iterdir():
            if sensor_path.name in "sensorid_mall":
                continue
            for item in (sensor_path / "60kv").iterdir():
                dcm_file = pydicom.dcmread(item)
                measurement_date = dcm_file.StudyDate
                break
            break
        break

    print(
        (
            f"\nMeasurement info\nclinic: {selected_clinic.name}\n"
            f"measured in lab: {selected_lab.name}\n"
            f"date: {measurement_date}\n"
        )
    )

    # get list of dose measurements
    dose_measurements = []
    for dose_measurement in (path_clinics_raw / "dosmätningar").iterdir():
        if "Date" in dose_measurement.name:
            continue
        dose_measurements.append(dose_measurement)

    # select dose measurement
    print("\nselect dose_measurement by index:\n")
    for i in range(len(dose_measurements)):
        print(
            i,
            dose_measurements[i].name[16:],
        )

    dose_index = int(input("\n"))
    # load dose measurements
    for kv in ["60kv", "70kv"]:
        dose_dict[kv] = pd.read_excel(
            dose_measurements[dose_index],
            kv,
        )["dose_mGy"]

    # copy dosemeasurements to parsed folder
    for src in (path_clinics_raw / "dosmätningar").iterdir():
        dest = path_clinics_parsed / "dosmätningar" / src.name
        shutil.copyfile(src, dest)

    # folder_clinic_parsed = f"\n{path_clinics_parsed}/{path_clinics_raw.name}_parsed"
    print(f"parsing clinic: {selected_clinic.name}")
    print(f"parsing lab: {selected_lab.name}")
    print(f"appending dose measurements from {dose_measurements[dose_index].name}\n")
    
    #for lab in selected_clinic.iterdir():
    
    print(f"parsing measurement from lab: {selected_lab.name}")
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

                path_res_folder = (
                    path_clinics_parsed / f"{selected_clinic.name}_parsed"
                )
                sub_path = Path(*kv.parts[9:])

                dcm_res_path = path_res_folder / sub_path
                dcm_res_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                plots_path = (
                    path_clinics_parsed / "plots" / f"{selected_clinic.name}_parsed"
                )
                plots_path.mkdir(exist_ok=True)
                dcm_files = []  # for DICOM files
                acq_times = []  # for acquisition times (for sorting)

                for dcm_file in kv.iterdir():
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
                    dcm_files[sort_order[i]].EntranceDoseInmGy = dose_dict[kv.name.lower()][
                        i
                    ]

                    parsed_file_name = f"{kv.name}_{ma}ma_{exp_times[i]}ms.dcm"

                    dcm_files[sort_order[i]].save_as(
                        dcm_res_path / parsed_file_name
                    )

        create_calibration_plot(
            main_folder=path_clinics_parsed,
            output_dir=plots_path,
            sensor_ids=sensor_id_list,
        )

        print("parsing completed")


path_clinics_raw = (
    Path("G:")
    / "CMTS"
    / "SF"
    / "Personal"
    / "Personliga mappar"
    / "Josef Lundman"
    / "FTV"
    / "Nya sensorer 2022 raw"
)

path_clinics_parsed = (
    Path("C:/")
    / "Users"
    / "maxh01"
    / "OneDrive - Region Västerbotten"
    / "General"
    / "FTV"
    / "Nya sensorer 2022"
    / "Nya sensorer 2022 parsed"
)

exp_times = [20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250]
ma = 7


parse_onepix_data_for_new_clinic(
    path_clinics_raw=path_clinics_raw,
    path_clinics_parsed=path_clinics_parsed,
    exp_times=exp_times,
    ma=ma,
)
