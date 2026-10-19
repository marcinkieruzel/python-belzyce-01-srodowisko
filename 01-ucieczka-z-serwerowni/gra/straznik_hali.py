#!/usr/bin/env python3
"""Strażnik hali serwerów: sprawdza sprzątanie z CZYTAJ_MNIE.txt i wydaje fragment 4 hasła.

  python3 straznik.py                   sprawdź halę
  python3 straznik.py --kopia-zapasowa  przywróć usunięte logi i kopie .bak (kosztuje minuty kary)
"""
import sys
from pathlib import Path

HALA = Path(__file__).resolve().parent
SWIAT = HALA.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SWIAT / ".silnik"))
import silnik  # noqa: E402

LOGI = HALA / "logi"
KOSZ = HALA / "kosz"


def pliki(katalog):
    """Nazwy plików w katalogu (razem z ukrytymi); pusty zbiór, gdy katalogu nie ma."""
    if not katalog.is_dir():
        return set()
    return {p.name for p in katalog.iterdir() if p.is_file()}


def sprawdz(stan):
    dane = stan["hala"]
    w_logach, w_koszu = pliki(LOGI), pliki(KOSZ)
    braki = []

    # .tmp — wszystkie usunięte
    tmp_w_logach = sorted(n for n in w_logach if n.endswith(".tmp"))
    if tmp_w_logach:
        ukryte = [n for n in tmp_w_logach if n.startswith(".")]
        opis = f"w logi/ są jeszcze pliki .tmp: {len(tmp_w_logach)}"
        if ukryte and len(ukryte) == len(tmp_w_logach):
            opis += " - ukryte (nazwa zaczyna się od kropki, a do takich nazw *.tmp nie pasuje; ls -a)"
        braki.append(opis)
    tmp_w_koszu = [n for n in w_koszu if n.endswith(".tmp")]
    if tmp_w_koszu:
        braki.append(f"w kosz/ są pliki .tmp: {len(tmp_w_koszu)} - "
                     "pliki tymczasowe miały zostać usunięte, a nie przeniesione")

    # .bak — wszystkie w koszu
    if not KOSZ.is_dir():
        braki.append("nie ma katalogu kosz/ (ma stać w hali, obok logi/)")
    bak_w_logach = [n for n in w_logach if n.endswith(".bak")]
    if bak_w_logach:
        braki.append(f"w logi/ są jeszcze pliki .bak: {len(bak_w_logach)} - przenieś je do kosz/")
    bak_zgubione = [n for n in dane["bak"] if n not in w_logach and n not in w_koszu]
    if bak_zgubione:
        braki.append(f"brakuje plików .bak: {len(bak_zgubione)} - nie ma ich ani w logi/, ani w kosz/; "
                     "usunięte pliki nie wracają, ale pan Piotr ma kopię: python3 straznik.py --kopia-zapasowa")

    # .log — wszystkie zostają w logi/
    log_zgubione = sorted(n for n in dane["log"] if n not in w_logach)
    log_w_koszu = [n for n in log_zgubione if n in w_koszu]
    log_usuniete = [n for n in log_zgubione if n not in w_koszu]
    if log_w_koszu:
        braki.append(f"w kosz/ są pliki .log: {len(log_w_koszu)}, np. {log_w_koszu[0]} - "
                     "logi mają zostać w logi/")
    if log_usuniete:
        opis = f"brakuje plików .log: {len(log_usuniete)}, np. {log_usuniete[0]}"
        pulapki = [n for n in log_usuniete if ".tmp." in n or ".bak." in n]
        if pulapki:
            opis += (f" - uwaga na wzorce: {pulapki[0]} kończy się na .log, więc *.tmp i *.bak "
                     "do niego nie pasują, ale *tmp* albo *bak* - już tak")
        opis += "; rm nie ma kosza, ale pan Piotr ma kopię: python3 straznik.py --kopia-zapasowa"
        braki.append(opis)

    # katalogi do usunięcia
    if (HALA / "stary-serwer").exists():
        braki.append("katalog stary-serwer/ wciąż stoi (jest pusty)")
    if (HALA / "zepsuty-serwer").exists():
        braki.append("katalog zepsuty-serwer/ wciąż stoi (nie jest pusty, więc rmdir go nie usunie)")
    return braki


def kopia_zapasowa(stan):
    dane = stan["hala"]
    w_logach, w_koszu = pliki(LOGI), pliki(KOSZ)
    brakujace = [n for n in dane["log"] + dane["bak"] if n not in w_logach and n not in w_koszu]
    if not brakujace:
        print("Nic nie zginęło - kopia zapasowa nie jest potrzebna.")
        return
    LOGI.mkdir(exist_ok=True)
    for nazwa in brakujace:
        (LOGI / nazwa).write_text(silnik.tresc_pliku_hali(nazwa), encoding="utf-8")
    print(f"Pan Piotr przywrócił do logi/ pliki z kopii zapasowej: {len(brakujace)}.")
    silnik.dolicz_kare(SWIAT, stan, "hala: kopia zapasowa")


def main():
    stan = silnik.wczytaj_stan(SWIAT)
    silnik.naglowek("STRAŻNIK HALI SERWERÓW")
    if "--kopia-zapasowa" in sys.argv[1:]:
        kopia_zapasowa(stan)
        return 0
    braki = sprawdz(stan)
    if braki:
        silnik.wypisz_braki(braki)
        return 1
    print("Dyski odetchnęły, wentylatory zwalniają. CERBER mruczy z zadowolenia.")
    print()
    silnik.wydaj_fragment(SWIAT, stan, 4, "hala")
    return 0


if __name__ == "__main__":
    sys.exit(main())
