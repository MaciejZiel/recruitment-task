# Ewaluacja: wynik systemu vs niezależne referencje

## 1. Co i jak porównano

- **Wejście A:** `examples/transkrypcja-spotkanie.md` (Grupa Auto Tama, 2026-10-06, wtorek) → `examples/output/auto-tama/` (`extraction.json`, `report.md`, `outbox.json`, `drafts/`).
- **Wejście B:** `examples/druga-rozmowa.md` (DentaVita, 2026-10-13, wtorek) → `examples/output/dentavita/`.
- **Referencja 1:** `eval/reference.md`: 41 oczekiwanych pozycji R01–R41, 33 pułapki, dla drugiej rozmowy pozycje S01–S07 i 3 pułapki.
- **Referencja 2:** 13-punktowa checklista niezależnego recenzenta (must-have dla Auto Tama).
- **Metoda:** dopasowanie po znaczeniu i cytatach dowodowych, nie po nazwach typów. Referencja używa starszej taksonomii jednoosiowej, system używa `kind × state`. Mapowanie: parked→`on_hold`, client_dependency→`waiting_on_client`, commitment→`task` (`do_now`/`scheduled`), decision→`info/no_action` albo zabezpieczenie (G), billing→`task`. Pozycję uznaję za FOUND, gdy wszystkie kluczowe fakty i ograniczenia są w wyniku, także wtedy, gdy system scalił ją z inną pozycją albo zabezpieczeniem. Daty oceniam osobno (sekcja 4.2), żeby nie liczyć tego samego błędu dwa razy.
- **Cytaty:** niezależnie od nagłówka raportu sprawdziłem skryptem (tylko odczyt), że każdy cytat jest podciągiem transkrypcji i że mówca się zgadza.
- **Zastrzeżenia:**
  - Referencję przygotował niezależny agent AI, checklistę dał recenzent, a ocenę wystawił ewaluator AI. To nie jest ocena człowieka-eksperta. Referencja też może się mylić (patrz R02/R17 w 4.2).
  - Wynik LLM różni się między uruchomieniami. Ten dokument ocenia **jedno konkretne uruchomienie**:

| Rozmowa | Model | Czas | Koszt |
|---|---|---|---|
| Auto Tama | `claude-opus-5-5` | 278 s (278 257 ms) | 0,85 USD |
| DentaVita | `claude-opus-5-5` | 56 s (56 417 ms) | 0,20 USD |

## 2. Wynik w liczbach

| Miara | Wynik |
|---|---|
| Pokrycie R01–R41 (Auto Tama) | **FOUND 40 · PARTIAL 1 · MISSING 0**. 4 z FOUND są scalone z innymi pozycjami: R07, R11, R13, R21 |
| Pokrycie S01–S07 (DentaVita) | **FOUND 7 · PARTIAL 0 · MISSING 0**. S02 jest scalone z A01 i szkicem D02 |
| Pułapki Auto Tama | **32/33 PASS**, 1 PARTIAL (nr 13), 0 FAIL |
| Pułapki DentaVita | **3/3 PASS** |
| Checklista recenzenta (13 pkt) | **12 PASS · 1 PARTIAL (pkt 7) · 0 FAIL** |
| Cytaty (nagłówek raportu) | 108/108 (Auto Tama), 19/19 (DentaVita). Niezależnie potwierdzone: 0 cytatów spoza transkrypcji, 0 złych mówców |
| Pozycje systemu bez odpowiednika (EXTRA) | **0**. Wszystkie A01–A37 i G01–G11 mają odpowiednik w referencji. Są 3 drobne nadinterpretacje w sformułowaniach (4.3) |
| Daty (Auto Tama) | 11 dat `due_date`, dni tygodnia wszystkie poprawne. 1 błąd znaczeniowy (A01), 2 brakujące daty (A07, A21), okno urlopu bez struktury (A37/G06) |
| Szkice | Auto Tama: 8, żaden nie łamie ograniczeń. DentaVita: 3, jeden ma błąd daty względnej („wczorajszym”) |

Ocena pozycji (skrót):

