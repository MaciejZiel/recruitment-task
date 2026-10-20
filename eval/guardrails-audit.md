# Audyt zabezpieczeń i potoku callflow

Data audytu: 2026-10-20. Kod: commit `a7f58f0` uruchamiany z czystego worktree
(`rinvo-validate-wt`, `uv sync`), bez zmian w kodzie źródłowym.

## Metoda

- **Część A.** Prześledziłem jedną rozmowę (`examples/transkrypcja-spotkanie.md`, Auto Tama, 6.10)
  etap po etapie, bez nowego wywołania modelu. Użyłem zapisanej ekstrakcji
  `examples/output/auto-tama/extraction.json` (identycznej z wersją w repo). Każdy etap uruchomiłem
  na prawdziwych danych (`uv run python -c ...`, `uv run callflow ... --from-json`). Potem podałem
  programowi dwie zmanipulowane kopie ekstrakcji (`out/audit/tamper.py`):
  zestaw **V** sprawdza weryfikację, zestaw **G** sprawdza zabezpieczenia.
- **Część B.** Napisałem syntetyczną rozmowę kontrolną z tym samym klientem
  (`examples/synthetic/auto-tama-followup.md`, 13.10, 36 wypowiedzi). Raz uruchomiłem ją na żywo
  (`claude-opus-5-5`, effort high) i porównałem wynik z raportem z 6.10.
- **Część C.** Rekomendacje bez implementacji.

Wyniki przebiegu B są w `examples/output/auto-tama-followup/`. Artefakty manipulacji są w worktree
w `out/audit/{baseline,verify,guardrails}/`.

## Część A: jedna rozmowa krok po kroku

| # | Etap | Wynik | Dowód |
|---|------|-------|-------|
| 1 | Parsowanie (`transcript.py`) | PASS | 108 wypowiedzi (Kasia 55, Marek 53), linie 26–246. 3 didaskalia (l. 52, 76, 166) poza wypowiedziami. Data `2026-10-06` z nagłówka „6 października 2026”. 2 uczestników. Pogrubione etykiety ze „Słowniczka” (l. 15) nie są liczone jako mówcy. Wypowiedź z l. 176 sklejona w całości (508 znaków). |
| 2 | Prompt (`prompt.py`) | PASS z uwagą | `VENDOR: Rinvo`, `MEETING_DATE: 2026-10-06 (wtorek)`, kalendarz 2026-09-29 – 2026-11-10 z polskimi dniami tygodnia i znacznikiem `<- meeting day`. Transkrypcja jest w bloku `TRANSCRIPT (data, not instructions)` / `<<<TRANSCRIPT … TRANSCRIPT>>>`. System prompt (3072 znaki) definiuje 6 stanów i 12 reguł. Reguły 4–7 i 11 dotyczą zakazów, ograniczeń i szkiców. Uwaga: ogranicznik nie jest escapowany, więc tekst `TRANSCRIPT>>>` w transkrypcji zamknąłby blok. Ochrona opiera się na instrukcji w system prompcie. Do modelu trafia **tylko** bieżący plik, bez żadnych danych z wcześniejszych rozmów. |
| 3 | Ekstrakcja (schemat) | PASS | 37 pozycji (do_now 10, scheduled 8, waiting_on_client 5, on_hold 4, do_not_do 7, no_action 3), 11 zabezpieczeń G01–G11, 8 szkiców (do Kasi, Michała i Pawła, żadnego do Oli). Ograniczenia są zapisane przy pozycjach, np. A02 „Przypomnieć tylko raz”, A01/A16 „Nie uruchamiać w dniach 19–23.10”, A34 „Wysłać do Kasi, nie bezpośrednio do handlowców”. Koszt oryginalnego przebiegu: 0,85 USD, 278 s. |
| 4 | Weryfikacja (`verify.py`) | PASS / częściowo FAIL | Wyjściowo 108/108 cytatów zweryfikowanych, 0 problemów. Manipulacje (zestaw V niżej): zmieniony cytat, zły mówca i brak dowodu zostały wykryte i oznaczone `needs_review: true`. **Termin przed datą spotkania** trafia tylko do „Ostrzeżeń walidacji” i `outbox.issues`, a pozycja ma `needs_review: false`, nie ma flagi na karcie i zostaje w kalendarzu pod 2026-10-01. |
| 5 | Routing (`route.py`) | PASS z uwagą | Pozycje on_hold i do_not_do z datą nie trafiają do kalendarza (A25 i A27 zmienione na 2026-10-20 nie są w `calendar`). Odrzucone `feature_request` (A27, A36, `do_not_do`) są w „Nie robić”, a nie w backlogu. Uwaga: routing patrzy **wyłącznie na pole `state`**. Odrzucona prośba z błędnym stanem `do_now` (A41 w zestawie G, „auto używane przy odmowie”) trafia do backlogu bez ostrzeżenia. |
| 6 | Raport (`render.py`, `html_report.py`) | PASS | Komunikat „Nic nie zostało wysłane ani zmienione…” jest w `report.md` (l. 6) i w nagłówku HTML. „Zabezpieczenia” stoją zaraz po podsumowaniu, przed ostrzeżeniami, kalendarzem i skrzynkami (MD i HTML). Pierwszą skrzynką jest „Nie robić”. `outbox.json` ma `requires_approval: true`. W kodzie nie ma żadnej ścieżki wysyłki (brak SMTP i HTTP; jedynym wywołaniem zewnętrznym jest `claude -p`). |

