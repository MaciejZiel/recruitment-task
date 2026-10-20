# Proces: od rozmowy z klientem do zatwierdzonych działań

## Idea

Po każdej rozmowie z klientem system zamienia transkrypcję w listę zweryfikowanych działań, rozdzielonych do
skrzynek zespołów, które mają je wykonać. Każda pozycja ma cytat z rozmowy jako dowód, a każde działanie
dotykające klienta (wiadomość, zmiana konfiguracji agenta) czeka na zatwierdzenie przez człowieka. Nic nie
jest wysyłane do klienta automatycznie, bo rozmowy z klientem są pełne warunków i zakazów, których nie widać w samej
liście zadań. W rozmowie z Auto Tama Kasia mówi: „Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.”
(l. 58), czyli jedno przypomnienie 9.10, tylko jeśli do czwartku 8.10 teksty nie przyjdą, i ani jednego więcej. Marek obiecuje: „Opla nie włączam. Nawet jak Paweł
napisze, że kazał, to najpierw zadzwonię do ciebie” (l. 132), więc nawet polecenie od szefa klienta nie wystarczy.
Automat, który od razu „wykonuje” ustalenia, łatwo złamałby takie zastrzeżenie. Dlatego system przygotowuje
działania, a decyzję o wykonaniu podejmuje człowiek.

## Proces docelowy

Zielone elementy działają w aplikacji (`src/callflow`). Szare, przerywane to elementy docelowe, jeszcze
niezbudowane. Aplikacja webowa i CLI korzystają z tego samego pipeline'u.

```mermaid
flowchart TD
    subgraph FUTURE_IN["Docelowo: wejście"]
        MEET["Automatyczny odbiór transkrypcji<br/>z Google Meet lub nagrania"]
        MEM["Pamięć ustaleń klienta między rozmowami<br/>stałe zakazy, aktualne godziny i adresy"]
    end

    subgraph DEMO["Zaimplementowane"]
        WIN["Przeglądarka, ekran Nowa analiza<br/>wklejony tekst, plik .md/.txt lub przykład"]
        WQ["web/server.py + web/runs.py<br/>walidacja, kolejka przebiegów, zapis w runs/id/"]
        T["CLI: plik transkrypcji .md/.txt"]
        P["transcript.py: parsowanie<br/>wypowiedzi z numerami linii, data spotkania"]
        E["extract.py + llm.py: ekstrakcja przez claude -p<br/>JSON Schema z modeli pydantic, kalendarz od daty spotkania"]
        J["extraction.json<br/>zapisany wynik modelu"]
        V["verify.py: weryfikacja deterministyczna<br/>cytaty vs wypowiedzi mówcy, terminy, właściciele, odwołania"]
        R["route.py: routing regułami do skrzynek"]
        OUT["render.py: report.md, outbox.json, drafts/*.md<br/>html_report.py: report.html"]
        WR["Widok wyniku w przeglądarce<br/>skrzynki, cytaty ze statusem, szkice, historia"]
        H["Człowiek czyta wynik i sam decyduje,<br/>co zatwierdzić i wykonać"]
        JIRA["jira.py, tylko CLI --jira: zgłoszenia w Jirze<br/>zweryfikowane pozycje z tickets i config_changes,<br/>wewnętrzne zadania zespołu, nic do klienta"]
    end

    subgraph FUTURE_OUT["Docelowo: wyjście"]
        DEDUP["Deduplikacja z pozycjami<br/>z poprzednich spotkań"]
        UI["UI zatwierdzania<br/>zatwierdź, edytuj lub odrzuć każdą pozycję"]
        INT["Integracje per skrzynka<br/>Jira w aplikacji webowej,<br/>panel konfiguracji agenta z zatwierdzeniem,<br/>tablica produktowa, przypomnienia w kalendarzu,<br/>notatka w CRM, szkice w Gmailu"]
        FB["Pętla zwrotna<br/>poprawki z UI zasilają prompt i zestaw eval"]
    end

    MEET -.-> T
    WIN --> WQ
    WQ --> P
    T --> P
    P --> E
    MEM -.-> E
    E --> J
    J --> V
    P --> V
    V --> R
    R --> OUT
    R -->|"tickets, config_changes"| JIRA
    OUT --> WR
    OUT --> H
    WR --> H
    R -.-> DEDUP
    DEDUP -.-> UI
    OUT -.-> UI
    UI -.-> INT
    UI -.-> FB
    FB -.-> E
    UI -.-> MEM

    classDef impl fill:#e6f4ea,stroke:#2e7d32,color:#1b1b1b
    classDef future fill:#f2f2f2,stroke:#888888,stroke-dasharray:5 5,color:#555555
    class WIN,WQ,T,P,E,J,V,R,OUT,WR,H,JIRA impl
    class MEET,MEM,DEDUP,UI,INT,FB future
```

