#!/usr/bin/env python3
"""Strażnik magazynu: sprawdza porządki z CZYTAJ_MNIE.txt i wydaje fragment 2 hasła.

  python3 straznik.py                   sprawdź magazyn
  python3 straznik.py --kopia-zapasowa  przywróć zgubione paczki i pliki (kosztuje minuty kary)
"""
import sys
from pathlib import Path

MAGAZYN = Path(__file__).resolve().parent
SWIAT = MAGAZYN.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SWIAT / ".silnik"))
import silnik  # noqa: E402

REGALY = ["regal-A", "regal-B", "regal-C"]
KATALOGI = [f"{regal}/polka-{nr}" for regal in REGALY for nr in (1, 2, 3)] + ["zwroty"]
SPIS_STARA_NAZWA = "Spis Inwentarza (kopia) FINAL.TXT"
SPIS = "spis-inwentarza.txt"
INSTRUKCJA = "instrukcja-bhp.txt"


def wzgledna(sciezka):
    tekst = str(sciezka.relative_to(MAGAZYN))
    return "magazyn" if tekst == "." else tekst


def gdzie_lezy(nazwa):
    """Katalogi (względem magazynu), w których leży plik o tej nazwie."""
    return sorted(wzgledna(p.parent) for p in MAGAZYN.rglob(nazwa) if p.is_file())


def pod_inna_nazwa(tekst):
    """Pliki w magazynie z taką treścią — gdy paczka dostała inną nazwę (np. mv do nieistniejącego katalogu)."""
    wzor = silnik.skrot(tekst)
    return sorted(wzgledna(p) for p in MAGAZYN.rglob("*") if p.is_file() and silnik.skrot_pliku(p) == wzor)


def podobny_katalog(oczekiwany):
    """Szuka katalogu, który różni się od oczekiwanego tylko wielkością liter."""
    sciezka = MAGAZYN
    for czesc in Path(oczekiwany).parts:
        if (sciezka / czesc).is_dir():
            sciezka = sciezka / czesc
            continue
        if not sciezka.is_dir():
            return None
        for kandydat in sciezka.iterdir():
            if kandydat.is_dir() and kandydat.name.lower() == czesc.lower():
                return str(kandydat.relative_to(MAGAZYN))
        return None
    return None