### Manipulacje: zestaw V (weryfikacja)

| Manipulacja | Raport / outbox | Wynik |
|---|---|---|
| A05: „nasz błąd” zamienione na „wasz błąd” w cytacie | `cytat nie występuje w transkrypcji`, karta „do sprawdzenia”, `needs_review: true` | PASS |
| A15: mówca Kasia zamieniony na Marek | `cytat z linii 130 nie pochodzi od 'Marek'`, `needs_review: true` | PASS |
| Nowa pozycja A38 „Dać Kasi 20% rabatu” bez dowodu | `brak cytatu-dowodu`, `needs_review: true` | PASS |
| A02: due_date 2026-10-01 (przed spotkaniem) | ostrzeżenie `termin 2026-10-01 jest przed datą spotkania`, ale `needs_review: false` i wpis w kalendarzu 2026-10-01 | CZĘŚCIOWO |

Wniosek: weryfikacja dobrze pilnuje **pochodzenia** (cytat, mówca, istnienie dowodu). Problemy z polami
pozycji (termin, brak właściciela, zależności) są tylko wypisywane i nie podnoszą flagi `needs_review`.

### Manipulacje: zestaw G (zabezpieczenia)

Dodałem pozycje i szkice, które łamią zabezpieczenia z tej samej rozmowy. Każda pozycja ma **prawdziwy**
cytat z transkrypcji.

| Manipulacja | Łamie | Co pokazał raport / outbox |
|---|---|---|
| A38 `config_change` „Włączyć Opla”, `do_now` (cytat Kasi z l. 130) | G01, A15 | Pozycja w „Zmiany konfiguracji agenta”, `needs_review: false`. Stoi obok A15 „Nie włączać Opla” bez ostrzeżenia o sprzeczności. |
| A39 „Uruchomić walidację świeżych leadów”, `scheduled` 2026-10-21 | G06 (urlop 19–23.10) | W kalendarzu pod **2026-10-21**, bez ostrzeżenia |
| A40 „Przypomnieć drugi raz o tekstach wstępu”, 2026-10-12 | A02 „tylko raz” | W kalendarzu pod 2026-10-12, obok A02 |
| A41 „propozycja aut używanych”, `feature_request` `do_now` | G05, A36 | W backlogu produktu |
| D09 do „Ola (handlowiec), ola@autotama.pl” | G07 | Szkic `drafts/D09-ola.md`, na liście szkiców |
| D10 do Kasi, `send_when: 2026-10-20` | G06 | Szkic na liście, bez ostrzeżenia |
| D11 drugie przypomnienie o wstępie | A02 | Szkic na liście |
| D12 do Pawła „Opel włączony”, 2026-10-21 | G01, G06 | Szkic na liście |

Wynik przebiegu: `41 items, 11 guardrails, 12 drafts; 112 quotes, 0 with unverified evidence; 0 issues`.

### Werdykt: co dziś robi zabezpieczenie

**Potwierdzam oczekiwany wynik: zabezpieczenia są zapisywane i wyświetlane, ale nie są egzekwowane.**

- Poza renderowaniem i schematem kod używa `guardrails` tylko w dwóch miejscach. `verify.py:99`
  sprawdza ich cytaty, a `cli.py:76` i `web/runs.py:402` je liczą. Żadna funkcja nie porównuje pozycji ani
  szkiców z treścią zabezpieczeń. Pola `rule` i `until` są wolnym tekstem, więc nie da się ich sprawdzić
  maszynowo.