| Ref | System | Ocena | Uwaga |
|---|---|---|---|
| R01 | A01, G02 | FOUND | Wszystkie ograniczenia są (2 wersje, Kasia pisze, AI+nagrywanie, 2 dni/2 miasta). Data: patrz 4.2 |
| R02 | A02, D02 | FOUND | „Raz”. Termin 10-09 zamiast 10-08 (do obrony) |
| R03 | A03 | FOUND | `bug/no_action`, „nie szukać”. Referencja: parked |
| R04 | A04 | FOUND | Miernik: więcej pełnych rozmów |
| R05 | A05 | FOUND | Toruńska 120 |
| R06 | A06 | FOUND | Sobota 9–15, oba salony |
| R07 | A05 (ograniczenie), D01 | FOUND (scalone) | Bez nagrania testowego, tylko wiadomość |
| R08 | A07 | FOUND | 16:40, końcówka 14, 6 przypadków, bez ruszania limitu |
| R09 | A08, G10 | FOUND | |
| R10 | A09 | FOUND | Pn–pt 9–19, sob. 9–15, „zastępuje” zawiera 14:00 |
| R11 | A12 | FOUND (scalone) | Lead, nie odmowa. Siedzi jednak w pozycji `info` razem z wynikami |
| R12 | A13, G09 | FOUND | Bez nazwy firmy i nazwiska |
| R13 | A13 (zatwierdza Paweł), A33 (plan spotkania), G09 | FOUND (scalone) | Brak osobnej pozycji `waiting_on_client` |
| R14 | A14 | FOUND | |
| R15 | A15, G01 | FOUND | |
| R16 | A16 | FOUND | Poniedziałek, bez wzoru, numer + miasto |
| R17 | A17, D03 | FOUND | Jeden mail. Termin 10-13 zamiast 10-12 |
| R18 | A18, G03 | FOUND | |
| R19 | A19, G08 | FOUND | |
| R20 | A20 | FOUND | |
| R21 | G07 (i ograniczenia A19/A20) | FOUND (scalone) | |
| R22 | A21 | FOUND | Data: patrz 4.2 |
| R23 | A22 | FOUND | Osobno od błędu filtra |
| R24 | A23 | FOUND | Warunkowo, `depends_on` A21. Stan `do_now` nie pasuje do warunku |
| R25 | A24 | FOUND | |
| R26 | A25, G04 | FOUND | Pełny zakres przyszłego projektu |
| R27 | A26, G04 | FOUND | |
| R28 | A27 | FOUND | |
| R29 | A28, D07 | FOUND | |
| R30 | A29 | FOUND | Właściciel: Michał |
| R31 | A10 | FOUND | |
| R32 | A11 | FOUND | Warunek: błąd po stronie Rinvo. Zależy od A07 i A10 |
| R33 | A30, D05 | FOUND | Tylko cena |
| R34 | A31 | FOUND | Zatwierdza Paweł |
| R35 | A32 | FOUND | ~30%, integracja z CRM, bez obietnicy w tym kwartale |
| R36 | A12 (tylko w opisie) | **PARTIAL** | „Paweł chciał wszystko wyłączyć” nie jest oznaczone jako ryzyko |
| R37 | A33, G11, D08 | FOUND | |
| R38 | A34, D06 | FOUND | |
| R39 | A35 | FOUND | |
| R40 | A36, G05 | FOUND | |
| R41 | A37, G06 | FOUND | Okno dat bez struktury (4.2) |

## 3. Pułapki (Auto Tama, 33)

