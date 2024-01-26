import pandas as pd
from pathlib import Path

# Read data
rootpath = Path("C:\slask\Produktion Persondosimetri")
pci_production = pd.read_csv(Path(rootpath, "PCI_produktion.csv"), sep=";")
personnel_dosimetry_PCI = pd.read_csv(Path(rootpath, "PersonnelDosimetryResult_PCI.csv"), sep=",")
personnel_dosimetry_nuklear = pd.read_csv(Path(rootpath, "PersonnelDosimetryResult_Nuklearmedicin.csv"), sep=",")
radpharma = pd.read_csv(Path(rootpath, "RadioPharmacaProduction_anonym.csv"), sep=";")

# format data
pci_production["Study date"] = pd.to_datetime(pci_production["Study date"])
personnel_dosimetry_PCI["measurement_period_start"] = pd.to_datetime(personnel_dosimetry_PCI["measurement_period_start"])
personnel_dosimetry_PCI["measurement_period_stop"] = pd.to_datetime(personnel_dosimetry_PCI["measurement_period_stop"])
pci_production['DAP [Gycm2]'] = pd.to_numeric(pci_production['DAP [Gycm2]'].str.replace(",", "."))
pci_production['Dose RP [mGy]'] = pd.to_numeric(pci_production['Dose RP [mGy]'].str.replace(",", "."))

radpharma["datum"] = pd.to_datetime(radpharma["datum"])
personnel_dosimetry_nuklear["measurement_period_start"] = pd.to_datetime(personnel_dosimetry_nuklear["measurement_period_start"])
personnel_dosimetry_nuklear["measurement_period_stop"] = pd.to_datetime(personnel_dosimetry_nuklear["measurement_period_stop"])
radpharma['activity_mbq'] = pd.to_numeric(radpharma['activity_mbq'].str.replace(",", "."))
radpharma['volume_ml'] = pd.to_numeric(radpharma['volume_ml'].str.replace(",", "."))



for row in personnel_dosimetry_PCI.itertuples():
    data = pci_production[(pci_production["Study date"] > row.measurement_period_start)
                        & (pci_production["Study date"] < row.measurement_period_stop)
                        & (pci_production["Performing physician name"] == str(row.personnel_id))]
    agg_data = data.groupby("Study description")[["DAP [Gycm2]", "Dose RP [mGy]", "Total fluoro time [s]"]].aggregate("sum")
    for study_type in agg_data.itertuples():
        personnel_dosimetry_PCI.at[row.Index, f'{study_type.Index}/DAP [Gycm2]'] = study_type._1
        personnel_dosimetry_PCI.at[row.Index, f'{study_type.Index}/Dose RP [mGy]'] = study_type._2
        personnel_dosimetry_PCI.at[row.Index, f'{study_type.Index}/Total fluoro time [s]'] = study_type._3


for row in personnel_dosimetry_nuklear.itertuples():
    data = radpharma[(radpharma["datum"] > row.measurement_period_start)
                        & (radpharma["datum"] < row.measurement_period_stop)
                        & (radpharma["signature"] == str(row.personnel_id))]
    agg_data = data.groupby("radiopharmaceutical")[["activity_mbq", "volume_ml"]].aggregate("sum")
    for pharma in agg_data.itertuples():
        personnel_dosimetry_nuklear.at[row.Index, f'{pharma.Index}/activity_mbq'] = pharma.activity_mbq
        personnel_dosimetry_nuklear.at[row.Index, f'{pharma.Index}/volume_ml'] = pharma.volume_ml


personnel_dosimetry_PCI.to_csv(Path(rootpath, "PCI.csv"), sep=";")
personnel_dosimetry_nuklear.to_csv(Path(rootpath, 'radpharma.csv'), sep=";")
