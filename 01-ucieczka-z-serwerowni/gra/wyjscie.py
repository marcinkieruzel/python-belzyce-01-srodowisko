#!/usr/bin/env python3
"""Terminal przy drzwiach wyjściowych: pyta o hasło awaryjne (4 fragmenty) i mierzy czas ucieczki."""
import re
import sys
import time
from pathlib import Path

SWIAT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SWIAT / ".silnik"))
import silnik  # noqa: E402

STREFY = {2: "magazyn", 3: "sejf", 4: "hala"}


def wypisz_wynik(stan):
    kara = silnik.minuty_kary(stan)
    czas = stan["koniec"] - stan["start"] + kara * 60
    print("+" + "-" * 46 + "+")
    print("|" + " " * 46 + "|")
    print(f"|{'DRZWI OTWARTE. WYCHODZISZ NA ZEWNĄTRZ.':^46}|")
    print("|" + " " * 46 + "|")
    print("+" + "-" * 46 + "+")
    print()
    print(f"Twój czas: {silnik.formatuj_czas(czas)}")
    if kara:
        print(f"(w tym {kara} min kary za kopie zapasowe)")
    komendy = SWIAT / "moje-komendy.txt"
    try:
        linie = [l for l in komendy.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    except OSError:
        linie = []
    print()
    if linie:
        print(f"Bonus zaliczony: historia poleceń w moje-komendy.txt (linii: {len(linie)}).")
    else:
        print("Bonus dla chętnych: zapisz historię swoich poleceń do pliku:")
        print("  history > ~/serwerownia/moje-komendy.txt")


def main():
    stan = silnik.wczytaj_stan(SWIAT)
    silnik.naglowek("DRZWI WYJŚCIOWE - TERMINAL AWARYJNY")
    if stan.get("koniec"):
        print("Te drzwi są już otwarte. CERBER pamięta twój wynik:")
        print()
        wypisz_wynik(stan)
        return 0

    zaliczone = [f"{nr} ({nazwa})" for nr, nazwa in STREFY.items() if nazwa in stan.get("ukonczone", {})]
    if zaliczone:
        print("Strażnicy wydali już fragmenty: " + ", ".join(zaliczone) + ".")
    print("Hasło awaryjne to cztery fragmenty po kolei, np.: lis-kot-pies-mysz")
    print()
    try:
        odpowiedz = input("Hasło: ")
    except EOFError:
        print()
        return 1
    podane = [s for s in re.split(r"[\s,;:-]+", odpowiedz.strip().lower()) if s]
    if len(podane) != 4:
        print(f"CERBER: hasło ma 4 fragmenty, a podano {len(podane)}.")
        return 1
    zle = [str(i + 1) for i, (a, b) in enumerate(zip(podane, stan["fragmenty"])) if a != b]
    if zle:
        print("CERBER: HASŁO ODRZUCONE.")
        print("Nie zgadzają się fragmenty nr: " + ", ".join(zle) + ".")
        if podane[0] == stan["wabik"]:
            print("Fragment 1 pochodzi z unieważnionej koperty. Prawdziwa leży gdzie indziej.")
        return 1

    stan["koniec"] = time.time()
    silnik.zapisz_stan(SWIAT, stan)
    print("CERBER: HASŁO PRZYJĘTE. Blokada zdjęta.")
    print()
    wypisz_wynik(stan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
