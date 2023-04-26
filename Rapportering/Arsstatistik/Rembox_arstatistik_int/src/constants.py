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
    "Hjärna (skallangio)": ["17500"],
    "Buk (gallvägar och urinvägar)": ["59100"], #Byte av nefrostomikateter...
    #"Buk (gallvägar och urinvägar)": ["59000"], #Percutan nefrostomi...
    #"Buk (gallvägar och urinvägar)": ["49005"], #PTC med externt dränage - i narkos
    #"Buk (gallvägar och urinvägar)": ["49948"], #Abdominell stentgraftinläggning
    #"Buk (gallvägar och urinvägar)": ["46051"], #Buköversikt akut - punktion + inl av kateter

    # GML-koder nedan
    #"GI (bariumkontrast)": ["44000"], #44000 Colon, Enkelkontrast
    #"GI (bariumkontrast)": ["44036"], #44036 Colon, enkelkontrast - anastomoskontroll
    #"Defekografi": ["44200"], #44200 Defekografi
    #"Kolangiografi": ["49055"], #49055 Cholangiografi
    #"Kolangiografi": ["45400"], #45400 Cholangiografi post op
    #"ERCP": ["E4900"], #E4900 ERCP
    #"ERCP": ["E4903"], #E4903 ERCP - utförd operation
    #"ERCP": ["E4905"], #E4905 ERCP - i narkos
    #"ERCP": ["E4976"], #E4976 ERCP - rendez-vous
    #"Myelografi": ["13000"], #13000 Myelografi lumbal -------------------- OBS! U104
    #"Myelografi": ["13200"], #13200 Myelografi thorakal
    #"Myelografi": ["13300"], #13300 Myelografi cervikal
    #"Myelografi": ["13400"], #13400 Myelografi total ---------------------
    #"Artrografi": ["63135"], #63135 Axel, ac-led - artrografi
    #"Artrografi": ["63935"], #63935 Höftled - arthrografi
    #"Artrografi": ["64235"], #64235 Knäled - artrografi
    #"Bäckenangiografi": ["57000"], #57000 Angiografi, bäcken
    #"Bäckenangiografi": ["57042"], #57042 Angiografi, bäcken - embolisering
    #"Bäckenangiografi": ["57072"], #57072 Angiografi, bäcken - trombolys
    #"Bukangiografi": ["47100"], #47100 Angiografi i en bukartär
    #"Bukangiografi": ["47142"], #47142 Angiografi i en bukartär - embolisering
    #"Bukangiografi": ["47200"], #47200 Angiografi i två eller flera bukartärer
    #"Bukangiografi": ["47242"], #47242 Angiografi i två eller flera bukartärer - embolisering
    #"Bukangiografi": ["47600"], #47600 Angiografi av lever
    #"Bukangiografi": ["47642"], #47642 Angiografi av lever - embolisering
    #"Perifer angiografi": ["67500"], #67500 Angiografi, arm
    #"Perifer angiografi": ["67600"], #67600 Angiografi, femoralis
    #"Perifer angiografi": ["67641"], #67641 Angiografi, femoralis - dilatation
    #"Perifer angiografi": ["67643"], #67643 Angiografi, femoralis - hybridingrepp
    #"Perifer angiografi": ["67648"], #67648 Angiografi, femoralis - stentinläggning
    #"Perifer angiografi": ["67672"], #67672 Angiografi, femoralis - trombolys
    #"Perifer angiografi": ["67700"], #67700 Angiografi, aortofemoral
    #"Perifer angiografi": ["67741"], #67741 Angiografi, aortofemoral - dilatation
    #"Perifer angiografi": ["67743"], #67743 Angiografi, aortofemoral - hybridingrepp
    #"Perifer angiografi": ["67748"], #67748 Angiografi, aortofemoral - stentinläggning
    #"Perifer angiografi": ["67772"], #67772 Angiografi, aortofemoral - trombolys
    #"Perifer angiografi": ["67900"], #67900 Angiografi av annan extremitetsartär
    #"Hals (mjukvävnad)": ["41100"], #41100 Hypofarynx och esofagus
    #"Hals (mjukvävnad)": ["41127"], #41127 Hypofarynx och esofagus - terapeutisk sväljning
    #"Hals (mjukvävnad)": ["41200"], #41200 Esofagus
    #"Hals (mjukvävnad)": ["41300"], #41300 Hypofarynx
    #"Hals (mjukvävnad)": ["41327"], #41327 Hypofarynx - terapeutisk sväljning
}

# Maskiner per verksamhetsplats

machines_at_hospital = {
    "Lycksele lasarett": ["L3"],
    "Skellefteå lasarett": ["S08"],
    "Norrlands universitetssjukhus": ["U104", "U105", "U105_old", "U106", "U106_old", "U110", "U601", "U602", "Arytmi 1", "Arytmi 2"],
}

# patient_group

patient_group = {
    "female-studies": "Kvinnor (16 år och äldre).Antal ",
    "female-dlp": "Kvinnor (16 år och äldre).DLP (mGy*cm)",
    "male-studies": "Män (16 år och äldre).Antal ",
    "male-dlp": "Män (16 år och äldre).DLP (mGy*cm)",
    "girl-studies": "Flickor (15 år och yngre).Antal ",
    "girl-dlp": "Flickor (15 år och yngre).DLP (mGy*cm)",
    "boy-studies": "Pojkar (15 år och yngre).Antal ",
    "boy-dlp": "Pojkar (15 år och yngre).DLP (mGy*cm)",
}
