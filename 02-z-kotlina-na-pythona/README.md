![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 02. Z Kotlina na Pythona — pierwszy notatnik

Znasz już Kotlina, więc nie zaczynamy od zera. W notatniku [`z-kotlina-na-pythona.ipynb`](z-kotlina-na-pythona.ipynb) dostajesz działające programy w Kotlinie i ściągę „Kotlin → Python”, a twoim zadaniem jest napisać te same programy w Pythonie — i trochę je rozbudować.

**Czas:** 30–45 minut na zajęciach · **Dzień 1** (26.10) · co nie zmieści się na zajęciach — w domu

## Jak otworzyć notatnik

Potrzebne jest środowisko `.venv` w repozytorium z ćwiczenia 00 (krok 4).

**VS Code:** otwórz folder repozytorium (`code ~/python-belzyce-01-srodowisko`), kliknij plik `.ipynb`, a w prawym górnym rogu **Select Kernel** → **Python Environments** → `.venv`. Jeśli VS Code poprosi o pakiet `ipykernel`, zgódź się.

**Przeglądarka:**

```bash
cd ~/python-belzyce-01-srodowisko
source .venv/bin/activate
jupyter notebook
```

Komórkę uruchamiasz klawiszami **Shift+Enter**. Pisz kod pod linijką `# Twój kod`, uruchom komórkę i porównaj to, co wypisał program, z blokiem **Oczekiwany wynik** pod spodem.

## Co jest w notatniku

| Zadanie | Program w Kotlinie | Do dopisania samodzielnie |
| --- | --- | --- |
| 1. Tabela temperatur | `when`, pętla z krokiem, `String.format` | temperatura, przy której skale Celsjusza i Fahrenheita się spotykają |
| 2. Siła haseł | funkcja, pętla po znakach, `isDigit`, `isUpperCase`, liczniki | funkcja, która mówi, czego hasłu brakuje |
| 3. Najczęstsze litery | słownik jako licznik, sortowanie, histogram z `#` | procent samogłosek w tekście i najrzadsza samogłoska |
| Dodatkowe. Szyfr Cezara | funkcja szyfrująca na kodach znaków | złamanie szyfru bez znajomości klucza |

Składnię Pythona omówimy dokładnie w kolejnych modułach. Na razie wystarczy ściąga na początku notatnika — gdy czegoś w niej brakuje, zapytaj prowadzącego albo poszukaj w dokumentacji (docs.python.org/pl/3).
