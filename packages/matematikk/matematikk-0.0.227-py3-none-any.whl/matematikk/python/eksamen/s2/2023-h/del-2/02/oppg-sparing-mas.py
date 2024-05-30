# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 2) - Sparebeløp
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere matematikk:
#   $ pip install matematikk
# - Klasser og funksjoner som også er i matematikk
#   - from os import system     -> os.system(<posix-command>)   -> Eks: os.system("clear")
#   - from copy import deepcopy -> copy.deepcopy(<objekt>)      -> Eks: mat_2 = copy.deepcopy(mat_1)
#   - from numpy import random  -> random.randint(<int>))       -> Eks: random.randint(len(matrix_jp_ls))
#   - import colorama           -> ...                          -> Eks: colorama.Fore.BLUE

import matematikk as mt


# Tøm terminal-skjerm for hvert run
_blokk = 1
if _blokk == 1:

    # Fungerer perfekt, men printer [H[2J[3J i editoren på programmering.no pga. en JavaScript-bug
    mt.system("clear")

# Variabler
if _blokk == 1:

    # Tabell
    _Periode_str        = "Periode"         # Periode n: Brukes flere ganger og er derfor en variabel (unngår skrifeil i strings)
    _Aar_str            = "År"              # År (YYYY): -"-
    _Innskudd_str       = "Innskudd"        # Inskudd: -"-"
    _Innskudd_d_str     = "Innskudd d"      # Inskudd d: Fast øking av innskudd (differansen i aritmetisk rekke)
    _B_start_str        = "B (start)"       # Beløp (start): Beløpet på konto i starten av perioden (året)
    _B_slutt_str        = "B (slutt)"       # Beløp (slutt): Beløpet på konto i slutten av perioden (året)
    tab_mat_0           = [                 # Miriam: Matrise-header for tabell-verdier (kopier med deepcopy for ikke å skrive over)
        [_Periode_str],                     #
        # [_B_start_str],                   # B (start): Tabellen kan vise kolonnene i valg-fri rekkefølge
        [_Aar_str],                         #
        [_Innskudd_str],                    # Innskudd
        [_Innskudd_d_str],                  # Innskudd d
        [_B_start_str],                     # Beløp (start)
        [_B_slutt_str]                      # Beløp (slutt)
    ]
    tab_bredde          = 12                # Antall char bredde på tabell-kolonne
    tab_print_1_start   = 0                 # Start-verdi for å printe tabell
    tab_print_1_slutt   = 2                 # Slutt-verdi for å printe tabell
    tab_print_2_start   = 19                # Start-verdi for å printe tabell
    tab_print_2_slutt   = 20                # Slutt-verdi for å printe tabell
    tab_desimal         = None              # Miriam: Avrunding svar i a)
    tab_is_farge        = 1                 # Hermod: Matrix effekt
    tab_farge_typ_mat   = "grønn"           # Hermod: Matrix-farge (grønn!!!)
    tab_farge_typ_svar  = "blå"             # Hermod: Svar-setninger

    # Spinner
    is_spinning         = 0                 # Vente-spinner når while-løkken kjører, kan ta lang tid, avbryt med ctrl + z

    # Matrix-effekt
    if _blokk == 1:
        matrix_jp_ls        = [             # Liste med japanske symbol (jp-sym) som hentes frem tilfeldig (alleer dobbelt så lange som vanlige char)
            "グ", "ケ", "ゲ", "コ", "ゴ", "サ", "ザ", "シ", "ジ", "ス", "ズ", "セ", "ゼ", "ソ", "ゾ", "タ"
        ]
        matrix_null_en_ls   = ["0", "1"]    # Liste med 0 og 1 som blandes med jp-sym
        matrix_f_ls         = [             # Filter-parametre som gir en tilfeldig, dynamisk blanding mellom to lister (se nedenfor): 3 i dette scopet og 4 som argumenter inn i tabell
            1.00, 0.10, 0.60, 0.80, 0.99, 0.10, 0.99
        ]
        matrix_cut_off      = 700000 / 10   # Gjør at flere el kommer etter hverandre (startet med 692 852 som er ca. 700 000 / 140 = 5000 el etter hverandre)

    # Oppg a)
    innskudd_0_mi       = 20000             # Miriam: Årlig innskudd (starten av året)
    innskudd_mi         = innskudd_0_mi     # Miriam: Årlig innskudd (starten av året), kopiers så slipper å resette før f.eks. CAS
    rente_mi            = 3.5               # Miriam: Rente
    vf_mi               = mt.vekstfaktor(   # Miriam: Vekstfaktor
        fortegn         = "+",
        p               = rente_mi,
        desimal         = -1
    )
    n_mi                = 20                # Miriam: Spare-periode, f.eks. 20.0 gir type-advarsel
    aar_start_mi        = 2024              # Miriam: Sparing start, f.eks. 2024.0 gir type-advarsel
    b_start_mi          = float()                   # Miriam: Start-beløp på konto etter n år
    b_slutt_mi          = float()                   # Miriam: Slutt-beløp på konto etter n år
    INSK_mi             = mt.Symbol("INSK_mi")      # Miriam: CAS-variabel for årlig innskudd
    b_n_mi_1            = float()                   # Miriam: CAS-variabel for beløp nr. n
    b_sum_mi_1          = 0                         # Miriam: CAS-variabel for summen av beløper
    b_20_mi_1           = 565594                    # Miriam: CAS: Beløps-grense like etter innskudd nr. 20

    # Oppg b)
    rente_he            = 3.5                       # Hermod: Rente
    vf_he               = mt.vekstfaktor(           # Hermod: Vekstfaktor
        "+",
        rente_he
    )
    n_he                = 20                        # Hermod: Spare-periode, f.eks. 20.0 gir type-advarsel
    aar_start_he        = 2024                      # Hermod: Sparing start, f.eks. 2024.0 gir type-advarsel
    INSK_he             = mt.Symbol("INSK_HE")     # Hermod: CAS-variabel for årlig innskudd
    b_20_he             = 692852                    # Hermod: Beløps-grense like etter innskudd nr. 20
    B_n_he              = mt.Symbol("B_n_he")       # Hermod: CAS-variabel for beløp nr. n
    B_sum_he            = 0                         # Hermod: CAS-variabel for summen av beløper
    belop_debug         = 0                         # Hermod: Debug utregningene av start-beløp i while-løkken (tar lang tid)

    # Oppg c)
    INSK_d_mi           = mt.Symbol("INSK_d_mi")    # Miriam: CAS-variabel for fast øking av innskudd
    B_n_mi_2            = mt.Symbol("B_n_mi_2")     # Miriam: CAS-variabel for beløp nr. n
    B_sum_mi_2          = 0                         # Miriam: CAS-variabel for summen av beløper
    b_20_mi_2           = 1000000                   # Miriam: Beløps-grense like etter innskudd nr. 20