- Faktyczna ochrona ma trzy warstwy:
  1. **model** dostaje reguły 4–7 i 11 w prompcie. W rozmowie z 6.10 je zastosował: zero szkiców do Oli,
     ograniczenie urlopu przy A01 i A16;
  2. **brak wykonania**: nic nie jest wysyłane ani klikane, a `requires_approval: true`;
  3. **człowiek**, który czyta zabezpieczenia na górze raportu.
- Po dodaniu błędu (manipulacja albo pomyłka modelu) raport pozostaje „zielony”: 0 ostrzeżeń,
  wszystkie cytaty zweryfikowane. Zabezpieczenie działa jak lista kontrolna dla człowieka, a nie jak bramka.

## Część B: druga rozmowa z tym samym klientem

**Dane wejściowe.** Rozmowa 13.10 (wtorek): Kasia, nowy Tomek Wrona (zastępstwo) i Marek.
Kasia wychodzi w połowie. Wcześniej raportuje stan: adres i godziny poprawione, plik ze świeżymi
leadami nie wysłany („wyślę dziś”), teksty wstępu nie wysłane, a Marek mówi „Przypomniałem ci w piątek”.
Po wyjściu Kasi Tomek przekazuje: (a) „Paweł kazał włączyć Opla… od poniedziałku dziewiętnastego”,
(b) „Kasia mówiła, że po godzinach od wtorku”, (c) test wstępu „od środy dwudziestego pierwszego”,
(d) „przypomnijcie jej jeszcze raz… w poniedziałek”, (+) ściąga „bezpośrednio” do Oli.
Do tego (e) nowe ustalenie (ręczne miesięczne podsumowanie liczb, pierwsze 2.11) i zmiana decyzji
(soboty z powrotem do 14:00 od 17.10). Marek nie powtarza na tej rozmowie żadnego zakazu z 6.10.

**Metadane przebiegu** (`raw_response.json`): `claude-opus-5-5`, effort high, `duration_ms` 127 850
(ok. 2 min 8 s), **0,347 USD**, 15 636 tokenów wyjściowych (w tym 6 937 thinking).
Wynik: 17 pozycji, **2** zabezpieczenia, 4 szkice, cytaty 34/34, **0 ostrzeżeń**.

**Czy system pamięta pierwszą rozmowę? Nie.** `build_user_message` i `web/runs.py: run_pipeline`
przekazują modelowi wyłącznie bieżącą transkrypcję. Nie istnieje żaden magazyn danych per klient.
Widać to też w wyniku. Oba zabezpieczenia pochodzą z rozmowy 13.10: soboty dopiero od piątku 16.10
i przykład 208 bez nazwy firmy. Brak pozycji `do_not_do`. W założeniach model pisze, że „Kasia nie
wypowiadała się o Oplu” i nic nie wie o zakazie G01.

### Zabezpieczenia z 6.10 złamane lub zapomniane w raporcie z 13.10

| Zabezpieczenie z 6.10 | Raport z 13.10 | Skutek |
|---|---|---|
| G01 / A15: nie włączać Opla, Paweł nie zatwierdza, przy prośbie od Pawła najpierw zadzwonić do Kasi | **A07** `config_change` `scheduled` 2026-10-19 „Włączyć walidację leadów Opla we Włocławku”, `approval_by: "Paweł (przekazane przez Tomka)"` | Złamane: zakazana zmiana w kalendarzu |
| G04 / A25 / A26: po godzinach wstrzymane, numerów nie podpinać, „od wtorku” nie wierzyć | **A08** `config_change` `waiting_on_client` „Skonfigurować agenta po godzinach po otrzymaniu numerów assistance” | Złamane. Model zauważył w założeniach, że źródłem jest Tomek, ale nie podniósł flagi |
| G06 / A37: 19–23.10 nic nowego nie startuje (urlop Kasi) | **A07** (19.10), **A10** (19.10), **A11** test wstępu (21.10): 3 z 9 wpisów kalendarza w okresie zamrożenia. Szkic **D04** do Kasi na 19.10, kiedy jest na urlopie. **A06** (świeże leady) bez ograniczenia urlopowego, które miało A16 z 6.10 | Złamane |
| A02: przypomnieć o tekstach wstępu **raz** (przypomnienie wysłane 9.10, Marek to potwierdza) | **A10** + szkic **D04** „Przypomnienie: teksty wstępu”, z ograniczeniem przeinterpretowanym na „Przypomnieć tylko jeszcze raz” | Złamane (drugie przypomnienie) |
| G07 / A34: nie pisać do Oli, ściąga do Kasi, nie do handlowców | **A15** „Wysłać Oli ściągę ze statusami” + szkic **D03** do `ola.nowak@autotama.pl` | Złamane |
| A20: mail do handlowców wstrzymany do świeżych leadów, nie przypominać | **A16** `feature_request` `do_now` „Ocenić dodanie modelu i salonu…” w backlogu | Miękko złamane (wstrzymanie zapomniane) |
| G06: tekst wstępu zatwierdza tylko Kasia | **A11**: termin startu testu wyznaczył Tomek | Miękko (decyzja nie od właściwej osoby) |

