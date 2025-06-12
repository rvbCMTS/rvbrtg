CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"

TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

# Machine types
machine_type_dict = {
    "CT": "CT",
    "Fluoroscopic": "XASTAT",
    "Mobile C-arm": "XAMOB",
    "Conventional": "DX",
    "Mammography": "MG",
    "Intraoral": "IO",
    "Panoramic": "PX",
    "Dental Cone Beam CT": "DCBCT",
    "PET": "PET",
    "PET/CT": "PETCT",
    "SPECT": "SPECT",
    "SPECT/CT": "SPECTCT",
    "Nuclear Medicine": "NM",
    "Mobile X-ray": "DXMOB",
    "Conventional with fluoro": "DXXA",
}

# Undersökningskoder
# Endoskopi/Kirurgi börjar med E. Exempelvis "ERCP - i narkos" har kod E4905
# Thorax börjar på 3. Exempelvis "Thorakal stengraftinläggning" har kod 39948 och "Pulmonalisangiografi" har kod 38200 (OBS endast på U104)
# Buk börjar på 4. Exempelvis "PTC med externt dränage - i narkos" har kod 49005 och "Abdominell stentgraftinläggning" har kod 49948 och "Buköversikt akut - punktion + inl av kateter" har kod 46051
# Njurar börjar på 5. Exempelvis "Byte av nefrostomikateter ..." har kod 59100 och "Percutan nefrostomi .." har kod 59000 (samma kod för höger och vänster)
# Extremiteter börjar på 6. Exempelvis "Angiografi, aortofemoral" har kod 67700
# Ultraljud har koder som börja på 9
# Skalle (angio) börjar på 17 och emboliseringar på 19. Exempelvis "Angiografi, komb av flera skallangio" har kod 17500 och "Intracraniell trombectomi + komb av flera skallangio - i narkos" har kod 19305

procedure_codes_dict = {
    "Hjärna": ["17500"],  # Skallangio - Komb fl skallangio
    "Buk (gallvägar och urinvägar)": ["59100", "59000", "49005", "49948", "46051"],
    # 59100 - Byte av nefrostomikateter...
    # 59000 - Percutan nefrostomi...
    # 49005 - PTC med externt dränage - i narkos
    # 49948 - Abdominell stentgraftinläggning
    # 46051 - Buköversikt akut - punktion + inl av kateter
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    "Lycksele lasarett": ["L3"],
    "Skellefteå lasarett": ["S08"],
    "Norrlands universitetssjukhus": [
        "U104",
        "U105",
        "U105_old",
        "U106",
        "U106_old",
        "U110",
        "U601",
        "U602",
        "Arytmi 1",
        "Arytmi 2",
    ],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor (16 år och äldre).Antal ",
    "female-dap": "Kvinnor (16 år och äldre).DAP (Gy*cm2)",
    "male-studies": "Män (16 år och äldre).Antal ",
    "male-dap": "Män (16 år och äldre).DAP (Gy*cm2)",
    # "girl-studies": "Flickor (15 år och yngre).Antal ",
    # "girl-dap": "Flickor (15 år och yngre).DAP (Gy*cm2)",
    # "boy-studies": "Pojkar (15 år och yngre).Antal ",
    # "boy-dap": "Pojkar (15 år och yngre).DAP (Gy*cm2)",
}
