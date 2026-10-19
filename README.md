![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# Moduł 1 — Środowisko pracy: Python i Linux

**Kurs „Python Developer”** · Bełżyce · zajęcia 26 i 27 października 2026

Ćwiczenia do pierwszego modułu kursu. Przygotujesz stanowisko pracy, uciekniesz z zamkniętej serwerowni samym terminalem, przetłumaczysz pierwsze programy z Kotlina na Pythona, rozwiążesz konflikt wersji bibliotek środowiskami venv i założysz z zespołem repozytorium projektu końcowego.

## Jak pobrać ćwiczenia

W terminalu, w katalogu domowym:

```bash
cd ~
git clone https://github.com/marcinkieruzel/python-belzyce-01-srodowisko.git
cd python-belzyce-01-srodowisko
```

Jeśli nie masz jeszcze Gita, zainstaluj go (`sudo apt install git`) albo pobierz repozytorium jako ZIP: zielony przycisk **Code** → **Download ZIP**, a potem rozpakuj je w katalogu domowym. Polecenia w ćwiczeniach zakładają, że repozytorium leży w `~/python-belzyce-01-srodowisko`.

## Ćwiczenia

| Nr | Ćwiczenie | Co ćwiczysz | Czas | Dzień |
| --- | --- | --- | --- | --- |
| 00 | [Instalacja i pierwszy skrypt](00-instalacja/) | `python3`, `apt`, VS Code, Jupyter, `chmod +x`, konfiguracja Gita | ok. 20 min | 1 (26.10) |
| 01 | [Ucieczka z serwerowni](01-ucieczka-z-serwerowni/) — gra terenowa w terminalu | `pwd`, `ls`, `cd`, `cat`, `mkdir`, `cp`, `mv`, `rm`, `touch`, `chmod`, ukryte pliki, wzorce `*` | 60–75 min | 1 (26.10) |
| 02 | [Z Kotlina na Pythona](02-z-kotlina-na-pythona/) — pierwszy notatnik | notatnik Jupyter, składnia Pythona na tle Kotlina | 30–45 min (reszta w domu) | 1 (26.10) |
| 03 | [Dwa projekty, jeden komputer](03-dwa-projekty-jeden-komputer/) | `pip`, `venv`, `requirements.txt`, `pip freeze` | ok. 25 min | 2 (27.10) |
| 04 | [Repozytorium zespołu](04-repo-zespolu/) — start projektu końcowego | `git init`, `add`, `commit`, `log`, `status`, `push`, `.gitignore`; sabotaż: `diff`, `restore`, `clean` | ok. 40 min | 2 (27.10) |

Ćwiczenia robisz po kolei. Wszystko działa w terminalu Linuksa (na zajęciach: Ubuntu) z Pythonem 3.10 lub nowszym.

## W domu na Windowsie: WSL

Na Windowsie 10 i 11 możesz mieć prawdziwego Ubuntu w okienku terminala — to WSL (*Windows Subsystem for Linux*). Wszystkie ćwiczenia działają w nim tak samo jak w pracowni.

1. Otwórz **PowerShell jako administrator** (menu Start → wpisz „PowerShell” → prawy przycisk → *Uruchom jako administrator*) i wpisz:
   ```powershell
   wsl --install
   ```
   Polecenie włącza WSL i instaluje Ubuntu. Uruchom ponownie komputer.
2. Po restarcie otworzy się okno Ubuntu (albo uruchom **Ubuntu** z menu Start). Wymyśl nazwę użytkownika i hasło do Linuksa — to hasło będzie potrzebne przy `sudo`. Przy wpisywaniu hasła nie widać gwiazdek, to normalne.
3. Zaktualizuj system i doinstaluj narzędzia z ćwiczenia 00:
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip git
   ```
4. Zainstaluj **VS Code** w Windowsie (code.visualstudio.com) i rozszerzenie **WSL**. W terminalu Ubuntu wpisz w katalogu projektu `code .` — VS Code otworzy się w Windowsie, ale będzie pracować na plikach w Linuksie.
5. Pracuj w katalogu domowym Linuksa (`~`), a nie na dysku Windowsa (`/mnt/c/...`). Na dysku Windowsa `chmod` nie działa jak trzeba (sejf z ćwiczenia 01 się nie otworzy), a wszystko chodzi wolniej. Pliki z Linuksa zobaczysz w Eksploratorze Windows pod adresem `\\wsl$\Ubuntu\home\TWOJA_NAZWA`.

## Co jest w repozytorium

- `00-instalacja/` … `04-repo-zespolu/` — ćwiczenia; każde ma własne `README.md` z instrukcją.
- `materialy/` — pliki wspólne (logotypy projektu).
- `.gitignore` — lista plików, których Git ma nie śledzić: środowiska `.venv/`, `__pycache__/`, punkty kontrolne Jupytera.
