from pathlib import Path

from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
VALID_STUDY_COLUMNS = StudyColumn()
VALID_SERIES_COLUMNS = SeriesColumn()

CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"

TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

MODALITY_CT: str = "CT"
MODALITY_DX: str = "DX"
MODALITY_MG: str = "MG"
MODALITY_XA: str = "XA"

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA
]

DROP_DUPLICATES_BY_ACQUISITION_PLANE = {
    'keep': {
        "default": "Plane A",
        "machine_specific":{
            "U104": "Plane A" # "<machine_display_name>": "<Acquisition Plane Value To Keep>"
        }
    }
}

COLUMN_SELECTION_PER_MODALITY = {
    MODALITY_CT: [
            VALID_STUDY_COLUMNS.Hospital,
            VALID_STUDY_COLUMNS.StudyDateTime,
            VALID_STUDY_COLUMNS.StudyInstanceUID,
            VALID_STUDY_COLUMNS.StudyId,
            VALID_STUDY_COLUMNS.Machine,
            VALID_STUDY_COLUMNS.AccessionNumber,
            VALID_STUDY_COLUMNS.StudyDescription,
            VALID_STUDY_COLUMNS.PatientAge,
            VALID_STUDY_COLUMNS.PatientsWeight,
            VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
            VALID_STUDY_COLUMNS.PerformingPhysicianName,
            VALID_STUDY_COLUMNS.PerformingPhysicianIdentificationSequence,
            VALID_STUDY_COLUMNS.PatientDbId,
            VALID_STUDY_COLUMNS.DlpTotal,
            VALID_STUDY_COLUMNS.PatientsSex,
            VALID_STUDY_COLUMNS.ProcedureCode,
            VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
            VALID_STUDY_COLUMNS.RequestedProcedureCodeMeaning,
    ],
    MODALITY_DX: [
        VALID_STUDY_COLUMNS.Hospital,
        VALID_STUDY_COLUMNS.StudyDateTime,
        VALID_STUDY_COLUMNS.StudyInstanceUID,
        VALID_STUDY_COLUMNS.StudyId,
        VALID_STUDY_COLUMNS.Machine,
        VALID_STUDY_COLUMNS.AccessionNumber,
        VALID_STUDY_COLUMNS.StudyDescription,
        VALID_STUDY_COLUMNS.PatientAge, #Finns inte för Philips
        VALID_STUDY_COLUMNS.PatientsWeight, #Saknas ofta #Vad används denna till?
        VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents, #Vad används denna till?
        VALID_STUDY_COLUMNS.PerformingPhysicianName, #Vad används denna till?
        VALID_STUDY_COLUMNS.PerformingPhysicianIdentificationSequence, #Vad används denna till?
        VALID_STUDY_COLUMNS.PatientDbId, #Vad används denna till?
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
        VALID_STUDY_COLUMNS.PatientsSex,
        VALID_STUDY_COLUMNS.ProcedureCode,
        VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
        VALID_STUDY_COLUMNS.RequestedProcedureCodeMeaning,
    ],
    MODALITY_MG: [
        VALID_STUDY_COLUMNS.Hospital,
        VALID_STUDY_COLUMNS.StudyDateTime,
        VALID_STUDY_COLUMNS.StudyInstanceUID,
        VALID_STUDY_COLUMNS.StudyId,
        VALID_STUDY_COLUMNS.Machine,
        VALID_STUDY_COLUMNS.AccessionNumber,
        VALID_STUDY_COLUMNS.StudyDescription,
        VALID_STUDY_COLUMNS.PatientAge,
        VALID_STUDY_COLUMNS.PatientDbId,
        VALID_STUDY_COLUMNS.PatientsSex,
        VALID_SERIES_COLUMNS.AcquisitionProtocol,
        VALID_STUDY_COLUMNS.ProcedureCode,
        VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
        VALID_STUDY_COLUMNS.RequestedProcedureCodeMeaning,
        VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts,
    ],
    MODALITY_XA: [
        VALID_STUDY_COLUMNS.Hospital,
        VALID_STUDY_COLUMNS.StudyDateTime,
        VALID_STUDY_COLUMNS.StudyInstanceUID,
        VALID_STUDY_COLUMNS.StudyId,
        VALID_STUDY_COLUMNS.Machine,
        VALID_STUDY_COLUMNS.AccessionNumber,
        VALID_STUDY_COLUMNS.StudyDescription,
        VALID_STUDY_COLUMNS.PatientAge, #Finns inte för Philips
        VALID_STUDY_COLUMNS.PatientsWeight, #Saknas ofta #Vad används denna till?
        VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents, #Vad används denna till?
        VALID_STUDY_COLUMNS.PerformingPhysicianName, #Vad används denna till?
        VALID_STUDY_COLUMNS.PerformingPhysicianIdentificationSequence, #Vad används denna till?
        VALID_STUDY_COLUMNS.PatientDbId, #Vad används denna till?
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
        VALID_STUDY_COLUMNS.PatientsSex,
        VALID_SERIES_COLUMNS.AcquisitionProtocol, #Vad används denna till?
        VALID_SERIES_COLUMNS.DateTimeStarted,
        VALID_STUDY_COLUMNS.ProcedureCode,
        VALID_STUDY_COLUMNS.ProcedureCodeMeaning,
        VALID_STUDY_COLUMNS.RequestedProcedureCodeMeaning,
    ]
}

