CLIENT_ID_ENV_VAR = "REMBOX_INT_CLIENT_ID"
CLIENT_PWD_ENV_VAR = "REMBOX_INT_CLIENT_PWD"

TOKEN_URI = "https://autoqa.vll.se/dpqaauth/connect/token"
API_URI = "https://rembox.vll.se/api"
ORIGIN_URI = "https://rembox.vll.se"

# Machine types
machine_type_dict = {
    "CT": "CT",
    "Fluoroscopic": "XASTAT",
    "Mobile C-arm": "XAMOB",
    "Conventional": "DX",
    "Mammography": "MG",
    "Intraoral": "IO",
    "Panoramic": "PX",
    "Dental Cone Beam CT": "DCBCT",
    "PET": "PET",
    "PET/CT": "PETCT",
    "SPECT": "SPECT",
    "SPECT/CT": "SPECTCT",
    "Nuclear Medicine": "NM",
    "Mobile X-ray": "DXMOB",
    "Conventional with fluoro": "DXXA",
}

# Undersökningskoder
# Endoskopi/Kirurgi börjar med E. Exempelvis "ERCP - i narkos" har kod E4905
# Thorax börjar på 3. Exempelvis "Thorakal stengraftinläggning" har kod 39948 och "Pulmonalisangiografi" har kod 38200 (OBS endast på U104)
# Buk börjar på 4. Exempelvis "PTC med externt dränage - i narkos" har kod 49005 och "Abdominell stentgraftinläggning" har kod 49948 och "Buköversikt akut - punktion + inl av kateter" har kod 46051
# Njurar börjar på 5. Exempelvis "Byte av nefrostomikateter ..." har kod 59100 och "Percutan nefrostomi .." har kod 59000 (samma kod för höger och vänster)
# Extremiteter börjar på 6. Exempelvis "Angiografi, aortofemoral" har kod 67700
# Ultraljud har koder som börja på 9
# Skalle (angio) börjar på 17 och emboliseringar på 19. Exempelvis "Angiografi, komb av flera skallangio" har kod 17500 och "Intracraniell trombectomi + komb av flera skallangio - i narkos" har kod 19305

procedure_codes_dict = {
    #"Antrografi": ["63135", "63935", "64235"], Finns inte i mallen längre
    # 63135 Axel, ac-led - artrografi
    # 63935 Höftled - arthrografi
    # 64235 Knäled - artrografi

    "Bukangiografi": ["47100", "47142", "47200", "47242", "47600", "47642"],
    # 47100 Angiografi i en bukartär
    # 47142 Angiografi i en bukartär - embolisering
    # 47200 Angiografi i två eller flera bukartärer
    # 47242 Angiografi i två eller flera bukartärer - embolisering
    # 47600 Angiografi av lever
    # 47642 Angiografi av lever - embolisering

    #"Bäckenangiografi": ["57000", "57042", "57072"], Finns inte i mallen längre
    # 57000 Angiografi, bäcken
    # 57042 Angiografi, bäcken - embolisering
    # 57072 Angiografi, bäcken - trombolys

    #Cerebral angiografi hanteras inom INT-årsstatistiken

    "Defekografi": ["44200"],
    # 44200 Defekografi

    "ERCP": ["E4900", "E4903", "E4905", "E4976"],
    # E4900 ERCP
    # E4903 ERCP - utförd operation
    # E4905 ERCP - i narkos
    # E4976 ERCP - rendez-vous

    "GI (bariumkontrast)": ["44000", "44036"],
    # 44000 Colon, Enkelkontrast
    # 44036 Colon, enkelkontrast - anastomoskontroll

    "Hals (mjukvävnad)": ["41100", "41127", "41200", "41300", "41327"],
    # 41100 Hypofarynx och esofagus
    # 41127 Hypofarynx och esofagus - terapeutisk sväljning
    # 41200 Esofagus
    # 41300 Hypofarynx
    # 41327 Hypofarynx - terapeutisk sväljning

    "Kolangiografi": ["49055", "45400"],
    # 49055 Cholangiografi
    # 45400 Cholangiografi post op

    #"Myelografi": ["13000", "13200", "13300", "13400"], Finns inte i mallen längre
    # 13000 Myelografi lumbal -------------------- OBS! U104 som inte får patientålder
    # 13200 Myelografi thorakal
    # 13300 Myelografi cervikal
    # 13400 Myelografi total ---------------------
    # 63135 Axel, ac-led - artrografi
    # 63935 Höftled - arthrografi
    # 64235 Knäled - artrografi

    "Perifer angiografi": ["67500", "67600", "67641", "67643", "67648", "67672",
                           "67700", "67741", "67743", "67748", "67772", "67900"],
    # 67500 Angiografi, arm
    # 67600 Angiografi, femoralis
    # 67641 Angiografi, femoralis - dilatation
    # 67643 Angiografi, femoralis - hybridingrepp
    # 67648 Angiografi, femoralis - stentinläggning
    # 67672 Angiografi, femoralis - trombolys
    # 67700 Angiografi, aortofemoral
    # 67741 Angiografi, aortofemoral - dilatation
    # 67743 Angiografi, aortofemoral - hybridingrepp
    # 67748 Angiografi, aortofemoral - stentinläggning
    # 67772 Angiografi, aortofemoral - trombolys
    # 67900 Angiografi av annan extremitetsartär

    #"Thoraxangiografi": Görs inte

    #"Urografi": Görs inte
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    "Lycksele lasarett": ["L3"],
    "Skellefteå lasarett": ["S08"],
    "Norrlands universitetssjukhus": ["U104", "U105", "U105_old", "U106", "U106_old",
                                      "U704", "U110", "U601", "U602", "Arytmi 1", "Arytmi 2"],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor (16 år och äldre).Antal ",
    "female-dap": "Kvinnor (16 år och äldre).DAP (Gy*cm2)",
    "male-studies": "Män (16 år och äldre).Antal ",
    "male-dap": "Män (16 år och äldre).DAP (Gy*cm2)",
    "girl-studies": "Flickor (15 år och yngre).Antal ",
    "girl-dap": "Flickor (15 år och yngre).DAP (Gy*cm2)",
    "boy-studies": "Pojkar (15 år och yngre).Antal ",
    "boy-dap": "Pojkar (15 år och yngre).DAP (Gy*cm2)",
}
