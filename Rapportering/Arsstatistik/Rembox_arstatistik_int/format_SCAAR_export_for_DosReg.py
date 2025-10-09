

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Formatera data från SCAAR så output manuellt kan föras in i DosReg""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Gå till https://www.ucr.uu.se/swedeheart/ och logga in med Siths-kort <br>
        Gå till **"Rapporter"**<br>
        Välj **"Export till Excel Angio-PCI"**<br>
        Gör följande urval:<br>
        **Rapportdatum:** T.ex 2022-01-01 - 2023-01-01<br>
        **Angio/PCI:** Angio och PCI i följd<br>
        **Procedur/Segment:** Procedur<br>
        Klicka på **"Beställ"** och ladda ner resulterande excel-fil (.xlsx) till *rvbrtg/Data/input_data*
        """
    )
    return


@app.cell
def _(__file__):
    import pandas as pd
    from pathlib import Path

    # Läs in data från SCAAR

    SCAAR_data_path = Path(__file__).parent.parent.parent.parent / "Data/input_data/Angio_PCI_2023.xlsx"
    data = pd.read_excel(SCAAR_data_path)

    data.head()
    return (data,)


@app.cell
def _(data):
    #Minska ner tabellen och döp om kolumner

    data_subset = data[["Kön", "Ålder vid procedur", "Längd (cm)", "Vikt (kg)", "Angiograför", "Punktionställe", "Labnamn", "Stråldos (µGym2)", "Genomlysningstid (h:mm:ss)", ]].copy()

    data_subset.columns = ["Sex", "Age", "Length_cm", "Weight_kg", "Operator", "Accesspoint", "Lab", "KAP_uGym2", "Fluorotime_h_mm_ss"]

    data_subset.head()
    return (data_subset,)


@app.cell
def _(data_subset):
    #Ersätt , med . samt byt från sträng till float och konvertera från uGym2 till Gycm2
    data_subset["KAP_uGym2"] = data_subset["KAP_uGym2"].replace(',','.',regex=True).astype(float)
    data_subset["KAP_uGym2"] = data_subset["KAP_uGym2"] * 0.01

    data_subset.rename(columns = {"KAP_uGym2":"KAP_Gycm2"}, inplace = True)

    #data_subset.dtypes
    data_subset.head()
    return


@app.cell
def _(data_subset):
    #Printa ut antal per kön och medelvärde för KAP för att skriva in i DosReg-mall

    print(data_subset.groupby("Sex").size())

    print(data_subset.groupby("Sex").mean(numeric_only = True))
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