| # | Pułapka | Wynik | Gdzie | Uwaga |
|---|---|---|---|---|
| 1 | Sobota dzwonienie 14→15 | PASS | A09 | Wartość ostateczna 9–15, 14:00 jako zastąpiona |
| 2 | Godziny salonu sob. 15 dla obu salonów | PASS | A06, D01 | |
| 3 | Tydzień 9–19, niedziela bez zmian | PASS | A09 | |
| 4 | Opel nawet jeśli Paweł napisze | PASS | A15, G01 | |
| 5 | Po godzinach ≠ zielone światło, „od wtorku” | PASS | A25, A26, G04 | |
| 6 | Zamrożenie 19–23.10, Paweł tylko gdy się pali | PASS | A37, G06, ograniczenia A01/A16 | Okno bez daty startu (4.2) |
| 7 | Paweł nie zatwierdza Opla ani wstępu | PASS | G01, G06, A01 | |
| 8 | Klientka na urlopie = lead | PASS | A12 | |
| 9 | Filtr (bug) ≠ kafelek (funkcja) | PASS | A21 / A22 | |
| 10 | Kolumna „nazwisko” tylko przy okazji | PASS | A23 | Stan `do_now` mimo warunku |
| 11 | Limit 5 prób zostaje | PASS | A08, G10, D04 | |
| 12 | Miernik A/B = pełne rozmowy | PASS | A04 | |
| 13 | Wstęp: 2 wersje, Kasia, nie w tym tygodniu, przypomnienie raz | **PARTIAL** | A01, A02, G02 | Treść poprawna, ale kalendarz ma „Uruchomić test wstępu” na 2026-10-08, czyli w tym tygodniu |
| 14 | Krótszy wstęp ujawnia AI i nagrywanie | PASS | A01, D02 | |
| 15 | Success story bez nazwy firmy i nazwiska | PASS | A13, G09, D08 | |
| 16 | VoiceDesk jako ryzyko | PASS | A32 | |
| 17 | Rozliczanie 3 s + odliczenie podwójnych (warunkowo) + liczba | PASS | A10, A11, D04 | |
| 18 | Korektę wystawia Michał, Marek przekazuje dziś | PASS | A28, A29, D07 | |
| 19 | Spotkanie 15.10 10:00, zaproszenie po potwierdzeniu | PASS | A33, G11, D08 | |
| 20 | Plik: poniedziałek, jeden mail, bez wzoru | PASS | A16, A17, D03 | |
| 21 | Starej bazy nie puszczać drugi raz | PASS | A18, G03 | |
| 22 | Przegląd Oli: nie zgadywać kampanii, czekać na Kasię | PASS | A19, G08 | |
| 23 | Nie pisać do Oli | PASS | G07 | Żaden szkic nie idzie do Oli |
| 24 | Bez nagrania testowego po poprawce | PASS | A05, D01 | |
| 25 | SMS: tylko cena, funkcja czeka na Pawła | PASS | A30, A31, D05 | |
| 26 | Mail do handlowców odłożony | PASS | A20 | |
| 27 | Przesunięcie prób odłożone | PASS | A14 | |
| 28 | Szkolenie po świeżych leadach, ściąga od razu | PASS | A34, A35, D06 | |
| 29 | Agent nie sprzedaje, bez aut używanych | PASS | A36, G05 | |
| 30 | „Drugi raz o model”: zaparkować, nie naprawiać | PASS | A03 | `no_action`, nie `on_hold`: brak wyzwalacza, gdyby nagranie się znalazło |
| 31 | Serwis w ciągu dnia: nie ruszać | PASS | A27 | |
| 32 | Paweł ≠ Kasia jako źródło decyzji | PASS | A01, A15, A25, A31, G09 | Koszty (SMS) i nazwa: Paweł. Opel, wstęp, po godzinach: Kasia |
| 33 | 8 rzeczy, których Marek wprost NIE zrobi | PASS | A01, G03, A26, A19, A15, A36, A07/A08, A16/A17 | Wszystkie 8 obecne |

Checklista recenzenta: 1 PASS (A07, A21 + A22 osobno; adres system też uznał za bug, co zgadza się z „to jest nasz błąd”) · 2 PASS (A05, A06, A09, A08) · 3 PASS (A23, zastrzeżenie o stanie) · 4 PASS (A28/A29, A11 zależy od A07) · 5 PASS (A30, A34, A33) · 6 PASS (A02/D02, A17/D03) · **7 PARTIAL**: 7 z 8 zakazów jest wśród zabezpieczeń G. „Nie wysyłać wzoru pliku” jest tylko ograniczeniem w A16/A17 i w `send_when` D03, nie ma go w G · 8 PASS (A36, A08) · 9 PASS (A32) · 10 PASS (A13, G09) · 11 PASS (A12) · 12 PASS (sekcja 5) · 13 PASS (108/108, potwierdzone niezależnie).

## 4. Braki i błędy (bez wprowadzonych poprawek)

### 4.1 Treść

1. **R36: ryzyko odejścia klienta nie jest ryzykiem.** „Paweł chciał wszystko wyłączyć” trafiło tylko do opisu A12 (`info`). Jedynym `risk` jest VoiceDesk (A32), a to razem z kontekstem 9/70 daje pełny obraz zagrożenia.
   *Poprawka:* reguła w prompcie: groźba wyłączenia lub rezygnacji przez decydenta to zawsze osobna pozycja `risk`.
2. **Checklista pkt 7: zakaz „wzoru pliku” poza listą G.** Jest tylko w ograniczeniach A16/A17.
   *Poprawka:* reguła w prompcie: każde „nie rób X” wypowiedziane wprost przez klienta, które dotyczy wiadomości wychodzących, trafia do `guardrails`. Ewentualnie test kodu: każde ograniczenie zaczynające się od „Nie wysyłać” ma odpowiednik w G.
3. **A12 łączy trzy rzeczy:** wyniki starej bazy, lead z urlopu i reakcję Pawła. Wszystko jest poprawne, ale trudno z tego zrobić osobne działania.
   *Poprawka:* reguła „jedna pozycja = jeden fakt do działania”.
4. **A23 ma stan `do_now` mimo warunku**, a A03 ma `no_action` zamiast `on_hold`. To niespójność klasyfikacji, która nie zmienia treści.
   *Poprawka:* test kodu: pozycja z niepustym `condition` nie może mieć stanu `do_now`.

