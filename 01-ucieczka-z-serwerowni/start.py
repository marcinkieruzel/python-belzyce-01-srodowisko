#!/usr/bin/env python3
"""Ucieczka z serwerowni — gra terenowa w terminalu. Ten program buduje świat gry w ~/serwerownia.

Użycie:
  python3 start.py             tworzy świat gry (jeśli jeszcze go nie ma)
  python3 start.py --od-nowa   usuwa stary świat gry i buduje nowy: nowe hasło, czas od zera
  python3 start.py --napraw    przywraca skrypty strażników, gdy któryś zniknie (postęp zostaje)
"""
import argparse
import os
import random
import secrets
import shutil
import sys
import time
from pathlib import Path

TUTAJ = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(TUTAJ / "gra"))
import silnik  # noqa: E402

SWIAT = Path.home() / "serwerownia"

# plik w folderze gra/  ->  miejsce w świecie gry
SKRYPTY = {
    "silnik.py": ".silnik/silnik.py",
    "straznik_magazynu.py": "magazyn/straznik.py",
    "otworz.py": "sejf/otworz.py",          # celowo bez prawa wykonywania (x) — to zagadka poziomu 3
    "straznik_hali.py": "hala/straznik.py",
    "wyjscie.py": "wyjscie.py",
}

# słowa na fragmenty hasła: bez polskich znaków, żeby łatwo je wpisać
SLOWA = [
    "kometa", "orbita", "rakieta", "planeta", "meteor", "galaktyka", "satelita", "teleskop",
    "kompas", "latarnia", "wulkan", "piorun", "burza", "tornado", "lawina", "gejzer",
    "magnes", "laser", "radar", "turbina", "dynamo", "bateria", "antena", "procesor",
    "pingwin", "tygrys", "jaguar", "delfin", "rekin", "panda", "koala", "zebra",
    "gepard", "kameleon", "borsuk", "wydra", "bocian", "sowa", "kruk", "smok",
    "feniks", "gryf", "pegaz", "kraken", "golem", "tytan", "cyklop", "hydra",
]


def zapisz(sciezka, tekst, tryb=0o644):
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    sciezka.write_text(tekst, encoding="utf-8")
    os.chmod(sciezka, tryb)


# =============================================================================================
#  Teksty
# =============================================================================================
WSTEP = """\
============================================================
  UCIECZKA Z SERWEROWNI
============================================================

Piątek, 21:47. Lubelskie Centrum Danych, poziom -1.

Zostajesz po praktykach dłużej, żeby dokończyć konfigurację
serwera. Nagle gaśnie główne światło, a z głośników słychać:

  "CERBER: WYKRYTO INTRUZA. BLOKADA WSZYSTKICH DRZWI."

CERBER to system bezpieczeństwa budynku. Telefon nie ma
zasięgu. Działa tylko ten terminal.

Drzwi otworzy hasło awaryjne. Administrator, pan Mariusz,
podzielił je na cztery fragmenty i rozdzielił między strefy:

  recepcja/   fragment 1 - trop zaczyna się tutaj i prowadzi do archiwum/
  magazyn/    fragment 2 - wyda go strażnik magazynu
  sejf/       fragment 3 - wyda go program otwierający sejf
  hala/       fragment 4 - wyda go strażnik hali serwerów

W każdej strefie leży plik CZYTAJ_MNIE.txt z zadaniem.
Strefy możesz przechodzić w dowolnej kolejności, ale
najłatwiej po kolei: recepcja, magazyn, sejf, hala.

Gdy zbierzesz cztery fragmenty, wróć tutaj i uruchom:

  python3 wyjscie.py

CERBER liczy czas od startu gry. Powodzenia.

Zasady:
- Wszystko zrobisz w terminalu: pwd, ls, cd, cat, mkdir,
  cp, mv, rm, touch, chmod. Edytor nie jest potrzebny.
- Nie ruszaj pliku .stan ani katalogu .silnik - to pamięć
  i mózg CERBERA.
- Gdy zniknie któryś skrypt strażnika, w folderze z grą
  uruchom: python3 start.py --napraw
"""

