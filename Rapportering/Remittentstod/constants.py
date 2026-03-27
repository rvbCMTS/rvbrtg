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

MG_COL_EXAM_INDEX = "ExamIndex"
MG_COL_PROJECTION = "Projection"
MG_COL_EXAM_TYPE = "ExamType"

MG_PROJ_LMLO = "LMLO"
MG_PROJ_RMLO = "RMLO"
MG_PROJ_LML = "LML"
MG_PROJ_RML = "RML"
MG_PROJ_LCC = "LCC"
MG_PROJ_RCC = "RCC"

MG_COMPRESSION_THICKNESS_RANGE = (40, 60)
MG_SERIES_COUNT_FILTER = 4

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_DX
]

COLUMN_SELECTION_GENERAL = [
    VALID_STUDY_COLUMNS.Hospital,
    VALID_STUDY_COLUMNS.StudyDateTime,
    VALID_STUDY_COLUMNS.Machine,
    VALID_STUDY_COLUMNS.StudyDescription,
    VALID_STUDY_COLUMNS.PatientAge,
    VALID_STUDY_COLUMNS.PatientAgeUnit,
    VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
    VALID_STUDY_COLUMNS.PatientDbId,
    VALID_STUDY_COLUMNS.PatientsSex,
    VALID_STUDY_COLUMNS.ProcedureCode,
]

COLUMN_SELECTION_PER_MODALITY = {
    MODALITY_CT: COLUMN_SELECTION_GENERAL + [
            VALID_STUDY_COLUMNS.DlpTotal,  
            VALID_SERIES_COLUMNS.MeanCTDIvol,
            VALID_SERIES_COLUMNS.kVp,       
            VALID_SERIES_COLUMNS.DlPv,
            VALID_SERIES_COLUMNS.SizeSpecificDoseEstimation,
            VALID_SERIES_COLUMNS.AcquisitionProtocol,
    ],
    MODALITY_XA: COLUMN_SELECTION_GENERAL + [
            VALID_STUDY_COLUMNS.FluoroDoseAreaProductTotal,
            VALID_STUDY_COLUMNS.FluoroDoseRPTotal,
            VALID_STUDY_COLUMNS.TotalFluoroTime,
            VALID_STUDY_COLUMNS.DoseAreaProductTotal,
            VALID_STUDY_COLUMNS.AcquisitionDoseAreaProductTotal,
            VALID_STUDY_COLUMNS.AcquisitionDoseRPTotal,
            VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents, #Antal pedaltramp (ej irradiation events) av typen "Stationary Acquisition"
    ],
    MODALITY_DX: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.TotalNumberOfRadiographicFrames,
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
    ],
    MODALITY_MG: [
        VALID_STUDY_COLUMNS.Hospital,
        VALID_STUDY_COLUMNS.StudyDateTime,
        VALID_STUDY_COLUMNS.Machine,
        VALID_STUDY_COLUMNS.StudyDescription,
        VALID_STUDY_COLUMNS.PatientAge,
        VALID_STUDY_COLUMNS.PatientAgeUnit,
        VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
        VALID_STUDY_COLUMNS.PatientDbId,
        VALID_STUDY_COLUMNS.PatientsSex,
        VALID_STUDY_COLUMNS.ProcedureCode,
        VALID_SERIES_COLUMNS.kVp,
        VALID_SERIES_COLUMNS.CompressionForce,
        VALID_SERIES_COLUMNS.CompressionThickness,
        VALID_SERIES_COLUMNS.PositionerPrimaryAngle,
        VALID_SERIES_COLUMNS.PositionerSecondaryAngle,
        VALID_SERIES_COLUMNS.Exposure,
        VALID_SERIES_COLUMNS.Laterality,
        VALID_SERIES_COLUMNS.AverageGlandularDose,
        VALID_SERIES_COLUMNS.AnodeTargetMaterial,
        VALID_SERIES_COLUMNS.XrayFilterMaterial
    ]
}