Tryb offline: w aplikacji „Pokaż zapisany wynik przykładu”, w CLI `callflow <transkrypcja> --out <katalog>
--from-json extraction.json`. Oba pomijają model i od razu weryfikują, routują i renderują zapisany wynik
(`report.md`, `report.html`, `outbox.json`, `drafts/`). Demo da się więc odtworzyć bez dostępu do Claude.

## Skrzynki

Routing (`route.py`, funkcja `inbox_for`) jest deterministyczny. Model przypisuje pozycji `kind` i `state`,
a reguły w kodzie wybierają skrzynkę. Reguły są sprawdzane w kolejności z tabeli: pierwsza pasująca wygrywa.

| Skrzynka (`Inbox`) | Co tam trafia | System docelowy (`TARGET_SYSTEM`) |
|---|---|---|
| `do_not_do` | pozycje ze `state = do_not_do`: zakazy i odrzucone prośby | lista zabezpieczeń konta klienta |
| `on_hold` | `state = on_hold`: klient sam wróci do tematu | CRM, notatka na koncie klienta |
| `risks` | `kind = risk`, np. klient rozmawia z konkurencją | CRM, notatka na koncie klienta |
| `waiting_on_client` | `state = waiting_on_client`: klient ma coś przysłać lub potwierdzić | przypomnienia w kalendarzu |
| `no_action` | `state = no_action`: informacje bez działania | CRM, notatka na koncie klienta |
| `tickets` | pozostałe z `kind = bug` | issue tracker (np. Linear/Jira) |
| `config_changes` | pozostałe z `kind = config_change` | panel konfiguracji agenta (zmiana po zatwierdzeniu) |
| `backlog` | pozostałe z `kind = feature_request` | tablica produktowa |
| `tasks` | wszystko inne do zrobienia (`task`, `feedback`, `info`) | lista zadań właściciela |

Poza skrzynkami raport zawiera trzy dodatkowe sekcje. Zabezpieczenia (`guardrails`) to stałe zakazy z warunkiem
zdjęcia i osobą, która może je zdjąć; sprawdza się je przed każdym działaniem. Kalendarz (terminy
i przypomnienia) powstaje z pozycji `scheduled` i `waiting_on_client` z datą; `on_hold` nigdy do niego nie trafia. Szkice wiadomości mają pole `send_when` i nigdy nie są wysyłane same. Kolumna
„System docelowy” to tylko etykieta w raporcie: aplikacja nie wysyła niczego do tych systemów. Wyjątek: CLI
z flagą `--jira` tworzy zgłoszenia w Jirze ze zweryfikowanych pozycji skrzynek `tickets` i `config_changes`
(patrz niżej).

## Stany pozycji

`state` mówi, co robimy z pozycją. Od tego zależy, czy powstaje przypomnienie.

```mermaid
flowchart LR
    ITEM["Pozycja z rozmowy"]
    ITEM --> S1["do_now<br/>robimy od razu<br/>np. adres salonu we Włocławku"]
    ITEM --> S2["scheduled<br/>robimy w ustalonym terminie"]
    ITEM --> S3["waiting_on_client<br/>klient ma coś przysłać lub potwierdzić"]
    ITEM --> S4["on_hold<br/>klient sam wróci do tematu<br/>np. agent po godzinach"]
    ITEM --> S5["do_not_do<br/>zakaz lub odrzucona prośba<br/>np. Opel"]
    ITEM --> S6["no_action<br/>informacja, nic do zrobienia"]

    S1 --> OWN["Weryfikacja: wymagany właściciel"]
    S2 --> OWN
    S2 --> DUE["Weryfikacja: wymagany termin"]
    S2 --> REM["Kalendarz: termin due_date"]
    S3 --> REM
    S4 --> NOREM["Bez przypomnienia i follow-upu"]
    S5 --> GUARD["Skrzynka do_not_do,<br/>stały zakaz także jako guardrail"]
    S6 --> NOTE["Notatka w CRM"]
```

