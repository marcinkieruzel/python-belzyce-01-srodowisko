#!/usr/bin/env python3
"""Sabotaż — zadanie z Gita dla zespołu.

Uruchom w katalogu REPOZYTORIUM ZESPOŁU, po pierwszym commicie, gdy git status nie pokazuje zmian:

  python3 ~/python-belzyce-01-srodowisko/04-repo-zespolu/sabotaz.py

Sabotażysta psuje pliki śledzone przez Gita w bieżącym repozytorium: zmienia treść dwóch plików,
usuwa jeden plik i podrzuca śmieci. Waszym zadaniem jest znaleźć szkody (git status, git diff)
i je naprawić (git restore, git clean). Wszystko da się odzyskać, bo jest w ostatnim commicie.

Program odmawia pracy poza repozytorium Gita, w repozytorium bez commitów, w repozytorium
z ćwiczeniami i wtedy, gdy macie niezapisane zmiany — żeby nie zniszczyć waszej pracy.

Opcje:
  --commit     trudniejsza wersja: sabotażysta robi też commit ze swoimi zmianami
               (do znalezienia: git log, git show; do naprawy: git revert)
  --tak        nie pytaj o potwierdzenie
  --zdradz     pokaż, co sabotażysta zrobił ostatnio (dla prowadzącego)
"""
import argparse
import random
import subprocess
import sys
from pathlib import Path

POMIJANE = {".gitignore", ".gitattributes", ".gitmodules"}
KATALOGI_POMIJANE = (".venv/", "venv/", "__pycache__/")
DZIENNIK = "sabotaz.log"          # zapisywany w katalogu .git — Git go nie śledzi
WPISY = {
    ".py": "# Ten kod jest teraz mój. - Sabotażysta",
    ".md": "Ten projekt przejął Sabotażysta.",
}
WPIS_DOMYSLNY = "SABOTAŻYSTA BYŁ TUTAJ"
SMIECI = [
    ("notatki-sabotazysty.txt", "Lista celów:\n1. repozytorium zespołu\n2. ???\n"),
    ("kopia main (1).py", "print('to tylko kopia, nic ważnego')\n"),
    ("haslo_do_wifi.txt", "Nie powiem.\n"),
]
KATALOG_SMIECI = ("tymczasowe", [("dump-001.dat", "0101010101\n"), ("dump-002.dat", "1010101010\n")])


def git(*argumenty, cwd=None, sprawdz=True):
    wynik = subprocess.run(["git", *argumenty], cwd=cwd, capture_output=True, text=True)
    if sprawdz and wynik.returncode != 0:
        raise RuntimeError(wynik.stderr.strip())
    return wynik


def odmowa(*linie):
    for linia in linie:
        print(linia)
    sys.exit(1)


def znajdz_repo():
    try:
        wynik = git("rev-parse", "--show-toplevel", sprawdz=False)
    except FileNotFoundError:
        odmowa("Nie znalazłem programu git. Zainstaluj go: sudo apt install git")
    if wynik.returncode != 0:
        odmowa("Tu nie ma repozytorium Gita.",
               "Wejdź (cd) do katalogu repozytorium zespołu i uruchom mnie jeszcze raz.")
    repo = Path(wynik.stdout.strip())
    if git("rev-parse", "--verify", "HEAD", cwd=repo, sprawdz=False).returncode != 0:
        odmowa("W tym repozytorium nie ma jeszcze żadnego commita.",
               "Najpierw: git add . i git commit -m \"Pierwszy commit\".")
    if (repo / "04-repo-zespolu" / "sabotaz.py").exists():
        odmowa("To repozytorium z ćwiczeniami, a nie repozytorium zespołu.",
               "Wejdź (cd) do repozytorium zespołu i uruchom mnie stamtąd.")
    if repo == Path.home():
        odmowa("Repozytorium Gita obejmuje cały katalog domowy. Tu nie sabotuję.")
    zmiany = git("status", "--porcelain", cwd=repo).stdout
    if zmiany.strip():
        odmowa("W repozytorium są niezapisane zmiany:", "", zmiany.rstrip(), "",
               "Sabotażysta działa tylko na czystym repozytorium, żeby nie zniszczyć waszej pracy.",
               "Zróbcie commit (git add, git commit) albo cofnijcie zmiany i spróbujcie jeszcze raz.")
    return repo


def pliki_do_sabotazu(repo):
    """Śledzone pliki tekstowe, które wolno popsuć (bez .gitignore i bez środowisk venv)."""
    wynik = []
    for nazwa in git("ls-files", "-z", cwd=repo).stdout.split("\0"):
        if not nazwa or Path(nazwa).name in POMIJANE or nazwa.startswith(KATALOGI_POMIJANE):
            continue
        sciezka = repo / nazwa
        if sciezka.is_symlink() or not sciezka.is_file():
            continue
        dane = sciezka.read_bytes()
        if b"\0" in dane:
            continue
        try:
            dane.decode("utf-8")
        except UnicodeDecodeError:
            continue
        wynik.append(nazwa)
    return wynik


def literowka(tekst, los):
    """Zamienia miejscami dwie sąsiednie litery w jednym słowie. Zwraca (nowy tekst, opis) albo None."""
    linie = tekst.split("\n")
    kandydaci = []
    for nr, linia in enumerate(linie):
        slowo = ""
        for i, znak in enumerate(linia + " "):
            if znak.isalpha():
                slowo += znak
                continue
            if len(slowo) >= 4 and slowo[1] != slowo[2]:
                kandydaci.append((nr, i - len(slowo), slowo))
            slowo = ""
    if not kandydaci:
        return None
    nr, poczatek, slowo = los.choice(kandydaci)
    zmienione = slowo[0] + slowo[2] + slowo[1] + slowo[3:]
    linia = linie[nr]
    linie[nr] = linia[:poczatek] + zmienione + linia[poczatek + len(slowo):]
    return "\n".join(linie), f"literówka w linii {nr + 1}: {slowo} -> {zmienione}"