# a) Miriam > Vis at Miriam har 565 594 kr like etter innskudd 20 > Formel
if _blokk == 1:

    # Variabler
    _n_periode = mt.sjekk_datatype(vari_navn = "_n_periode", vari = n_mi, typ = int)

    # Geometrisk formel: b_n = b_1 * k ** (n - 1)
    for n in range(1, _n_periode + 1):
        b_n_mi_1    = (innskudd_0_mi) * vf_mi ** (n - 1)
        b_sum_mi_1  += b_n_mi_1

    # Avrunding
    b_sum_mi_1 = round(b_sum_mi_1, tab_desimal)

    # Print svar-setninger
    mt.oppg_strek(1)
    print(f"")
    print(f"- Miriam har {b_sum_mi_1} kr like etter innskudd {n_mi}, QED")

# a) Miriam > Vis at Miriam har 565 594 kr like etter innskudd 20 > Tabell (rekker)
if _blokk == -1:

    mt.oppg_strek(1)
    print(f""); print(f"Oppg a) Miriam: Vis beløp 565 594 kr etter innskudd {n_mi}"); print(f"")

    # Debug
    _debug_mat = 0

    # Resetting
    tab_mat = mt.deepcopy(tab_mat_0)

    # Regner og printer ut tabell
    tab_mat = mt.tabell_økonomi_lag(
        tab_mat             = tab_mat,
        tab_desimal         = None,                 # None, -1
        tab_print           = 1,
        tab_print_1_start   = tab_print_1_start,    # tab_print_1_start,
        tab_print_1_slutt   = tab_print_1_slutt,    # tab_print_1_slutt, n_mi
        tab_print_2_start   = tab_print_2_start,    # tab_print_2_start, 0
        tab_print_2_slutt   = tab_print_2_slutt,    # tab_print_2_slutt, 0
        tab_bredde          = tab_bredde,
        vf                  = vf_mi,
        n_periode           = n_mi,
        aar_start           = aar_start_mi,
        innskudd            = innskudd_mi,
        innskudd_desimal    = -1,                   # -1, None,
        innskudd_d          = 0,
        innskudd_d_desimal  = -1,                   # -1, None
        b_start_desimal     = -1,                   # -1, None
        b_slutt_desimal     = -1,                   # -1, None
    )

    # Debug
    if _debug_mat == 1:
        print(""); print("debug > done ::")
        for j in range(len(tab_mat)): print(tab_mat[j])

    # Finn start-beløpet
    tab_mat_el = mt.tabell_finn_el(tab_mat, n_mi, _B_start_str)

    # Print svar-setninger
    print(f"")
    print(f"- Miriam har {tab_mat_el} kr like etter innskudd {n_mi}, QED")