MODALITY_FILTER_SELECTION_PER_MODALITY = {
    MODALITY_CT: ["CT"],
    MODALITY_DX: ["DX"],
    MODALITY_MG: ["MG"],
    MODALITY_XA: ["XASTAT", "XAMOB"],
}


EXAM_GROUPING_TYPE_STUDY_DESCRIPTION = "Study Description"
EXAM_GROUPING_TYPE_PROTOCOL_CODE = "Protocol Code"
EXAM_GROUPING_TYPE_PROCEDURE_CODE = "Procedure Code"
EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL = "Acquisition protocol"

CHILD_EXAM_PREFIX = "Barn-"

EXAM_GROUPING_RULES_BY_MODALITY = {
    MODALITY_CT: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {},
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {},
        EXAM_GROUPING_TYPE_PROTOCOL_CODE: {},
        EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL: {
            # Hjärna utan kontrast
            "CT hjärna": ["1.1 1.1 Hjärna"],
            # Halsrygg
            "CT halsrygg": ["3.2 3.2 Halsrygg Fraktur"],
            # Thorax med kontrast
            "CT thorax": ["5.2 5.2 Torax"],
            # Buk med kontrast
            "CT buk": ["6.2 6.2 Buk"],
            # Urinvägar
            "CT urinvägar": ["6.7 6.7 Urinvägar - stenöversikt"],
            # Urografi
            "CT urografi": ["6.8 6.8.1 Urinvägar 3 faser"],
        }
    },
    MODALITY_DX: {
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {
            "Ansiktsskelett eller del därav": ["Ansiktsskelett"],
            "Armbågsled": ["Armbågsled DX", "Armbågsled SIN", "Arm, barn SIN", "Arm, barn DX"],
            "Axel, ac-led": ["Axel, AC-led DX", "Axel, AC-led SIN"],
            "Benlängdsskillnad": ["Benlängd"],
            "Benvinkelmätning-belastning": ["Benvinkel DX", "Benvinkel SIN"],
            "Bröstryggrad": ["Bröstrygg"],
            "Buköversikt": ["Buköversikt"],
            "Bäcken": ["Bäcken"],
            "Epifarynx/nasofraynx": [], #Skalle sidobild
            "Fot, häl, tår": ["Fot DX", "Fot SIN", "Fot belastad DX", "Fot belastad SIN"],
            "Fotled": ["Fotled DX", "Fotled SIN", "Fotled belastad DX", "Fotled belastad SIN"],
            "Halsryggrad": ["Halsrygg"],
            "Hand": ["Hand DX", "Hand SIN"],
            "Handled": ["Handled DX", "Handled SIN"],
            "Helrygg": ["Helrygg"],
            "Höftled": ["Höftled DX", "Höftled SIN", "Höftleder, barn"],
            "Knäled": ["Knäled DX", "Knäled SIN"],
            "Lungor": ["Lungor", "Lungor, liggande"],
            "Lungor-buköversikt nyfödd": ["Lunga-buk nyfödd"],
            "Lårben": ["Lårben DX", "Lårben SIN", "Ben, barn DX", "Ben, barn SIN"],
            "Ländryggrad": ["Ländrygg"],
            "Nyckelben": ["Nyckelben DX", "Nyckelben SIN"],
            "Protesbäcken": ["Protesbäcken"],
            "Revben": ["Revben"],
            "Sacroiliacaleder": ["Sacroiliacaleder"],
            "Sacrum, coccyx": ["Sacrum, coccyx"],
            "Schaphoideum": ["Scaphoideum DX", "Scaphoideum SIN"],
            "Skalle": ["Skalle"],
            "Skelettåldersbestämning": ["Skelettålder"],
            "Skulderblad": ["Skulderblad DX", "Skulderblad SIN"],
            "Sternoclavikularleder": [], # Prio om till DT.
            "Sternum": ["Sternum"],
            "Tunntarm": ["Tunntarm"],
            "Underarm": ["Underarm DX", "Underarm SIN", "Arm, barn SIN", "Arm, barn DX"],
            "Underben": ["Underben DX", "Underben SIN", "Ben, barn DX", "Ben, barn SIN"],
            "Öra cochlea implantat": ["Öra cochlea DX", "Öra cochlea SIN"],
            "Överarm": ["Överarm DX", "Överarm SIN", "Arm, barn SIN", "Arm, barn DX"],
        },
        # Helkroppsskelett: [] #metodbok säger vilka bilder.
    },
    MODALITY_XA: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "Koronarangiografi": ["37300"],
            "Nefrostomiinläggning": ["59000", "59005"],
            "ERCP": ["E4905", "E4903"],
        }
    },
    MODALITY_MG: {
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "Screening": ["66200"],
            "Klinisk Tomosyntes": ["66061"],
            "Klinisk": ["66000", "66059", "66058"]
        }
    },
}

