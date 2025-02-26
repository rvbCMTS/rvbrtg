from pathlib import Path

from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
VALID_STUDY_COLUMNS = StudyColumn()
VALID_SERIES_COLUMNS = SeriesColumn()

CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"

TOKEN_URI = "https://rembox.jll.jllad.se/dpqaauth/connect/token"
API_URI = "https://rembox.jll.jllad.se/api"
ORIGIN_URI = "https://rembox.jll.jllad.se"

MODALITY_CT: str = "CT"
MODALITY_DX: str = "DX"
MODALITY_MG: str = "MG"
MODALITY_XA: str = "XA"


REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_CT,
#    MODALITY_DX,
#    MODALITY_MG,
#    MODALITY_XA
]

COLUMN_SELECTION_PER_MODALITY = {
    MODALITY_CT: [
            VALID_STUDY_COLUMNS.Hospital,
            VALID_STUDY_COLUMNS.StudyDateTime,
            VALID_STUDY_COLUMNS.Machine,
            VALID_STUDY_COLUMNS.StudyDescription,
            VALID_STUDY_COLUMNS.PatientAge,
            VALID_STUDY_COLUMNS.PatientsWeight,
            VALID_STUDY_COLUMNS.PatientsWeightDate,
            VALID_STUDY_COLUMNS.PatientsWeightSource,
            VALID_STUDY_COLUMNS.TotalNumberOfIrradiationEvents,
            VALID_STUDY_COLUMNS.PatientDbId,
            VALID_STUDY_COLUMNS.DlpTotal,
            VALID_STUDY_COLUMNS.PatientsSex,
            VALID_STUDY_COLUMNS.PatientsSize,
            VALID_STUDY_COLUMNS.PatientsSizeDate,
            VALID_STUDY_COLUMNS.PatientsSizeSource,
            VALID_STUDY_COLUMNS.ProcedureCode,
            VALID_SERIES_COLUMNS.MeanCTDIvol,
            VALID_SERIES_COLUMNS.kVp,
            VALID_SERIES_COLUMNS.AcquisitionProtocol,
            VALID_SERIES_COLUMNS.DlPv,
            VALID_SERIES_COLUMNS.SizeSpecificDoseEstimation,
    ],
}

MODALITY_FILTER_SELECTION_PER_MODALITY = {
    MODALITY_CT: ["CT"],
    MODALITY_DX: ["DX", "XASTAT", "XAMOB"],
    MODALITY_MG: ["MG"],
    MODALITY_XA: ["XASTAT", "XAMOB"]
}


REPORT_TEMPLATE_PATH_PER_MODALITY = {
    MODALITY_CT: Path(__file__).parent / "ReportTemplates/CT Mall DsnRegistrering.xlsx",
}

EXAM_GROUPING_TYPE_STUDY_DESCRIPTION = "Study Description"
EXAM_GROUPING_TYPE_PROTOCOL_CODE = "Protocol Code"
EXAM_GROUPING_TYPE_PROCEDURE_CODE = "Procedure Code"
EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL = "Acquisition protocol"

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
        EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL: {}
    },
    MODALITY_XA: {
        EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL: {}
    },
    MODALITY_MG: {
        EXAM_GROUPING_TYPE_ACQUISITION_PROTOCOL: {}
    },
}

OUTPUT_COL_EXAM = "Undersökning"
