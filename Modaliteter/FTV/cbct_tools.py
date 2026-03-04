import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

def translate_column_names_swe_eng(df):
    df = df.rename(columns={
        "Datum": "Date",
        "Tid": "Time",
        "Kön": 'Patient Sex',
        "Modalitet": "Modality",
        "Grader": 'Scan',
        "Exp. Tid": "Scan time",
        "Tänder": "Model Name"
    })

    return df

def remove_unnecessary_columns(df):
    columns_to_drop = [
        'Efternamn',
        'Förnamn',
        'Mellannamn',
        'Gravid',
        'Indikation',
        'Datum för föregående röntgenundersökning',
        'Användare',
        'QA',
        'Exp.läge',
        'Extrafilter',
        'Födelsedatum',
        'CTDIw (mGy)',
        'Kommentar',
        'Modalitet.1',
        'Modalitetens serienummer',
        'Röntgenhuvud serienummer',
        'Röntgenrörsmodell',
        'Röntgenrör serienummer',
        'Röntgenrum'
        ]
    df = df.drop(columns=columns_to_drop)
    return df

def append_mas(df):

    df["mAs"] = df['mA'] * df["Scan time"]
    return df

def parse_scan_column(df):
    df["Scan"] = df["Scan"].str[:-1].astype(int)
    return df

def parse_fov_and_imaging_from_fov_column(df):
    conditions = [
        df["FOV"].str.contains("Std.", case=False, na=False),
        df["FOV"].str.contains("Hi-Spd", case=False, na=False),
        df["FOV"].str.contains("Hi-Res", case=False, na=False),
        df["FOV"].str.contains("Hi-Fi", case=False, na=False),
    ]
    df["Imaging"] = np.select(conditions, ["Std", "Hi-Speed", "Hi-Res", "Hi-Fi"], default="no match")
    df["FOV"] = [item.split()[0] for item in df["FOV"]]
    return df

def parse_patient_age_from_id(df):
    birth_date = pd.to_datetime(
        df["Id"]
            .astype(str)
            .str.slice(0, 8),
        format="%Y%m%d",
        errors="coerce"
    )
    df["Patient age"] = ((df["DateTime"] - birth_date).dt.days / 365.25).round(0)

    return df

def parse_datetime(df, sort_by_datetime=True):
    date = pd.to_datetime(df["Date"], format="%Y%m%d")
    time = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time
    df["DateTime"] = date + pd.to_timedelta(time.astype(str))
    
    if sort_by_datetime:
        df = df.sort_values("DateTime")
    return df

def parse_gender_from_swedish_id(df):
    def parse_gender_from_id(pnr):
        pnr = str(pnr).replace("-", "")
        
        gender_digit = int(pnr[-2])
        
        return "M" if gender_digit % 2 == 1 else "F"

    df = df.copy()
    
    mask = df["Patient Sex"] == "O"
    df.loc[mask, "Patient Sex"] = df.loc[mask, "Id"].apply(parse_gender_from_id)

    return df



def cbct_color_map():
    return {
        (360, "Std"):      "#1f77b4",  # C0
        (360, "Hi-Speed"): "#ff7f0e",  # C1
        (360, "Hi-Fi"):    "#2ca02c",  # C2
        (360, "Hi-Res"):   "#d62728",  # C3
        (360, "no match"): "#9467bd",  # C4

        (180, "Std"):      "#8c564b",  # C5
        (180, "Hi-Speed"): "#e377c2",  # C6
        (180, "Hi-Fi"):    "#7f7f7f",  # C7
        (180, "Hi-Res"):   "#bcbd22",  # C8
    }

def color_for(scan, imaging):
    cmap = cbct_color_map()
    return cmap.get((scan, imaging), "#000000")

