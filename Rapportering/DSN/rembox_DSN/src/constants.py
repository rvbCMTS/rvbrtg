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


# Maskiner vid verksamhetsplats
machines_at_hospital = {
    "Lycksele lasarett": ["L11", "L5"],
    "Skellefteå lasarett": ["S06", "S07"],
    "Norrlands universitetssjukhus": ["U209", "U210", "U211", "U213"],
}
# Undersökningar
procedure_codes_adults = {
    "Hjärna utan kontrast": 81000,
    "Halsrygg": 82000,
    "Thorax med kontrast": 83080,
    "Buk med kontrast": 84080,
    "Urinvägar": 8400,
    "Urografi": 85463,
}

''' 
trauma i u umeå "838M1 thorax, 810M1 hjärna...
838M1 thorax-buk multitrauma med iv kontrast
810M0 hjärna multitrauma
820M0 halsrygg multitrauma
'''

# TODO: procedure codes missing for "ventrikel/shunt"
# Har pratat med Emma om att lägga till dem framöver.
procedure_codes_kids = {
    "Hjärna utan kontrast": 81000,
    "Hjärna ventrikel/shunt utan kontrast": 81000,
    "Thorax med kontrast": 83080,
    "HR Thorax med kontrast": 83080,
    "Buk med kontrast": 84080,
    "Trauma med kontrast": 88080,
}

# TODO: procedure codes missing for "ventrikel/shunt"
# Har pratat med Emma om att lägga till dem framöver.
procedure_codes_young_kids = {
    "Hjärna utan kontrast": 81000,
    "Hjärna ventrikel/shunt utan kontrast": 81000,
    "Thorax med kontrast": 83080,
    "HR Thorax med kontrast": 83080,
    "Buk med kontrast": 84080,
    "Trauma med kontrast": 88080,
}

machines_in_region = ["L11", "L5", "S06", "S07", "U209", "U210", "U211", "U213"]

report_template_columns = [
    "CTDIvol (mGy)",
    "DLP (mGy*cm)",
    "SSDE (mGy)",
    "Ålder (Anges i år om patientgruppen är vuxna och barn från 4 år, annars i månader)",
    "Man/kvinna",
    "Längd (cm)",
    "Vikt (kg)",
]
