import numpy as np
import pandas as pd

# ----------------------------------
# Load data provided from supervisor
# ----------------------------------
study_data = r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\studies.csv"
series_data = r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\series.csv"

study_array = pd.read_csv(study_data, sep = ';')
series_array = pd.read_csv(series_data, sep = ';')

# Test if data is successfully loaded
#print(study_array)
#print(series_array)

# ----------------------------------
# Calculations / Main
# ----------------------------------

study_ID_data = study_array['Study instance UID']
series_ID_data = series_array['Irradiation event UID']

def find_indices_for_identicalUI (array1, array2):
    
    # If arrays are pandas.Series, convert them to NumPy arrays
    if isinstance(array1, pd.Series):
        array1 = array1.to_numpy()
    if isinstance(array2, pd.Series):
        array2 = array2.to_numpy()
    
    # Check if there are any matches
    indices = np.where(array1 == array2)[0]
    if indices.size > 0:
        print("Identical values found at indices:", indices)
    else:
        print("Error: No identical values found between the two arrays.")

find_indices_for_identicalUI(study_ID_data, series_ID_data)



## Authors notes
# Apperently valueerror "operands could not be broadcast together with shapes (6139,) (33427,)"
# Error tells that the arrays are of vastly different lenghts.... and cant be compared by the script.
