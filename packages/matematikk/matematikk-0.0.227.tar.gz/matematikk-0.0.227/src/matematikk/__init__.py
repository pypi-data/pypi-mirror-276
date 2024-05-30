# Versjon: 0.0.226

# '''

# os
from os import(
    system,
    )

# copy
from copy import(
    deepcopy,
    )

# numpy
from numpy import(
    random,
    mean,
    sqrt,

    polyfit,
    )

# sympy
from sympy import (
    ConditionSet,
    core,
    diff,
    Eq,
    FiniteSet,
    Intersection,
    ln,
    log,
    nsolve,
    Reals,
    solve,
    solveset,
    Symbol,
    )

# colorama
from colorama import(
    Style,
    Fore,
    )

# DEV
# - Dobbelsjekk alle export-funk med her og faktisk fil-liste
# - Sjekk import innsiden / utsiden av funk


##########################################
# import matematikk
##########################################

##########################################
# DEV > ... > Ingen dependencies
##########################################

# sjekk_datatype()
from ._exports.def_sjekk_datatype_mas import (
    sjekk_datatype,

    # Alias > 1 > ...

    # Alias > 2 > ...
    datatype_sjekk,
    )

# oppg_strek()
from ._exports.def_oppg_strek_mas import (
    oppg_strek,

    # Alias > 1 > ...

    # Alias > 2 > ...
    strek_oppg,
    )

# spinner()
from ._exports.def_spinner_mas import (
    spinner,
    )

##########################################
# DEV > ... > Dependencies > Skriv på!
##########################################

# farge_txt()
# - Dep 1 > matematikk
# - Dep 2 > - colorama
from ._exports.def_farge_txt_mas import (
    farge_txt,

    # Alias > 1 > ...
    farge_tekst,

    # Alias > 2 > ...
    )

# sannsynlighet_x_fra_mu_sd()
# - Dep 1 > matematikk
# - Dep 2 > - colorama
# - Dep 3 > - numpy
from ._exports.def_normalfordeling_standard_mas import (
    sannsynlighet_x_fra_mu_sd,
    sannsynlighet_x_mindre_enn_fra_mu_sd,
    sannsynlighet_gjennomsnitt_x_fra_mu_sd,
    sannsynlighet_hypotese_test_fra_mu_sd,
    sannsynlighet_for_x,
 
    # Alias > 1 > sannsynlighet_x_fra_mu_sd
    sannsynlighet_X_fra_mu_sd,
    sannsynlighet_k_fra_mu_sd,
    sannsynlighet_gunstig_fra_mu_sd,

    # Alias > 1 > sannsynlighet_x_mindre_enn_fra_mu_sd
    sannsynlighet_x_storre_enn_fra_mu_sd,

    # Alias > 1 > sannsynlighet_gjennomsnitt_x_fra_mu_sd
    sannsynlighet_gjennomsnitt_x_mindre_fra_mu_sd,

    # Alias > 1 > sannsynlighet_hypotese_test_fra_mu_sd > ...

    # Alias > 1 > sannsynlighet_for_x
    sannsynlighet_for_k,

    )

# tabell / funks
from ._exports.def_tabell_mas import (
    tabell_print_effekt,
    tabell_print_farge,
    tabell_print_kolonne_padding,
    tabell_print_rad,
    tabell_print,
    tabell_finn_el,
    tabell_økonomi_lag,

    # Alias > 1
    tabell_okonomi_lag,
    )

# deriver()
from ._exports.def_deriver_mas import (
    deriver,

    # Alias > 1
    derivert,
    momentan_vekst,
    momentan_vekstfart,
    )

# DEV > Fix filnavn og linjen under til _mas slik at ulik fra funk
# vekstfaktor()
from ._exports.def_vekstfaktor import (
    vekstfaktor
    )

# DEV > Fix filnavn og linjen under til _mas slik at ulik fra funk
# vekstfaktor_cas()
from ._exports.def_vekstfaktor_cas import (
    vekstfaktor_cas,
    )

# reggis()
from ._exports.def_reggis_matematikk_mas import (
    reggis,

    # Alias > 1
    reggis_cas,
    regresjon,
    regresjon_cas,
    regresjon_polynom,
    regresjon_polynom_cas,

    # Alias > 2
    cas_regresjon,
    cas_regresjon_polynom,
    regresjon_polynom_cas,
    )

# superlos()
from ._exports.def_superlos_matematikk_mas import (
    superløs,

    # Alias > 1
    los,
    losning,
    løs,
    løsning,
    superlos,
    super_los,
    super_løs,

    # Alias > 2
    los_super,
    løs_super,
    )

# ekstremalpunkt_max()
from ._exports.def_ekstremalpunkt_max_mas import (
    ekstremalpunkt_max,

    # Alias > 1
    ekstremalpunkt_maks,
    ekstremalpunkt_maksimalt,
    toppunkt,

    # Alias > 2 > ...
    )

# overskudd_max()
from ._exports.def_enhet_fra_overskudd_max_mas import (
    enhet_fra_overskudd_max,

    # Alias > 1
    enhet_fra_overskudd_maks,
    enhet_fra_overskudd_maksimalt,
    enhet_fra_overskudd_mest,
    enhet_fra_overskudd_storst,
    enhet_fra_overskudd_størst,

    # Alias > 2
    enhet_fra_maks_overskudd,
    enhet_fra_maksimalt_overskudd,
    enhet_fra_mest_overskudd,
    enhet_fra_storst_overskudd,
    enhet_fra_størst_overskudd,
    )

# enhet_fra_overskudd_max_med_kostnad()
from ._exports.def_enhet_fra_overskudd_max_med_kostnad_mas import (
    enhet_fra_overskudd_max_med_kostnad,

    # Alias > 1 ...
    enhet_fra_overskudd_max_kostnad,

    # Alias > 2 > ...
    enhet_fra_max_overskudd_med_kostnad,
    enhet_fra_max_overskudd_kostnad,
    )

# enhet_og_pris_fra_inntekt_max()
from ._exports.def_enhet_og_pris_fra_inntekt_max_mas import (
    enhet_og_pris_fra_inntekt_max,

    # Alias > 1
    enhet_og_pris_fra_inntekt_max,

    # Alias > 2 > ...
    )

# Alle svar
# økonomi()
from ._exports.def_alle_svar_okonomi_mas import (
    økonomi,

    # Alias > 1
    # enhet_og_pris_fra_inntekt_max,

    # Alias > 2 > ...
    )

# Alle svar
# eksamen()
from ._exports.def_alle_svar_eksamen_mas import (
    eksamen,

    # Alias > 1
    # enhet_og_pris_fra_inntekt_max,

    # Alias > 2 > ...
    )

# '''
