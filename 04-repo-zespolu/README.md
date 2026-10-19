![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 04. Repozytorium zespołu

Przez cały kurs w zespołach 2–3 osobowych budujecie projekt końcowy: **quiz wiedzy** albo **grę tekstową**. Dziś zakładacie dla niego repozytorium Git — z porządną strukturą katalogów, własnym środowiskiem venv i pierwszym commitem — i wysyłacie je na serwer. Na koniec sprawdzicie, czy umiecie posprzątać po sabotażyście.

**Czas:** ok. 40 minut (z tego sabotaż 10–15 minut) · **Dzień 2** (27.10)

## Krok 0. Ustalenia

- Wybierzcie: quiz wiedzy czy gra tekstowa, i wymyślcie nazwę projektu: małe litery, cyfry i myślniki, bez spacji i polskich znaków, np. `quiz-o-kosmosie` albo `ucieczka-z-zamku`. Poniżej przykład dla quizu — przy grze zamiast katalogu `quiz/` zróbcie `gra/`.
- Jedna osoba (lider) zakłada repozytorium na swoim komputerze. Reszta dołącza w kroku 5.
- Każdy u siebie sprawdza, czy Git wie, kim jest (ćwiczenie 00, krok 6): `git config --global --list`. Dodatkowo ustawcie, żeby `git pull` nie zadawał pytań:
  ```bash
  git config --global pull.rebase true
  ```

## Krok 1. Struktura katalogów

```text
quiz-o-kosmosie/
├── README.md          opis projektu: co to jest, kto robi, jak uruchomić
├── .gitignore         czego Git ma nie śledzić
├── requirements.txt   lista bibliotek (na razie pusta)
├── quiz/              kod programu
│   └── main.py        punkt startowy, na razie ekran tytułowy
├── dane/              pytania, plansze, zapisy gry
│   └── pytania.txt
└── testy/             testy (pojawią się w kolejnych modułach)
    └── .gitkeep
```

Lider buduje tę strukturę w terminalu:

```bash
cd ~
mkdir quiz-o-kosmosie
cd quiz-o-kosmosie
mkdir quiz dane testy
touch README.md quiz/main.py dane/pytania.txt testy/.gitkeep
code .
```

Git nie śledzi pustych katalogów. Pusty plik `.gitkeep` to umowny sposób, żeby katalog `testy/` trafił do repozytorium, zanim pojawią się w nim testy.

W VS Code wpiszcie do `quiz/main.py` ekran tytułowy (z waszymi imionami):

```python
print("=" * 44)
print("            QUIZ O KOSMOSIE")
print("     zespół: Ola, Kuba i Natalia")
print("=" * 44)
print("Wkrótce: pytania, punkty i ranking.")
```

Sprawdźcie: `python3 quiz/main.py`. Do `dane/pytania.txt` wpiszcie dwa, trzy pierwsze pytania, w dowolnym formacie, np. `Najbliższa Ziemi gwiazda?;Słońce`. Do `README.md` — nazwę projektu, skład zespołu i polecenie, którym uruchamia się program.

## Krok 2. Własne środowisko venv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip freeze > requirements.txt
```

Projekt nie używa jeszcze żadnych bibliotek, więc `requirements.txt` jest pusty — to też informacja. Gdy zainstalujecie bibliotekę, zapiszcie listę od nowa tym samym `pip freeze > requirements.txt`.

## Krok 3. `git init` i `.gitignore`

```bash
git init -b main
git status
```

`git init -b main` zakłada repozytorium z gałęzią główną o nazwie `main` (taką nazwę ma też GitHub). `git status` pokazuje pliki nieśledzone (*Untracked files*). Jest wśród nich `.venv/`? Środowisko ma tysiące plików i działa tylko na tym jednym komputerze, więc nie wrzucamy go do repozytorium — każdy odtworzy je sobie z `requirements.txt` (ćwiczenie 03). Na Pythonie 3.13 i nowszym `venv` sam ukrywa się przed Gitem, więc `.venv/` może nie być na liście; pozostali w zespole mogą mieć starszego Pythona, więc i tak zróbcie `.gitignore`.

Utwórzcie plik `.gitignore` (w VS Code albo poleceniem `code .gitignore`) z taką treścią:

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
```

Jeszcze raz `git status` — `.venv/` zniknął z listy, a pojawił się `.gitignore`.

## Krok 4. Pierwszy commit

```bash
git add .
git status
git commit -m "Struktura projektu i ekran tytułowy"
git log --oneline
git status
```

- `git add .` przygotowuje wszystkie zmiany do zapisania (*staging*) — `git status` pokazuje je teraz na zielono jako *Changes to be committed*,
- `git commit -m "…"` zapisuje je w historii z opisem; opis mówi, **co** zmieniliście, krótko i konkretnie,
- `git log --oneline` pokazuje historię: jeden commit w jednej linijce,
- na koniec `git status` powinien powiedzieć *nothing to commit, working tree clean*.

## Krok 5. Wysyłka na serwer (`push`)

### Ścieżka A: GitHub

1. **Lider** zakłada na github.com nowe repozytorium (**+** → **New repository**): nazwa taka jak folder, *Public* albo *Private*, **bez** zaznaczania „Add a README file” — repozytorium na GitHubie ma być puste.
2. Lider dodaje kolegów: **Settings → Collaborators → Add people**. Koledzy muszą zaakceptować zaproszenie (przychodzi e-mailem).
3. Logowanie z terminala: przy `push` GitHub nie przyjmuje hasła do konta. Są dwie drogi:
   - **token (HTTPS):** na GitHubie **Settings → Developer settings → Personal access tokens** → wygeneruj token z dostępem do repozytoriów i wklej go zamiast hasła, gdy `git push` zapyta o *Password*. Token to hasło — nie wklejaj go nigdzie indziej,
   - **klucz SSH:** `ssh-keygen -t ed25519 -C "twoj@email.pl"` (trzy razy Enter), potem `cat ~/.ssh/id_ed25519.pub` i wklej wynik na GitHubie w **Settings → SSH and GPG keys → New SSH key**. Adres repozytorium ma wtedy postać `git@github.com:LOGIN/quiz-o-kosmosie.git`.
4. Lider łączy repozytorium z GitHubem i wysyła commit:
   ```bash
   git remote add origin https://github.com/LOGIN/quiz-o-kosmosie.git
   git push -u origin main
   ```
5. **Koledzy** pobierają repozytorium i odtwarzają środowisko:
   ```bash
   cd ~
   git clone https://github.com/LOGIN/quiz-o-kosmosie.git
   cd quiz-o-kosmosie
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python3 quiz/main.py
   ```
6. Każdy dopisuje własne pytanie w osobnym pliku (żeby nie edytować naraz tego samego), np. `dane/pytania-kuba.txt`, i wysyła je:
   ```bash
   git add dane/pytania-kuba.txt
   git commit -m "Pytanie od Kuby"
   git push
   ```
   Jeśli `git push` zostanie odrzucony (*rejected … fetch first*), ktoś był szybszy: najpierw `git pull`, potem znowu `git push`. Na koniec wszyscy robią `git pull` i sprawdzają `git log --oneline` — historia powinna być u wszystkich taka sama.

### Ścieżka B: bez kont — „serwer” na własnym komputerze

Repozytorium „gołe” (*bare*) to repozytorium bez plików roboczych, samą historią — tak wygląda repozytorium po stronie serwera GitHuba. Możecie zrobić takie na własnym komputerze i ćwiczyć na nim `push`, `clone` i `pull`:

```bash
git init --bare -b main ~/serwer/quiz.git
cd ~/quiz-o-kosmosie
git remote add origin ~/serwer/quiz.git
git push -u origin main
```

Drugi członek zespołu to drugi folder na tym samym komputerze:

```bash
git clone ~/serwer/quiz.git ~/kolega/quiz
cd ~/kolega/quiz
echo "Jak nazywa się nasza galaktyka?;Droga Mleczna" > dane/pytania-kuba.txt
git add dane/pytania-kuba.txt
git commit -m "Pytanie od Kuby"
git push
cd ~/quiz-o-kosmosie
git pull
git log --oneline
```

Gdy założycie konto na GitHubie, wystarczy zmienić adres serwera: `git remote set-url origin https://github.com/LOGIN/quiz-o-kosmosie.git` i `git push -u origin main`.

## Krok 6. Sabotaż

W repozytorium zespołu grasuje sabotażysta. Program `sabotaz.py` z tego folderu zmienia treść dwóch śledzonych plików, usuwa jeden plik i podrzuca śmieci. Wasze zadanie: znaleźć wszystkie szkody i je naprawić — samym Gitem, bez kasowania repozytorium i klonowania go od nowa.

1. `git status` musi pokazywać *nothing to commit, working tree clean* (inaczej sabotażysta odmówi pracy, żeby nie zniszczyć waszych zmian).
2. Jedna osoba z zespołu odwraca się od ekranu, druga uruchamia sabotaż:
   ```bash
   cd ~/quiz-o-kosmosie
   python3 ~/python-belzyce-01-srodowisko/04-repo-zespolu/sabotaz.py
   ```
3. Osoba, która nie patrzyła, szuka szkód i naprawia repozytorium. Koniec, gdy `git status` znowu pokazuje czyste drzewo, a `python3 quiz/main.py` działa jak wcześniej. Potem zamiana ról.

<details>
<summary>Podpowiedź 1: co się zmieniło?</summary>

`git status` pokazuje trzy rodzaje szkód: pliki zmienione (*modified*), usunięte (*deleted*) i nowe, nieśledzone (*Untracked files*). `git diff` pokazuje, co dokładnie się zmieniło: linie z `-` to stara treść, z `+` — nowa. Jedna zmiana jest łatwa do przeoczenia.
</details>

<details>
<summary>Podpowiedź 2: zmienione i usunięte pliki</summary>

`git restore PLIK` przywraca plik do stanu z ostatniego commita — zarówno zmieniony, jak i usunięty. `git restore .` robi to ze wszystkimi plikami naraz. Uwaga: zmian cofniętych przez `git restore` nie da się odzyskać.
</details>

<details>
<summary>Podpowiedź 3: śmieci</summary>

Nowe pliki nie są w żadnym commicie, więc `git restore` ich nie dotyczy. Usuwa je `git clean`, ale najpierw zawsze sprawdź, co zamierza usunąć: `git clean -n` (same pliki) albo `git clean -nd` (także katalogi). Gdy lista się zgadza: `git clean -fd`. `git clean` usuwa na zawsze także wasze nowe pliki, których jeszcze nie dodaliście do commita. Nigdy nie dodawaj `-x` — to usunęłoby też `.venv`.
</details>

**Wersja trudniejsza.** `python3 ~/python-belzyce-01-srodowisko/04-repo-zespolu/sabotaz.py --commit` — sabotażysta zatrze ślady: zrobi commit ze swoimi zmianami, więc `git status` będzie czysty. Znajdźcie go w historii (`git log --oneline`, `git log --format="%h %an %s"`), obejrzyjcie szkody (`git show --stat HEAD`, `git show HEAD`) i cofnijcie je nowym commitem: `git revert --no-edit HEAD`. Dlaczego lepiej cofnąć commit nowym commitem, niż usunąć go z historii, kiedy repozytorium jest już na GitHubie?

Prowadzący może sprawdzić, co zrobił sabotażysta: `python3 ~/python-belzyce-01-srodowisko/04-repo-zespolu/sabotaz.py --zdradz` (w repozytorium zespołu).

## Na koniec

- `git status` — czyste drzewo,
- `git log --oneline` — historia ze wszystkimi commitami zespołu,
- repozytorium jest na serwerze (GitHub albo `~/serwer/quiz.git`), a każdy w zespole ma jego klon i własny `.venv`.

Do tego repozytorium będziecie dokładać kod przez cały kurs. Commitujcie często i małymi krokami — sabotaż pokazał, że Git odda tylko to, co było w commicie.
