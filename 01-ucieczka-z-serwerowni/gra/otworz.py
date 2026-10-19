#!/usr/bin/env python3
"""Program otwierający sejf: sprawdza szyfr i regulamin sejfu, a potem wydaje fragment 3 hasła.

  ./otworz.py SZYFR             otwórz sejf
  ./otworz.py --kopia-zapasowa  przywróć dziennik lub szyfr, gdy zginą (kosztuje minuty kary)
"""
import os
import re
import stat
import sys
from pathlib import Path

SEJF = Path(__file__).resolve().parent
SWIAT = SEJF.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SWIAT / ".silnik"))
import silnik  # noqa: E402

DZIENNIK = SEJF / "dziennik-wejsc.txt"
SKRYTKA = SEJF / "skrytka"
SZYFR = SKRYTKA / "szyfr.txt"
WPIS = re.compile(r"^OTWIERA:\s*\S+", re.M)


def prawa(sciezka):
    """Prawa jak w ls -l (bez pierwszego znaku) i ósemkowo, np. ('rw-r--r--', '644')."""
    tryb = stat.S_IMODE(sciezka.stat().st_mode)
    return stat.filemode(tryb)[1:], f"{tryb:o}"


def kopia_zapasowa(stan):
    przywrocone = []
    dziennik = stan["sejf"]["dziennik"]
    try:
        obecny = DZIENNIK.read_text(encoding="utf-8")
    except OSError:
        obecny = None
    if obecny is None or not obecny.startswith(dziennik):
        if DZIENNIK.exists():
            os.chmod(DZIENNIK, 0o644)
        DZIENNIK.write_text(dziennik, encoding="utf-8")
        os.chmod(DZIENNIK, 0o444)
        przywrocone.append("dziennik-wejsc.txt (bez twojego wpisu, tylko do odczytu)")
    try:
        szyfr_jest = SZYFR.exists()
    except PermissionError:
        szyfr_jest = True                       # skrytka zamknięta, więc szyfr leży w środku
    if not szyfr_jest:
        SKRYTKA.mkdir(exist_ok=True)
        os.chmod(SKRYTKA, 0o700)
        SZYFR.write_text(f"SZYFR DO SEJFU: {stan['sejf']['kod']}\n", encoding="utf-8")
        os.chmod(SZYFR, 0o000)
        przywrocone.append("skrytka/szyfr.txt (znowu bez żadnych praw)")
    if not przywrocone:
        print("Nic nie zginęło - kopia zapasowa nie jest potrzebna.")
        return
    print("Z kopii zapasowej wróciło:")
    for nazwa in przywrocone:
        print(f"  {nazwa}")
    silnik.dolicz_kare(SWIAT, stan, "sejf: kopia zapasowa")


def sprawdz_regulamin(stan):
    braki = []
    oryginal = stan["sejf"]["dziennik"]
    try:
        dziennik = DZIENNIK.read_text(encoding="utf-8")
    except FileNotFoundError:
        dziennik = None
        braki.append("nie ma dziennika dziennik-wejsc.txt - przywróć go: ./otworz.py --kopia-zapasowa")
    except PermissionError:
        dziennik = None
        braki.append("nie mogę przeczytać dziennika - ktoś zabrał prawo odczytu (r)")
    if dziennik is not None:
        if not dziennik.startswith(oryginal):
            braki.append("dziennik został nadpisany - zniknęły dawne wpisy (czyżby > zamiast >>?); "
                         "przywróć go: ./otworz.py --kopia-zapasowa")
        elif not WPIS.search(dziennik[len(oryginal):]):
            braki.append("nie ma twojego wpisu w dzienniku - dopisz na końcu pliku dziennik-wejsc.txt "
                         "linię: OTWIERA: twoje imię")
    for sciezka, nazwa, wzor, liczba_wzor in ((SKRYTKA, "skrytka", "rwx------", "700"),
                                              (SZYFR, "szyfr.txt", "rw-------", "600")):
        try:
            symbol, liczba = prawa(sciezka)
        except FileNotFoundError:
            braki.append(f"nie ma: {nazwa} - przywróć szyfr: ./otworz.py --kopia-zapasowa")
            continue
        except PermissionError:
            braki.append(f"nie widzę, jakie prawa ma {nazwa} - skrytce brakuje prawa x")
            continue
        if liczba != liczba_wzor:
            braki.append(f"{nazwa} ma prawa {symbol} ({liczba}), a ma mieć {wzor} - "
                         "ustaw je poleceniem chmod z liczbą ósemkową")
    return braki


def main():
    stan = silnik.wczytaj_stan(SWIAT)
    silnik.naglowek("SEJF - PROGRAM OTWIERAJĄCY")
    if not os.access(__file__, os.X_OK):
        print("ODMOWA. CERBER słucha tylko programów, które mają prawo wykonywania (x).")
        print("Zobacz prawa: ls -l otworz.py")
        print("Gdy dasz mi prawo x, uruchom mnie jak program: ./otworz.py SZYFR")
        return 1
    argumenty = sys.argv[1:]
    if argumenty == ["--kopia-zapasowa"]:
        kopia_zapasowa(stan)
        return 0
    if len(argumenty) != 1:
        print("Użycie: ./otworz.py SZYFR")
        print("Szyfr leży w pliku skrytka/szyfr.txt.")
        return 2
    if argumenty[0].strip() != stan["sejf"]["kod"]:
        print("ZŁY SZYFR. Sejf ani drgnie.")
        print("Prawdziwy szyfr leży w pliku skrytka/szyfr.txt.")
        return 1
    print("Szyfr się zgadza. CERBER sprawdza regulamin sejfu...")
    print()
    braki = sprawdz_regulamin(stan)
    if braki:
        silnik.wypisz_braki(braki)
        return 1
    print("Zamek szczęka, drzwi sejfu się uchylają.")
    print()
    silnik.wydaj_fragment(SWIAT, stan, 3, "sejf")
    return 0


if __name__ == "__main__":
    sys.exit(main())