### 4.2 Daty (dzień spotkania 2026-10-06, wtorek)

Dni tygodnia są wszędzie poprawne: 10-08 czwartek, 10-09 piątek, 10-12 poniedziałek, 10-13 wtorek, 10-15 czwartek, 10-16 piątek. Poprawne są też A05, A06, A09, A28 (10-06), A16 (10-12), A29 (10-16) i A30 (10-09).

5. **A01: data niezgodna z tytułem.** `due_date` 2026-10-08 to termin przysłania tekstów przez Kasię, a tytuł pozycji brzmi „Uruchomić test wstępu”. W kalendarzu wychodzi uruchomienie w czwartek tego tygodnia, co przeczy G02. W założeniach system sam wnioskuje „najwcześniej 2026-10-12”, ale nie przeniósł tego do daty.
   *Poprawka:* rozdzielić pola `client_input_due` i `action_due`. Test kodu: `due_date` pozycji nie może wpadać w okno zabezpieczenia, które blokuje tę pozycję.
6. **A07 i A21 bez daty**, choć mają `due_text` „zaraz po rozmowie”, a Marek mówi: „Drugi telefon i filtr biorę zaraz po rozmowie”. Referencja daje 10-06. Obu nie ma w kalendarzu.
   *Poprawka:* test kodu: gdy `due_text` jest niepusty, a `due_date` pusty, zgłosić ostrzeżenie. Reguła w prompcie: „po callu / zaraz po rozmowie / dziś” oznacza dzień spotkania.
7. **A37/G06: okno 19–23.10 bez struktury.** A37 ma `due_date` = null, a G06 ma tylko `until` 2026-10-23, bez daty początku. Okna nie ma w kalendarzu i nie da się go automatycznie sprawdzić względem A01/A16.
   *Poprawka:* pola `from`/`until` jako daty ISO w zabezpieczeniach i test kolizji z datami pozycji.
8. **A33:** `due_date` 2026-10-15 to dzień spotkania, a pozycja to „Wysłać zaproszenie”. Zaproszenie trzeba wysłać wcześniej, zaraz po potwierdzeniu. To drobna sprawa, bo warunek jest opisany.
9. **A02 (10-09 zamiast 10-08) i A17 (10-13 zamiast 10-12):** system przyjmuje „przypomnienie dzień po upływie terminu” i zapisał to w założeniach. To interpretacja do obrony, nie liczę jej jako błędu. Możliwe, że to referencja jest tu zbyt dosłowna.

### 4.3 Nadinterpretacje (drobne)

10. **G07** rozszerza zakaz na „ani z handlowcami bezpośrednio”. W rozmowie padło tylko „do Oli nie piszę, ustalam wszystko z tobą”. Kontekst (ściąga i szkolenie przez Kasię) to wspiera, ale nikt tego nie powiedział wprost.
11. **D07:** „Obiecałem, że korekta dotrze w przyszłym tygodniu”. W rozmowie było „powinna przyjść”, czyli bez obietnicy.
12. **D08:** „pokażę… jakie są dotychczasowe wyniki”. Marek mówił „pokażę, co mamy”. Sformułowanie jest łagodnie rozszerzone, ale nieszkodliwe.

*Poprawka do 10–12:* reguła w prompcie: w szkicach i zabezpieczeniach nie wzmacniać modalności („powinna” ≠ „obiecałem”) i nie rozszerzać zakresu osób.

## 5. Szkice wiadomości (Auto Tama)

Sprawdzone dla każdego szkicu: odbiorca dozwolony, liczba wysyłek, zakres treści, brak obietnic spoza rozmowy, brak kontaktu z Olą.

| Szkic | Do | Werdykt | Uzasadnienie |
|---|---|---|---|
| D01 | Kasia | OK | Adres, godziny salonów i dzwonienia zgodne z wersją ostateczną. Bez nagrania testowego, „możesz puścić sobie test” |
| D02 | Kasia | OK | Warunkowe, „wysłać raz”. Przypomina o AI i nagrywaniu. Nie pisze tekstu za Kasię |
| D03 | Kasia | OK | Jeden mail, warunkowo, bez wzoru pliku. Wymóg „numer + miasto” zgodny z rozmową |
| D04 | Kasia | OK | Łączy informację o błędzie z liczbą przypadków, zgodnie z „napiszę razem z informacją”. Odliczenie tylko warunkowo. Placeholdery zamiast zgadywania |
| D05 | Kasia | OK | Tylko cena, bez przykładowej treści. Decyzja zostaje u Pawła |
| D06 | Kasia | OK | Ściąga idzie do Kasi, nie do handlowców. Szkolenie czeka na termin Kasi. „W załączniku” zakłada gotową ściągę, co pokrywa `send_when` |
| D07 | Michał (wewn.) | OK z uwagą | Merytorycznie poprawny (podmioty, termin). Słowo „Obiecałem” jest za mocne (pkt 11) |
| D08 | Paweł | OK | Wysyłka dopiero po potwierdzeniu Kasi. 30 min, 15.10, 10:00. Nie wspomina VoiceDesk, nazwy firmy ani 208. Brak adresu e-mail, co system jawnie zaznaczył |

