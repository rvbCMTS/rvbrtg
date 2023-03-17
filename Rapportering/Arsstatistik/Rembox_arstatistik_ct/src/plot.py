import plotly.express as px


def dose_rp_total_above(study_data, dose):

    # Filtrera fram alla ingrepp där doseRPTotal överstiger 5 Gy

    study_data_dlp_high = study_data[study_data.dlpTotal > dose]

    # Kika på innehåll i dataframe
    # study_data_DLP_high

    fig = px.scatter(
        study_data_dlp_high,
        study_data_dlp_high.studyDateTime,
        study_data_dlp_high.dlpTotal,
        title="DLP over 5 000 mGycm")

    return fig

