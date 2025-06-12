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
procedure_codes_dict = {
    # "CT hjärna": ["81000"],
    # "CT skalle (skelett)": ["81500"],
    # "CT hals (mjukvävnad)": ["81880"],
    # "CT halsrygg": ["82000"],
    # "CT bröstrygg": ["82200"],
    # "CT ländrygg": ["82400"],
    # "CT lungor": ["83079"],
    # "CT buk": ["84000"],
    # CT urografi": ["85481", "85464"],
    # "CT bäcken": ["86800"],
    "Mammografi 2D - klinisk (ett eller två bröst)": ["66000", "66000D", "66000S"],
    "Mammografi 2D - screening (ett eller två bröst)": ["66200"],
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    # "Lycksele lasarett": ["L11", "L5"],
    # "Skellefteå lasarett": ["S06", "S07"],
    # "Norrlands universitetssjukhus": ["U209", "U210", "U211", "U213"],
    "Mammografivagnen": ["Mammovagnen - M113"],
    "Skellefteå lasarett": ["M109"],
    "Norrlands universitetssjukhus": ["M103", "M400", "M401"],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor.Antal ",
    "female-agd": "Kvinnor.AGD",
    "male-studies": "Män.Antal",
    "male-agd": "Män.AGD",
    # "girl-studies": "Flickor (15 år och yngre).Antal ",
    # "girl-dlp": "Flickor (15 år och yngre).DLP (mGy*cm)",
    # "boy-studies": "Pojkar (15 år och yngre).Antal ",
    # "boy-dlp": "Pojkar (15 år och yngre).DLP (mGy*cm)",
}