def plot_mas_per_mmas_per_frame(
    df,
    imaging_modes=('Std', 'Hi-Fi', 'Hi-Res', 'Hi-Speed'),
    scan_modes=(180, 360),
    highlight_mas_range=None,
    export_to_browser=False
):

    hover_lines = []
    for i, col in enumerate(df.columns):
        hover_lines.append(f"{col}: " + "%{customdata[" + str(i) + "]}")
    hovertemplate = "<br>".join(hover_lines) + "<extra></extra>"

    df_plot = df[(df["Imaging"].isin(imaging_modes)) &
                 (df["Scan"].isin(scan_modes))].copy()

    if "mAs" not in df_plot.columns or "mmAs_per_frame" not in df_plot.columns:
        raise ValueError("DataFrame must contain 'mAs' and 'mmAs_per_frame' columns.")

    groups = [(scan, im) for scan in scan_modes for im in imaging_modes]

    fig = go.Figure()

    for scan, im in groups:
        tdf = df_plot[(df_plot["Scan"] == scan) &
                      (df_plot["Imaging"] == im)]
        if tdf.empty:
            continue

        fig.add_trace(go.Scatter(
            y=tdf["mAs"],
            x=tdf["mmAs_per_frame"],
            mode="markers",
            marker=dict(
                size=10,
                color=color_for(scan, im),
                line=dict(color="black", width=0.4)
            ),
            name=f"{scan}, {im}",
            customdata=tdf.values.tolist(),
            hovertemplate=hovertemplate,
            visible=True
        ))

    fig.update_layout(
        title=(
            "<b>mAs vs mmAs_per_frame</b><br>"
            f"<b>Modes:</b> {imaging_modes} &nbsp;&nbsp; "
            f"<b>Scans:</b> {scan_modes}"
        ),
        yaxis_title="mAs",
        xaxis_title="mmAs_per_frame",
        template="plotly_white",
        hovermode="closest",
        legend_title_text="Scan, Imaging"
    )

    if highlight_mas_range is not None:
        y0, y1 = highlight_mas_range
        fig.add_shape(
            type="rect",
            xref="paper", x0=0, x1=1,
            yref="y",     y0=y0, y1=y1,
            fillcolor="rgba(0, 0, 255, 0.25)",
            line=dict(width=0),
            layer="below"
        )
    
    if export_to_browser:
        pio.show(fig, renderer="browser")
    else:
        fig.show()

def plot_parameter(df, parameter='mAs',
                   imaging_modes=('Std', 'Hi-Fi', 'Hi-Res', 'Hi-Speed'),
                   scan_modes=(180, 360),
                   export_to_browser=False):

    hover_lines = []
    for i, col in enumerate(df.columns):
        hover_lines.append(f"{col}: " + "%{customdata[" + str(i) + "]}")
    hovertemplate = "<br>".join(hover_lines) + "<extra></extra>"

    df = df[(df["Imaging"].isin(imaging_modes)) &
            (df["Scan"].isin(scan_modes))].copy()

    df = df.sort_values(["Scan", "Imaging", parameter])
    df["x_inc"] = df.groupby(["Scan", "Imaging"]).cumcount()

    fig = go.Figure()
    groups = [(scan, im) for scan in scan_modes for im in imaging_modes]

    for scan, im in groups:
        tdf = df[(df["Scan"] == scan) & (df["Imaging"] == im)]
        if tdf.empty:
            continue

        fig.add_trace(go.Scatter(
            x=tdf["x_inc"],
            y=tdf[parameter],
            mode="markers",
            marker=dict(
                size=10,
                color=color_for(scan, im),
                line=dict(color="black", width=0.4)
            ),
            name=f"{scan}, {im}",
            customdata=tdf.values.tolist(),
            hovertemplate=hovertemplate
        ))

    fig.update_layout(
        title=f"<b>Increasing {parameter}</b> — Modes: {imaging_modes}, Scans: {scan_modes}",
        xaxis_title=f"Index (increasing {parameter})",
        yaxis_title=parameter,
        template="plotly_white",
        hovermode="closest",
        legend_title_text="Scan, Imaging"
    )

    if export_to_browser:
        pio.show(fig, renderer="browser")
    else:
        fig.show()

