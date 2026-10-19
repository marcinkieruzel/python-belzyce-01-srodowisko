"""Stary projekt: ile waluty dostaniesz na wycieczkę klasową. Napisany rok temu pod bibliotekę kantor 1.x."""
import kantor

print(f"Kalkulator kieszonkowego (kantor {kantor.__version__})")
print()
print("Kursy w kantorze:")
for waluta, kurs in kantor.KURSY.items():
    print(f"  1 {waluta} = {kurs:.2f} zł")
print()

kieszonkowe = 400
for waluta in ["CZK", "EUR"]:
    print(f"{kieszonkowe} zł to {kantor.przelicz(kieszonkowe, waluta)} {waluta}")
