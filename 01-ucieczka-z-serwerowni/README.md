![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 01. Ucieczka z serwerowni — gra terenowa w terminalu

Piątek, 21:47. Zostajesz po praktykach w Lubelskim Centrum Danych, żeby dokończyć konfigurację serwera. Nagle gaśnie światło, a system bezpieczeństwa CERBER ogłasza: „WYKRYTO INTRUZA. BLOKADA WSZYSTKICH DRZWI”. Telefon nie ma zasięgu. Działa tylko terminal.

Drzwi otworzy hasło awaryjne z czterech fragmentów. Każdy fragment zdobędziesz w innej strefie budynku — samymi poleceniami Linuksa.

**Czas:** 60–75 minut · **Dzień 1** (26.10)

## Start

```bash
cd ~/python-belzyce-01-srodowisko/01-ucieczka-z-serwerowni
python3 start.py
cd ~/serwerownia
cat CZYTAJ_MNIE.txt
```

`start.py` buduje świat gry w katalogu `~/serwerownia` i losuje hasło — każdy ma inne, więc nie da się go ściągnąć od sąsiada. CERBER mierzy czas od tej chwili: na koniec zobaczysz swój wynik.

Zasady:

- wszystko robisz w terminalu; edytor nie jest potrzebny,
- nie ruszaj pliku `.stan` ani katalogu `.silnik` w `~/serwerownia` — to pamięć i mózg CERBERA,
- strażnicy mówią, czego jeszcze brakuje — czytaj ich komunikaty uważnie.

## Ściąga

| Polecenie | Co robi |
| --- | --- |
| `pwd` | pokazuje, w którym katalogu jesteś (*print working directory*) |
| `ls`, `ls -a`, `ls -l` | lista plików; `-a` także ukrytych (nazwa od kropki); `-l` z prawami i rozmiarem |
| `cd KATALOG`, `cd ..`, `cd ~`, `cd -` | wejdź do katalogu; piętro wyżej; do katalogu domowego; z powrotem do poprzedniego katalogu |
| `cat PLIK` | wypisuje zawartość pliku |
| `mkdir KATALOG`, `mkdir -p A/B/C` | tworzy katalog; `-p` od razu z katalogami po drodze |
| `cp CO GDZIE` | kopiuje plik (oryginał zostaje) |
| `mv CO GDZIE` | przenosi plik albo zmienia jego nazwę |
| `touch PLIK` | tworzy pusty plik |
| `rm PLIK`, `rmdir KATALOG`, `rm -r KATALOG` | usuwa plik; pusty katalog; katalog z całą zawartością |
| `chmod u+x PLIK`, `chmod 600 PLIK` | zmienia prawa dostępu: literami albo liczbą ósemkową |
| `echo "tekst" >> PLIK` | dopisuje linię na końcu pliku (`>` zamiast `>>` nadpisuje cały plik!) |
| `*` we wzorcu | dowolny ciąg znaków, np. `ls *.txt` — wszystkie pliki kończące się na `.txt` |

Klawisze: **Tab** dopełnia nazwy plików (naciśnij dwa razy, żeby zobaczyć podpowiedzi), **strzałka w górę** przywraca poprzednie polecenie, **Ctrl+C** przerywa program, **Ctrl+L** czyści ekran.

**Ścieżki.** Ścieżka bezwzględna zaczyna się od `/` albo `~` i działa z każdego miejsca (`~/serwerownia/magazyn`). Ścieżka względna liczy się od katalogu, w którym jesteś (`magazyn/rampa`, `../hala`).

## Poziom 1. Recepcja — orientacja w terenie

Fragment 1 leży gdzieś w archiwum (`~/serwerownia/archiwum`), ale archiwum ma setki plików i kilka fałszywych tropów. Trop zaczyna się w recepcji: przeczytaj `recepcja/CZYTAJ_MNIE.txt` i rozejrzyj się po biurku portiera. Tego fragmentu nie wyda żaden strażnik — gdy znajdziesz kopertę, po prostu go zapisz.

Polecenia: `pwd`, `ls`, `ls -a`, `cd`, `cat`.

<details>
<summary>Podpowiedź 1</summary>

W recepcji są dwa ważne papiery: lista pracowników w `biurko/` i tablica ogłoszeń. Jedno mówi, *kiedy* pan Mariusz zaczął pracę, drugie — *gdzie* trzyma swoje rzeczy. Sprawdź też `ls -a` w samej recepcji.
</details>

<details>
<summary>Podpowiedź 2</summary>

Pan Mariusz zaczął pracę w 2017 roku, więc szukaj w `archiwum/2017`. Plik `haslo.txt` to pułapka. Prywatne rzeczy Mariusza są w katalogu, którego zwykłe `ls` nie pokazuje.
</details>

<details>
<summary>Podpowiedź 3</summary>

`cd ~/serwerownia/archiwum/2017`, potem `ls -a` — katalog z kropką na początku nazwy. W środku jest biurko z szufladami; notatka portiera mówi, która szuflada. W szufladzie znowu przyda się `ls -a`. Uważaj na kopertę z innego rocznika — sprawdź, czy jest ważna.
</details>

## Poziom 2. Magazyn — budowanie

Kierowniczka magazynu zostawiła listę zadań w `magazyn/CZYTAJ_MNIE.txt`: postawić regały z półkami, rozładować rampę (każda paczka ma w środku etykietę z miejscem), rozdać instrukcję BHP do regałów, poprawić nazwę pliku ze spisem i zgłosić gotowość. Wynik sprawdza strażnik:

```bash
cd ~/serwerownia/magazyn
python3 straznik.py
```

Polecenia: `mkdir -p`, `cat`, `mv`, `cp`, `touch`.

<details>
<summary>Podpowiedź 1</summary>

`mkdir -p regal-A/polka-1` tworzy od razu regał i półkę. Do `mkdir` możesz podać wiele katalogów naraz. Skrót dla leniwych: `mkdir -p regal-{A,B,C}/polka-{1,2,3}` — powłoka sama rozwinie nawiasy klamrowe na 9 ścieżek (sprawdź: `echo regal-{A,B,C}/polka-{1,2,3}`).
</details>

<details>
<summary>Podpowiedź 2</summary>

`cat rampa/paczka-01.txt` pokazuje etykietę. Przenosząc, pisz ukośnik na końcu katalogu docelowego: `mv rampa/paczka-01.txt regal-B/polka-2/`. Gdy katalogu nie ma, `mv` z ukośnikiem zgłosi błąd, a bez ukośnika — po cichu zmieni nazwę paczki na `polka-2`.
</details>

<details>
<summary>Podpowiedź 3</summary>

Instrukcję kopiujesz trzy razy: `cp instrukcja-bhp.txt regal-A/` i tak dalej. Nazwę ze spacjami i nawiasami weź w cudzysłów: `mv "Spis Inwentarza (kopia) FINAL.TXT" spis-inwentarza.txt` — albo wpisz `mv Spis` i naciśnij Tab. Pusty plik: `touch gotowe.txt`.
</details>

## Poziom 3. Sejf — prawa dostępu

Fragment 3 leży w sejfie, który otwiera program `./otworz.py SZYFR`. Szyfr jest w `sejf/skrytka/szyfr.txt`, ale CERBER odebrał prawa do skrytki i do szyfru, a programowi — prawo wykonywania. Regulamin sejfu w `sejf/CZYTAJ_MNIE.txt` wymaga jeszcze wpisu do dziennika (który jest tylko do odczytu) i ustawienia praw zapisem ósemkowym.

Polecenia: `ls -l`, `ls -ld`, `chmod`, `echo >>`.

Jak czytać prawa w `ls -l`: `-rwxr-x---` to typ (`-` plik, `d` katalog) i trzy trójki: właściciel (`u`), grupa (`g`), pozostali (`o`). W każdej trójce: `r` — odczyt, `w` — zapis, `x` — wykonywanie (dla katalogu: wejście do niego), `-` — brak prawa.

<details>
<summary>Podpowiedź 1</summary>

`ls -l` w sejfie: skrytka ma `d---------`, a `otworz.py` nie ma `x`. Dla katalogu `r` pozwala obejrzeć listę plików, a `x` — wejść do środka i dostać się do plików. `chmod u+rwx skrytka` dodaje właścicielowi (`u`) wszystkie trzy prawa.
</details>

<details>
<summary>Podpowiedź 2</summary>

Kolejno: `chmod u+r skrytka/szyfr.txt` i `cat skrytka/szyfr.txt`; `chmod +x otworz.py` i `./otworz.py SZYFR`. Dziennik: `chmod u+w dziennik-wejsc.txt`, potem `echo "OTWIERA: Ola" >> dziennik-wejsc.txt`. Dwa znaki `>>` dopisują, jeden `>` kasuje całą starą treść.
</details>

<details>
<summary>Podpowiedź 3</summary>

Zapis ósemkowy: `r` = 4, `w` = 2, `x` = 1, a cyfra trójki to suma. `rwx` = 4+2+1 = 7, `rw-` = 4+2 = 6, `---` = 0. Trzy cyfry to kolejno właściciel, grupa i pozostali, więc `rwx------` to `700`, a `rw-------` to `600`.
</details>

## Poziom 4. Hala serwerów — sprzątanie

W `hala/logi` jest ponad 200 plików. Pliki tymczasowe `.tmp` trzeba usunąć, kopie `.bak` przenieść do katalogu `kosz/`, a wszystkie logi `.log` zostawić. Do tego dwa katalogi do usunięcia: pusty i pełny. Szczegóły w `hala/CZYTAJ_MNIE.txt`, sprawdzenie: `python3 straznik.py` w hali.

Polecenia: `ls` ze wzorcem `*`, `rm`, `mv`, `mkdir`, `rmdir`, `rm -r`.

> **Uwaga: `rm` usuwa na zawsze.** W terminalu nie ma kosza, z którego można coś wyciągnąć. Zanim usuniesz pliki wzorcem, wypisz je tym samym wzorcem przez `ls` i sprawdź, co do niego pasuje. Nigdy nie wpisuj `rm -r *` ani `sudo rm`, jeśli nie masz absolutnej pewności, gdzie jesteś (`pwd`).

<details>
<summary>Podpowiedź 1</summary>

Policz, zanim usuniesz: `ls logi | wc -l` (wszystkie pliki), `ls logi/*.tmp | wc -l` (same `.tmp`). `wc -l` liczy linie tego, co wypisało polecenie przed `|`.
</details>

<details>
<summary>Podpowiedź 2</summary>

`*.tmp` to „cokolwiek, a na końcu `.tmp`”. Wzorzec `*tmp*` („`tmp` gdziekolwiek w nazwie”) złapie też plik, który tylko udaje plik tymczasowy. Wzorzec `*` nie pasuje do nazw zaczynających się od kropki — po `rm logi/*.tmp` sprawdź `ls -a logi | grep tmp`.
</details>

<details>
<summary>Podpowiedź 3</summary>

`mkdir kosz`, potem `mv logi/*.bak kosz/`. Pusty katalog usuwa `rmdir stary-serwer`; na pełnym `rmdir` zgłosi `Directory not empty` — wtedy obejrzyj go (`ls -R zepsuty-serwer`) i usuń z zawartością: `rm -r zepsuty-serwer`.
</details>

## Finał

Gdy masz cztery fragmenty:

```bash
cd ~/serwerownia
python3 wyjscie.py
```

Wpisz fragmenty po kolei, oddzielone myślnikami, np. `lis-kot-pies-mysz`. CERBER wypisze twój czas — porównaj go z innymi.

**Bonus.** Zapisz historię swoich poleceń do pliku i uruchom `wyjscie.py` jeszcze raz:

```bash
history > ~/serwerownia/moje-komendy.txt
cat ~/serwerownia/moje-komendy.txt
```

Znak `>` przekierowuje to, co polecenie wypisuje, do pliku zamiast na ekran (i nadpisuje plik). Ile poleceń było potrzeba? `wc -l ~/serwerownia/moje-komendy.txt`.

## Gdy coś pójdzie nie tak

- **Coś zniknęło przez pomyłkę?** Strażnicy magazynu i hali oraz sejf mają kopię zapasową: `python3 straznik.py --kopia-zapasowa` (w sejfie: `./otworz.py --kopia-zapasowa`). Każde przywrócenie kosztuje 3 minuty kary doliczone do czasu.
- **Zniknął skrypt strażnika?** W folderze z grą: `python3 start.py --napraw` — przywraca skrypty, postęp zostaje.
- **Chcesz zacząć od zera?** `python3 start.py --od-nowa` — usuwa `~/serwerownia` i buduje nowy świat z nowym hasłem; czas liczy się od nowa.
