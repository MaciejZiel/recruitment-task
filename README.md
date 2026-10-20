# callflow: od rozmowy z klientem do zweryfikowanych działań

`callflow` bierze transkrypcję rozmowy z klientem i zamienia ją w listę tego, co z rozmowy wynika: błędy,
zmiany konfiguracji agenta, zadania, prośby o funkcje, rzeczy, na które czekamy, zakazy i szkice wiadomości.
Model (Claude) tylko interpretuje rozmowę i zwraca JSON zgodny ze schematem. Deterministyczny kod sprawdza
każdy cytat-dowód w transkrypcji (mówca i numer linii), kontroluje pola i rozdziela pozycje do skrzynek.
Głównym interfejsem jest lokalna aplikacja webowa (`callflow-web`); to samo robi z wiersza poleceń CLI
(`callflow`). Do klienta nic nie trafia automatycznie, a konfiguracja agenta się nie zmienia: aplikacja
przygotowuje raport, dane dla integracji i szkice wiadomości do zatwierdzenia przez człowieka.

## Co oddaję

| Element z zadania | Gdzie w repo |
|---|---|
| Aplikacja | `uv run callflow-web`, potem http://127.0.0.1:8000/ ([opis](#aplikacja-webowa)): wklejasz lub wczytujesz transkrypcję, uruchamiasz analizę i przeglądasz wynik (pozycje w skrzynkach z cytatami, zabezpieczenia, terminy, szkice) oraz historię analiz. Alternatywnie CLI: `uv run callflow` ([opis](#cli)) |
| Prototyp procesu | [`docs/process.md`](docs/process.md): proces docelowy i stany pozycji (Mermaid), skrzynki, bezpieczniki, co jest, a czego nie ma |
| Demo na załączonej transkrypcji | [`examples/output/auto-tama/report.md`](examples/output/auto-tama/report.md) (czytelny bezpośrednio na GitHubie), [`report.html`](examples/output/auto-tama/report.html) (ten sam raport jako strona; GitHub pokazuje źródło HTML, więc plik trzeba pobrać i otworzyć lokalnie w przeglądarce) oraz `outbox.json` (wersja maszynowa), `drafts/` (szkice wiadomości), `extraction.json` (zwalidowany wynik modelu), `raw_response.json` (surowa odpowiedź `claude -p`) |
| Logi z pracy z AI | [`ai-logs/`](ai-logs/): wyeksportowane rozmowy z Claude Code |

Dodatkowo: druga, fikcyjna rozmowa z innej branży do testów ([`examples/druga-rozmowa.md`](examples/druga-rozmowa.md))
i jej wynik w [`examples/output/dentavita/`](examples/output/dentavita/report.md), a także niezależny wzorzec
odpowiedzi dla rozmowy z Auto Tama ([`eval/reference.md`](eval/reference.md)). Trzecia, też syntetyczna
rozmowa ([`examples/synthetic/fitstudio-rozmowa.md`](examples/synthetic/fitstudio-rozmowa.md), wynik
w [`examples/output/fitstudio/`](examples/output/fitstudio/report.md)) jest jednym z przykładów w aplikacji.
[`examples/transkrypcja-spotkanie.json`](examples/transkrypcja-spotkanie.json) to załączona transkrypcja
rozbita na wypowiedzi z mówcą i numerem linii (`uv run python -m callflow.transcript
examples/transkrypcja-spotkanie.md -o examples/transkrypcja-spotkanie.json`).

## Jak to działa

Diagramy procesu i stanów są w [`docs/process.md`](docs/process.md). W skrócie (`src/callflow/`):

1. **`transcript.py`**: parsuje plik `.md`/`.txt` na wypowiedzi z mówcą i numerem linii, czyta datę spotkania
   z nagłówka.
2. **`prompt.py`**: buduje prompt. Prompt systemowy jest ogólny (rozmowa B2B, nic o Auto Tama). Wiadomość zawiera
   dostawcę (`--vendor`), datę spotkania z kalendarzem dni (7 dni wstecz, 35 naprzód) i transkrypcję wydzieloną
   znacznikami jako dane.
3. **`llm.py`**: jedno wywołanie `claude -p` z JSON Schema wygenerowanym z modeli pydantic (`schema.py`), bez
   narzędzi, serwerów MCP, ustawień użytkownika i zapisu sesji.