def sprawdz(stan):
    dane = stan["magazyn"]
    braki = []

    # 1. regały i półki
    brakujace = [k for k in KATALOGI if not (MAGAZYN / k).is_dir()]
    if brakujace:
        braki.append("brakuje katalogów: " + ", ".join(brakujace))
        for k in brakujace:
            if (MAGAZYN / k).is_file():
                braki.append(f"{k} to plik, a nie katalog - mv do katalogu, którego nie ma, zmienia "
                             f"tylko nazwę pliku; zobacz, co to za plik: cat {k}")
                continue
            podobny = podobny_katalog(k)
            if podobny:
                braki.append(f"jest katalog {podobny}, a ma być {k} - Linux rozróżnia wielkie i małe litery")

    # 2. paczki z rampy
    na_rampie = []
    for nazwa, etykieta in sorted(dane["paczki"].items()):
        miejsca = gdzie_lezy(nazwa)
        if not miejsca:
            inne = pod_inna_nazwa(dane["teksty"][nazwa])
            if inne:
                braki.append(f"paczka {nazwa} leży pod inną nazwą: {', '.join(inne)} - "
                             "przywróć jej nazwę (mv)")
            else:
                braki.append(f"paczka {nazwa} zniknęła z magazynu (usunięta?) - "
                             "pani Halina ma kopię: python3 straznik.py --kopia-zapasowa")
        elif len(miejsca) > 1:
            braki.append(f"paczka {nazwa} leży w kilku miejscach naraz ({', '.join(miejsca)}) - "
                         "paczki się przenosi (mv), a nie kopiuje (cp); zbędne kopie usuń")
        elif miejsca[0] == "rampa":
            na_rampie.append(nazwa)
        elif miejsca[0] != etykieta:
            braki.append(f"paczka {nazwa} leży w złym miejscu ({miejsca[0]}) - "
                         "przeczytaj etykietę w środku paczki (cat)")
    if na_rampie:
        braki.append(f"na rampie leży jeszcze {len(na_rampie)} z {len(dane['paczki'])} paczek: "
                     + ", ".join(na_rampie))

    # 3. instrukcja BHP: oryginał w magazynie i kopia w każdym regale
    wzor = silnik.skrot(dane["instrukcja"])
    if not (MAGAZYN / INSTRUKCJA).is_file():
        braki.append(f"oryginał {INSTRUKCJA} zniknął z magazynu - miał zostać skopiowany (cp), "
                     "a nie przeniesiony (mv); odłóż jedną kopię na miejsce")
    elif silnik.skrot_pliku(MAGAZYN / INSTRUKCJA) != wzor:
        braki.append(f"oryginał {INSTRUKCJA} ma zmienioną treść")
    bez_instrukcji = [r for r in REGALY if silnik.skrot_pliku(MAGAZYN / r / INSTRUKCJA) != wzor]
    if bez_instrukcji:
        braki.append(f"brakuje kopii {INSTRUKCJA} w: " + ", ".join(bez_instrukcji))

    # 4. spis inwentarza pod nową nazwą
    if (MAGAZYN / SPIS_STARA_NAZWA).exists():
        braki.append(f'plik "{SPIS_STARA_NAZWA}" ma wciąż starą nazwę - zmień ją na {SPIS} '
                     "(nazwę ze spacjami weź w cudzysłów albo dopełnij klawiszem Tab)")
    elif not (MAGAZYN / SPIS).is_file():
        braki.append(f"nie widzę pliku {SPIS} (sprawdź pisownię: ls)")
    elif silnik.skrot_pliku(MAGAZYN / SPIS) != silnik.skrot(dane["spis"]):
        braki.append(f"{SPIS} ma inną treść niż dawny spis - to ma być ten sam plik, tylko pod nową nazwą")

    # 5. zgłoszenie gotowości
    gotowe = MAGAZYN / "gotowe.txt"
    if not gotowe.is_file():
        braki.append("brakuje pustego pliku gotowe.txt w magazynie (touch)")
    elif gotowe.stat().st_size > 0:
        braki.append("plik gotowe.txt ma być pusty")
    return braki


def kopia_zapasowa(stan):
    dane = stan["magazyn"]
    przywrocone = []
    for nazwa, tekst in dane["teksty"].items():
        if not gdzie_lezy(nazwa) and not pod_inna_nazwa(tekst):
            (MAGAZYN / "rampa").mkdir(exist_ok=True)
            (MAGAZYN / "rampa" / nazwa).write_text(tekst, encoding="utf-8")
            przywrocone.append(f"rampa/{nazwa}")
    if not gdzie_lezy(INSTRUKCJA):
        (MAGAZYN / INSTRUKCJA).write_text(dane["instrukcja"], encoding="utf-8")
        przywrocone.append(INSTRUKCJA)
    if not (MAGAZYN / SPIS_STARA_NAZWA).exists() and not gdzie_lezy(SPIS):
        (MAGAZYN / SPIS_STARA_NAZWA).write_text(dane["spis"], encoding="utf-8")
        przywrocone.append(SPIS_STARA_NAZWA)
    if not przywrocone:
        print("Nic nie zginęło - kopia zapasowa nie jest potrzebna.")
        return
    print("Pani Halina przyniosła z kopii zapasowej:")
    for nazwa in przywrocone:
        print(f"  {nazwa}")
    silnik.dolicz_kare(SWIAT, stan, "magazyn: kopia zapasowa")


def main():
    stan = silnik.wczytaj_stan(SWIAT)
    silnik.naglowek("STRAŻNIK MAGAZYNU")
    if "--kopia-zapasowa" in sys.argv[1:]:
        kopia_zapasowa(stan)
        return 0
    braki = sprawdz(stan)
    if braki:
        silnik.wypisz_braki(braki)
        return 1
    print("Magazyn lśni. Pani Halina byłaby dumna.")
    print()
    silnik.wydaj_fragment(SWIAT, stan, 2, "magazyn")
    return 0


if __name__ == "__main__":
    sys.exit(main())