RECEPCJA = """\
RECEPCJA - poziom 1: orientacja w terenie
-----------------------------------------

Na ladzie leży kartka od portiera, pana Zdzisława:

  "Hasło awaryjne? Pierwszą część Mariusz schował gdzieś
   w archiwum (katalog archiwum/ obok recepcji). Gdzie
   dokładnie - nie wiem. Na moim biurku leżą papiery
   z kadr, może pomogą. I uważaj: Mariusz lubi rzeczy,
   których nie widać."

Zadanie: znajdź w archiwum kopertę z fragmentem 1 hasła.
Ten fragment nie wyda żaden strażnik - po prostu go zapisz.

Przydadzą się:
  pwd        gdzie jestem?
  ls         co tu leży?
  ls -a      co tu leży, razem z ukrytymi plikami
             (ukryty plik lub katalog ma nazwę zaczynającą się od kropki)
  cd KATALOG wejdź do katalogu
  cd ..      wyjdź piętro wyżej
  cd ~       wróć do katalogu domowego
  cat PLIK   pokaż zawartość pliku

Klawisz Tab dopełnia nazwy plików i katalogów. Używaj go!
"""

TABLICA = """\
TABLICA OGŁOSZEŃ
----------------

* Archiwum jest ułożone według lat. Każdy rocznik ma swój
  katalog: archiwum/2015, archiwum/2016 i tak dalej.

* Prośba od pana Mariusza: nie ruszajcie moich prywatnych
  rzeczy w archiwum. Trzymam je w roczniku, w którym
  zacząłem tu pracę. Zresztą i tak ich nie zobaczycie.

* Kto zostawił kubek z herbatą na serwerze nr 3?!
  - A. Kowalczyk
"""

KADRY = """\
LUBELSKIE CENTRUM DANYCH - LISTA PRACOWNIKÓW (wyciąg z kadr)

Nazwisko i imię      Stanowisko                 Rok zatrudnienia
-----------------------------------------------------------------
Kowalczyk Anna       kierowniczka zmiany        2015
Nowak Zdzisław       portier                    2016
Wrona Mariusz        administrator systemów     2017
Lis Halina           kierowniczka magazynu      2019
Mazur Piotr          technik serwerowni         2021
Zając Ola            praktykantka               2024
"""

NOTATKA_PORTIERA = """\
Notatka portiera (na odwrocie paragonu):

Mariusz zawsze powtarza, że najważniejsze rzeczy trzyma
w trzeciej szufladzie swojego biurka. Biurko stoi tam,
gdzie jego prywatne rzeczy.
"""

SEKRET_RECEPCJI = """\
Dobrze, że sprawdzasz ukryte pliki (ls -a)!
Tutaj nic nie ma, ale w archiwum ta sztuczka się przyda.
"""

FALSZYWE_HASLO = """\
Naprawdę? Plik o nazwie haslo.txt, leżący na samym wierzchu?
Mariusz nie jest aż tak naiwny. Szukaj tego, czego nie widać.
"""

PRYWATNE = """\
PRYWATNE RZECZY MARIUSZA WRONY. NIE RUSZAĆ!

Biurko stoi obok.
"""

ULOTKA = """\
PIZZERIA "BAJT" - DOWOZIMY DO 23:00
Pizza Margherita ........ 28 zł
Pizza Serwerowa ......... 35 zł  (podwójny ser, potrójne kable)

Nic ciekawego. Ale czy na pewno widzisz wszystko,
co leży w tej szufladzie?
"""

KOPERTA = """\
KOPERTA - ŚCIŚLE TAJNE

FRAGMENT 1 HASŁA AWARYJNEGO:  {fragment}

Zapisz go. Pozostałe fragmenty wydadzą strażnicy
w magazynie, w sejfie i w hali serwerów.

- M.W.
"""

STARA_KOPERTA = """\
KOPERTA - ŚCIŚLE TAJNE

FRAGMENT 1 HASŁA AWARYJNEGO:  {fragment}

UNIEWAŻNIONY 12.03.2018 - hasło zmienione po audycie.
Nie używać. Aktualna koperta jest tam, gdzie zawsze.
"""

