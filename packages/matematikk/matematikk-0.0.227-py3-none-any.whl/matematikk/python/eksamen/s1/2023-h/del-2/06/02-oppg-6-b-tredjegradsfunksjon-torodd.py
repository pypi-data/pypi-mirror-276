# 🚀 programmering.no | 🤓 matematikk.as
# S1 - Eksamen - 2023 Høst (Torodd)
# Oppgave 6 b) Tredjegradsfunksjon - Påstand 2: Alle linjer på formen y = ax + b vil skjære grafen til f 

from sympy import symbols, limit, oo

# definerer funksjonen og symbola
x, a, b, c, d = symbols("x a b c d")
f = a*x**3 + b*x**2 + c*x + d

# grense mot uendeleg
limit(f, x, oo)

# grense mot minus uendeleg
løsning = limit(f, x, -oo)
print(løsning)
