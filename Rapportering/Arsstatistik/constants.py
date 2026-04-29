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
MODALITY_DCBCT: str = "DCBCT",
MODALITY_NUK: str = "NUK"

REPORT_OUTPUT_DIR: Path = Path(__file__).parent / "Reports"

MODALITY_LIST = [
    MODALITY_CT
    MODALITY_DX,
    MODALITY_MG,
    MODALITY_XA
]

MISC_CATEGORY_GROUP_CT = "DT10:Datortomograf (fast installerad eller mobil):Diagnostik:Övrig diagnostik"
MISC_CATEGORY_GROUP_STATIONARY_DX = "RTG08:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övrig diagnostik"
MISC_CATEGORY_GROUP_MOBILE_DX_VAL = "MOB1:Mobil röntgenutrustning för bildtagning:Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg"
MISC_CATEGORY_GROUP_MOBILE_DX_REF = "RTG02:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg"
MISC_CATEGORY_GROUP_MOBILE_DX_REF2 = "RTG06:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled"
MISC_CATEGORY_GROUP_MOBILE_DX_VAL2 = "MOB2:Mobil röntgenutrustning för bildtagning:Diagnostik:Extremiteter, inklusive axlar/axelled"
MISC_CATEGORY_GROUP_MOBILE_DX_REF3 = MISC_CATEGORY_GROUP_STATIONARY_DX
MISC_CATEGORY_GROUP_MOBILE_DX_VAL3 = "MOB3:Mobil röntgenutrustning för bildtagning:Diagnostik:Övrigt"
MISC_CATEGORY_GROUP_MG = "MAM3:Mammografiutrustning (fast installerad):Diagnostik:Övrigt"
MISC_CATEGORY_GROUP_MOBILE_XA = "MOB5:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning i samband med kirurgi:Övrigt"
MISC_CATEGORY_GROUP_STATIONARY_XA_DIAGNOSTIC = "INT21:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Övrigt"
MISC_CATEGORY_GROUP_STATIONARY_XA_TREATMENT = "INT14:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Övrig behandling"

