from pathlib import Path

from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
VALID_STUDY_COLUMNS = StudyColumn()
VALID_SERIES_COLUMNS = SeriesColumn()

CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"

TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"
VERIFY_SSL_CERT = False

MODALITY_CT: str = "CT"
MODALITY_DX: str = "DX"
MODALITY_MG: str = "MG"
MODALITY_XA: str = "XA"
MODALITY_DCBCT: str = "DCBCT"

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA
]

COLUMN_SELECTION_GENERAL = [
    VALID_STUDY_COLUMNS.Hospital,
    VALID_STUDY_COLUMNS.StudyDateTime,
    VALID_STUDY_COLUMNS.StudyInstanceUID,
    VALID_STUDY_COLUMNS.StudyId,
    VALID_STUDY_COLUMNS.Machine,
    VALID_STUDY_COLUMNS.MachineType,
    VALID_STUDY_COLUMNS.StudyDescription,
    VALID_STUDY_COLUMNS.AccessionNumber,
    VALID_STUDY_COLUMNS.PatientAge,
    VALID_STUDY_COLUMNS.PatientAgeUnit,
    VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
    VALID_STUDY_COLUMNS.PatientDbId,
    VALID_STUDY_COLUMNS.PatientsSex,
    VALID_STUDY_COLUMNS.PatientsSize,
    VALID_STUDY_COLUMNS.PatientsSizeDate,
    VALID_STUDY_COLUMNS.PatientsSizeSource,
    VALID_STUDY_COLUMNS.ProcedureCode,
]

COLUMN_SELECTION_PER_MODALITY = {
    MODALITY_CT: COLUMN_SELECTION_GENERAL + [
            VALID_STUDY_COLUMNS.DlpTotal,
    ],
    MODALITY_DX: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
    ],
    MODALITY_MG: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts,
    ],
    MODALITY_XA: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
    ],
    MODALITY_DCBCT: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
    ]
}

MODALITY_FILTER_SELECTION_PER_MODALITY = {
    MODALITY_CT: ["CT"],
    MODALITY_DX: ["DX", "XAMOB"],
    MODALITY_MG: ["MG"],
    MODALITY_XA: ["XASTAT"],
    MODALITY_DCBCT: ["CT", "DCBCT"],
}

REPORT_TEMPLATE_PATH_PER_MODALITY = {
    MODALITY_CT: Path(__file__).parent / "ReportTemplates/CT Mall årsredovisning DosReg 2025.xlsx",
    MODALITY_DX: Path(__file__).parent / "ReportTemplates/RTG Mall årsredovisning DosReg 2025.xlsx",
    MODALITY_MG: Path(__file__).parent / "ReportTemplates/MAM Mall årsredovisning DosReg 2025.xlsx",
    MODALITY_XA: Path(__file__).parent / "ReportTemplates/INT Mall årsredovisning DosReg 2025.xlsx",
    MODALITY_DCBCT: Path(__file__).parent / "ReportTemplates/Dental CBCT Mall årsredovisning DosReg 2025.xlsx",
}

EXAM_GROUPING_TYPE_STUDY_DESCRIPTION = "Study Description"
EXAM_GROUPING_TYPE_PROTOCOL_CODE = "Protocol Code"
EXAM_GROUPING_TYPE_PROCEDURE_CODE = "Procedure Code"

