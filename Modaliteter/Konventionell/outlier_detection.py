import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"
from rembox_integration_tools import REMboxDataQuery
from rembox_integration_tools.rembox_analysis import StudyColumn, SeriesColumn
from typing import Dict, List
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"
TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

rembox = REMboxDataQuery(
    client_id_environment_variable=CLIENT_ID_ENV_VAR,
    client_secret_environment_variable=CLIENT_PWD_ENV_VAR,
    token_uri=TOKEN_URI,
    api_uri=API_URI,
    origin_uri=ORIGIN_URI,
    verify_ssl_cert=False
)


def get_data_from_REMbox(rembox: REMboxDataQuery,
                         procedures: List[str],
                         protocol: str,
                         study_descriptions: List[str]) -> pd.DataFrame:
    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()

    rembox.reset_filter_options()

    rembox.filter_options.set_inclusive_tags(machine_types=['DX'])

    if procedures:
        rembox.filter_options.set_inclusive_tags(procedures=procedures)

    if study_descriptions:
        rembox.filter_options.set_inclusive_tags(study_descriptions=study_descriptions)

    if protocol:
        rembox.filter_options.set_inclusive_tags(acquisition_protocols=protocol)
    

    # 2025 time period
    rembox.filter_options.study_time_interval_start_date = "2025-01-01T00:00:00Z"
    rembox.filter_options.study_time_interval_end_date = "2025-12-31T00:00:00Z"


    # Only with patient age data
    rembox.filter_options.patient_age_interval_include_nulls = False

    # Include patient without weight data
    rembox.filter_options.patient_weight_in_kilograms_include_nulls = True

    rembox.add_columns(
        columns=[
            valid_study_columns.StudyDateTime,
            valid_study_columns.StudyInstanceUID,
            valid_study_columns.AccessionNumber,
            valid_study_columns.StudyId,
            valid_study_columns.Machine,
            valid_study_columns.StudyDescription,
            valid_study_columns.PatientAge,
            valid_study_columns.PatientsWeight,
            valid_study_columns.PatientsWeightDate,
            valid_study_columns.PatientsSize,
            valid_study_columns.DoseAreaProductTotal,
            valid_series_columns.AcquisitionProtocol,
            valid_series_columns.DoseAreaProduct,
            valid_series_columns.ExposureIndex,
            valid_series_columns.kVp,
            valid_series_columns.DistanceSourceToDetector,
            valid_series_columns.XrayFilterThicknessMaximum,
            valid_series_columns.Exposure,
            valid_series_columns.ExposureTime,
            valid_series_columns.CollimatedFieldArea,
            valid_series_columns.CollimatedFieldHeight,
            valid_series_columns.CollimatedFieldWidth,
            valid_series_columns.XrayGridFocalDistance,
        ]
    )
    study_data, series_data = rembox.run_query()

    # Merge study and series
    data = series_data.merge(study_data, on=['studyInstanceUID'], how="left")

    # add system
    def _system_name(row):
         rax = ['L2', 'S01', 'S02', 'U204', 'U207', 'U208']
         ysio = ['LVILM', 'LTARNA', 'L4', 'S04', 'U205', 'U206']
         mira = ['L10', 'S12', 'U220', 'U221', 'U222']
         if row['machine'] in rax:
             val = 'Multitom Rax'
         elif row['machine'] in ysio:
             val = 'Ysio Max'
         elif row['machine'] in mira:
             val = 'Mira Max'
         else:
             val = ""

         return val

    data['system'] = data.apply(_system_name, axis=1)


    return data