MAGAZYN = """\
MAGAZYN - poziom 2: porządki u pani Haliny
------------------------------------------

Kierowniczka magazynu, pani Halina, zostawiła listę zadań.
Strażnik magazynu wyda fragment 2, gdy wszystko będzie zrobione.

1. Regały. W magazynie mają stać trzy regały: regal-A, regal-B
   i regal-C, a w każdym regale trzy półki: polka-1, polka-2
   i polka-3. Do tego katalog zwroty na uszkodzone paczki.
   (mkdir -p tworzy katalog razem z brakującymi katalogami
   nadrzędnymi, np. mkdir -p regal-A/polka-1)

2. Rampa. W katalogu rampa/ leżą paczki. Miejsce każdej paczki
   jest zapisane na etykiecie W ŚRODKU paczki - zajrzyj (cat).
   Przenieś każdą paczkę (mv) na właściwe miejsce.

3. Instrukcja BHP. Skopiuj (cp) plik instrukcja-bhp.txt do
   każdego regału. Oryginał zostaje w magazynie.

4. Spis inwentarza. Plik ze spisem ma okropną nazwę.
   Zmień ją (mv) na: spis-inwentarza.txt

5. Zgłoszenie. Na koniec utwórz w magazynie pusty plik
   gotowe.txt (touch).

Sprawdzenie:  python3 straznik.py
Strażnik powie, czego jeszcze brakuje.
"""

INSTRUKCJA_BHP = """\
INSTRUKCJA BHP - MAGAZYN

1. Nie wspinaj się po regałach. Od tego jest drabina.
2. Ciężkie paczki kładź na dolnych półkach.
3. Przejścia między regałami muszą być wolne.
4. Uszkodzonych paczek nie otwieraj - odkładaj do zwrotów.
5. Kawa i herbata tylko w kuchni. Dotyczy także serwerowni!
"""

SPIS_STARA_NAZWA = "Spis Inwentarza (kopia) FINAL.TXT"
SPIS = """\
SPIS INWENTARZA MAGAZYNU - stan na 1.10.2026

drabina aluminiowa ......................... 1 szt.
wózek paletowy ............................. 2 szt.
taśma pakowa ............................... 14 rolek
skaner kodów kreskowych .................... 3 szt.
kubek z napisem "Najlepszy admin" .......... 1 szt. (własność M. Wrony)
"""

POZYCJE = [f"regal-{regal}/polka-{polka}" for regal in "ABC" for polka in (1, 2, 3)]
ZAWARTOSCI = [
    "40 x kabel sieciowy RJ45, 2 m",
    "12 x dysk SSD 1 TB",
    "6 x zasilacz serwerowy 800 W",
    "2 x przełącznik sieciowy, 48 portów",
    "30 x pamięć RAM DDR5 32 GB",
    "100 x opaska zaciskowa do kabli",
    "4 x wentylator do szafy rack",
    "1 x klawiatura mechaniczna (bez klawisza Escape)",
]
NADAWCY = [
    "Hurtownia Elektroniczna ISKRA, Lublin",
    "Serwery i Spółka, Kraśnik",
    "KABLEX, Świdnik",
    "Bajt-Hurt, Puławy",
]
PACZKA = """\
=== PACZKA {numer:02d} ===
Nadawca:   {nadawca}
Zawartość: {zawartosc}
Waga:      {waga} kg
{uwaga}
ETYKIETA MAGAZYNOWA: {etykieta}
"""

SEJF = """\
SEJF - poziom 3: prawa dostępu
------------------------------

Fragment 3 leży w sejfie. Sejf otwiera program otworz.py:

  ./otworz.py SZYFR

Szyfr leży w skrytce: skrytka/szyfr.txt. Kłopot w tym, że
CERBER odebrał wszystkim prawa do skrytki i do szyfru,
a programowi otworz.py - prawo wykonywania.

Regulamin sejfu (CERBER sprawdza każdy punkt):

1. Każde otwarcie sejfu trzeba wpisać do dziennika. Dopisz
   na końcu pliku dziennik-wejsc.txt nową linię:
       OTWIERA: twoje imię
   Dziennik jest tylko do odczytu, a to, co już w nim jest,
   musi zostać.

2. Po otwarciu sejfu skrytka i szyfr mają mieć takie prawa:
       skrytka     rwx------   (wszystko dla właściciela, nic dla innych)
       szyfr.txt   rw-------   (odczyt i zapis dla właściciela, nic dla innych)
   Ustaw je zapisem ósemkowym (liczbą), np. chmod 644 PLIK.
   Jaka liczba odpowiada rwx------, a jaka rw-------?

Przydadzą się:
  ls -l                  pokazuje prawa dostępu plików
  ls -ld KATALOG         prawa samego katalogu (a nie jego zawartości)
  chmod u+r PLIK         dodaj właścicielowi (u) prawo odczytu (r)
  chmod +x PLIK          dodaj prawo wykonywania (x)
  echo "tekst" >> PLIK   dopisz linię na końcu pliku
                         (uwaga: jeden znak > zamiast >> nadpisuje cały plik!)
"""

