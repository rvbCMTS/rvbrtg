import numpy as np
import pandas as pd
from pathlib import Path


def plot_io_dose_graph(dp):

    data = dict()

    for item in dp.iterdir():
        if item.name[:2] == "~$":
            continue

        lab = item.name.split("_")[1]

        if lab == "LabName":
            continue

        date = item.name.split("_")[2].split(".")[0]

        if lab not in data.keys():
            data[lab] = dict()

        data[lab][date] = dict()
        meas = pd.read_excel(item)

        for param in ("exposure_time_ms", "dose_mGy"):
            data[lab][date][param] = np.array(meas[param])

    for lab in data:
        for date in data[lab]:
            for param in ("exposure_time_ms", "dose_mGy"):
                nanmask = np.isnan(data[lab][date][param])
                data[lab][date][param] = data[lab][date][param][~nanmask]

    import plotly.graph_objects as go

    fig = go.Figure()

    for lab in data:
        for date in data[lab]:
            fig.add_trace(
                go.Scatter(
                    x=data[lab][date]["exposure_time_ms"],
                    y=data[lab][date]["dose_mGy"],
                    mode="lines+markers",  # punkter + linjer
                    line=dict(dash="dash"),  # streckade linjer
                    marker=dict(size=6),
                    name=f"lab: {lab}, date: {date}",
                )
            )

    fig.update_layout(
        xaxis_title="Exposure time (ms)",
        yaxis_title="Dose (mGy)",
        legend_title="Measurement",
        template="plotly_white",
    )

    fig.show()


dp = Path(r"V:\Enhetsytor\5-1-1-3. Strålningsfysik\Radiologi\FTV\Nya sensorer 2022 raw\dosmätningar")

plot_io_dose_graph(dp=dp)
