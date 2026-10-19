"""Nowy projekt: gdzie najtaniej kupić konsolę? Napisany pod bibliotekę kantor 2.x."""
import kantor

sklepy = [
    ["Polska", 2099, "PLN"],
    ["Niemcy", 449, "EUR"],
    ["USA", 499, "USD"],
    ["Wielka Brytania", 429, "GBP"],
]

print(f"Porównywarka cen konsoli (kantor {kantor.__version__})")
print()
najtanszy_kraj = None
najnizsza_cena = None
for kraj, cena, waluta in sklepy:
    w_zlotych = kantor.przelicz(cena, waluta, "PLN")
    print(f"{kraj:<16} {cena:>5} {waluta} = {w_zlotych:8.2f} zł")
    if najnizsza_cena is None or w_zlotych < najnizsza_cena:
        najtanszy_kraj = kraj
        najnizsza_cena = w_zlotych
print()
print(f"Najtaniej: {najtanszy_kraj}, {najnizsza_cena:.2f} zł")
