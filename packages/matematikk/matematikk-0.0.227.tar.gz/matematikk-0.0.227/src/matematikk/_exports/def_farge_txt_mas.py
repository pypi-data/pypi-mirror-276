import matematikk as mt

def farge_txt(txt = str(), tab_farge_typ = str()):

    # - Alternativ
    # - $ pip install colorama
    # - import colorama
    # - min_farge_txt = f"{colorama.Fore.GREEN}min_txt{colorama.Style.RESET_ALL}"
    # - print(min_farge_txt)
 
    # Farge
    if tab_farge_typ == "blå":          return f"{mt.Fore.BLUE}      {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "grønn":        return f"{mt.Fore.GREEN}     {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "magentea":     return f"{mt.Fore.MAGENTA}   {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "rød":          return f"{mt.Fore.RED}       {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "gul":          return f"{mt.Fore.YELLOW}    {txt}{mt.Style.RESET_ALL}"

    # Ingen farge (bypass)
    return txt


##########################################
# farge_txt()
##########################################

# Alias > 1 > farge_txt
farge_tekst = farge_txt

# Alias > 2 > ...