OUTPUT_COL_EXAM = "Undersökning"
OUTPUT_COL_WEIGTH_CATEGORY = "Viktgrupp"
OUTPUT_COL_AGE_CATEGORY = "Åldersgrupp"
OUTPUT_COL_EFFECTIVE_DOSE = "EffectiveDose"
OUTPUT_COL_BODY_PART = "BodyPart"


# Table 7, B G Wall, R Haylock, J T M Jansen, M C Hillier, D Hart and P C Shrimpton,
# Radiation Risks from Medical X-ray Examinations as a Function of the Age and Sex of the Patient, Health Protection Agency, 2011
# mSv / Gy cm^2
EFFECTIVE_DOSE_PER_UNIT_DAP = {
    "Head": 0.058,
    "Cervical Spine": 0.19,
    "Shoulder": 0.064,
    "Chest": 0.16,
    "Thoracic spine": 0.24,
    "Lumbar spine": 0.22,
    "Abdomen": 0.18,
    "Pelvis": 0.14,
    "Hip": 0.13,
    "Femur": 0.036,
    "Knee": 0.0034,
    "Foot": 0.0032,
}

BODY_PART_GIVEN_STUDY_DESCRIPTION = {
    "Head": ["Öra cochlea DX", "Öra cochlea SIN", "Ansiktsskelett", "Skalle"],
    "Cervical Spine": ["Halsrygg"],
    "Shoulder": ["Nyckelben DX", "Nyckelben SIN", "Axel, AC-led DX", "Axel, AC-led SIN"],
    "Chest": ["Lungor", "Lungor, liggande", "Lunga-buk nyfödd", "Skulderblad DX", "Skulderblad SIN", "Revben", "Sternum"],
    "Thoracic spine": ["Helrygg", "Bröstrygg"],
    "Lumbar spine": ["Ländrygg", "Sacrum, coccyx"],
    "Abdomen": ["Tunntarm", "Buköversikt"],
    "Pelvis": ["Sacroiliacaleder", "Protesbäcken", "Bäcken"],
    "Hip": ["Höftled DX", "Höftled SIN", "Höftleder, barn"],
    "Femur": ["Lårben DX", "Lårben SIN", "Benvinkel DX", "Benvinkel SIN", "Benlängd"],
    "Knee": ["Scaphoideum DX", "Scaphoideum SIN", "Scaphoideum", "Överarm DX", "Överarm SIN",
             "Armbågsled DX", "Armbågsled SIN", "Underarm DX", "Underarm SIN",
             "Knäled DX", "Knäled SIN", "Underben DX", "Underben SIN",
             "Arm, barn SIN", "Arm, barn DX","Ben, barn DX", "Ben, barn SIN"],
    "Foot": ["Handled DX", "Handled SIN", "Hand DX", "Hand SIN", "Fotled DX", "Fotled SIN",
             "Fotled belastad DX", "Fotled belastad SIN", "Skelettålder", "Fot DX", "Fot SIN", "Fot belastad DX", "Fot belastad SIN"],
}

# years : cm
PATIENT_SIZE_PER_AGE = {
    1: 76,
    2: 88,
    3: 96,
    4: 104,
    5: 112,
    6: 118,
    7: 124,
    8: 130,
    9: 136,
    10: 140,
    11: 146,
    12: 152,
    13: 160,
    14: 166,
    15: 172,
}