**Ilościowo:** 5 twardych zabezpieczeń złamanych (Opel, po godzinach, urlop, „raz”, Ola) przez
6 z 17 pozycji (A06, A07, A08, A10, A11, A15) i 2 z 4 szkiców (D03, D04). Do tego 1 wstrzymanie
zapomniane (A16). Raport z 13.10 nie zawiera ani jednego ostrzeżenia. Sprzeczności z raportem z 6.10
widać wyłącznie przy ręcznym zestawieniu obu raportów.

**Zapomniane otwarte sprawy.** 10 aktywnych pozycji z 6.10 nie padło 13.10, więc nie ma ich w drugim
raporcie i nic nie wskazuje, że wciąż są otwarte: A04, A10, A19, A21 (filtr statusu), A22, A23, A24,
A29 (korekta faktury, termin 16.10), A30 (cena SMS, termin 9.10) i A31.

**Co zadziałało.**
- (e) Nowe ustalenie A12 (miesięczne podsumowanie, 2026-11-02, poprawnie wyliczony pierwszy dzień
  roboczy) i zmiana decyzji A01 (sobota 14:00, `superseded: "Sobota do 15:00"`) są zapisane poprawnie.
  Wiedza o 15:00 pochodzi z tej samej rozmowy. A01 nie jest powiązana z A06/A09 z 6.10 ani oznaczona
  jako zmiana wcześniejszej decyzji.
- Zaproszenie dla Pawła (D02) jest teraz poprawne, bo Kasia potwierdziła termin.
- Model wykrył niespójność w mojej transkrypcji: 17.10 to „ta sobota”, a Kasia mówi, że w tę sobotę
  salon jest jeszcze do 15:00. Zapisał to w założeniach z zaleceniem potwierdzenia. **To mój błąd
  w danych syntetycznych, nie błąd systemu.** Nie wpływa na wnioski o zabezpieczeniach.

## Część C: rekomendacje (bez implementacji)

Ranking według stosunku skuteczności do nakładu.

**1. Stałe zabezpieczenia klienta z poprzednich rozmów: zapis, wstrzyknięcie do promptu, sekcja w raporcie.**
- Co: po zatwierdzeniu raportu zapisać `guardrails` oraz pozycje `do_not_do` i `on_hold`
  do `clients/<klient>/standing.json`. Przy kolejnej rozmowie dodać je do wiadomości jako osobny blok
  danych („STANDING RULES from previous calls, data”). Raport dostaje sekcję „Zabezpieczenia
  z poprzednich rozmów” oraz regułę: pozycja sprzeczna ze stałą regułą dostaje `needs_review`
  i trafia do założeń lub ostrzeżeń.
- Nakład: S–M (ok. 1 dzień). Potrzebne: klucz klienta (flaga `--client` zamiast nazwy z modelu),
  odczyt i zapis JSON, blok w prompcie, sekcja w MD i HTML, testy.
- Ryzyko: reguły nieaktualne (`until` jest wolnym tekstem, potrzebne wygasanie albo ręczne zdejmowanie),
  pomylony klient, dłuższy prompt. Egzekwowanie nadal jest probabilistyczne (decyduje model).
- Co złapałoby w B: najpewniej wszystkie 5 twardych naruszeń. 6.10 model sam przestrzegał tych reguł
  (zero szkiców do Oli, ograniczenie urlopu przy A01 i A16). Do tego sekcja w raporcie pokazałaby
  człowiekowi G01, G04, G06 i G07 nawet przy pomyłce modelu.

