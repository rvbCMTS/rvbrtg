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