def plot_statistic(
    df,
    parameter='mAs',
    imaging_modes=('Std', 'Hi-Fi', 'Hi-Res', 'Hi-Speed', 'no match'),
    scan_modes=(180, 360),
    export_to_browser=False,
    shade_y_regions=None,              
    shade_labels=None,
    shade_fillcolors=None,
    shade_line_colors=None,
    reference_levels=None,
    reference_labels=None,
    reference_colors=None,
    reference_dash=None,
    dark_mode=False
):
    df = df[(df["Imaging"].isin(imaging_modes)) &
            (df["Scan"].isin(scan_modes))].copy()

    df = df.reset_index(drop=False)

    cols = df.columns.tolist()

    hover_lines = [f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(cols)]
    hovertemplate = "<br>".join(hover_lines) + "<extra></extra>"

    fig = go.Figure()

    if shade_y_regions is not None and len(shade_y_regions) > 0:

        n = len(shade_y_regions)

        if shade_labels is None:
            shade_labels = [f"Region {i+1}" for i in range(n)]
        if shade_fillcolors is None:
            shade_fillcolors = ["rgba(0,128,0,0.15)"] * n
        if shade_line_colors is None:
            shade_line_colors = ["rgba(0,0,0,0)"] * n

        while len(shade_labels) < n:
            shade_labels.append(f"Region {len(shade_labels)+1}")
        while len(shade_fillcolors) < n:
            shade_fillcolors.append("rgba(0,128,0,0.15)")
        while len(shade_line_colors) < n:
            shade_line_colors.append("rgba(0,0,0,0)")

        x_min = df["index"].min()
        x_max = df["index"].max()

        for (low, high), label, fillc, linec in zip(
            shade_y_regions, shade_labels, shade_fillcolors, shade_line_colors
        ):
            y0, y1 = (low, high) if low <= high else (high, low)

            x_poly = [x_min, x_max, x_max, x_min]
            y_poly = [y0, y0, y1, y1]

            fig.add_trace(go.Scatter(
                x=x_poly, y=y_poly,
                name=label,
                mode="none",
                fill="toself",
                fillcolor=fillc,
                line=dict(color=linec),
                hoverinfo="skip",
                showlegend=True
            ))

    if reference_levels is not None and len(reference_levels) > 0:

        n = len(reference_levels)

        if reference_labels is None:
            reference_labels = [f"Ref {i+1}" for i in range(n)]
        if reference_colors is None:
            reference_colors = ["black"] * n
        if reference_dash is None:
            reference_dash = ["dash"] * n

        while len(reference_labels) < n:
            reference_labels.append(f"Ref {len(reference_labels)+1}")
        while len(reference_colors) < n:
            reference_colors.append("black")
        while len(reference_dash) < n:
            reference_dash.append("dash")

        x_min = df["index"].min()
        x_max = df["index"].max()

        for y, label, col, dash in zip(
            reference_levels, reference_labels, reference_colors, reference_dash
        ):
            fig.add_trace(go.Scatter(
                x=[x_min, x_max],
                y=[y, y],
                mode="lines",
                name=label,
                line=dict(color=col, width=2, dash=dash),
                hoverinfo="skip",
                showlegend=True
            ))


    groups = [(scan, im) for scan in scan_modes for im in imaging_modes]

    for scan, im in groups:
        tdf = df[(df["Scan"] == scan) & (df["Imaging"] == im)]
        if tdf.empty:
            continue

        customdata = tdf[cols].values

        fig.add_trace(go.Scatter(
            x=tdf["index"],
            y=tdf[parameter],
            mode="markers",
            marker=dict(
                size=10,
                color=color_for(scan, im),
                line=dict(color="black" if not dark_mode else 'white', width=0.4)
            ),
            name=f"{scan}, {im}",
            customdata=customdata,
            hovertemplate=hovertemplate
        ))


    template_name = "plotly_dark" if dark_mode else "plotly_white"
    font_color = "white" if dark_mode else "black"

    fig.update_layout(
        title=f"<b>Statistics plot</b> — {parameter}",
        xaxis_title="Index (original dataframe order)",
        yaxis_title=parameter,
        template=template_name,
        hovermode="closest",
        legend_title_text="Scan, Imaging",
        font=dict(color=font_color),
    )

    if export_to_browser:
        import plotly.io as pio
        pio.show(fig, renderer="browser")
    else:
        fig.show()