# b) Hermod > Manuell brute force med binært søk
if _blokk == -1:

    # Resetting
    tab_mat = mt.deepcopy(tab_mat_0)

    # 692852: Prøver verdier fra 0 til 1836.33
    innskudd_he = 24500

    # Lager tabell
    tab_mat = mt.tabell_økonomi_lag(
        tab_mat             = tab_mat,
        tab_desimal         = None,                 # None, -1
        tab_print           = -1,
        tab_bredde          = tab_bredde,
        vf                  = vf_he,
        n_periode           = n_he,
        aar_start           = aar_start_he,
        innskudd            = innskudd_he,
        innskudd_desimal    = 2,                   # -1, None,
        innskudd_d          = 0,
        innskudd_d_desimal  = -1,                   # -1, None
        b_start_desimal     = -1,                   # -1, None
        b_slutt_desimal     = -1,                   # -1, None
    )

    # Finn start-beløpet
    tab_mat_el = mt.tabell_finn_el(tab_mat, n_he, _B_start_str)

    # Print tabell og svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg b) Hermod: Manuell brute force med binært søk"); print("")
    mt.tabell_print( # mt
        tab_mat             = tab_mat,
        tab_print_1_start   = tab_print_1_start,
        tab_print_1_slutt   = tab_print_1_slutt,
        tab_print_2_start   = tab_print_2_start,
        tab_print_2_slutt   = tab_print_2_slutt,
        tab_bredde          = tab_bredde,
        n_periode           = n_he
    )
    print(f"")
    print(f"- Hermod må ha et årlig innskudd på ca. {innskudd_he} kr")
    print(f"  for å få {tab_mat_el} kr like etter innskudd {n_he} ")