DZIENNIK = """\
DZIENNIK WEJŚĆ DO SEJFU
Każde otwarcie sejfu dopisz w nowej linii: OTWIERA: imię
--------------------------------------------------------
2026-09-30 08:12  Mariusz Wrona - przegląd roczny
2026-10-14 16:40  Anna Kowalczyk - wymiana dysków
"""

HALA = """\
HALA SERWERÓW - poziom 4: wielkie sprzątanie
--------------------------------------------

Dyski serwerów są pełne i CERBER zaczyna się dławić.
Technik, pan Piotr, zostawił instrukcję:

1. W katalogu logi/ są setki plików. Usuń wszystkie pliki
   tymczasowe (kończące się na .tmp) - co do jednego.

2. Kopie zapasowe (kończące się na .bak) przenieś do katalogu
   kosz/ - ma stać tutaj, w hali, obok katalogu logi/.

3. Pliki .log zostaw w logi/ - wszystkie. To dowody dla CERBERA.

4. Usuń katalogi stary-serwer/ (jest pusty) i zepsuty-serwer/
   (pełen złomu).

UWAGA! Polecenie rm usuwa na zawsze. W terminalu nie ma kosza,
z którego można coś wyciągnąć. Zanim usuniesz pliki wzorcem,
np. *.tmp, sprawdź, co do niego pasuje:  ls *.tmp

Sprawdzenie:  python3 straznik.py
"""


# =============================================================================================
#  Budowanie świata
# =============================================================================================
def buduj_recepcje():
    recepcja = SWIAT / "recepcja"
    zapisz(recepcja / "CZYTAJ_MNIE.txt", RECEPCJA)
    zapisz(recepcja / "tablica-ogloszen.txt", TABLICA)
    zapisz(recepcja / ".sekret.txt", SEKRET_RECEPCJI)
    zapisz(recepcja / "biurko" / "kadry.txt", KADRY)
    zapisz(recepcja / "biurko" / "notatka-portiera.txt", NOTATKA_PORTIERA)
    zapisz(recepcja / "biurko" / "kubek.txt", "Kubek z zimną herbatą. Lepiej go nie ruszać.\n")


def buduj_archiwum(los, stan):
    archiwum = SWIAT / "archiwum"
    dostawcy = ["ENERGA-PRĄD", "Sklep z kablami KABLEX", "Pizzeria BAJT", "Serwis klimatyzacji CHŁÓD"]
    for rok in range(2015, 2025):
        katalog = archiwum / str(rok)
        for nr in range(1, los.randint(2, 4) + 1):
            zapisz(katalog / "faktury" / f"faktura-{rok}-{nr:02d}.txt",
                   f"Faktura nr {nr}/{rok}\nDostawca: {los.choice(dostawcy)}\n"
                   f"Kwota: {los.randint(120, 9800)},00 zł\n")
        zapisz(katalog / "raporty" / f"raport-roczny-{rok}.txt",
               f"Raport roczny {rok}\nAwarie serwerów: {los.randint(0, 9)}\n"
               f"Wypite kawy: {los.randint(900, 4000)}\n")
    rocznik = archiwum / "2017"
    zapisz(rocznik / "haslo.txt", FALSZYWE_HASLO)
    prywatne = rocznik / ".mariusz"
    zapisz(prywatne / "PRYWATNE.txt", PRYWATNE)
    biurko = prywatne / "biurko"
    zapisz(biurko / "szuflada-1" / "rachunki.txt", "Rachunki za prąd. Same zera i jedynki.\n")
    zapisz(biurko / "szuflada-2" / "zdjecie-kota.txt", "Zdjęcie kota Mariusza. Kot ma na imię Bajt.\n")
    zapisz(biurko / "szuflada-3" / "ulotka.txt", ULOTKA)
    zapisz(biurko / "szuflada-3" / ".koperta.txt", KOPERTA.format(fragment=stan["fragmenty"][0]))
    zapisz(archiwum / "2018" / ".mariusz" / "stara-koperta.txt",
           STARA_KOPERTA.format(fragment=stan["wabik"]))