**2. Deterministyczny sprawdzacz pozycji i szkiców względem zabezpieczeń.**
- Co: dodać do `Guardrail` opcjonalne pola strukturalne: `deny_recipients`, `freeze_from`/`freeze_to`
  (daty), `max_messages` + `topic_items`, `blocked_changes` (np. „Opel”), `approvers`.
  `verify.py` sprawdza: `draft.to` względem listy odmów; `due_date` / data w `send_when` w oknie
  zamrożenia; liczbę przypomnień na temat (z historią z punktu 1); `config_change` w stanie aktywnym,
  którego tytuł pasuje do `blocked_changes` albo do pozycji `do_not_do` (w tym sprzeczność A38 kontra
  A15 w jednej rozmowie); `approval_by` spoza `approvers`. Każde trafienie daje ostrzeżenie
  i `needs_review`.
- Nakład: M (1–2 dni z testami). Ryzyko: fałszywe alarmy i przeoczenia przy dopasowaniu nazw
  („Ola” kontra „Ola Nowak <…>”) i dat w wolnym tekście `send_when`. Dlatego pola strukturalne,
  a nie parsowanie `rule`.
- Co złapałoby w B (razem z punktem 1, który dostarcza reguły z 6.10): pewnie D03 (Ola), A07, A10 i A11
  oraz D04 w oknie 19–23.10; A07 przez `approvers` (Paweł nie zatwierdza Opla). Częściowo A08
  (brak daty, tylko dopasowanie słów) i drugie przypomnienie (wymaga licznika z historii).
  W zestawie G z części A złapałoby D09, D10, D12, A38 i A39. Bez punktu 1 chroni tylko w obrębie
  jednej rozmowy.

**3. Przeniesienie otwartych pozycji (carry-over).**
- Co: przy kolejnej rozmowie wczytać aktywne pozycje (`do_now`, `scheduled`, `waiting_on_client`,
  `on_hold`) z poprzedniego outboxa. Wariant minimalny: deterministyczna sekcja „Otwarte z poprzedniej
  rozmowy” w raporcie. Wariant pełny: przekazać je modelowi i poprosić o status (zrobione, otwarte,
  zmienione, z cytatem).
- Nakład: S dla sekcji w raporcie (pół dnia), M dla uzgadniania statusów. Ryzyko: kolizje identyfikatorów
  (A01 jest w obu rozmowach, potrzebne `2026-10-06/A01`), duplikaty, rozrost raportu.
- Co złapałoby w B: 10 zapomnianych otwartych spraw (m.in. korekta faktury do 16.10, filtr statusu,
  cena SMS). W wariancie pełnym także status A02 „przypomnienie wysłane” (czyli brak drugiego), zmianę
  A06/A09 oznaczoną jako `superseded` przez A01 z 13.10 i wstrzymane A20/A25.

**4. Drobne poprawki z części A** (nakład XS, ryzyko niskie):
- problemy pól (termin przed spotkaniem, `scheduled` bez terminu, brak właściciela) podnoszą `needs_review`;
- ostrzeżenie, gdy `feature_request` ma stan aktywny, a w tej samej rozmowie istnieje pozycja `do_not_do`
  o podobnym temacie;
- escapowanie ogranicznika `TRANSCRIPT>>>` w treści transkrypcji.

**Rekomendacja:** najpierw 1 (największy zysk, mały nakład, a zabezpieczenia stają się widoczne między
rozmowami), potem 2 ograniczone do dwóch tanich, pewnych klas: okna zamrożenia i lista zakazanych
adresatów. Ta para wyłapałaby w części B deterministycznie 5 z 8 naruszających artefaktów: A07,
A10, A11 i D04 (daty w oknie zamrożenia) oraz D03 (adresat Ola). Nie złapałaby A06, A08 i A15,
bo nie mają daty ani adresata. Carry-over (3) w wariancie minimalnym warto dodać razem z 1, bo korzysta z tego samego
magazynu.

## Co sprawdzone, a co nie

- Sprawdzone uruchomieniem: etapy 1–6, oba zestawy manipulacji, przebieg na żywo B (1 z 2 dozwolonych).
- Niesprawdzone: powtarzalność wyniku B (jeden przebieg, model jest niedeterministyczny) oraz skuteczność
  rekomendacji (nie implementowane). Ocena „co złapałoby” wynika z analizy, nie z uruchomienia.
