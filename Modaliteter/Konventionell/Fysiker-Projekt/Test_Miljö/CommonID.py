import pandas as pd

# Load data as pickle
df_Series = pd.read_pickle("Modaliteter\Konventionell\Fysiker-Projekt\Data_24-12-05\series_data.pkl")
df_Study = pd.read_pickle("Modaliteter\Konventionell\Fysiker-Projekt\Data_24-12-05\study_data.pkl")

print(df_Series)
print(df_Study)