def evaluate():
    valid_study_columns = StudyColumn()
    valid_series_columns = SeriesColumn()
    chest = get_data_from_REMbox(rembox=rembox,
                                procedures=[],
                                protocol=[],
                                study_descriptions=["Lungor"])
    
    # TODO: Hur kan man inkludera ej komplett data så som längd och vikt.

    # TODO: Lägga till en scroring på hur avvikande värdet är

    # TODO: Lägga till förklaring till varför avvikande värde.

    # TODO: Undersök om det är bäst att göra per undersökning eller per bild? Förmodligen är båda bra.
    # För undersökning, skapa featues som är aggregerade över alla bilder i undersökningen.
    

    continuous_features = [valid_study_columns.PatientAge,
                valid_series_columns.DistanceSourceToDetector,
                valid_series_columns.XrayFilterThicknessMaximum,
                valid_series_columns.Exposure,
                valid_series_columns.ExposureTime,
                valid_series_columns.DoseAreaProduct,
                valid_series_columns.kVp,
                valid_series_columns.ExposureIndex,
                ]
    categorical_features = [valid_study_columns.Machine,
                valid_series_columns.AcquisitionProtocol]

    data = chest[continuous_features + categorical_features]
    data = data.dropna()

    data = data[(data[valid_series_columns.DoseAreaProduct] > 0) & (data[valid_study_columns.PatientAge] <150)]


    # Continus data: Scale data for zero mean and unit variance
    scaler = preprocessing.StandardScaler().fit(data[continuous_features].values)
    data_continous_scaled = scaler.fit_transform(data[continuous_features].values)

    # Categorical data: One-hot encode categorical features
    encoder = preprocessing.OneHotEncoder(min_frequency=round(0.01 * len(data)), sparse_output=False).fit(data[categorical_features].values)
    data_categorical_encoded = encoder.transform(data[categorical_features].values)

    # Merge continous and categorical data
    data_preprocessed = pd.concat([pd.DataFrame(data_continous_scaled), pd.DataFrame(data_categorical_encoded)], axis=1)

   
    # Local Outlier Factor and Isolation Forest are two popular algorithms for outlier detection.
    forest = IsolationForest(random_state=42, contamination=0.001).fit(data_preprocessed)
    local_outlier_factor = LocalOutlierFactor(n_neighbors=20, contamination=0.005).fit(data_preprocessed)
    # prediction = forest.predict(data_preprocessed)
    prediction = local_outlier_factor.fit_predict(data_preprocessed)
    data = data.assign(outlier=prediction)

    # Colors based on prediction
    colors = ['red' if pred == -1 else 'blue' for pred in prediction]

    # Create hover text for each point
    hover_text = data.apply(lambda row: '<br>'.join([f"{col}: {row[col]}" for col in continuous_features + categorical_features]), axis=1).to_list()

    
    # Skapa subplots: 1 row, 2 columns
    fig = make_subplots(
        rows=2, cols=4,
    )

    # --- Plot 1: Exposure vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.Exposure],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="Exposure vs DAP",
            text=hover_text,
        ),
        row=1, col=1
    )

    # --- Plot 2: Age vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_study_columns.PatientAge],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="Age vs DAP",
            text=hover_text,
        ),
        row=1, col=2
    )

    # --- Plot 3: Distance vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.DistanceSourceToDetector],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="Distance vs DAP",
            text=hover_text,
        ),
        row=1, col=3
    )

    # --- Plot 4: Filter vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.XrayFilterThicknessMaximum],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="Filter vs DAP",
            text=hover_text,
        ),
        row=1, col=4
    )

    # --- Plot 5: Exposure time vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.ExposureTime],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="Exposure time vs DAP",
            text=hover_text,
        ),
        row=2, col=1
    )

    # --- Plot 6: kvp time vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.kVp],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="kvp time vs DAP",
            text=hover_text,
        ),
        row=2, col=2
    )

    # --- Plot 6: EI time vs DAP ---
    fig.add_trace(
        go.Scatter(
            x=data[valid_series_columns.ExposureIndex],
            y=data[valid_series_columns.DoseAreaProduct],
            mode="markers",
            marker=dict(color=colors, size=6),
            name="EI time vs DAP",
            text=hover_text,
        ),
        row=2, col=3
    )

    

    # Layout-inställningar
    fig.update_layout(
        xaxis=dict(title='Exposure'),
        yaxis=dict(title='DoseAreaProduct'),
        xaxis2=dict(title='PatientAge'),  
        yaxis2=dict(title='DoseAreaProduct'),
        xaxis3=dict(title='DistanceSourceToDetector'),  
        yaxis3=dict(title='DoseAreaProduct'),
        xaxis4=dict(title='MaximumXrayFilterThickness'),  
        yaxis4=dict(title='DoseAreaProduct'),
        xaxis5=dict(title='ExposureTime'),  
        yaxis5=dict(title='DoseAreaProduct'),
        xaxis6=dict(title='kVp'),  
        yaxis6=dict(title='DoseAreaProduct'),
        xaxis7=dict(title='ExposureIndex'),  
        yaxis7=dict(title='DoseAreaProduct'),
        title="Outliers i originalskalor",
    )
    fig.show()



if __name__ == '__main__':
    evaluate()
