from pathlib import Path
import pandas as pd

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

COL_MARKER_LINE_WIDTH = "markerLineWidth"

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
#    MODALITY_CT,
    MODALITY_DX
#    MODALITY_MG,
#    MODALITY_XA
]

COLUMN_SELECTION_GENERAL = [
    VALID_STUDY_COLUMNS.Hospital,
    VALID_STUDY_COLUMNS.StudyDateTime,
    VALID_STUDY_COLUMNS.Machine,
    VALID_STUDY_COLUMNS.StudyDescription,
    VALID_STUDY_COLUMNS.PatientAge,
    VALID_STUDY_COLUMNS.PatientAgeUnit,
    VALID_STUDY_COLUMNS.PatientsWeight,
    VALID_STUDY_COLUMNS.PatientsWeightDate,
    VALID_STUDY_COLUMNS.PatientsWeightSource,
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


REPORT_TEMPLATE_PATH_PER_MODALITY = {
    MODALITY_CT: Path(__file__).parent / "ReportTemplates/CT Mall DsnRegistrering.xlsx",
    MODALITY_DX: Path(__file__).parent / "ReportTemplates/RTG DsnRegistrering.xlsx",
    MODALITY_XA: Path(__file__).parent / "ReportTemplates/INT Mall DsnRegistrering.xlsx",
    MODALITY_MG: Path(__file__).parent / "ReportTemplates/MG Mall DsnRegistrering.xlsx",
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
            "Epifarynx/nasofraynx": [],
            "Lungor": ["Lugnor", "Lungor, liggande"],
            "Lungor-buköversikt nyfödd": ["Lunga-buk nyfödd"],
            "Tunntarm": ["Tunntarm"],
            "Buköversikt": ["Buköversikt"],
            "Schaphoideum": ["Schaphoideum DX", "Schaphoideum SIN"],
            "Skalle": [""],
            "Ansiktsskelett eller del därav": [""],
            "Öra cochlea implantat": ["Öra cochlea DX", "Öra cochlea SIN"],
            "Sternum": ["Sternum"],
            "Halsryggrad": ["Halsrygg"],
            "Bröstryggrad": ["Bröstrygg"],
            "Ländryggrad": ["Ländrygg"],
            "Revben": ["Revben"],
            "Sternoclavikularleder": [],
            "Bäcken": ["Bäcken"],
            "Sacroiliacaleder": ["Sacroiliacaleder"],
            "Sacrum, coccyx": ["Sacrum, coccyx"],
            "Helrygg": ["Helrygg"],
            "Nyckelben": ["Nyckelben DX", "Nyckelben SIN"],
            "Axel, ac-led": ["Axel, ac-led DX", "Axel, ac-led SIN"],
            "Skulderblad": ["Skulderblad DX", "Skulderblad SIN"],
            "Överarm": ["Överarm DX", "Överarm SIN"],
            "Armbågsled": ["Armbågsled DX", "Armbågsled SIN"],
            "Underarm": ["Underarm DX", "Underarm SIN"],
            "Handled": ["Handled DX", "Handled SIN"],
            "Hand": ["Hand DX", "Hand SIN"],
            "Höftled": ["Höftled DX", "Höftled SIN"],
            "Lårben": ["Lårben DX", "Lårben SIN"],
            "Knäled": ["Knäled DX", "Knäled SIN"],
            "Protesbäcken": ["Protesbäcken"],
            "Benlängdsskillnad": ["Benlängd"],
            "Benvinkelmätning-belastning": ["Benvinkel DX", "Benvinkel SIN"],
            "Underben": ["Underben DX", "Underben SIN"],
            "Fotled": ["Fotled DX", "Fotled SIN", "Fotled belastad DX", "Fotled belastad SIN"],
            "Skelettåldersbestämning": ["Skelettålder"],
            "Fot, häl, tår": ["Fot DX", "Fot SIN", "Fot belastad DX", "Fot belastad SIN"],
        },
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

WEIGHT_CATEGORY_0_5 = "0-5kg"
WEIGHT_CATEGORY_5_15 = "5-15kg"
WEIGHT_CATEGORY_15_30 = "15-30kg"
WEIGHT_CATEGORY_30_50 = "30-50kg"
WEIGHT_CATEGORY_50_70 = "50-70kg"
WEIGHT_CATEGORY_60_90 = "60-90kg"
AGE_CATEGORY_0_1 = "<1 år"
AGE_CATEGORY_1_6 = "1-<6 år"
AGE_CATEGORY_6_16 = "6-<16 år"

OUTPUT_COL_EXAM = "Undersökning"
OUTPUT_COL_WEIGTH_CATEGORY = "Viktgrupp"
OUTPUT_COL_AGE_CATEGORY = "Åldersgrupp"
OUTPUT_COL_EFFECTIVE_DOSE = "Effektiv dos"


# Table 7, Radiation Risks from Medical X-ray Examinations as a Function of the Age and Sex of the Patient
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
    "Head": ["Öra cochlea DX", "Öra cochlea SIN"],
    "Cervical Spine": ["Halsrygg"],
    "Shoulder": ["Nyckelben DX", "Nyckelben SIN", "Axel, ac-led DX", "Axel, ac-led SIN"],
    "Chest": ["Lugnor", "Lungor, liggande", "Lunga-buk nyfödd", "Skulderblad DX", "Skulderblad SIN"],
    "Thoracic spine": ["Helrygg", "Bröstrygg"],
    "Lumbar spine": ["Ländrygg", "Sacrum, coccyx"],
    "Abdomen": ["Tunntarm", "Buköversikt"],
    "Pelvis": ["Sacroiliacaleder", "Protesbäcken"],
    "Hip": ["Höftled DX", "Höftled SIN"],
    "Femur": ["Lårben DX", "Lårben SIN"],
    "Knee": ["Schaphoideum DX", "Schaphoideum SIN", "Överarm DX", "Överarm SIN",
             "Armbågsled DX", "Armbågsled SIN", "Underarm DX", "Underarm SIN",
             "Knäled DX", "Knäled SIN", "Benlängd", "Benvinkel DX", "Benvinkel SIN", "Underben DX", "Underben SIN"],
    "Foot": ["Handled DX", "Handled SIN", "Hand DX", "Hand SIN", "Fotled DX", "Fotled SIN",
             "Fotled belastad DX", "Fotled belastad SIN", "Skelettålder", "Fot DX", "Fot SIN", "Fot belastad DX", "Fot belastad SIN"],
}
























