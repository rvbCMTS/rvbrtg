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
MODALITY_DCBCT: str = "DCBCT"

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_CT,
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA
]

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
    MODALITY_XA: ["XASTAT", "XAMOB"],
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
            "RTG01:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Huvud och hals": ['Ansiktsskelett', 'Shuntkontroll', 'Shuntöversikt', 'Skalle'],
            "RTG02:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": ['Lungor', 'Lungor, liggande'],
            "RTG03:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övre buk (exklusive njurar)": [],
            "RTG04:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Nedre Buk (inklusive njurar, exklusive bäcken/höft)": ['Buköversikt', 'Lunga-buk nyfödd', 'Tunntarm'],
            "RTG05:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Bäcken höfter": ['Bäcken', 'Protesbäcken', 'Höftleder, barn', 'Höft stereo DX', 'Höft stereo SIN', 'Höftled DX', 'Höftled SIN'],
            "RTG06:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled": ['Axel, AC-led DX', 'Axel, AC-led SIN', 'Armbågsled DX', 'Armbågsled SIN', 'Benlängd', 'Benvinkel DX', 'Benvinkel SIN', 'Fot DX', 'Fot SIN', 'Fot belastad DX', 'Fot belastad SIN', 'Fotled DX', 'Fotled SIN', 'Fotled belastad DX', 'Fotled belastad SIN', 'Hand DX', 'Hand SIN', 'Handled DX', 'Handled SIN', 'Knäled DX', 'Knäled SIN', 'Knäled', 'Lårben DX', 'Lårben SIN', 'Lårben', 'Scaphoideum DX', 'Scaphoideum SIN', 'Skelettålder', 'Underarm DX', 'Underarm SIN', 'Underben DX', 'Underben SIN', 'Överarm DX', 'Överarm SIN'],
            "RTG07:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Ryggraden": ['Halsrygg', 'Helrygg', 'Ländrygg'],
            "RTG08:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övrig diagnostik": [],
            "MOB1:Mobil röntgenutrustning för bildtagning:Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": ['Lungor', 'Lungor, liggande'],
            "MOB2:Mobil röntgenutrustning för bildtagning:Diagnostik:Extremiteter, inklusive axlar/axelled": ['Axel, AC-led DX', 'Axel, AC-led SIN', 'Armbågsled DX', 'Armbågsled SIN', 'Benlängd', 'Benvinkel DX', 'Benvinkel SIN', 'Fot DX', 'Fot SIN', 'Fot belastad DX', 'Fot belastad SIN', 'Fotled DX', 'Fotled SIN', 'Fotled belastad DX', 'Fotled belastad SIN', 'Hand DX', 'Hand SIN', 'Handled DX', 'Handled SIN', 'Knäled DX', 'Knäled SIN', 'Knäled', 'Lårben DX', 'Lårben SIN', 'Lårben', 'Scaphoideum DX', 'Scaphoideum SIN', 'Skelettålder', 'Underarm DX', 'Underarm SIN', 'Underben DX', 'Underben SIN', 'Överarm DX', 'Överarm SIN'],
            "MOB3:Mobil röntgenutrustning för bildtagning:Diagnostik:Övrigt": [],
            "MOB4:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning:i samband med kirurgi	Skelett": [],
            "MOB5:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning:i samband med kirurgi	Övrigt": [],
            "BEN1:Bentäthetsmätare:Diagnostik:Inget specifikt": [],
        }
    },
    MODALITY_MG: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "MAM1:Mammografiutrustning (fast installerad):Diagnostik:Bröstkörtlar 2D": ["66000", "66000D", "66000S"],
            "MAM2:Mammografiutrustning (fast installerad):Diagnostik:Bröstkörtlar tomosyntes": [],
            "MAM3:Mammografiutrustning (fast installerad):Diagnostik:Övrigt": [],
            "MAM4:Mammografiutrustning (fast installerad):Screening:Bröstkörtlar 2D": ["66200"],
            "MAM5:Mammografiutrustning (fast installerad):Screening:Bröstkörtlar tomosyntes": [],
        }
    },
    MODALITY_XA: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "INT01:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Huvud och hals": [],
            "INT02:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Thorax inklusive lungor, exklusive hjärta": [],
            "INT03:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Hjärta": [],
            "INT04:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Buk": [],
            "INT05:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Bäcken": [],
            "INT06:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Extremiteter": [],
            "INT07:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Övrig diagnostik": [],
            "INT08:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Huvud och hals": [],
            "INT09:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Thorax inklusive lungor, exklusive hjärta": [],
            "INT10:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Hjärta": [],
            "INT11:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Buk": [],
            "INT12:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Bäcken": [],
            "INT13:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Extremiteter": [],
            "INT14:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Övrig behandling": [],
            "INT15:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Huvud och hals": [],
            "INT16:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Thorax": [],
            "INT17:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Buk": [],
            "INT18:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Ryggraden": [],
            "INT19:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Bäcken, inklusive höfter/höftled": [],
            "INT20:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Extremiteter, inklusive axlar/axelled": [],
            "INT21:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Övrigt": [],
            "INT22:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Huvud och hals": [],
            "INT23:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Thorax": [],
            "INT24:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Buk": [],
            "INT25:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Ryggraden": [],
            "INT26:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Bäcken": [],
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

AGE_SEX_CATEGORY_JUNIOR_MALE = "Pojkar"
AGE_SEX_CATEGORY_JUNIOR_FEMALE = "Flickor"
AGE_SEX_CATEGORY_ADULT_MALE = "Män"
AGE_SEX_CATEGORY_ADULT_FEMALE = "Kvinnor"

OUTPUT_COL_AGE_SEX_CATEGORY = "ageSexCategory"
OUTPUT_COL_EXAM = "Undersökning"