def plot_summary_statistics(
    df,
    export_to_browser=False,
    age_bin_width=10,
    age_range=None,
    n_rows=4,
    n_cols=3,
    dark_mode=False,
):
    def clean_value(v):
        if isinstance(v, (int, np.integer)):
            return str(v)
        if isinstance(v, float):
            return f"{v:.3f}".rstrip("0").rstrip(".")
        return str(v)

    def categorical_hist(series: pd.Series):
        s = series.dropna()
        if len(s) == 0:
            return [], [], []

        cleaned = s.apply(clean_value)
        counts = cleaned.value_counts()
        idx_list = list(counts.index)

        def _is_float(x: str):
            try:
                float(x)
                return True
            except Exception:
                return False

        if all(_is_float(x) for x in idx_list):
            ordered = sorted(idx_list, key=lambda x: float(x))
            counts = counts.reindex(ordered)
        else:
            counts = counts.sort_index()

        percent = (counts / counts.sum() * 100).round(1)
        return counts.index.tolist(), counts.values.tolist(), percent.values.tolist()

    def date_hist(series: pd.Series, month_fmt="%Y-%m"):
        s = pd.to_datetime(series, errors="coerce").dropna()
        if len(s) == 0:
            return [], [], []

        months = s.dt.to_period("M")
        counts = months.value_counts().sort_index()
        labels = [p.strftime(month_fmt) for p in counts.index.to_timestamp()]
        percent = (counts / counts.sum() * 100).round(1)
        return labels, counts.values.tolist(), percent.values.tolist()

    def age_hist(series: pd.Series, bin_width=10, rng=None):
        s = pd.to_numeric(series, errors="coerce").dropna()
        if len(s) == 0:
            return [], [], []

        if rng is None:
            vmin, vmax = float(s.min()), float(s.max())
        else:
            vmin, vmax = float(rng[0]), float(rng[1])

        start = np.floor(vmin / bin_width) * bin_width
        end = np.ceil(vmax / bin_width) * bin_width
        if end <= start:
            end = start + bin_width

        edges = np.arange(start, end + bin_width, bin_width)
        counts, edges = np.histogram(s, bins=edges)
        percent = (counts / counts.sum() * 100).round(1)

        labels = [f"{int(edges[i])}-{int(edges[i + 1])}" for i in range(len(edges) - 1)]
        return labels, counts.tolist(), percent.tolist()

    def add_bar_from_series(title: str, series: pd.Series, mode: str, row: int, col: int):
        if mode == "age":
            x, y, perc = age_hist(series, bin_width=age_bin_width, rng=age_range)
        elif mode == "date":
            x, y, perc = date_hist(series)
        else:
            x, y, perc = categorical_hist(series)

        custom = np.c_[perc] if len(perc) else np.empty((0, 1))
        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                customdata=custom,
                hovertemplate="Value: %{x}<br>Number: %{y} (%{customdata:.1f}%)<extra></extra>",
            ),
            row=row,
            col=col,
        )
        fig.update_xaxes(title_text=title, row=row, col=col, type="category")

    # --- Create subplots ---
    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        shared_xaxes=False,
        horizontal_spacing=0.08,
        vertical_spacing=0.12,
    )

    plots = [
        ("Date", df["DateTime"], "date"),
        ("kV", df["kV"], "cat"),
        ("mA", df["mA"], "cat"),
        ("Scan time", df["Scan time"], "cat"),
        ("Imaging", df["Imaging"], "cat"),
        ("Scan (deg)", df["Scan"].astype(str), "cat"),
        ("FOV", df["FOV"], "cat"),
        ("DAP (mGycm2)", df["DAP (mGycm2)"], "cat"),
        ("mAs", df["mAs"], "cat"),
        ("Model Name", df["Model Name"], "cat"),
        ("Patient age", df["Patient age"], "age"),
        ("Patient sex", df["Patient Sex"], "cat"),
    ]

    for idx, (title, series, mode) in enumerate(plots, start=1):
        row = (idx - 1) // n_cols + 1
        col = (idx - 1) % n_cols + 1
        if row <= n_rows:
            add_bar_from_series(title, series, mode, row=row, col=col)

    for r in range(1, n_rows + 1):
        for c in range(1, n_cols + 1):
            fig.update_yaxes(title_text="num scans", row=r, col=c)

    template_name = "plotly_dark" if dark_mode else "plotly_white"
    font_color = "white" if dark_mode else "black"

    fig.update_layout(
        template=template_name,
        showlegend=False,
        font=dict(color=font_color),
    )

    if export_to_browser:
        import plotly.io as pio
        pio.show(fig, renderer="browser")
    else:
        fig.show()





