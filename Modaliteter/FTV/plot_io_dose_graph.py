import numpy as np
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots


def plot_io_dose_graph(dp, kvs=('60kv', '70kv')):

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
        for kv in kvs:
            data[lab][date][kv] = dict()
            meas = pd.read_excel(item, sheet_name=kv)

            for param in ("exposure_time_ms", "dose_mGy"):
                data[lab][date][kv][param] = np.array(meas[param])

    for lab in data:
        for date in data[lab]:
            for kv in kvs:
                for param in ("exposure_time_ms", "dose_mGy"):
                    nanmask = np.isnan(data[lab][date][kv][param])
                    data[lab][date][kv][param] = data[lab][date][kv][param][~nanmask]


    import plotly.graph_objects as go


    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("60 kV", "70 kV"),
        shared_xaxes=False
    )

    for lab in data:
        for date in data[lab]:

            # --- 60 kV ---
            fig.add_trace(
                go.Scatter(
                    x=data[lab][date]["60kv"]["exposure_time_ms"],
                    y=data[lab][date]["60kv"]["dose_mGy"],
                    mode="lines+markers",
                    line=dict(dash="dash"),
                    marker=dict(size=6),
                    name=f"{lab}, {date} (60 kV)"
                ),
                row=1, col=1
            )

            # --- 70 kV ---
            fig.add_trace(
                go.Scatter(
                    x=data[lab][date]["70kv"]["exposure_time_ms"],
                    y=data[lab][date]["70kv"]["dose_mGy"],
                    mode="lines+markers",
                    line=dict(dash="dash"),
                    marker=dict(size=6),
                    name=f"{lab}, {date} (70 kV)"
                ),
                row=1, col=2
            )

    # Layout
    fig.update_layout(
        height=800,
        xaxis_title="Exposure time (ms)",
        yaxis_title="Dose (mGy)",
        template="plotly_white",
        legend_title="Measurement"
    )

    fig.show()


# enter path
dp = Path("")
plot_io_dose_graph(dp=dp)
