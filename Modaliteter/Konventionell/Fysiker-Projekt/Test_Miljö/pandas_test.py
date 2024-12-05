import pandas as pd 

# Load data as pickle
df_Series = pd.read_pickle("Modaliteter\Konventionell\Fysiker-Projekt\Data_24-12-05\series_data.pkl")
df_Study = pd.read_pickle("Modaliteter\Konventionell\Fysiker-Projekt\Data_24-12-05\study_data.pkl")

# Merge data based on studyInstanceUID
merged = pd.merge(df_Series.reset_index(), df_Study.reset_index(), on='studyInstanceUID', how="left")

print(merged)
# Export data as csv
#merged.to_csv('merged_output.csv', index=False)





column_name = 'acquisitionProtocol'
counts = merged[column_name].value_counts()
duplicates = counts[counts > 1]

# Display the results
print(f"Unique duplicates and their counts in column '{column_name}':")
for value, count in duplicates.items():
    print(f"  Value {value} appears {count} times")