Żaden szkic nie idzie do Oli ani do handlowców. Żaden nie obiecuje integracji, terminu funkcji ani włączenia Opla. Liczba wysyłek jest zgodna z ustaleniami: jedno przypomnienie o tekstach, jeden mail o pliku.

## 6. Druga rozmowa (DentaVita)

Pokrycie S01–S07:

| Ref | System | Ocena |
|---|---|---|
| S01 | A01 | FOUND (10-12, godz. 8:00/8:30/9:00, dr Kania, sprawdzić inne dni) |
| S02 | A01 („potem przekazać wynik”), D02 | FOUND (scalone) |
| S03 | A02 | FOUND (17:30, obie kliniki; 19:00 i 18:00 jako zastąpione) |
| S04 | A03, G01 | FOUND |
| S05 | A04 | FOUND (bez terminu, brak integracji z grafikiem) |
| S06 | A05, G02, G03 | FOUND |
| S07 | A06 | FOUND |

Pułapki: 17:30 zamiast 18:00 PASS (A02) · propozycja Gdyni odrzucona, nie jest zobowiązaniem: PASS (A05 `do_not_do`, propozycja jako „zastępuje”) · „przekażę rejestracji” to obecne zachowanie agenta, nie zadanie: PASS (brak takiej pozycji).

Daty: A02 = 2026-10-13 (dziś), A01 = 2026-10-15 (czwartek), w D02 „poniedziałek 12.10”. Wszystkie poprawne.

Szkice:
- **D01: BŁĄD.** Treść „potwierdzam zmianę ustaloną na **wczorajszym** callu” jest zła, bo szkic ma wyjść po zmianie konfiguracji, planowanej na 2026-10-13, czyli w dniu callu. Pozostała treść (17:30, obie kliniki, zapowiedź odpowiedzi do 15.10) jest zgodna.
  *Poprawka:* w szkicach używać dat bezwzględnych. Test kodu: słowa „wczoraj/jutro” w treści porównać z planowaną datą wysyłki.
- **D02: OK.** Bez nagrań, odsyła do panelu, placeholdery zamiast przyczyny.
- **D03: OK.** Wysyłka dopiero po ustaleniu z Michałem, bez zgadywania.

Brak adresu e-mail Agnieszki jest poprawny, bo adres nie padł w rozmowie.

## 7. Wnioski

- **Pokrycie jest bardzo wysokie:** 40/41 pozycji, 7/7 w drugiej rozmowie, bez braków. Pułapki logiczne (korekty w trakcie rozmowy, kto zatwierdza, odrzucone propozycje, „nie wierzcie, jeśli ktoś napisze”) są obsłużone, a 108 + 19 cytatów jest faktycznie w transkrypcji i ma poprawnych mówców.
- **Najsłabszy obszar to daty, nie treść.** Dzień tygodnia jest zawsze dobry, ale `due_date` bywa podpięty pod zły fakt (A01), bywa pusty mimo jasnego „zaraz po rozmowie” (A07, A21), a okno urlopu nie ma struktury. Kalendarz jest więc najmniej wiarygodnym wyjściem i wymaga testów kodu, nie tylko reguł w prompcie.
- **Szkice są bezpieczne:** zero naruszeń ograniczeń w 11 szkicach. Zdarzają się drobne wzmocnienia sformułowań i jeden błąd daty względnej. Zatwierdzenie przez człowieka przed wysyłką nadal jest potrzebne.
- **Klasyfikacja `kind × state` jest miejscami niespójna** (warunkowe `do_now`, `no_action` zamiast `on_hold`, pozycja `info` zbierająca kilka faktów). Na razie nie gubi informacji, ale utrudni automatyczne kierowanie pozycji do systemów docelowych.
- **To jeden przebieg** (0,85 USD, 278 s dla dłuższej rozmowy). Odporność trzeba by potwierdzić kilkoma przebiegami i oceną człowieka. Referencja i ocena pochodzą od AI.