# b) Hermod > While-løkke - Matrix-effekt
if _blokk == -1:

    # While-løkken kjører så lenge beløpet er mindre enn 1 000 000
    _n_periode          = mt.sjekk_datatype(vari_navn = "n_periode", vari = n_he, typ = int)
    innskudd_he         = 0 # Debug fra 24000
    belop_start_ink_he  = 0 # Start på 0

    # Spinner
    i_spin              = 0 # Telle-variabel for spinner

    # Videre som argument inn i tabell
    _mat_matrix = mt.tabell_print_effekt(n_perioder    = b_20_he,
                                      mat_fx        = ["matrix", matrix_jp_ls, matrix_null_en_ls, matrix_f_ls, matrix_cut_off])

    # Kjør løkken så lenge start-beløpet nr. 20 er mindre enn en mill
    while belop_start_ink_he < b_20_he:

        # (*) Oppdater el med den økende verdien slik at neste el i _matrix_jp_null_ls kan brukes (lager variasjonen)
        _mat_matrix[2][0] = belop_start_ink_he

        # Spinner
        if is_spinning == 1: i_spin = mt.spinner(i_spin)

        # Debug > Lang utregning
        if belop_debug == 1: print(f"{_B_start_str} :: ", belop_start_ink_he)

        # Resetting
        tab_mat = mt.deepcopy(tab_mat_0)

        # Tøm terminal-skjerm for hvert run
        mt.system("clear")

        # Lager tabell
        tab_mat = mt.tabell_økonomi_lag(
            tab_mat             = tab_mat,
            tab_desimal         = None,                 # None, -1
            tab_print           = 1,
            tab_bredde          = tab_bredde,
            tab_is_farge        = tab_is_farge,
            tab_farge_typ       = tab_farge_typ_mat,    # Default: Hvit
            tab_fx              = _mat_matrix,          # Default: Ingen effekt
            vf                  = vf_he,
            n_periode           = n_he,
            aar_start           = aar_start_he,
            innskudd            = innskudd_he,
            innskudd_desimal    = 2,                    # -1, None,
            innskudd_d          = 0,
            innskudd_d_desimal  = -1,                   # -1, None
            b_start_desimal     = -1,                   # -1, None
            b_slutt_desimal     = -1,                   # -1, None
        )

        # Finn elementet
        belop_start_ink_he = mt.tabell_finn_el(tab_mat, _n_periode, _B_start_str)

        # Øker det neste innskudd_d_mi-argumentet neste tabell-iterasjon
        innskudd_he += 1

    # Dekrement med 1 for å få forrige innskudd_d_mi
    innskudd_he -= 1

    # Print tabell og svar-setninger
    # mt.oppg_strek(1)
    print("")
    _oppg_txt_s = mt.tabell_print_farge(f"------------------------------------------", tab_farge_typ_svar)
    _oppg_txt_1 = mt.tabell_print_farge(f"Oppg c) Hermod - While-løkke", tab_farge_typ_svar)
    _oppg_txt_2 = mt.tabell_print_farge(f"- Hermod må ha et årlig innskudd på ca. {innskudd_he} kr", tab_farge_typ_svar)
    _oppg_txt_3 = mt.tabell_print_farge(f"  for å få {b_20_he} kr like etter innskudd {_n_periode}", tab_farge_typ_svar)
    print(_oppg_txt_s)
    print(f""); print(_oppg_txt_1); print("")
    mt.tabell_print( # mt
        tab_bredde          = tab_bredde,
        tab_mat             = tab_mat,
        tab_print_1_start   = tab_print_1_start,
        tab_print_1_slutt   = tab_print_1_slutt,
        tab_print_2_start   = tab_print_2_start,
        tab_print_2_slutt   = tab_print_2_slutt,
        tab_is_farge        = tab_is_farge,
        tab_farge_typ       = tab_farge_typ_svar,
        n_periode           = _n_periode
    )
    print(f"")
    print(_oppg_txt_2)
    print(_oppg_txt_3)

# b) Hermod > 692 852 kr like etter innskudd 20 > import matematikk (CAS)
if _blokk == -1:

    # Variabler
    _n_periode = mt.sjekk_datatype(vari_navn = "_n_periode", vari = n_he, typ = int)

    # Geometrisk formel: B_n_mi_2 = b_1 * k ** (n - 1)
    for n in range(1, _n_periode + 1):
        B_n_he     = (INSK_he) * vf_he ** (n - 1)
        B_sum_he   += B_n_he

    # Løser likningen med superløs()
    insk = mt.superløs(variabel = INSK_he,
                       vs       = B_sum_he,
                       hs       = b_20_he,
                       rund     = tab_desimal,
                       debug    = -1)

    # Print svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg b) Hermod - import matematikk"); print(f"")
    print(f"- Hermod må ha et årlig innskudd på ca. {insk} kr")
    print(f"  for å få ca. {b_20_he} kr like etter innskudd {_n_periode} ")