COLUMN_SELECTION_GENERAL = [
    VALID_STUDY_COLUMNS.Hospital,
    VALID_STUDY_COLUMNS.StudyDateTime,
    VALID_STUDY_COLUMNS.StudyInstanceUID,
    VALID_STUDY_COLUMNS.StudyId,
    VALID_STUDY_COLUMNS.Machine,
    VALID_STUDY_COLUMNS.StudyDescription,
    VALID_STUDY_COLUMNS.AccessionNumber,
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
    ],
    MODALITY_DX: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.DoseAreaProductTotal,
    ],
    MODALITY_MG: COLUMN_SELECTION_GENERAL + [
        VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseBothBreasts,
        VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseLeftBreast,
        VALID_STUDY_COLUMNS.AccumulatedAverageGlandularDoseRightBreast
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
    MODALITY_NUK: ["SPECT/CT", "PET/CT"]
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
            ####################### Diagnostik ##########################
            "DT01:Datortomograf (fast installerad eller mobil):Diagnostik:Huvud och hals": [
                "80100", "80101", "80105", "80180", "80181", "801D1", "801HH", # spottkörtlar
                "80300", "80301", "80305", "80380", "80381", "803HH", # munbotten
                "80400", "80401", "804HH", # Tandimplantat
                "80800", "80801", "80805", "80880", "80881", "808HH", # Perfusion hjärna
                "81000", "81001", "81003", "81005", "81070", "81071", "81080", "81081", "81087", "81097", "810D0",
                "810E0", "810E1", "810HH", "810M0", "810RH", "810RM", # DT hjärna
                "81100", "81101", "811HH", # DT hjärna + cistern
                "81200", "81201", "81205", "81280", "81281", "812HH", #DT orbita
                "81500", "81501", "81505", "81550", "81580", "81581", "815HH2", "815KK", "815SS", # skalle/sinus/ansikte
                "81600", "81601", "81605", "81680", "81681", "816HH", # Temporalben
                "81700", "81701", "81705", "81780", "81781", "817HH", # DT käkleder
                "81800", "81801", "81805", "81850", "81880", "81881", "818D1", "818HH", # DT hals/larynx/thyr
                "81900", "81901", "81968", "81969", # DT esofagus
                "87500", "87501", "87580", "87581", "875A1", "875A2", "875C1", "875C2", "875R2", "875V1", "875V2", # DT angio
            ],
            "DT02:Datortomograf (fast installerad eller mobil):Diagnostik:Thorax inkl lunga/hjärta/bröstkorg": [
                "83000", "83000F", "83001", "83005", "83050", "83067", "83068", "83069", "83070", "83071", "83079",
                "83080", "83081", "830D1", "830E0", "830E1", "830HH", # DT thorax
                "83100", "83101", "83105", "83116", "83180", "83181", "83184", "83185", "831HH", # DT hjärta
                "83201", "832HH", # DT lungor
                "83300", "83301", "83380", "83384", "833HH", # DT aorta thorakalangio
                "83600", "83601", "83605", "83680", "83681", "836HH", #DT thorax-hals
                "86100", "86101", "86105", "86150", "86181", # DT sternum
                "87601", "87680", "876D1", "876E1", # DT pulm angio
                "87700", "87701", "87716", "87755", "87763", "87780", "87781", "87783", "87785", # DT aorta angio
                "87800", "87801", "87805", "87880", "87881", # DT lungvener
                "87900", "87901", "87980", "87981", # DT aorta-pulm angio
                "89500", "89501", "89516", "89580", "89581", "89584", "89585", "895CS" # DT kranskärl
            ],
            "DT03:Datortomograf (fast installerad eller mobil):Diagnostik:Buk": [
                "84000", "84001", "84005", "84050", "84063", "84068", "84069", "84070", "84071", "84075", "84080",
                "84081", "84095", "840D1", "840D3", "840D4", "840E0", "840E1", "840HH", # DT buk
                "84100", "84101", "8405", "84150", "84168", "84169", "84179", "84180", "84181", "841HH", # DT övre buken
                "84300", "84301", "84305", "84350", "84363", "84380", "84381", # DT pancreas
                "84400", "84401", "84405", "84450", "84463", "84464", "84480", "84481", # DT lever
                "85100", "85101", "85163", "85180", #DT bukangio småkärl
                "84700", "84701", "84705", "84780", "84781", # DT colon
                "84800", "84801", "84880", "84881", "848D0", # DT urinvägsöversikt
                "85200", "85201", "85205", "85250", "85263", "85264", "85280", "85281", # DT njurar
                "85300", "85305", "85350", "85380", "85381", # DT binjurar
                "85400", "85401", "85405", "85463", "85464", "85480", "85481", # DT urografi
                "85500", "85501", "85505", "85550", "85568", "85569", "85580", "85581", # DT nedre buk/lilla bäckenet

            ],
            "DT05:Datortomograf (fast installerad eller mobil):Diagnostik:Bäcken, höfter": [
                "82600", "82601", "82605", "82649", "82650", "82680", "82681", "826HH" # DT sacrum
                "82800", "82801", "82805", "82850", "82880", "82881", "828D0", "828HH",  # DT sacroiliaceleder
                "82900", "82901", "82903", "82905", "82939", "82950", "82980", "82981", #DT bäcken/höftled
                "88900", "88901", # DT bäckenmätning
            ],
            "DT06:Datortomograf (fast installerad eller mobil):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled": [
                "86200", "86201", "86205", "86250", "86250", "86280", "86281", "86288", #DT axelled
                "86300", "86301", "86305", "86350", "86380", "86381", # DT överarm
                "86400", "86401", "86405", "86450", "86480", "86481", # DT armbåde
                "86500", "86501", "86505", "86550", "86580", "86581", # DT underarm
                "86600", "86601", "86605", "86650", "86680", "86681", # DT handled
                "86700", "86701", "86705", "86750", "86780", "86781", # DT hand
                "86800", "86801", "86805", "86850", "86880", "86881", # DT lårben
                "86900", "86901", "86905", "86939", "86950", "86980", "86981" # DT knäled
                "87000", "87001", "87005", "87050", "87080", "87081", # DT underben
                "87100", "87101", "87105", "87150", "87180", "897181", # DT fotled
                "87200", "87201", "87205", "87250", "87280", "87281", # DT fot
                "87300", "87301", "87305", "87350", "87380", "87381", # DT extremiteter
                "87400", "87401", # DT scaphoideum
            ],
            "DT07:Datortomograf (fast installerad eller mobil):Diagnostik:Ryggraden": [
                "82000", "82001", "82003", "82005", "82049", "82050", "82080", "82081", "820D0", "820HH", "820M0",  # DT halsryggrad
                "82200", "82201", "82203", "82205", "82249", "82250", "82280", "82281", "822D0", "822HH", #bröstryggrad
                "82300", "82301", "82303", "82380", "82381", "82381", "823D0", "823D0", "823HH", # Bröst-ländrygg
                "82400", "82401", "82403", "82405", "82449", "82450", "82480", "82481", "82488", "824D0", "824HH" # DT ländryggrad
            ],
            "DT08:Datortomograf (fast installerad eller mobil):Diagnostik:Hela bålen (inkl. thorax-buk kombination)": [
                "83500", "83501", "83505", "83575", "83580", "83581", "835D1", "835D3", "835HH", # DT hals-thorax-buk"
                "83800", "83801", "83805", "83863", "83869", "83871", "83871", "83875", "83878", "83880", "83881",
                "838D1", "838D3", "838D4", "838E0", "838E1", "838M1", # Thorax-buk
                "83900", "83901", "83980", "83981", "839HH", # Thorax - övre buk
                "85600", "85601", "85663", "85664", # DT thorax-urografi
                "85900", "85901", "85980", "85981", # DT aorta bukangio
            ],
            "DT09:Datortomograf (fast installerad eller mobil):Diagnostik:Hela kroppen (multitrauma)": [
                "88001", "88080", # DT multitrauma
                "89100", "89101", # helkropp lågdos
                "89200", "89201", # DT myelomskelett
            ],
            "DT10:Datortomograf (fast installerad eller mobil):Diagnostik:Övrig diagnostik": [

            ],
            ####################### Behandling ##########################
            "DT11:Datortomograf (fast installerad eller mobil):Behandling:Huvud och hals": [],
            "DT12:Datortomograf (fast installerad eller mobil):Behandling:Thorax inkl lunga/hjärta/bröstkorg": [],
            "DT13:Datortomograf (fast installerad eller mobil):Behandling:Övrigt": [],
        }
    },
    MODALITY_DX: {
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {
            "RTG01:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Huvud och hals": ['Ansiktsskelett', 'Shuntkontroll', 'Shuntöversikt', 'Skalle', "Öra cochlea DX", "Öra cochlea SIN"],
            "RTG02:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": ['Lungor', 'Lungor, liggande', "Sternum", "Skulderblad DX", "Skulderblad SIN", "Revben"],
            "RTG03:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Buk": ['Buköversikt', 'Lunga-buk nyfödd', 'Tunntarm'],
            "RTG05:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Bäcken höfter": ['Bäcken', 'Protesbäcken', 'Höftleder, barn', 'Höft stereo DX', 'Höft stereo SIN', 'Höftled DX', 'Höftled SIN', "Sacroiliacaleder"],
            "RTG06:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Extremitetsskelett,  inklusive axlar/axelled": ['Axel, AC-led DX', 'Axel, AC-led SIN', 'Armbågsled DX', 'Armbågsled SIN', 'Armbågsled',
                                                                                                                                    'Benlängd', 'Benvinkel DX', 'Benvinkel SIN', 'Fot DX', 'Fot SIN', 'Fot',
                                                                                                                                    'Fot belastad DX', 'Fot belastad SIN', 'Fotled DX', 'Fotled SIN', 'Fotled belastad DX', 'Fotled belastad SIN',
                                                                                                                                    'Hand DX', 'Hand SIN', 'Handled DX', 'Handled SIN', 'Knäled DX', 'Knäled SIN', 'Knäled', 'Lårben DX', 'Lårben SIN',
                                                                                                                                    'Lårben', 'Scaphoideum DX', 'Nyckelben DX', 'Nyckelben SIN', 'Scaphoideum SIN', 'Skelettålder',
                                                                                                                                    'Underarm DX', 'Underarm SIN', 'Underben DX', 'Underben SIN', 'Överarm DX', 'Överarm SIN'],
            "RTG07:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Ryggraden": ["Bröstrygg", 'Halsrygg', 'Helrygg', 'Ländrygg', "Sacrum, coccyx"],
            "RTG08:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övrig diagnostik": [],
            "MOB1:Mobil röntgenutrustning för bildtagning:Diagnostik:Thorax inkl lunga/hjärta, Bröstkorg": [],
            "MOB2:Mobil röntgenutrustning för bildtagning:Diagnostik:Extremiteter, inklusive axlar/axelled": [],
            "MOB3:Mobil röntgenutrustning för bildtagning:Diagnostik:Övrigt": [],
            "MOB4:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning i samband med kirurgi:Skelett": ['Ortopedi'],
            "BEN1:Bentäthetsmätare:Diagnostik:Inget specifikt": [],
        },
        EXAM_GROUPING_TYPE_PROCEDURE_CODE: {
            "MOB4:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning i samband med kirurgi:Skelett": ["X621", "X622", "X623", "X626", "X630", "X631", "X633", "X634", 
                                                                                                                      "X643", "X636", "X637", "X638", "X639", "X641", "X642",
                                                                                                                      "X642", "X645", "X646", "X648"],
            "MOB5:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning i samband med kirurgi:Övrigt": [],
        }
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
        EXAM_GROUPING_TYPE_STUDY_DESCRIPTION: {
           "INT10:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Hjärta": ["Biosense Carto EP", "Implantat - externt bokad", 
                                                                                                                      "Lungvensablation - externt bokad", "Ordinär ablation - externt bokad"],
        },
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
            "INT09:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Thorax inklusive lungor, exklusive hjärta": ["39900", "39948", "39951", "3995A"],
            "INT10:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Hjärta": ["32700", "32800", "33000", "33100", "33500", "36000", "36600",
                                                                                                                       "37728", "37300", "38400", "38500", "39100", "39500", "X401", "X402"],
            "INT11:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Buk": ["47100", "47142", "47148", "47200", "47242", "47900", "49500", 
                                                                                                                    "49900", "49905", "49948", "49951", "59500", "59600", "59748", 
                                                                                                                    "59800", "59900"],
            "INT12:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Bäcken": ["57000", "57042", "57400"],
            "INT13:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Extremiteter": ["67600", "67672", "67700", "67772", "67800", "67500"],
            "INT14:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Övrig behandling": [],
            "INT15:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Huvud och hals": ["10100", "10500", "10528", "10555", "41100", 
                                                                                                                                      "41127", "41200", "4124B", "41327",  ],
            "INT16:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Thorax": ["32000", "32028", "32500", "41600", "42000", ],
            "INT17:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Buk": ["45400", "43000", "43200", "44000", "44900", "45000", 
                                                                                                                           "46128",],
            "INT18:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Ryggraden": [],
            "INT19:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Bäcken, inklusive höfter/höftled": ["44000", "63935", "64000"],
            "INT20:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Extremiteter, inklusive axlar/axelled": ["63135"],
            "INT21:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Övrigt": [],
            "INT22:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Huvud och hals": [],
            "INT23:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Thorax": ["39051", "39348", "39900", "48451", "48452", "48455", 
                                                                                                                              "4845A", "48551", "48552", "4855A"],
            "INT24:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Buk": ["42051", "46028", "46051", "46052", "46055", "46136", "46151",
                                                                                                                           "46152", "46155", "46248", "49000", "49005", "49055", 
                                                                                                                           "49100", "49105", "49148", "49148", "49150", "49155", 
                                                                                                                           "49200", "49205", "49300", "49600", "49928", "49960", "49961", 
                                                                                                                           "58700", "59000", "59005", "59100", "E4976", "E4900", "E4905"],
            "INT25:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Ryggraden": ["13000", "13200", "13400", "13800", "1384A",  "17800", "17805"],
            "INT26:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Bäcken": ["44200","50351", "51200", "51255", "51348", "53000", "53100", "53200"],
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
AGE_SEX_CATEGORY_ADULT_FEMALE = "Kvinnor (16 år och äldre)"
AGE_SEX_CATEGORY_ADULT_MALE = "Män (16 år och äldre)"
AGE_SEX_CATEGORY_ADULT_MALE_16_40 = "Män 16-40"
AGE_SEX_CATEGORY_ADULT_FEMALE_16_40 = "Kvinnor 16-40"
AGE_SEX_CATEGORY_ADULT_MALE_41_65 = "Män 41-65"
AGE_SEX_CATEGORY_ADULT_FEMALE_41_65 = "Kvinnor 41-65"
AGE_SEX_CATEGORY_ADULT_MALE_66plus = "Män 66+"
AGE_SEX_CATEGORY_ADULT_FEMALE_66plus = "Kvinnor 66+"
AGE_SEX_CATEGORY_DOSE_BOY = "Pojkar för dosberäkning"
AGE_SEX_CATEGORY_DOSE_GIRL = "Flickor för dosberäkning"
AGE_SEX_CATEGORY_DOSE_MALE = "Män för dosberäkning"
AGE_SEX_CATEGORY_DOSE_FEMALE = "Kvinnor för dosberäkning"

EXAMS_EXEMPT_FROM_REPORTING_DOSE = [
    "DT10:Datortomograf (fast installerad eller mobil):Diagnostik:Övrig diagnostik",
    "DT13:Datortomograf (fast installerad eller mobil):Behandling:Övrigt",
    "RTG08:Konventionella röntgenutrustningar (fast installerad):Diagnostik:Övrig diagnostik",
    "MOB3:Mobil röntgenutrustning för bildtagning:Diagnostik:Övrigt",
    "MOB5:Mobil röntgenutrustning för genomlysning (C-bågar etc.):Vägledning i samband med kirurgi:Övrigt",
    "MAM3:Mammografiutrustning (fast installerad):Diagnostik:Övrigt",
    "INT03:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Diagnostik:Hjärta",
    "INT14:Genomlysningsutrustning (användning för hjärta och blodkärl, fast installerad):Behandling:Övrig behandling",
    "INT21:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Diagnostik:Övrigt",
    "INT27:Genomlysningsutrustning (övrig användning inte hjärta och blodkärl, fast installerad):Behandling:Extremiteter, inklusive axlar/axelled",
]

OUTPUT_COL_AGE_SEX_CATEGORY = "ageSexCategory"
OUTPUT_COL_AGE_SEX_CATEGORY_DOSE = "ageSexCategoryDose"
OUTPUT_COL_EXAM = "Undersökning"
OUTPUT_KEY_MEAN_DOSE = "dose_mean"
OUTPUT_KEY_MEDIAN_DOSE = "dose_median"
OUTPUT_KEY_Q1_DOSE = "dose_Q1"
OUTPUT_KEY_Q3_DOSE = "dose_Q3"

MODALITY_DX_MACHINE_GENERAL = ["L2", "L4", "LSTORU", "LTARNA", "LVILM", "S01", "S02", "S04", "U220", "U221", "U222"]
MODALITY_DX_MACHINE_MOBILE = ["L10", "S12", "U220", "U221", "U222"]
MODALITY_XA_MACHINE_TREATMENT = ["U104", "U105", "U106", "U601", "U601_2025", "U602", "Arytmi 1", "Arytmi 2"]
MODALITY_XA_MACHINE_DIAGNOSTIC = ["U110", "S08", "L3"]
MODALITY_XA_MACHINE_MOBILE = [
    "L7", "L8", "L12",
    "SX", "S20", "S21", "S23", "S25", "S28",
    "U703", "U704", "U707", "U708", "U711", "U713", "U719", "U720", "U721",
    "U921"
]