4. **`extract.py`**: waliduje odpowiedź względem schematu; inną datę spotkania niż podana zastępuje datą znaną
   programowi i zapisuje to w założeniach raportu.
5. **`verify.py`**: deterministycznie szuka każdego cytatu w wypowiedziach wskazanego mówcy i sprawdza pola
   (lista niżej).
6. **`route.py`**: regułami (`kind` + `state` od modelu) przypisuje pozycje do skrzynek: zakazy, zgłoszenia błędów,
   zmiany konfiguracji, zadania, backlog, czekamy na klienta, ryzyka, wstrzymane, bez działania. Pozycje
   `scheduled` i `waiting_on_client` z datą trafiają do kalendarza.
7. **`render.py`**: zapisuje `report.md`, `outbox.json` (`requires_approval: true`, `needs_review` przy
   niezweryfikowanych cytatach) i `drafts/D*.md`.
8. **`html_report.py`**: zapisuje `report.html`, ten sam raport w tej samej kolejności jako jeden plik HTML
   (CSS i JS wbudowane, z zewnątrz tylko font z Google Fonts), w stylistyce rinvo.io bez logo i grafik.
9. **`web/runs.py`**: waliduje żądanie z przeglądarki, wykonuje przebiegi po kolei w wątku w tle tym samym
   pipeline'em co CLI (kroki 1–8) i zapisuje je w `runs/<id>/`; po restarcie wczytuje historię.
10. **`web/server.py`** i **`web/static/`**: serwer HTTP z biblioteki standardowej (`ThreadingHTTPServer`)
    z API JSON (`/api/examples`, `/api/runs`, `/api/runs/<id>`, `/api/runs/<id>/result`) i plikami przebiegów
    oraz jednostronicowy frontend w czystym HTML/CSS/JS, bez frameworka i kroku budowania.

## Uruchomienie

Wymagania:

