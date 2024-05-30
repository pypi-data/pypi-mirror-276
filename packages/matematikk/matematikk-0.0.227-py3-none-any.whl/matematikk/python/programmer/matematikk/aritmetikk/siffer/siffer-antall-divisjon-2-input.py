# 🚀 programmering.no | 🤓 matematikk.as
# - Finn antall siffer i et heltall

# Input
n = input("Tall: ")

# Regner ut antall siffer i heltallet n
def siffer_antall_divisjon(n):

    # Type cast inp-str -> int
    n = int(n)

    # Nullstill
    siffer_ant = 0

    # Itererer frem antall siffer (stop når n = 0)
    while n != 0:
        siffer_ant += 1   # Øk antall siffer med 1 for hver iterasjon
        n = int(n / 10)   # Eks: 371 (3 siffer) / 10 = 37.1 => int(37.1) = 37 (2 siffer) => ... => int(3.7) = 3 (1 siffer)

    return siffer_ant

# Antall siffer i heltallet n
siffer_ant = siffer_antall_divisjon(n)

# Print
print(f"Antall siffer i {n} er: {siffer_ant}")
