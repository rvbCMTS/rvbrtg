import datetime as dt
import pandas as pd


def _fetch_latest_dose_measurement(dcm_file, dose_measurements, lab):
    date_raw = dcm_file.AcquisitionDate
    date_sensor_exposure = dt.datetime(year=int(date_raw[:4]), month=int(date_raw[4:6]), day=int(date_raw[6:8]))

    print(f"date of sensor exposure: {date_sensor_exposure}")

    dose_dose_measurements_in_lab = []
    date_dose_measurements_in_lab = []
    # fetch list of dose measurements from the same lab
    for item in dose_measurements:
        if lab.name.replace(" ", "")[3:] in item.name:
            dose_dose_measurements_in_lab.append(item)

    # create datetimes for those measurements
    for item in dose_dose_measurements_in_lab:
        date_raw = item.name.split("_")[2].replace(".xlsx", "")

        date = dt.datetime(year=int(date_raw[:4]), month=int(date_raw[4:6]), day=int(date_raw[6:8]))
        date_dose_measurements_in_lab.append(date)

    # time dt in between sensor esposure and measurement date
    delta_t = [date_sensor_exposure - date_dose_measurement for date_dose_measurement in date_dose_measurements_in_lab]
    delta_t_int = [time.days for time in delta_t]
    # closest measurement dt
    min_pos_dt = min([i for i in delta_t_int if i >= 0])
    # index to that measurement date
    dose_index = delta_t_int.index(min_pos_dt)

    dose_dict = dict()
    for kv in ["60kv", "70kv"]:
        dose_dict[kv] = pd.read_excel(
            dose_measurements[dose_index],
            kv,
        )["dose_mGy"]

    print(f"appending: {dose_dose_measurements_in_lab[dose_index].name}")

    return dose_dict