# b) Hermod > 692 852 kr like etter innskudd 20 > import sympy (CAS)
if _blokk == -1:

    # Import
    import sympy as sp

    # Resett
    _n_periode  = mt.sjekk_datatype(vari_navn = "_n_periode", vari = n_he, typ = int)
    INSK_he     = sp.Symbol("IS__he")   # Hermod: CAS-variabel for årlig innskudd
    b_20_he     = 692852                # Hermod: Beløps-grense like etter innskudd nr. 20
    B_n_he      = sp.Symbol("B_n_he")   # Hermod: CAS-variabel for beløp nr. n
    B_sum_he    = 0                     # Hermod: CAS-variabel for summen av beløper

    # Geometrisk formel: B_n_mi_2 = b_1 * k ** (n - 1)
    for n in range(1, _n_periode + 1):
        B_n_he     = (INSK_he) * vf_he ** (n - 1)
        B_sum_he   += B_n_he

    # Lager likning
    likning_he = sp.Eq(B_sum_he, b_20_he)

    # Løser likningen
    insk_ls_he = sp.solve(likning_he, INSK_he, domain = sp.Reals)

    # Henter verdien i fra løsnings-settet
    insk_el_he = round(insk_ls_he[0], tab_desimal) # Her ble løsningen en liste

    # Print svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg b) Hermod - import sympy"); print(f"")
    print(f"- Hermod må ha et årlig innskudd på ca. {insk_el_he} kr")
    print(f"  for å få ca. {b_20_he} kr like etter innskudd {_n_periode} ")

# c) Miriam > Millionær > Manuell brute force med binært søk
if _blokk == -1:

    # Resetting
    tab_mat = mt.deepcopy(tab_mat_0)

    # 1 000 000: Prøver verdier fra 0 til 1836.33
    innskudd_d_mi = 1836.33 # 1655 (rente = 4)

    # Lager tabell
    tab_mat = mt.tabell_økonomi_lag(
        tab_mat             = tab_mat,
        tab_desimal         = -1,                   # None, -1
        tab_print           = -1,
        tab_bredde          = tab_bredde,
        vf                  = vf_mi,
        n_periode           = n_mi,
        aar_start           = aar_start_mi,
        innskudd            = innskudd_mi,
        innskudd_desimal    = 2,                    # -1, None,
        innskudd_d          = innskudd_d_mi,
        innskudd_d_desimal  = -1,                   # -1, None
        b_start_desimal     = None,                 # -1, None
        b_slutt_desimal     = None,                 # -1, None
    )

    # Finn start-beløpet
    tab_mat_el = mt.tabell_finn_el(tab_mat, n_mi, _B_start_str)

    # Print tabell og svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg c) Miriam: Manuell brute force med binært søk"); print("")
    mt.tabell_print(
        tab_mat             = tab_mat,
        tab_print_1_start   = tab_print_1_start,
        tab_print_1_slutt   = tab_print_1_slutt,
        tab_print_2_start   = tab_print_2_start,
        tab_print_2_slutt   = tab_print_2_slutt,
        tab_bredde          = tab_bredde,
        n_periode           = n_mi
    )
    print(f"")
    print(f"- Miriam må øke innskuddet med nøyaktig {innskudd_d_mi} kr")
    print(f"  for å få {tab_mat_el} kr like etter innskudd {n_mi} ")