def dopisek(nazwa, tekst, los):
    wpis = WPISY.get(Path(nazwa).suffix, WPIS_DOMYSLNY)
    linie = tekst.split("\n")
    gdzie = los.randint(0, max(0, len(linie) - 1))
    linie.insert(gdzie, wpis)
    return "\n".join(linie), f"wstawiona linia {gdzie + 1}: {wpis}"


def czy_ignorowany(repo, sciezka):
    return git("check-ignore", "-q", str(sciezka), cwd=repo, sprawdz=False).returncode == 0


def sabotuj(repo, los):
    pliki = pliki_do_sabotazu(repo)
    if len(pliki) < 2:
        odmowa("W repozytorium jest za mało plików (potrzebne co najmniej 2 pliki tekstowe poza .gitignore).",
               "Zbudujcie najpierw strukturę projektu z instrukcji i zróbcie commit.")
    # najpierw pliki z treścią (README, kod, dane), na końcu puste (np. .gitkeep)
    pelne = [p for p in pliki if (repo / p).stat().st_size > 0]
    puste = [p for p in pliki if p not in pelne]
    los.shuffle(pelne)
    los.shuffle(puste)
    pliki = pelne + puste
    raport = []

    # 1. subtelna zmiana: literówka (jeśli się da), w drugim pliku wyraźny dopisek
    do_zmiany = pliki[:2] if len(pliki) >= 3 else pliki[:1]
    for i, nazwa in enumerate(do_zmiany):
        sciezka = repo / nazwa
        tekst = sciezka.read_text(encoding="utf-8")
        zmiana = literowka(tekst, los) if i == 0 else None
        if zmiana is None:
            zmiana = dopisek(nazwa, tekst, los)
        sciezka.write_text(zmiana[0], encoding="utf-8")
        raport.append(f"zmieniony {nazwa}: {zmiana[1]}")

    # 2. usunięty plik
    usuniety = pliki[len(do_zmiany)]
    (repo / usuniety).unlink()
    raport.append(f"usunięty {usuniety}")

    # 3. śmieci: plik w repozytorium i katalog z plikami
    katalogi = sorted({str(Path(p).parent) for p in pliki_do_sabotazu(repo)} | {"."})
    for nazwa, tresc in los.sample(SMIECI, len(SMIECI)):
        cel = repo / los.choice(katalogi) / nazwa
        if not cel.exists() and not czy_ignorowany(repo, cel):
            cel.write_text(tresc, encoding="utf-8")
            raport.append(f"podrzucony plik {cel.relative_to(repo)}")
            break
    katalog, zawartosc = KATALOG_SMIECI
    if not (repo / katalog).exists() and not czy_ignorowany(repo, repo / katalog / zawartosc[0][0]):
        (repo / katalog).mkdir()
        for nazwa, tresc in zawartosc:
            (repo / katalog / nazwa).write_text(tresc, encoding="utf-8")
        raport.append(f"podrzucony katalog {katalog}/ ({len(zawartosc)} pliki)")
    return raport


def main():
    parser = argparse.ArgumentParser(description="Sabotaż w repozytorium zespołu (ćwiczenie z Gita).")
    parser.add_argument("--commit", action="store_true", help="sabotażysta robi też commit")
    parser.add_argument("--tak", action="store_true", help="nie pytaj o potwierdzenie")
    parser.add_argument("--zdradz", action="store_true", help="pokaż, co sabotażysta zrobił ostatnio")
    args = parser.parse_args()

    if args.zdradz:
        wynik = git("rev-parse", "--git-dir", sprawdz=False)
        dziennik = Path(wynik.stdout.strip()) / DZIENNIK if wynik.returncode == 0 else None
        if dziennik is None or not dziennik.exists():
            odmowa("Tu jeszcze nie było sabotażu.")
        print(dziennik.read_text(encoding="utf-8"), end="")
        return 0

    repo = znajdz_repo()
    print(f"Repozytorium: {repo}")
    print("Sabotażysta zmieni i usunie tu pliki śledzone przez Gita (wszystko da się odzyskać).")
    if not args.tak:
        try:
            odpowiedz = input("Wpisz TAK, żeby zacząć: ")
        except EOFError:
            odpowiedz = ""
        if odpowiedz.strip().upper() != "TAK":
            print("Sabotaż odwołany.")
            return 1

    raport = sabotuj(repo, random.Random())
    if args.commit:
        git("add", "-A", cwd=repo)
        git("-c", "user.name=Sabotażysta", "-c", "user.email=sabotazysta@example.invalid",
            "commit", "-q", "-m", "Drobne poprawki", cwd=repo)
        raport.append("zmiany zapisane w commicie „Drobne poprawki” (autor: Sabotażysta)")

    git_dir = Path(git("rev-parse", "--absolute-git-dir", cwd=repo).stdout.strip())
    with open(git_dir / DZIENNIK, "a", encoding="utf-8") as plik:
        plik.write("Sabotaż:\n" + "".join(f"  - {linia}\n" for linia in raport))

    print()
    print("Sabotaż wykonany. Coś się zmieniło - ale co?")
    if args.commit:
        print("Tym razem sabotażysta zatarł ślady commitem. Zacznijcie od: git log --oneline")
    else:
        print("Zacznijcie od: git status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