def buduj_magazyn(los, stan):
    magazyn = SWIAT / "magazyn"
    zapisz(magazyn / "CZYTAJ_MNIE.txt", MAGAZYN)
    zapisz(magazyn / "instrukcja-bhp.txt", INSTRUKCJA_BHP)
    zapisz(magazyn / SPIS_STARA_NAZWA, SPIS)
    (magazyn / "rampa").mkdir(parents=True, exist_ok=True)

    zawartosci = los.sample(ZAWARTOSCI, len(ZAWARTOSCI))
    uszkodzona = los.randrange(len(zawartosci))
    miejsca = iter(los.sample(POZYCJE, len(zawartosci) - 1))
    paczki, teksty = {}, {}
    for i, zawartosc in enumerate(zawartosci):
        nazwa = f"paczka-{i + 1:02d}.txt"
        if i == uszkodzona:
            etykieta = "zwroty"
            uwaga = "UWAGA: paczka uszkodzona w transporcie - odeślij do dostawcy.\n"
        else:
            etykieta = next(miejsca)
            uwaga = ""
        tekst = PACZKA.format(numer=i + 1, nadawca=los.choice(NADAWCY), zawartosc=zawartosc,
                              waga=f"{los.randint(1, 25)},{los.randint(0, 9)}", uwaga=uwaga,
                              etykieta=etykieta)
        zapisz(magazyn / "rampa" / nazwa, tekst)
        paczki[nazwa] = etykieta
        teksty[nazwa] = tekst
    stan["magazyn"] = {"paczki": paczki, "teksty": teksty,
                       "instrukcja": INSTRUKCJA_BHP, "spis": SPIS}


def buduj_sejf(los, stan):
    sejf = SWIAT / "sejf"
    kod = str(los.randint(1000, 9999))
    zapisz(sejf / "CZYTAJ_MNIE.txt", SEJF)
    zapisz(sejf / "dziennik-wejsc.txt", DZIENNIK, 0o444)
    zapisz(sejf / "skrytka" / "szyfr.txt", f"SZYFR DO SEJFU: {kod}\n", 0o000)
    os.chmod(sejf / "skrytka", 0o000)
    stan["sejf"] = {"kod": kod, "dziennik": DZIENNIK}


def unikalne(los, ile, wzory):
    nazwy = set()
    while len(nazwy) < ile:
        nazwy.add(los.choice(wzory)(los))
    return sorted(nazwy)


def buduj_hale(los, stan):
    hala = SWIAT / "hala"
    zapisz(hala / "CZYTAJ_MNIE.txt", HALA)
    logi = unikalne(los, los.randint(110, 130), [
        lambda l: f"serwer-{l.randint(1, 12):02d}-2026-10-{l.randint(1, 19):02d}.log",
        lambda l: f"dostep-2026-10-{l.randint(1, 19):02d}-{l.randint(0, 23):02d}h.log",
        lambda l: f"cerber-{l.randint(1000, 9999)}.log",
    ]) + ["raport-kwartalny.tmp.log", "stara-konfiguracja.bak.log"]
    tymczasowe = unikalne(los, los.randint(80, 95), [
        lambda l: f"sesja-{l.randint(10000, 99999)}.tmp",
        lambda l: f"cache-{l.getrandbits(24):06x}.tmp",
        lambda l: f"upload-{l.randint(1, 9999):04d}.tmp",
    ]) + [".sesja-ukryta.tmp"]
    kopie = unikalne(los, los.randint(30, 40), [
        lambda l: f"konfig-serwer-{l.randint(1, 12):02d}-v{l.randint(1, 9)}.bak",
        lambda l: f"baza-2026-{l.randint(1, 10):02d}-{l.randint(1, 28):02d}.bak",
    ])
    for nazwa in logi + tymczasowe + kopie:
        zapisz(hala / "logi" / nazwa, silnik.tresc_pliku_hali(nazwa))
    (hala / "stary-serwer").mkdir()
    zlom = hala / "zepsuty-serwer"
    zapisz(zlom / "notatka-technika.txt", "Złom. Do usunięcia razem z całym katalogiem. - P. Mazur\n")
    zapisz(zlom / "dysk-1" / "sektor-0.dat", "BŁĄD ODCZYTU\n")
    zapisz(zlom / "dysk-1" / "sektor-1.dat", "BŁĄD ODCZYTU\n")
    zapisz(zlom / "dysk-2" / "partycja" / "dane.dat", "?? uszkodzone dane ??\n")
    stan["hala"] = {"log": logi, "tmp": tymczasowe, "bak": kopie}


def kopiuj_skrypty(naprawa=False):
    """Kopiuje skrypty strażników do świata gry. Przy naprawie zostawia prawa istniejących plików."""
    for zrodlo, cel in SKRYPTY.items():
        sciezka = SWIAT / cel
        tresc = (TUTAJ / "gra" / zrodlo).read_text(encoding="utf-8")
        tryb = 0o644
        if naprawa and sciezka.exists():
            tryb = sciezka.stat().st_mode & 0o777
            os.chmod(sciezka, 0o644)
        zapisz(sciezka, tresc, tryb)