- Python 3.12+ i [uv](https://docs.astral.sh/uv/).
- Zainstalowany i zalogowany Claude Code CLI (`claude`). Silnikiem LLM jest `claude -p`, więc klucz API nie jest
  potrzebny. Na Windows npm instaluje shim `claude.cmd`; `llm.py` omija go automatycznie i woła natywny
  `claude.exe`, bo przez `cmd.exe` psują się cudzysłowy i nowe linie w prompcie.
- Tryb offline (w aplikacji „Pokaż zapisany wynik przykładu”, w CLI `--from-json`) nie potrzebuje Claude.

```bash
uv sync
```

### Aplikacja webowa

```bash
uv run callflow-web
```

Aplikacja działa pod http://127.0.0.1:8000/ (inny adres: `--port`, `--host`). Serwer używa tylko biblioteki
standardowej Pythona; z zewnątrz frontend pobiera jedynie font z Google Fonts.

Ekrany:

1. **Nowa analiza**: wklejenie transkrypcji, wczytanie pliku `.md`/`.txt` albo wybór przykładu (Auto Tama,
   DentaVita, FitStudio); data spotkania (puste pole: data z nagłówka transkrypcji), firma (`vendor`) i dokładność
   (`effort`: niska, średnia, wysoka).
2. **Przebieg**: etapy analizy (wczytanie, analiza AI, weryfikacja cytatów, raport), licznik czasu, ostrzeżenia
   i błędy.
3. **Wynik**: statystyki (pozycje, zabezpieczenia, szkice, zweryfikowane cytaty, ostrzeżenia, czas, koszt), kafelki
   i zakładki per skrzynka oraz dla zabezpieczeń, terminów i szkiców, karty pozycji z cytatami (numer linii, status
   weryfikacji), szkice z przyciskiem „Kopiuj treść”, linki do `report.html`, `report.md` i `outbox.json`.
4. **Historia**: zapisane analizy od najnowszej, z wynikiem albo przebiegiem.

Dwa tryby:

- **„Uruchom analizę (Claude)”**: przebieg na żywo przez `claude -p`; kosztuje (patrz [CLI](#cli)) i trwa około
  1–5 minut zależnie od długości rozmowy i dokładności. Naraz działa jedna analiza na żywo; kolejna zgłoszona
  w tym czasie dostaje błąd.
- **„Pokaż zapisany wynik przykładu”**: bez modelu i bez kosztów; weryfikacja, routing i raport z zapisanego
  `extraction.json` przykładu. Wymaga niezmienionej transkrypcji przykładu; zmieniony tekst trzeba analizować
  na żywo. Data spotkania pochodzi z zapisanego wyniku.

Bezpieczeństwo: domyślnie serwer słucha tylko na adresie pętli zwrotnej i nie ma uwierzytelniania. Odrzuca
żądania z obcym nagłówkiem `Host` (ochrona przed DNS rebinding) oraz `POST` z obcym `Origin`. Adres inny niż
pętla zwrotna wymaga `--allow-remote`, które wyłącza kontrolę `Host` i udostępnia aplikację bez żadnej ochrony,
więc tylko w zaufanej sieci.

Zapis: każda analiza ma katalog `runs/<id>/` w bieżącym katalogu (`transcript.md`, `run.json`, `extraction.json`,
`raw_response.json` przy przebiegu na żywo, `result.json`, `report.md`, `report.html`, `outbox.json`, `drafts/`).
`runs/` jest w `.gitignore`. Historia przetrwa restart serwera; analizy przerwane wyłączeniem serwera są oznaczane
jako przerwane.

### CLI

Uruchomienie na żywo na załączonej transkrypcji. Trwa około 4–5 minut i kosztuje około 0,7–0,9 USD użycia Claude
(domyślnie `claude-opus-5-5`, `--effort high`; zapisany przebieg demo: 278 s, 0,85 USD). `--effort medium` jest
szybsze. Krótsza rozmowa DentaVita: 56 s, 0,20 USD.

```bash
uv run callflow examples/transkrypcja-spotkanie.md --out out/auto-tama
```

Offline, bez Claude: weryfikacja, routing i raport z zapisanego wyniku modelu.

```bash
uv run callflow examples/transkrypcja-spotkanie.md --out out/demo --from-json examples/output/auto-tama/extraction.json
```

`out/demo/report.html` otwiera się w przeglądarce dwuklikiem, bez serwera.

Inna rozmowa: dowolny plik `.md` lub `.txt` z wypowiedziami w liniach `**Imię:** tekst` albo `Imię: tekst`
(dopuszczalny znacznik czasu, np. `[00:01:02] Imię: tekst`). Jeśli plik ma sekcję `## Transkrypcja` lub
`## Transcript`, tylko ona jest traktowana jako dialog. Datę spotkania program czyta z nagłówka przed pierwszą
sekcją `##` (formaty `6 października 2026`, `2026-10-06`, `6.10.2026`).

```bash
uv run callflow sciezka/do/rozmowy.md --out out/inna --meeting-date 2026-10-20 --vendor Rinvo
```

- `--meeting-date YYYY-MM-DD` nadpisuje datę z nagłówka. Bez daty program ostrzega i działa dalej, ale terminów
  względnych („do czwartku”) nie przelicza; raport mówi o tym na górze. Z `--from-json` data pochodzi z pliku JSON.
- `--vendor` to firma, w imieniu której przygotowywane są działania (domyślnie `Rinvo`).
- `--model` i `--effort` (`low`, `medium`, `high`, `xhigh`) przekazywane są do `claude -p`.

### Jira

<!-- TODO lead: jira -->
Zgłoszenia błędów i zmiany konfiguracji mogą trafiać do Jiry (konfiguracja w `.env`).

### Testy i lint

```bash
uv run pytest
uv run ruff check src tests
```

## Wynik demo

Rozmowa Grupa Auto Tama × Rinvo z 6.10.2026 ([`report.md`](examples/output/auto-tama/report.md),
[`report.html`](examples/output/auto-tama/report.html) do otwarcia lokalnie):

- **37 pozycji, 11 zabezpieczeń, 8 szkiców**, cytaty zweryfikowane: **108/108** (każdy z numerem linii i zgodnym
  mówcą), **0 ostrzeżeń walidacji**.
- **Zabezpieczenia** (stałe zakazy z warunkiem zdjęcia i osobą, która może je zdjąć), np. Opel nie wchodzi nawet
  na polecenie Pawła, w tygodniu urlopu Kasi (19–23.10) nic nowego nie startuje, nie wierzyć wiadomościom
  „Kasia mówiła, że po godzinach od wtorku”.
- **Korekty w trakcie rozmowy**: godziny dzwonienia w sobotę 9–14 (l. 104) zmienione później na 9–15 (l. 232–234);
  raport pokazuje wersję ostateczną i wersje zastąpione.
- **Kalendarz** z datami przeliczonymi od dnia spotkania, np. 8.10 (teksty wstępu od Kasi), 9.10 (przypomnienie
  „tylko raz”), 12.10 (plik ze świeżymi leadami), 13.10 (jeden mail, jeśli pliku nie będzie), 15.10 (spotkanie
  z Pawłem, zaproszenie dopiero po potwierdzeniu Kasi). Niejednoznaczne
  terminy („w tym tygodniu”, „w przyszłym tygodniu”) są rozpisane w sekcji założeń modelu.
- **Szkice wiadomości** z warunkiem wysłania (`send_when`), np. jedno przypomnienie o tekstach wstępu tylko wtedy,
  gdy nie przyjdą do czwartku; nic nie zostało wysłane.
- **Walidacja zadziałała jak bezpiecznik**: w pierwszym przebiegu zgłosiła 4 prośby o funkcje oznaczone jako
  `scheduled` bez terminu. Zamiast wyciszać kontrolę, doprecyzowałem w prompcie znaczenie stanów; obecny przebieg
  ma 0 ostrzeżeń.
- **Druga rozmowa** ([DentaVita](examples/output/dentavita/report.md)): 6 pozycji, 3 zabezpieczenia, 3 szkice,
  19/19 cytatów.

## Jakość i weryfikacja

- **Cytaty sprawdzane dosłownie.** Każda pozycja i każde zabezpieczenie musi mieć cytat z mówcą. `verify.py`
  szuka go w wypowiedziach tego mówcy (normalizuje tylko cudzysłowy, myślniki, białe znaki i wielkość liter;
  „Kasia Malinowska” od modelu pasuje do etykiety „Kasia”). Raport podaje numer linii; cytat nieznaleziony lub
  wypowiedziany przez kogoś innego dostaje ostrzeżenie, a w `outbox.json` `needs_review: true`.
- **Kontrole pól** (`verify.py`, `extract.py`):
  - wynik niezgodny ze schematem jest odrzucany (surowa odpowiedź zostaje zapisana); inna data spotkania od modelu
    nie przerywa przebiegu, tylko jest zastępowana znaną datą z adnotacją w założeniach;
  - zduplikowane id, brak cytatu;
  - termin wcześniejszy niż spotkanie albo termin podany mimo nieznanej daty spotkania;
  - `do_now` lub `scheduled` bez właściciela, `scheduled` bez terminu;
  - zależności i szkice odwołujące się do nieistniejących pozycji, szkic niepowiązany z żadną pozycją.
- **Testy jednostkowe** (`tests/`): parser, prompt, weryfikacja, routing, render, CLI, aplikacja webowa (API,
  bezpieczeństwo ścieżek, kolejka). Nie wołają modelu
  (`claude -p` i ekstrakcja są podmieniane); fixture `tests/fixtures/extraction.json` pochodzi z prawdziwego
  przebiegu na rozmowie z Auto Tama.
- **Eval**: wynik porównywany ręcznie z [`eval/reference.md`](eval/reference.md). Wzorzec przygotował osobny agent
  AI, niezależnie od ekstraktora; nigdy nie trafia do promptu modelu.
  Wynik ([`eval/results.md`](eval/results.md), jeden przebieg, ocena agenta AI): **40/41 pozycji znalezionych
  (1 częściowo), 32/33 pułapek zaliczonych (1 częściowo), 7/7 pozycji w drugiej rozmowie, 0 pozycji
  zmyślonych**. Wykryte słabości (np. termin klienta przypięty do działania Rinvo, brak daty przy „zaraz po
  rozmowie”) są tam opisane wraz z propozycjami poprawek.

## Założenia

Zadanie każe przyjąć założenia zamiast dopytywać. Przyjąłem:

1. **Perspektywa dostawcy (Rinvo).** Działania są przygotowywane dla zespołu Rinvo (`--vendor`), bo to Rinvo ma
   obsłużyć to, co wynika z rozmowy.
2. **Wszystko, co idzie do klienta albo zmienia konfigurację agenta, czeka na zatwierdzenie człowieka.** Rozmowa
   jest pełna warunków i zastrzeżeń: „Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.” (l. 58) oraz
   „Opla nie włączam. Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie” (l. 132). Automat
   wykonujący ustalenia łatwo złamałby takie zastrzeżenie.
3. <!-- TODO lead: jira -->**Integracje (issue tracker, CRM, kalendarz, poczta, panel agenta) są stanem docelowym.** W demo zastępują je pliki
   (`report.md`, `report.html`, `outbox.json`, `drafts/`), bo tak da się pokazać cały proces bez dostępu do systemów Rinvo.
4. **Terminy względne są przeliczane od daty spotkania** według kalendarza dołączonego do promptu, a niejasne
   („w tym tygodniu”) model rozstrzyga i zapisuje jako jawne założenie w raporcie, żeby człowiek mógł je poprawić.
5. **Bez daty spotkania terminy nie są przeliczane**, bo zgadnięta data byłaby gorsza niż jej brak; raport i CLI
   o tym ostrzegają.
6. **Jedna rozmowa to jedno wywołanie modelu**, bo poprawki wymagają kontekstu całej rozmowy, np. sobota do 14
   (l. 104) zmieniona na 15 pod koniec rozmowy (l. 232).
7. **Transkrypcja to dane, nie polecenia** (ochrona przed prompt injection): jest wydzielona znacznikami,
   a `claude -p` działa bez narzędzi, więc nie może niczego wykonać.
8. **Druga rozmowa (`examples/druga-rozmowa.md`) jest syntetyczna**: napisał ją agent AI do testów na innej
   branży i jest oznaczona w nagłówku jako fikcyjna.
9. **Dane są fikcyjne.** Produkcyjnie transkrypcje z danymi osobowymi wymagałyby umowy powierzenia (DPA) z
   dostawcą modelu albo anonimizacji przed wysłaniem.

## Ograniczenia i co dalej

- **Niedeterminizm modelu.** Kolejne przebiegi na tej samej rozmowie dają różne listy (liczba pozycji, podział
  na pozycje, stany). Weryfikacja cytatów łapie zmyślenia, ale nie pominięcia.
- **Jakość oceniana ręcznie** względem `eval/reference.md`; brak automatycznego scoringu i większego zestawu
  rozmów.
- **Brak pamięci między rozmowami i deduplikacji.** Stały zakaz z poprzedniego spotkania nie przechodzi
  automatycznie na następne.
- **Ograniczenia są zapisane, nie egzekwowane.** „Przypomnij mi. Raz.” to `constraints` pozycji i warunek szkicu;
  nie ma harmonogramu, który pilnowałby limitu przy wysyłce.
- **Brak skrzynki „inne”.** Aktywna pozycja (`do_now`, `scheduled`) rodzaju innego niż błąd, zmiana konfiguracji
  czy prośba o funkcję, w tym `feedback` i `info`, trafia do „Zadania zespołu”.
- **Koszt i czas**: około 4–5 minut i 0,7–0,9 USD na 36-minutową rozmowę przy `--effort high`.
- **`--allow-remote` nie chroni niczym**: brak uwierzytelniania i ochrony przed DNS rebinding.
- **Pipeline częściowo zduplikowany** między CLI (`cli.py`) a aplikacją webową (`web/runs.py`).
- **Aplikacja tylko pokazuje wynik.** Nie ma w niej zatwierdzania, edycji ani odrzucania pozycji; szkice
  kopiuje się ręcznie.
- **Integracje** (CRM, kalendarz, Gmail, panel konfiguracji agenta) oraz UI zatwierdzania są
  w [`docs/process.md`](docs/process.md) jako stan docelowy. <!-- TODO lead: jira -->Jira: patrz [wyżej](#jira).

## Praca z AI

- **Claude Code (Opus 5.5)** jako prowadzący: analiza zadania, projekt, implementacja i decyzje.
- **Subagenci** do niezależnych części: analiza transkrypcji, wzorzec eval, dokumentacja, wybrane moduły
  i druga, syntetyczna rozmowa.
- **Osobne sesje recenzenta tylko do odczytu** i doradców do przeglądu kodu i decyzji projektowych.
- Eksport rozmów: [`ai-logs/`](ai-logs/).
