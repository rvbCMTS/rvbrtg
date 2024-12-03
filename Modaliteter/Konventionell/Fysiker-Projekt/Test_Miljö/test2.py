## Script is made by Philip
# Only used to test and debunc functions.

import numpy as np
import pandas as pd

# ----------------------------------
# Load data provided from supervisor
# ----------------------------------
study_data = r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\studies.csv"
series_data = r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\series.csv"

study_array = pd.read_csv(study_data, sep = ';')
series_array = pd.read_csv(series_data, sep = ';')

array1 = study_array['Study instance UID']
array2 = series_array['Irradiation event UID']

if isinstance(array1, pd.Series):
    array1 = array1.to_numpy()
if isinstance(array2, pd.Series):
    array2 = array2.to_numpy()

# Debugging: Print shapes
print("Shape of array1:", array1.shape)
print("Shape of array2:", array2.shape)

# Truncate to the same length
min_length = min(len(array1), len(array2))
array1 = array1[:min_length]
array2 = array2[:min_length]

print("Min length", min_length)

# Compare values
indices = np.where(array1 == array2)[0]

# Check if matches exist
if indices.size > 0:
    print("Identical values found at indices:", indices)
else:
    print("Error: No identical values found.")