"""Silnik gry „Ucieczka z serwerowni” — kod wspólny dla strażników i drzwi wyjściowych.

start.py kopiuje ten plik do ~/serwerownia/.silnik/. Żeby przejść grę, nie musisz go czytać.
"""
import base64
import hashlib
import json
import sys
import time
from pathlib import Path

ZNACZNIK = "SERWEROWNIA-GRA 1"      # pierwsza linijka pliku .stan — po niej start.py poznaje świat gry
PLIK_STANU = ".stan"
KARA_MINUTY = 3                     # kara za skorzystanie z kopii zapasowej
_KLUCZ = b"cerber-pilnuje-drzwi"


# --- plik stanu -----------------------------------------------------------------------------
def _xor(dane):
    return bytes(b ^ _KLUCZ[i % len(_KLUCZ)] for i, b in enumerate(dane))


def zakoduj(stan):
    surowe = json.dumps(stan, ensure_ascii=False).encode("utf-8")
    return base64.b64encode(_xor(surowe)).decode("ascii")


def odkoduj(tekst):
    return json.loads(_xor(base64.b64decode(tekst)).decode("utf-8"))


def czy_swiat_gry(swiat):
    """Czy w katalogu leży plik stanu z naszym znacznikiem."""
    try:
        linie = (Path(swiat) / PLIK_STANU).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return False
    return bool(linie) and linie[0].strip() == ZNACZNIK


def zapisz_stan(swiat, stan):
    tresc = (f"{ZNACZNIK}\n"
             "# Pamięć CERBERA. Nie zmieniaj i nie usuwaj tego pliku.\n"
             f"{zakoduj(stan)}\n")
    (Path(swiat) / PLIK_STANU).write_text(tresc, encoding="utf-8")


def wczytaj_stan(swiat):
    """Odczytuje stan gry; gdy pliku nie ma albo jest uszkodzony, kończy program z instrukcją."""
    sciezka = Path(swiat) / PLIK_STANU
    try:
        linie = sciezka.read_text(encoding="utf-8").splitlines()
        if not linie or linie[0].strip() != ZNACZNIK:
            raise ValueError("brak znacznika")
        return odkoduj(linie[-1].strip())
    except (OSError, ValueError, UnicodeDecodeError):
        print(f"CERBER: nie mogę odczytać swojej pamięci ({sciezka}).")
        print("Jeśli ten plik został usunięty albo zmieniony, zacznij grę od nowa:")
        print("  python3 start.py --od-nowa   (w folderze 01-ucieczka-z-serwerowni)")
        sys.exit(3)


# --- wspólne komunikaty ---------------------------------------------------------------------
def naglowek(tytul):
    print("=" * 60)
    print(f"  {tytul}")
    print("=" * 60)


def wypisz_braki(braki):
    print("Jeszcze nie. Do zrobienia:")
    for brak in braki:
        print(f"  - {brak}")
    print()
    print("Popraw i uruchom mnie jeszcze raz.")


def wydaj_fragment(swiat, stan, numer, strefa):
    """Wypisuje fragment hasła i zapamiętuje, że strefa jest zaliczona."""
    fragment = stan["fragmenty"][numer - 1]
    tekst = f"FRAGMENT {numer} Z 4:  {fragment}"
    print("+" + "-" * 46 + "+")
    print(f"|  {tekst:<44}|")
    print("+" + "-" * 46 + "+")
    print("Zapisz go. Będzie potrzebny przy drzwiach: python3 wyjscie.py")
    ukonczone = stan.setdefault("ukonczone", {})
    if strefa not in ukonczone:
        ukonczone[strefa] = time.time()
        zapisz_stan(swiat, stan)


def dolicz_kare(swiat, stan, powod):
    stan.setdefault("kary", []).append({"minuty": KARA_MINUTY, "powod": powod, "czas": time.time()})
    zapisz_stan(swiat, stan)
    print(f"CERBER doliczył {KARA_MINUTY} minuty kary do twojego czasu.")


def minuty_kary(stan):
    return sum(k["minuty"] for k in stan.get("kary", []))


def formatuj_czas(sekundy):
    sekundy = int(round(sekundy))
    godziny, reszta = divmod(sekundy, 3600)
    minuty, sek = divmod(reszta, 60)
    if godziny:
        return f"{godziny} h {minuty:02d} min {sek:02d} s"
    return f"{minuty} min {sek:02d} s"


def skrot(tekst):
    """Odcisk treści pliku — strażnik porównuje nim kopie z oryginałem."""
    return hashlib.sha256(tekst.encode("utf-8")).hexdigest()


def skrot_pliku(sciezka):
    try:
        return hashlib.sha256(Path(sciezka).read_bytes()).hexdigest()
    except OSError:
        return None


# --- treść plików w hali serwerów (start.py i kopia zapasowa strażnika tworzą je tak samo) ------
def tresc_pliku_hali(nazwa):
    if nazwa.endswith(".log"):
        return (f"[{nazwa}]\n"
                "00:00:01 INFO  serwer uruchomiony\n"
                "03:14:15 WARN  temperatura w szafie: 41 C\n"
                "21:47:00 ALERT CERBER: wykryto intruza, blokada drzwi\n")
    if nazwa.endswith(".bak"):
        return f"[{nazwa}]\nkopia zapasowa konfiguracji — przenieść do kosz/\n"
    return f"[{nazwa}]\nplik tymczasowy — do usunięcia\n"