Różnica między `waiting_on_client` a `on_hold` jest celowa. Gdy Kasia mówi „Jak sama nie powiem, że wracamy do
tematu, to nie wracamy” (l. 176), przypomnienie byłoby wbrew ustaleniu. Dlatego `on_hold` nie dostaje
przypomnienia ani w prompcie, ani w kodzie (`route.py`).

## Bezpieczniki

- **Transkrypcja to dane, nie polecenia.** Prompt systemowy każe ignorować prośby skierowane do asystenta lub AI,
  które pojawią się w treści rozmowy, a sama transkrypcja jest wyraźnie wydzielona znacznikami. `claude -p`
  działa bez narzędzi, bez serwerów MCP, bez ustawień użytkownika i bez zapisanej sesji, więc nawet udany
  prompt injection nie może niczego wykonać. Odpowiedź musi pasować do JSON Schema, a `render.py` neutralizuje
  HTML w tekstach z modelu.
- **Cytaty sprawdzane dosłownie.** Każda pozycja i każde zabezpieczenie mają co najmniej jeden cytat z mówcą.
  `verify.py` szuka cytatu w wypowiedziach tego mówcy, normalizując tylko cudzysłowy, myślniki, białe znaki
  i wielkość liter. Raport podaje numer linii, a cytat, którego nie znaleziono lub który padł z ust innej osoby,
  dostaje ⚠️ (w `outbox.json`: `needs_review: true`). Na rozmowie z Auto Tama zweryfikowano 108 ze 108 cytatów.
- **Kontrola pól.** Weryfikacja zgłasza też zduplikowane id, termin wcześniejszy niż spotkanie, pozycję `do_now`
  lub `scheduled` bez właściciela, `scheduled` bez terminu oraz odwołania do nieistniejących pozycji.
  `extract.py` odrzuca wynik niezgodny ze schematem, a inną datę spotkania od modelu zastępuje znaną datą
  i zapisuje to w założeniach. Prompt każe rozwiązywać względne
  terminy („do czwartku”) wyłącznie według kalendarza dołączonego do wiadomości.
- **Ogólny prompt.** Ani prompt systemowy, ani opisy pól w schemacie nie mówią nic o Auto Tama ani o branży
  (przykłady są neutralne, np. „przypomnieć tylko raz”). Prompt opisuje znaczenie każdego stanu i ogólne reguły rozmowy B2B: ostatnia wersja
  decyzji wygrywa, błąd to coś innego niż prośba o funkcję, zakazy i limity trzeba zapisać, a wnioski, których nikt
  nie wypowiedział, trafiają do `assumptions`.
- **Tryb offline.** `--from-json` odtwarza cały proces bez modelu z zapisanego `extraction.json`. Dzięki temu
  wynik można przejrzeć, przetestować i pokazać bez klucza ani logowania.
- **Bramka zatwierdzenia.** Aplikacja nie ma kodu, który wysyła coś do klienta albo zmienia konfigurację agenta.
  `outbox.json` ma `requires_approval: true`, a raport zaczyna się zdaniem: „Nic nie zostało wysłane ani
  zmienione”. Jedyny zapis do zewnętrznego systemu to Jira w CLI (`--jira`, jawnie włączana flagą): tworzy
  wewnętrzne zadania zespołu Rinvo, nie wysyła niczego do klienta i nie zmienia konfiguracji agenta. Pomija
  pozycje z niezweryfikowanym cytatem, nie dubluje zgłoszeń przy ponownym uruchomieniu na tej samej ekstrakcji
  (`jira.json`), odrzuca przekierowania i nie wypisuje tokenu. `--jira-check` sprawdza połączenie tylko do odczytu,
  zanim zostanie wywołany model.