def przywroc_prawa(katalog):
    """Nadaje właścicielowi pełne prawa do katalogu i podkatalogów, żeby dało się je usunąć.
    Dowiązań symbolicznych nie rusza — mogą prowadzić poza świat gry."""
    os.chmod(katalog, 0o700)
    with os.scandir(katalog) as wpisy:
        for wpis in wpisy:
            if wpis.is_dir(follow_symlinks=False):
                przywroc_prawa(wpis.path)


def zbuduj_swiat():
    los = random.Random(secrets.randbits(64))
    slowa = los.sample(SLOWA, 5)
    stan = {
        "fragmenty": slowa[:4],
        "wabik": slowa[4],              # fałszywy fragment 1 z unieważnionej koperty
        "start": time.time(),
        "ukonczone": {},
        "kary": [],
        "koniec": None,
    }
    SWIAT.mkdir()
    zapisz(SWIAT / "CZYTAJ_MNIE.txt", WSTEP)
    buduj_recepcje()
    buduj_archiwum(los, stan)
    buduj_magazyn(los, stan)
    buduj_sejf(los, stan)
    buduj_hale(los, stan)
    kopiuj_skrypty()
    silnik.zapisz_stan(SWIAT, stan)


def main():
    parser = argparse.ArgumentParser(description="Ucieczka z serwerowni: buduje świat gry w ~/serwerownia.")
    tryb = parser.add_mutually_exclusive_group()
    tryb.add_argument("--od-nowa", action="store_true",
                      help="usuń stary świat gry i zbuduj nowy (nowe hasło, czas od zera)")
    tryb.add_argument("--napraw", action="store_true",
                      help="przywróć skrypty strażników, nie ruszając postępu")
    args = parser.parse_args()

    if os.name != "posix":
        print("Ta gra działa w terminalu Linuksa. Na Windowsie uruchom ją w WSL (Ubuntu).")
        return 1
    if os.geteuid() == 0:
        print("Nie uruchamiaj gry jako root (przez sudo). Root może wszystko,")
        print("więc zagadki z prawami dostępu w sejfie przestałyby działać.")
        return 1

    if SWIAT.is_symlink() or (SWIAT.exists() and not SWIAT.is_dir()):
        print(f"{SWIAT} to nie zwykły katalog. Nic nie ruszam - zmień jego nazwę i spróbuj jeszcze raz.")
        return 1

    if args.napraw:
        if not silnik.czy_swiat_gry(SWIAT):
            print(f"W {SWIAT} nie ma świata gry. Zbuduj go: python3 start.py")
            return 1
        kopiuj_skrypty(naprawa=True)
        print("Skrypty strażników przywrócone. Twój postęp i czas zostały bez zmian.")
        return 0

    if SWIAT.exists():
        if not silnik.czy_swiat_gry(SWIAT):
            print(f"Katalog {SWIAT} już istnieje, ale to nie jest świat gry")
            print("(brak pliku .stan ze znacznikiem gry). Nie usunę go - mogą tam być twoje pliki.")
            print("Zmień jego nazwę (mv) albo usuń go sam, jeśli na pewno jest niepotrzebny.")
            return 1
        if not args.od_nowa:
            print(f"Świat gry już istnieje: {SWIAT}")
            print()
            print("Graj dalej:")
            print("  cd ~/serwerownia")
            print()
            print("Albo zacznij od nowa (nowe hasło, czas od zera, cały postęp przepada):")
            print("  python3 start.py --od-nowa")
            return 1
        przywroc_prawa(SWIAT)
        shutil.rmtree(SWIAT)
        print(f"Stary świat gry usunięty: {SWIAT}")

    zbuduj_swiat()

    print(f"Świat gry gotowy: {SWIAT}")
    print("CERBER zaczął liczyć czas.")
    print()
    print("Zacznij tak:")
    print("  cd ~/serwerownia")
    print("  cat CZYTAJ_MNIE.txt")
    if os.access(SWIAT / "sejf" / "skrytka", os.R_OK):
        print()
        print("UWAGA: prawa dostępu nie działają tu tak, jak trzeba, więc poziom 3 (sejf)")
        print("nie będzie miał sensu. Graj w katalogu domowym Linuksa, nie na dysku Windowsa (/mnt/c).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