EXAM_GROUPING_RULES_BY_MODALITY = {
    MODALITY_CT: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "DT01:Datortomograf (fast installerad eller mobil):Diagnostik:Huvud och hals": [],
            "DT02:Datortomograf (fast installerad eller mobil):Diagnostik:Thorax inkl lunga/hjärta/bröstkorg": [],
            "DT03:Datortomograf (fast installerad eller mobil):Diagnostik:Övre buk (exlusive njurar)": [],
            "DT04:Datortomograf (fast installerad eller mobil):Diagnostik:Nedre Buk (inklusive njurar)": [],
            "DT05:Datortomograf (fast installerad eller mobil):Diagnostik:Bäcken, höfter": [],
            "DT06:Datortomograf (fast installerad eller mobil):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled": [],
            "DT07:Datortomograf (fast installerad eller mobil):Diagnostik:Ryggraden": [],
            "DT08:Datortomograf (fast installerad eller mobil):Diagnostik:Hela bålen (inkl. thorax-buk kombination)": [],
            "DT09:Datortomograf (fast installerad eller mobil):Diagnostik:Hela kroppen (multitrauma)": [],
            "DT10:Datortomograf (fast installerad eller mobil):Diagnostik:Övrig diagnostik": [],
            "DT11:Datortomograf (fast installerad eller mobil):Behandling:Huvud och hals": [],
            "DT12:Datortomograf (fast installerad eller mobil):Behandling:Thorax inkl lunga/hjärta/bröstkorg": [],
            "DT13:Datortomograf (fast installerad eller mobil):Behandling:Övrigt": [],
        }
    },
    MODALITY_DX: {
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {
            "RTG01:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Huvud och hals": ["Ansiktsskelett", "Skalle", "Öra cochlea DX", "Öra cochlea SIN"],
            "RTG02:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": ["Lungor", "Lungor, liggande", "Sternum"],
            "RTG03:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övre buk (exklusive njurar)": [],
            "RTG04:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Nedre Buk (inklusive njurar, exklusive bäcken/höft)": ["Buköversikt", "Tunntarm"],
            "RTG05:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Bäcken höfter": ["Bäcken", "Protesbäcken", "Höftled DX", "Höftled SIN", "Sacroiliacaleder"],
            "RTG06:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled": [
                "Armbågsled DX",
                "Armbågsled SIN",
                "Axel, AC-led DX",
                "Axel, AC-led SIN",
                "Benlängd",
                "Fot DX",
                "Fot SIN",
                "Fotled DX",
                "Fotled SIN",
                "Fotled belastad DX",
                "Fotled belastad SIN",
                "Hand DX",
                "Hand SIN",
                "Handled DX",
                "Handled SIN",
                "Knäled DX",
                "Knäled SIN",
                "Lårben DX",
                "Lårben SIN",
                "Scaphoideum DX",
                "Scaphoideum SIN",
                "Underarm DX",
                "Underarm SIN",
                "Underben DX",
                "Underben SIN",
                "Överarm DX",
                "Överarm SIN"
            ],
            "RTG07:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Ryggraden": ["Bröstryggrad", "Halsryggrad", "Helrygg", "Ländryggrad", "Sacrum, coccyx"],
            "RTG08:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övrig diagnostik": [],
            "MOB1:Mobil röntgenutrustning för bildtagning:Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": [],
            "MOB2:Mobil röntgenutrustning för bildtagning:Diagnostik:Extremiteter, inklusive axlar/axelled": [],
            "MOB3:Mobil röntgenutrustning för bildtagning:Diagnostik:Övrigt": [],
            "MOB4:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning:i samband med kirurgi	Skelett": [], # Finns under procedure code 
            "MOB5:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning:i samband med kirurgi	Övrigt": [],
            "BEN1:Bentäthetsmätare:Diagnostik:Inget specifikt": [],
        },
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "MOB4:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning:i samband med kirurgi	Skelett": ["X621", "X622", "X623", "X626", "X630", "X631", "X633",
                                                                                                                      "X643", "X636", "X637", "X638", "X639", "X641", "X642",
                                                                                                                      "X642", "X645", "X646", "X648"], 
    },
    MODALITY_MG: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "MAM1:Mammografiutrustning (fast installerad):Diagnostik:Bröstkörtlar 2D": ["66000", "66000D", "66000S"],
            "MAM2:Mammografiutrustning (fast installerad):Diagnostik:Bröstkörtlar tomosyntes": ["66061"],
            "MAM3:Mammografiutrustning (fast installerad):Diagnostik:Övrigt": [],
            "MAM4:Mammografiutrustning (fast installerad):Screening:Bröstkörtlar 2D": ["66200"],
            "MAM5:Mammografiutrustning (fast installerad):Screening:Bröstkörtlar tomosyntes": [],
        }
    },
    MODALITY_XA: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "INT01:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Huvud och hals": [],
            "INT02:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Thorax inklusive lungor, exklusive hjärta": ["38200"],
            "INT03:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Hjärta": [], #Lämnar denna tom då coronarangiografi ej kan skiljas från PCI
            "INT04:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Buk": ["58300"],
            "INT05:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Bäcken": [],
            "INT06:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Extremiteter": [],
            "INT07:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Övrig diagnostik": [],
            "INT08:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Huvud och hals": ["11005", "11100", "17005", "17500", "17505", 
                                                                                                                               "19000", "19005", "19100", "19305", "19900", 
                                                                                                                               "19950", "19951"],
            "INT09:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Thorax inklusive lungor, exklusive hjärta": ["39900", "39951", "3995A"],
            "INT10:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Hjärta": ["32700", "32800", "33000", "33100", "33500", "36000", "36600",
                                                                                                                       "37300", "38400", "38500", "39100", "39500", "X401", "X402"],
            "INT11:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Buk": ["47100", "47142", "47148", "47200", "47242", "47900", "49500", 
                                                                                                                    "49900", "49905", "49948", "49951", "59500", "59600", "59748", 
                                                                                                                    "59800", "59900"],
            "INT12:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Bäcken": ["57000", "57042", "57400"],
            "INT13:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Extremiteter": ["67600", "67700", "67772", "67800", "67500"],
            "INT14:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Övrig behandling": [],
            "INT15:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Huvud och hals": ["10100", "10500", "10528", "10555", "41100", 
                                                                                                                                      "41127", "41200", "4124B", "41327",  ],
            "INT16:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Thorax": ["32000", "32028", "41600", "42000", ],
            "INT17:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Buk": ["45400", "43000", "43200", "44000", "44900", "45000", 
                                                                                                                           "46128",],
            "INT18:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Ryggraden": [],
            "INT19:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Bäcken, inklusive höfter/höftled": ["44000", "63935", "64000"],
            "INT20:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Extremiteter, inklusive axlar/axelled": [],
            "INT21:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Övrigt": [],
            "INT22:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Huvud och hals": [],
            "INT23:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Thorax": ["39051", "39348", "39900", "48451", "48452", "48455", 
                                                                                                                              "4845A", "48551", "48552", "4855A"],
            "INT24:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Buk": ["42051", "46028", "46052", "46055", "46136", "46151",
                                                                                                                           "46152", "46155", "46248", "49000", "49005", "49055", 
                                                                                                                           "49100", "49105", "49148", "49148", "49150", "49155", 
                                                                                                                           "49200", "49205", "49300", "49600", "49928", "49960", "49961", 
                                                                                                                           "58700", "59000", "59005", "59100", "E4976", "E4900"],
            "INT25:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Ryggraden": ["13800", "1384A",  "17800", "17805"],
            "INT26:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Bäcken": ["50351", "51200", "51255", "51348", "53000", "53100", "53200"],
            "INT27:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Extremiteter, inklusive axlar/axelled": [],
            "INT28:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Övrigt": [],
        }
    },
    MODALITY_DCBCT: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "CBCT1:CBCT:Diagnostik:Odontologisk undersökning": [],
        }
    },
    }
}