MODALITY_FILTER_SELECTION_PER_MODALITY = {
    MODALITY_CT: ["CT"],
    MODALITY_DX: ["DX", "XASTAT", "XAMOB"],
    MODALITY_MG: ["MG"],
    MODALITY_XA: ["XASTAT", "XAMOB"]
}

REPORT_TEMPLATE_PATH_PER_MODALITY = {
    MODALITY_CT: Path(__file__).parent / "ReportTemplates/CT Mall årsredovisning DosReg.xlsx",
    MODALITY_DX: Path(__file__).parent / "ReportTemplates/RTG Mall årsredovisning DosReg.xlsx",
    MODALITY_MG: Path(__file__).parent / "ReportTemplates/MAM Mall årsredovisning DosReg.xlsx",
    MODALITY_XA: Path(__file__).parent / "ReportTemplates/INT Mall årsredovisning DosReg.xlsx",
}

EXAM_GROUPING_TYPE_STUDY_DESCRIPTION = "Study Description"
EXAM_GROUPING_TYPE_PROTOCOL_CODE = "Protocol Code"
EXAM_GROUPING_TYPE_PROCEDURE_CODE = "Procedure Code"

EXAM_GROUPING_RULES_BY_MODALITY = {
    MODALITY_CT: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "CT bröstrygg": ["82200", "82203", "82205", "82249", "82250", "82280", "82281", "822D0"],
            "CT buk": ["84000", "84005", "84050", "84063", "84068", "84069", "84070", "84071", "84075", "84078", "84080", "84081", "84095", "840D1", "840E1", "84100", "84105", "84150", "84168", "84169", "84179", "84180", "84181", "84300", "84305", "84350", "84363", "84380", "84381", "84400", "84405", "84450", "84463", "84464", "84480", "84481", "84700", "84705", "84780", "84781", "84800", "84880", "84881", "848D0", "85200", "85205", "85250", "85263", "85264", "85280", "85281", "85300", "85301", "85305", "85350", "85380", "85381", "85500", "85505", "85550", "85568", "85569", "85580", "85581", "86000", "86005", "86068", "86069"],
            "CT bäcken": ["82600", "82605", "82649", "82650", "82680", "82681", "82800", "82805", "82850", "82880", "82881", "82900", "82903", "82905", "82939", "82950", "82980", "82981", "86800"],
            "CT bäckenmätning (pelvimetri)": ["88900"],
            "CT hals (mjukvävnad)": ["81800", "81805", "81850", "81880", "81881", "818D1"],
            "CT halsrygg": ["82000", "82003", "82005", "82038", "82049", "82050", "82080", "82081", "820D0", "820M0", "820RM"],
            # CT hela bålen behöver ej rapporteras men vi tar med dem då vi har koderna
            "CT hela bålen": ["83800", "83805", "83863", "83868", "83869", "83870", "83871", "83875", "83878", "83880", "83881", "838D1", "838D3", "838E0", "838E1", "838M1", "838OD"],
            "CT hjärna": ["81000", "81005", "81038", "81070", "81071", "81080", "81081","81087", "81097", "810D0", "810E1", "810M0", "810RH", "810RM", "81100"],
            "CT lungor": ["83000", "83005", "83038", "83050", "83067", "83068", "83069", "83070", "83071", "83079", "83080", "83081", "830E0", "830E1"],
            "CT ländrygg": ["82400", "82403", "82405", "82449", "82450", "82480", "82481", "82488", "824D0"],
            "CT skalle (skelett)": ["81500", "81505", "815SS", "81524", "81536", "81537", "81550", "81580", "81581", "815KK"],
            "CT urografi": ["85400", "85405", "85463", "85464", "85480", "85481"],
        }
    },
    MODALITY_DX: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "Bröstkorg (revben)": [],
            "Bröstrygg": [],
            "Buk": [],
            "Bukangiografi": ["47100", "47142", "47200", "47242", "47600", "47642"],
            "Bäcken/höft (skelett)": [],
            "Cerebral angiografi": [],
            "Defekografi": ["44200"],
            "ERCP": ["E4900", "E4903", "E4905", "E4976"],
            "Extremitetsskelett och –leder": [],
            "GI (bariumkontrast)": ["44000", "44036"],
            "Hals (mjukvävnad)": ["41100", "41127", "41200", "41300", "41327"],
            "Halsrygg": [],
            "Hjärta/lungor": [],
            "Huvud (skall- och ansiktsskelett)": [],
            "Kolangiografi": ["49055", "45400"],
            "Kolecystografi": [],
            "Lymfangiografi": [],
            "Ländrygg": [],
            "Perifer angiografi": ["67500", "67600", "67641", "67643", "67648", "67672", "67700", "67741", "67743", "67748", "67772", "67900"],
            "SI-led": [],
            "Skolios (vinkelmätning)": [],
            "Thoraxangiografi": [],
            "Urografi": [],
        },
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {
            'Bröstkorg (revben)': ['Revben', 'Axel, AC-led DX', 'Axel, AC-led SIN', 'Nyckelben', 'Nyckelben DX', 'Nyckelben SIN', 'Skulderblad DX', 'Skulderblad SIN', 'Sternum'],
            'Bröstrygg': ['Bröstrygg'],
            'Buk': ['Buköversikt', 'Lunga-buk nyfödd', 'Tunntarm'],
            'Bäcken/höft (skelett)': ['Bäcken', 'Protesbäcken', 'Höftleder, barn', 'Höft stereo DX', 'Höft stereo SIN', 'Höftled DX', 'Höftled SIN', 'Sacrum, coccyx'],
            'Extremitetsskelett och –leder': ['Armbågsled DX', 'Armbågsled SIN', 'Benlängd', 'Benvinkel DX', 'Benvinkel SIN', 'Fot DX', 'Fot SIN', 'Fot belastad DX', 'Fot belastad SIN', 'Fotled DX', 'Fotled SIN', 'Fotled belastad DX', 'Fotled belastad SIN', 'Hand DX', 'Hand SIN', 'Handled DX', 'Handled SIN', 'Knäled DX', 'Knäled SIN', 'Knäled', 'Lårben DX', 'Lårben SIN', 'Lårben', 'Scaphoideum DX', 'Scaphoideum SIN', 'Skelettålder', 'Underarm DX', 'Underarm SIN', 'Underben DX', 'Underben SIN', 'Överarm DX', 'Överarm SIN'],
            'Hals (mjukvävnad)': [''],
            'Halsrygg': ['Halsrygg'],
            'Hjärta/lungor': ['Lungor', 'Lungor, liggande'],
            'Huvud (skall- och ansiktsskelett)': ['Ansiktsskelett', 'Shuntkontroll', 'Shuntöversikt', 'Skalle'],
            'Ländrygg': ['Ländrygg'],
            'SI-led': ['Sacroiliacaleder'],
            'Skolios (vinkelmätning)': ['Helrygg']
        }
    },
    MODALITY_MG: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "Mammografi 2D - klinisk (ett eller två bröst)": ["66000", "66000D", "66000S"],
            "Mammografi 2D - screening (ett eller två bröst)": ["66200"]
        }
    },
    MODALITY_XA: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "Buk (gallvägar och urinvägar)": ["59100", "59000", "49005", "49948", "46051"],
            "Buk (TIPS)": [],
            "Bäcken": [],
            "Hjärna": ["17500"],
            "Pacemaker": [],
            "PTCA": ["37300"],
        }
    },
}

AGE_SEX_CATEGORY_JUNIOR_MALE = "Pojkar"
AGE_SEX_CATEGORY_JUNIOR_FEMALE = "Flickor"
AGE_SEX_CATEGORY_ADULT_MALE = "Män"
AGE_SEX_CATEGORY_ADULT_FEMALE = "Kvinnor"

OUTPUT_COL_AGE_SEX_CATEGORY = "ageSexCategory"
OUTPUT_COL_EXAM = "Undersökning"
