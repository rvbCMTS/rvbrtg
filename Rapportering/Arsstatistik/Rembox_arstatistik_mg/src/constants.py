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
    #"CT hjärna": ["81000"],
    #"CT skalle (skelett)": ["81500"],
    #"CT hals (mjukvävnad)": ["81880"],
    #"CT halsrygg": ["82000"],
    #"CT bröstrygg": ["82200"],
    #"CT ländrygg": ["82400"],
    #"CT lungor": ["83079"],
    #"CT buk": ["84000"],
    #"CT urografi": ["85481", "85464"],
    #"CT bäcken": ["86800"],
    "MG kliniskt": ["66000", "66000D", "66000S"],
    "MG screening": ["66200"],
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    "Mammografivagnen": ["M100", "M113"],
    "Skellefteå lasarett": ["M109"],
    "Norrlands universitetssjukhus": ["M400", "M401", "M103", "U213"],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor (16 år och äldre).Antal ",
    "female-dlp": "Kvinnor (16 år och äldre).AGD ",
    "male-studies": "Män (16 år och äldre).Antal ",
    "male-dlp": "Män (16 år och äldre).AGD ",
    "girl-studies": "Flickor (15 år och yngre).Antal ",
    "girl-dlp": "Flickor (15 år och yngre).AGD ",
}
