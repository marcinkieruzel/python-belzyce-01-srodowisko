![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 03. Dwa projekty, jeden komputer

Na twoim komputerze są dwa projekty, które korzystają z tej samej biblioteki `kantor` (przelicza waluty):

- `stary-projekt/` — kalkulator kieszonkowego na wycieczkę klasową, napisany rok temu pod **kantor 1.0**,
- `nowy-projekt/` — porównywarka cen konsoli w sklepach z różnych krajów, napisana pod **kantor 2.0**.

W wersji 2.0 autorzy biblioteki zmienili sposób jej używania: funkcja `przelicz()` dostała trzeci argument, a słownik `KURSY` zniknął. Obie wersje biblioteki leżą w katalogu `paczki/` jako gotowe paczki Pythona (pliki `.whl`), więc instalacja działa bez internetu. Każdy projekt ma plik `requirements.txt` z listą tego, czego potrzebuje.

**Zadanie:** zainstaluj wszystko tak, żeby oba programy działały — i to jednocześnie.

**Czas:** ok. 25 minut · **Dzień 2** (27.10)

## Krok 1. Spróbuj po prostu zainstalować

```bash
cd ~/python-belzyce-01-srodowisko/03-dwa-projekty-jeden-komputer/stary-projekt
cat requirements.txt
pip install -r requirements.txt
```

Na Ubuntu 23.04 i nowszych `pip` odmówi:

```text
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    ...
hint: See PEP 668 for the detailed specification.
```

Systemowy Python należy do Ubuntu: korzystają z niego programy systemowe, a jego biblioteki instaluje `apt`. Gdyby `pip` podmienił w nim jakąś bibliotekę na inną wersję, mógłby zepsuć narzędzia systemu. Dlatego od Ubuntu 23.04 `pip` poza środowiskiem wirtualnym odmawia instalacji (to reguła PEP 668) i sam podpowiada, co zrobić: utworzyć środowisko wirtualne (*venv*). Opcji `--break-system-packages` z ostatniej linijki komunikatu nie używaj — nazwa mówi, co robi.

Inne możliwe wyniki:

- `pip: command not found` — w systemie nie ma `pip` (pakiet `python3-pip`). Nic nie szkodzi: każde środowisko venv ma własnego `pip`.
- Na Ubuntu 22.04 `pip` zainstaluje bibliotekę bez protestu do `~/.local`, wspólnego dla wszystkich projektów. To jeszcze gorzej — w kroku 2 zobaczysz dlaczego. Posprzątaj po sobie: `pip uninstall -y kantor`.

## Krok 2. Jedno środowisko dla obu projektów?

Utwórz jedno środowisko wirtualne i zainstaluj w nim to, czego potrzebuje stary projekt:

```bash
python3 -m venv ~/venv-wspolny
source ~/venv-wspolny/bin/activate
cd ~/python-belzyce-01-srodowisko/03-dwa-projekty-jeden-komputer/stary-projekt
pip install -r requirements.txt
python kieszonkowe.py
```

Po `source …/activate` na początku linii poleceń pojawia się `(venv-wspolny)`. Program powinien wypisać:

```text
Kalkulator kieszonkowego (kantor 1.0.0)

Kursy w kantorze:
  1 EUR = 4.25 zł
  1 USD = 3.90 zł
  1 GBP = 5.00 zł
  1 CZK = 0.17 zł
  1 UAH = 0.10 zł

400 zł to 2352.94 CZK
400 zł to 94.12 EUR
```

Teraz w tym samym środowisku nowy projekt:

```bash
cd ../nowy-projekt
pip install -r requirements.txt
python porownywarka.py
```

```text
Porównywarka cen konsoli (kantor 2.0.0)

Polska            2099 PLN =  2099.00 zł
Niemcy             449 EUR =  1908.25 zł
USA                499 USD =  1946.10 zł
Wielka Brytania    429 GBP =  2145.00 zł

Najtaniej: Niemcy, 1908.25 zł
```

Działa. A stary projekt?

```bash
cd ../stary-projekt
python kieszonkowe.py
```

Przeczytaj uważnie, co wypisał `pip install` w nowym projekcie, oraz ostatnią linijkę błędu w starym. Sprawdź `pip list`. Dlaczego stary projekt przestał działać, choć nikt nie zmienił w nim ani jednej linijki? Czy da się mieć w jednym środowisku dwie wersje tej samej biblioteki?

Na koniec wyjdź ze środowiska i usuń je:

```bash
deactivate
rm -rf ~/venv-wspolny
```

## Krok 3. Każdy projekt ma własne środowisko

Środowisko venv tworzy się zwykle w katalogu projektu, w ukrytym katalogu `.venv`:

```bash
cd ~/python-belzyce-01-srodowisko/03-dwa-projekty-jeden-komputer/stary-projekt
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python kieszonkowe.py
pip freeze
which python
deactivate
```

- `pip freeze` wypisuje zainstalowane biblioteki z wersjami — w tym samym formacie co `requirements.txt` (`pip freeze > requirements.txt` zapisuje taką listę do pliku),
- `which python` pokazuje, który Python się uruchamia: ten z `.venv` projektu.

Zrób to samo w `nowy-projekt` (z programem `porownywarka.py`).

Teraz sprawdź, że oba działają **jednocześnie**: otwórz dwa terminale (w terminalu Ubuntu: **Ctrl+Shift+T** otwiera nową kartę). W pierwszym aktywuj środowisko starego projektu i uruchom `kieszonkowe.py`, w drugim — środowisko nowego i `porownywarka.py`. Każdy program widzi swoją wersję biblioteki.

## Krok 4. Zagadki

1. **Bez aktywacji.** Uruchom `kieszonkowe.py` ze środowiskiem starego projektu jednym poleceniem, bez `source …/activate`. Wskazówka: gdzie leży Python, którego pokazało `which python`? Porównaj `echo $PATH` przed aktywacją środowiska i po niej — co tak naprawdę robi `activate`?
2. **Zepsuj i napraw.** W aktywnym środowisku nowego projektu zainstaluj starą wersję biblioteki: `pip install ../paczki/kantor-1.0.0-py3-none-any.whl` i uruchom `porownywarka.py`. Jaki błąd dostajesz i w której linijce? Napraw środowisko jednym poleceniem, nie wpisując numeru wersji.
3. **Środowisko jest jednorazowe.** Usuń środowisko nowego projektu (`deactivate`, potem `rm -rf .venv`) i odtwórz je. Ile poleceń potrzeba? Sprawdź, ile miejsca zajmuje `.venv` (`du -sh .venv`), i zobacz w `../../.gitignore`, dlaczego `git status` w repozytorium w ogóle go nie pokazuje. Do Gita trafia przepis (`requirements.txt`), a nie środowisko.
4. **Dla dociekliwych.** `pip show kantor` pokazuje, gdzie leży biblioteka (`Location`). Zajrzyj tam i obejrzyj jej kod. Porównaj kod obu wersji: `diff` z dwiema ścieżkami do plików `__init__.py`.

## Ściąga

| Polecenie | Co robi |
| --- | --- |
| `python3 -m venv .venv` | tworzy środowisko w katalogu `.venv` |
| `source .venv/bin/activate` | włącza środowisko (w linii poleceń widać `(.venv)`) |
| `pip install -r requirements.txt` | instaluje biblioteki z listy |
| `pip list`, `pip freeze` | pokazuje zainstalowane biblioteki; `freeze` w formacie `requirements.txt` |
| `pip freeze > requirements.txt` | zapisuje listę bibliotek do pliku |
| `deactivate` | wyłącza środowisko |
| `rm -rf .venv` | usuwa środowisko (projekt zostaje) |