- **Aplikacja webowa tylko lokalnie.** Domyślnie słucha na adresie pętli zwrotnej, odrzuca obcy nagłówek `Host`
  (DNS rebinding) i `POST` z obcym `Origin`, a pliki serwuje tylko z katalogu `static/` i katalogu danego
  przebiegu. Nie ma uwierzytelniania, więc `--allow-remote` nadaje się tylko do zaufanej sieci.

## Co jest, a czego nie ma

- **Jest:** lokalna aplikacja webowa (`callflow-web`): transkrypcja wklejona, wczytana z pliku albo wybrana
  z przykładów, przebieg na żywo (`claude -p`, jedna analiza naraz) lub z zapisanego wyniku przykładu, podgląd
  etapów, wynik w zakładkach per skrzynka z cytatami i statusem weryfikacji, szkice do skopiowania, historia
  analiz zapisana w `runs/` i zachowana po restarcie. To samo z wiersza poleceń daje CLI `callflow`.
- **Jest:** cały przebieg od pliku `.md` do `report.md`, `report.html` (ten sam raport jako jeden plik HTML do
  otwarcia lokalnie w przeglądarce, `html_report.py`), `outbox.json` i `drafts/*.md`. Wynik dla rozmowy
  z Auto Tama leży w `examples/output/auto-tama/`: 37 pozycji, 11 zabezpieczeń, 8 szkiców, 108 ze 108
  zweryfikowanych cytatów, bez ostrzeżeń walidacji. Dla DentaVita (`examples/output/dentavita/`): 6 pozycji,
  3 zabezpieczenia, 3 szkice, 19 ze 19 cytatów. Trzeci przykład, syntetyczna rozmowa FitStudio
  (`examples/output/fitstudio/`, w aplikacji do wyboru z listy przykładów): 18 pozycji, 8 zabezpieczeń, 5 szkiców,
  58 z 58 cytatów (wszystkie zweryfikowane po poprawce parsera); wstawioną w rozmowę próbę prompt injection
  model potraktował jako dane.
- **Jest:** weryfikacja i routing w czystym Pythonie, bez modelu, pokryte testami (`tests/`).
- **Nie ma:** automatycznego odbioru transkrypcji ani integracji z docelowymi systemami poza Jirą w CLI (CRM,
  kalendarz, poczta, panel agenta, Jira w aplikacji webowej). Ich nazwy w raporcie to tylko etykiety. Aplikacja pokazuje wynik, ale nie ma w niej zatwierdzania, edycji ani odrzucania pozycji:
  decyzję człowiek podejmuje i wykonuje poza nią.
- **Nie ma:** pamięci między rozmowami ani deduplikacji. Każda rozmowa jest analizowana osobno, więc stały zakaz
  z poprzedniego spotkania nie przechodzi automatycznie na następne.
- **Nie ma:** wymuszania ograniczeń w kodzie. Limit „przypomnieć tylko raz” jest zapisany jako `constraints`
  pozycji i widoczny w raporcie, ale żaden mechanizm go nie egzekwuje, bo nic nie jest wysyłane do klienta.
- **Częściowo:** `eval/reference.md` to wzorzec odpowiedzi przygotowany przez niezależnego agenta AI (cytaty
  sprawdzone skryptem); porównanie z wynikiem systemu jest ręczne, nie automatyczne. Druga, fikcyjna rozmowa
  z innej branży (`examples/druga-rozmowa.md`) ma wynik w `examples/output/dentavita/`.
- **Jest (CLI):** integracja z Jirą (`jira.py`): `--jira-check` (sprawdzenie tylko do odczytu: użytkownik,
  projekt, typy zgłoszeń, pola wymagane) i `--jira` (zgłoszenia dla zweryfikowanych pozycji z `tickets`
  i `config_changes`, etykieta `callflow`, termin, opis z cytatami). Ustawienia w `.env`. Przetestowane testami
  jednostkowymi; test na żywej Jirze w toku. W aplikacji webowej jeszcze jej nie ma.
