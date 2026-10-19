![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 00. Instalacja i pierwszy skrypt

Lista kontrolna stanowiska na Ubuntu. Przejdź punkty po kolei. Na końcu jest lista do odhaczenia — pokaż ją prowadzącemu.

**Czas:** ok. 20 minut · **Dzień 1** (26.10)

> **Uwaga o `sudo`.** Polecenia zaczynające się od `sudo` instalują programy dla całego systemu i pytają o hasło administratora (podczas wpisywania nie widać gwiazdek — to normalne). Na szkolnych komputerach możesz nie mieć tego prawa. Wtedy prowadzący pokaże ten krok na swoim komputerze, a programy w pracowni są już zainstalowane — sprawdź tylko, czy działają.

## 1. Terminal i Python

Otwórz terminal: **Ctrl+Alt+T**. Sprawdź, jaki masz Python:

```bash
python3 --version
which python3
```

Potrzebny jest Python 3.10 lub nowszy (Ubuntu 22.04 ma 3.10, Ubuntu 24.04 — 3.12). W Ubuntu polecenie nazywa się `python3`; samo `python` często kończy się błędem `command not found`.

## 2. apt — instalowanie programów

`apt` to menedżer pakietów Ubuntu: pobiera programy z serwerów Ubuntu i sam je instaluje razem z tym, czego potrzebują.

```bash
sudo apt update
sudo apt install python3-venv python3-pip git
```

- `apt update` odświeża listę dostępnych pakietów (niczego jeszcze nie instaluje),
- `python3-venv` — moduł do tworzenia środowisk wirtualnych (bez niego `python3 -m venv` kończy się błędem o `ensurepip`),
- `python3-pip` — `pip`, instalator bibliotek Pythona,
- `git` — system kontroli wersji.

Sprawdź: `git --version`.

**apt a pip.** `apt` instaluje programy systemowe dla wszystkich użytkowników, z repozytoriów Ubuntu. `pip` instaluje biblioteki Pythona z serwisu PyPI — i robimy to w środowiskach venv, każde dla jednego projektu (ćwiczenie 03).

### Ubuntu a Fedora

Ubuntu i Fedora to dwie popularne dystrybucje Linuksa. Polecenia z tego kursu (`ls`, `cd`, `chmod`, `git`, `python3`) działają w obu tak samo — różni się głównie instalowanie programów.

| | Ubuntu | Fedora |
| --- | --- | --- |
| Rodzina | Debian | Red Hat |
| Menedżer pakietów | `apt` | `dnf` |
| Format pakietów | `.deb` | `.rpm` |
| Instalacja Gita | `sudo apt install git` | `sudo dnf install git` |
| Moduł `venv` | osobny pakiet `python3-venv` | od razu w pakiecie `python3` |
| Nowe wydania | co pół roku, wersje LTS co 2 lata (5 lat wsparcia) | co pół roku, ok. 13 miesięcy wsparcia |

## 3. VS Code i Codex

Jeśli VS Code nie jest zainstalowany: `sudo snap install code --classic` albo pobierz pakiet `.deb` ze strony code.visualstudio.com i zainstaluj go poleceniem `sudo apt install ./code_*.deb`.

1. Uruchom VS Code i zainstaluj rozszerzenia (**Ctrl+Shift+X**): **Python** i **Jupyter** — oba od Microsoftu.
2. Otwórz folder z ćwiczeniami: w terminalu `code ~/python-belzyce-01-srodowisko`.
3. Terminal w VS Code otwierasz skrótem **Ctrl+`** (klawisz pod Esc).

**Codex** to asystent AI firmy OpenAI, dostępny jako rozszerzenie VS Code (wymaga konta). Umie wyjaśnić fragment kodu, znaleźć przyczynę błędu albo zaproponować zmianę. Na kursie używamy go do wyjaśniania, a nie do odrabiania zadań: najpierw spróbuj sam, a każdą propozycję AI przeczytaj i zrozum, zanim ją przyjmiesz.

## 4. Jupyter w środowisku venv

Notatniki Jupytera (ćwiczenie 02) uruchomisz w środowisku wirtualnym repozytorium. Środowisko venv to osobny „pokój” na biblioteki jednego projektu — dokładnie zajmiemy się nim w ćwiczeniu 03.

```bash
cd ~/python-belzyce-01-srodowisko
python3 -m venv .venv
source .venv/bin/activate
pip install notebook ipykernel
```

Po `source .venv/bin/activate` na początku linii poleceń pojawia się `(.venv)` — od teraz `python` i `pip` działają w tym środowisku. `pip install` pobiera pakiety z internetu.

Sprawdź, czy Jupyter działa:

```bash
jupyter notebook
```

Otworzy się przeglądarka z listą plików. Serwer zatrzymasz w terminalu klawiszami **Ctrl+C**. Zamiast klasycznego notatnika możesz zainstalować nowszy JupyterLab: `pip install jupyterlab`, uruchomienie: `jupyter lab`.

## 5. Pierwszy skrypt: trzy sposoby uruchomienia

Utwórz w tym folderze plik `witaj.py` (w VS Code: **File → New File**, albo w terminalu `code witaj.py`) i wpisz:

```python
#!/usr/bin/env python3
"""Mój pierwszy skrypt."""
import platform

imie = "Ola"
print(f"Cześć, {imie}! Witaj na kursie Python Developer.")
print(f"Działam na Pythonie {platform.python_version()} w systemie {platform.system()}.")
```

Zmień imię na swoje i zapisz plik (**Ctrl+S**).

**Sposób 1 — interpreter z nazwy:**

```bash
cd ~/python-belzyce-01-srodowisko/00-instalacja
python3 witaj.py
```

**Sposób 2 — skrypt jak program:**

```bash
./witaj.py
```

Dostaniesz `Permission denied`. Sprawdź prawa pliku: `ls -l witaj.py` — na początku jest `-rw-rw-r--`, nie ma litery `x` (prawo wykonywania). Dodaj ją i spróbuj jeszcze raz:

```bash
chmod +x witaj.py
ls -l witaj.py
./witaj.py
```

Teraz uruchomienie działa dzięki pierwszej linijce, `#!/usr/bin/env python3` (tzw. *shebang*): mówi systemowi, którym programem wykonać plik.

Zagadka: usuń na chwilę pierwszą linijkę, zapisz plik i uruchom `./witaj.py`. Co się stało i dlaczego? Potem przywróć linijkę (**Ctrl+Z**).

**Sposób 3 — w VS Code:** otwórz `witaj.py` i kliknij przycisk z trójkątem w prawym górnym rogu (*Run Python File*). Wynik pojawi się w terminalu na dole okna. Jeśli VS Code zapyta o interpreter, wybierz `.venv` albo systemowy `python3` (**Ctrl+Shift+P** → *Python: Select Interpreter*).

## 6. Git: kim jesteś?

Git podpisuje każdy zapis (commit) imieniem i adresem e-mail. Ustaw je raz na swoim koncie:

```bash
git config --global user.name "Imię Nazwisko"
git config --global user.email "twoj@email.pl"
git config --global init.defaultBranch main
git config --global --list
```

Adres e-mail z commitów widać publicznie na GitHubie. Jeśli nie chcesz go pokazywać, w ustawieniach GitHuba (**Settings → Emails**) zaznacz *Keep my email addresses private* i wpisz w `user.email` adres w postaci `…@users.noreply.github.com`, który GitHub tam poda.

## Lista kontrolna

- [ ] `python3 --version` pokazuje wersję 3.10 lub nowszą
- [ ] `git --version` działa
- [ ] VS Code ma rozszerzenia Python i Jupyter
- [ ] w repozytorium jest `.venv`, a `jupyter notebook` otwiera przeglądarkę
- [ ] `witaj.py` działa na trzy sposoby; wiesz, po co jest pierwsza linijka
- [ ] `git config --global --list` pokazuje `user.name` i `user.email`
