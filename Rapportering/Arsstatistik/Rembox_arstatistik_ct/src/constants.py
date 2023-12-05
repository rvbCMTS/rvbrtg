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
    "CT skalle (skelett)": [
        "81500", "81505", "815SS", "81524", "81536", "81537", "81550", "81580", "81581", "815KK"
    ],
    "CT hjärna": [
        "81000", "81005", "81038", "81070", "81071", "81080", "81081","81087", "81097",
        "810D0", "810E1", "810M0", "810RH", "810RM", "81100"
    ],
    "CT halsrygg": [
        "82000", "82003", "82005", "82038", "82049", "82050", "82080", "82081", "820D0", "820M0", "820RM"
    ],
    "CT hals (mjukvävnad)": [
        "81800", "81805", "81850", "81880", "81881", "818D1"
    ],
    "CT bröstrygg": [
        "82200", "82203", "82205", "82249", "82250", "82280", "82281", "822D0"
    ],
    "CT lungor": [
        "83000", "83005", "83038", "83050", "83067", "83068", "83069", "83070", "83071", "83079", "83080",
        "83081", "830E0", "830E1"
    ],
    "CT ländrygg": [
        "82400", "82403", "82405", "82449", "82450", "82480", "82481", "82488", "824D0"
    ],
    "CT buk": [
        "84000", "84005", "84050", "84063", "84068", "84069", "84070", "84071", "84075", "84078", "84080", "84081",
        "84095", "840D1", "840E1", "84100", "84105", "84150", "84168", "84169", "84179", "84180", "84181", "84300",
        "84305", "84350", "84363", "84380", "84381", "84400", "84405", "84450", "84463", "84464", "84480", "84481",
        "84700", "84705", "84780", "84781", "84800", "84880", "84881", "848D0", "85200", "85205", "85250", "85263",
        "85264", "85280", "85281", "85300", "85301", "85305", "85350", "85380", "85381", "85500", "85505", "85550",
        "85568", "85569", "85580", "85581", "86000", "86005", "86068", "86069"
    ],
    "CT bäcken": [
        "82600", "82605", "82649", "82650", "82680", "82681", "82800", "82805", "82850", "82880", "82881",
        "82900", "82903", "82905", "82939", "82950", "82980", "82981", "86800"
    ],
    "CT urografi": [
        "85400", "85405", "85463", "85464", "85480", "85481"
    ],
    "CT bäckenmätning (pelvimetri)": ["88900"],
    "CT hela bålen": [
        "83800", "83805", "83863", "83868", "83869", "83870", "83871", "83875", "83878", "83880", "83881",
        "838D1", "838D3", "838E0", "838E1", "838M1", "838OD"
  ]
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    "Lycksele lasarett": ["L11", "L5"],
    "Skellefteå lasarett": ["S06", "S07"],
    "Norrlands universitetssjukhus": ["U209", "U210", "U211", "U213"],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor (16 år och äldre).Antal ",
    "female-dlp": "Kvinnor (16 år och äldre).DLP (mGy*cm)",
    "male-studies": "Män (16 år och äldre).Antal ",
    "male-dlp": "Män (16 år och äldre).DLP (mGy*cm)",
    "girl-studies": "Flickor (15 år och yngre).Antal ",
    "girl-dlp": "Flickor (15 år och yngre).DLP (mGy*cm)",
    "boy-studies": "Pojkar (15 år och yngre).Antal ",
    "boy-dlp": "Pojkar (15 år och yngre).DLP (mGy*cm)",
}
