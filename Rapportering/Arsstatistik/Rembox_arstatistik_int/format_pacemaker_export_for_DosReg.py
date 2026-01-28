import marimo

__generated_with = "0.18.1"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Formatera data från Svenska ICD och Pacemakerregistret så output kan föras in i DosReg
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Gå till https://www.pacemakerregistret.se/ och logga in med Siths-kort<br>
    Gå till **"Statistik"** och sedan **"Rapporter"**<br>
    För att titta på t.ex. pacemakrar,  ICD:r osv. och primärimplantationer, skall du välja **"Tom rapport"**.<br>
    Gör till urval:<br>
    **Sjukhus:** Norrlands Universitetssjukhus<br>
    **Patient:** Alla<br>
    **Implantat:** Implantattyp - Pacemaker, Interventionstyp - Implantation, Orsak - Primärimplantation<br>
    **Intervention:** Alla<br>
    **Tidsperiod:** Fast period - T.ex. 2022-01-01 - 2023-01-01<br>
    Välj Excelfil längst ner på sidan och spara nerladdad fil (.xlsx) till *rvbrtg/Data/input_data*<br>
    Kontakta helena.p.karlsson@regionstockholm.se för access till registret. Måste ha godkännande från Medicinsk Chef vid Arytmi-lab.
    """)
    return


@app.cell
def _():
    import pandas as pd
    from pathlib import Path

    #Importera data från PM-registret

    PM_data_path = Path(__file__).parent.parent.parent.parent / "Data/input_data/svenska_pacemaker_registret_2024.xlsx"
    data = pd.read_excel(PM_data_path)

    data.head()
    return (data,)


@app.cell
def _(data):
    #Minska ner tabellen och döp om kolumner

    data_subset = data[["SEX", "BIRTHDATE", "OPERATOR", "FLUORODOSE", "FLUOROTIME"]].copy()

    data_subset.columns = ["Sex", "Birthdate", "Operator", "KAP_Gycm2", "Fluorotime_min"]

    data_subset.head()
    return (data_subset,)


@app.cell
def _(data_subset):
    #Ta bort rader utan dosdata

    data_subset_KAP = data_subset.dropna(subset=["KAP_Gycm2"])

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
