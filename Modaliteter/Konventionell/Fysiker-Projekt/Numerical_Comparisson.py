## --------------------------------------
# Script is part of a student project at NuS,
# part of clinical-internship for Medicalphysicist students.

# Goal is to estimate the percentage of x-ray examinations that include 
# some sort of "extra" image. When the first exposure was not enough and 
# the nurses took a second.
## --------------------------------------
# Date: 2024-12-03
# Author: Philip Beckman
# Contact: phbe0019@student.umu.se
## --------------------------------------

import numpy as np
import pandas as pd

# ----------------------------------
# Define functions
# ----------------------------------

# Function will match two datasets and identify indices for matching data UI
def find_indices_for_identicalUI (array1, array2, Var):
    
    # If arrays are pandas.Series, convert them to NumPy arrays
    if isinstance(array1, pd.Series):
        array1 = array1.to_numpy()
    if isinstance(array2, pd.Series):
        array2 = array2.to_numpy()
    
    # If wanted, truncate to the same length
    if Var is not None:
        min_length = min(len(array1), len(array2))
        array1 = array1[:min_length]
        array2 = array2[:min_length]
    
    # Check if there are any matches
    indices = np.where(array1 == array2)[0]
    if indices.size > 0:
        print("Identical values found at indices:", indices)
    else:
        print("Error: No identical values found between the two arrays.")

# ----------------------------------
# Load data provided from supervisor
# ----------------------------------
study_data = pd.read_csv(r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\studies.csv", sep = ';')
series_data = pd.read_csv(r"Modaliteter\Konventionell\Fysiker-Projekt\analysis_2024-12-02_125529\series.csv", sep = ';')

# ----------------------------------
# Calculations / Main
# ----------------------------------
study_ID_data = study_data['Study instance UID']
series_ID_data = series_data['Irradiation event UID']


find_indices_for_identicalUI(study_ID_data, series_ID_data, 1)
    # Third variable: Use "1" to truncate datasets to similar length. Use "None" to not.