# c) Miriam > Millionær > While-løkke
if _blokk == -1:

    # While-løkken kjører så lenge beløpet er mindre enn 1 000 000
    _n_periode          = mt.sjekk_datatype(vari_navn = "n_periode", vari = n_mi, typ = int)
    innskudd_d_mi       = 0 # 1655 # 1837
    belop_start_ink_mi  = 0

    # Kjør løkken så lenge start-beløpet nr. 20 er mindre enn en mill
    while belop_start_ink_mi < b_20_mi_2:

        # Resetting
        tab_mat = mt.deepcopy(tab_mat_0)

       # Regner ut tabellen
        tab_mat = mt.tabell_økonomi_lag(
            tab_mat             = tab_mat,
            tab_desimal         = None,             # None, -1
            tab_print           = -1,
            tab_bredde          = tab_bredde,
            vf                  = vf_mi,
            n_periode           = _n_periode,
            aar_start           = aar_start_mi,
            innskudd            = innskudd_mi,
            innskudd_desimal    = -1,               # -1, None,
            innskudd_d          = innskudd_d_mi,
            innskudd_d_desimal  = -1,               # -1, None
            b_start_desimal     = -1,               # -1, None
            b_slutt_desimal     = -1,               # -1, None
        )

        # Finn elementet
        belop_start_ink_mi = mt.tabell_finn_el(tab_mat, _n_periode, _B_start_str)

        # Øker det neste innskudd_d_mi-argumentet neste tabell-iterasjon
        innskudd_d_mi += 1

    # Dekrement med 1 for å få forrige innskudd_d_mi
    innskudd_d_mi -= 1

    # Print tabell og svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg c) Miriam - While-løkke"); print(f"")
    mt.tabell_print(
        tab_bredde          = tab_bredde,
        tab_mat             = tab_mat,
        tab_print_1_start   = tab_print_1_start,
        tab_print_1_slutt   = tab_print_1_slutt,
        tab_print_2_start   = tab_print_2_start,
        tab_print_2_slutt   = tab_print_2_slutt,
        n_periode           = n_mi
    )
    print(f"")
    print(f"- Miriam må øke innskuddet med ca. {innskudd_d_mi} kr")
    print(f"  for å få ca. {b_20_mi_2} kr like etter innskudd {_n_periode} ")

# c) Miriam > Millionær > import matematikk (CAS)
if _blokk == -1:

    # Resetting
    _n_periode = mt.sjekk_datatype(vari_navn = "_n_periode", vari = n_mi, typ = int)

    # Geometrisk formel: B_n_mi_2 = b_1 * k ** (n - 1)
    for n in range(1, _n_periode + 1):
        B_n_mi_2     = (innskudd_0_mi + (n - 1) * INSK_d_mi) * vf_mi ** (n - 1)
        B_sum_mi_2   += B_n_mi_2

    # Løser likningen med superløs()
    inn_d_val = mt.superløs(variabel = INSK_d_mi,
                            vs       = B_sum_mi_2,
                            hs       = b_20_mi_2,
                            rund     = tab_desimal,
                            debug    = -1)

    # Print svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg c) Miriam - import matematikk"); print(f"")
    print(f"- Miriam må øke innskuddet med ca. {inn_d_val} kr")
    print(f"  for å få ca. {b_20_mi_2} kr like etter innskudd {n_mi} ")

# c) Miriam > Millionær > import sympy (CAS)
if _blokk == -1:

    # Import
    import sympy as sp

    # Resett
    INSK_d_mi           = mt.Symbol("INSK_d_mi")    # Miriam: CAS-variabel for fast øking av innskudd
    B_n_mi_2            = mt.Symbol("B_n_mi_2")     # Miriam: CAS-variabel for beløp nr. n
    B_sum_mi_2          = 0                         # Miriam: CAS-variabel for summen av beløper
    b_20_mi_2           = 1000000                   # Miriam: Beløps-grense like etter innskudd nr. 20
    _n_periode          = mt.sjekk_datatype(vari_navn = "_n_periode", vari = n_mi, typ = int)

    # Geometrisk formel: B_n_mi_2 = b_1 * k ** (n - 1)
    for n in range(1, _n_periode + 1):
        B_n_mi_2     = (innskudd_0_mi + (n - 1) * INSK_d_mi) * vf_mi ** (n - 1)
        B_sum_mi_2   += B_n_mi_2

    # Lager likning
    likning_mi = sp.Eq(B_sum_mi_2, b_20_mi_2)

    # Løser likningen
    insk_ls_mi = sp.solve(likning_mi, INSK_d_mi, domain = sp.Reals)

    # Henter verdien i fra løsnings-settet
    insk_el_mi = round(insk_ls_mi[0], tab_desimal) # Her ble løsningen en liste

    # Print svar-setninger
    mt.oppg_strek(1)
    print(f""); print(f"Oppg c) Miriam - import sympy"); print(f"")
    print(f"- Miriam må øke innskuddet med ca. {insk_el_mi} kr")
    print(f"  for å få ca. {b_20_mi_2} kr like etter innskudd {n_mi} ")