AGE_SEX_CATEGORY_JUNIOR_MALE = "Pojkar"
AGE_SEX_CATEGORY_JUNIOR_FEMALE = "Flickor"
AGE_SEX_CATEGORY_ADULT_MALE_16_40 = "Män 16-40"
AGE_SEX_CATEGORY_ADULT_FEMALE_16_40 = "Kvinnor 16-40"
AGE_SEX_CATEGORY_ADULT_MALE_41_65 = "Män 41-65"
AGE_SEX_CATEGORY_ADULT_FEMALE_41_65 = "Kvinnor 41-65"
AGE_SEX_CATEGORY_ADULT_MALE_66plus = "Män 66+"
AGE_SEX_CATEGORY_ADULT_FEMALE_66plus = "Kvinnor 66+"
AGE_SEX_CATEGORY_DOSE_BOY = "Pojkar för dosberäkning"
AGE_SEX_CATEGORY_DOSE_GIRL = "Flickor för dosberäkning"
AGE_SEX_CATEGORY_DOSE_MALE = "Män för dosberäkning"
AGE_SEX_CATEGROY_DOSE_FEMALE = "Kvinnor för dosberäkning"

OUTPUT_COL_AGE_SEX_CATEGORY = "ageSexCategory"
OUTPUT_COL_AGE_SEX_CATEGORY_DOSE = "ageSexCategoryDose"
OUTPUT_COL_EXAM = "Undersökning"

MODALITY_DX_MACHINE_GENERAL = ["L2", "L4", "LSTORU", "LTARNA", "LVILM", "S01", "S02", "S04", "U220", "U221", "U222"]
MODALITY_DX_MACHINE_MOBILE = ["L10", "S12", "U220", "U221", "U222"]
MODALITY_XA_MACHINE_TREATMENT = ["U104", "U105", "U106", "U601", "U601_2025", "U602", "Arytmi 1", "Arytmi 2"]
MODALITY_XA_MACHINE_DIAGNOSTIC = ["U110", "S08", "L3"]
