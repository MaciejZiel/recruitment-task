# Reference: what follows from the call (eval answer key)

Source: `examples/transkrypcja-spotkanie.md` — Grupa Auto Tama × Rinvo, 2026-10-06 (wtorek). Perspective: Rinvo (Marek).
Prepared independently as a human-quality reference for evaluating the extractor. All quotes in backticks are exact substrings of the transcript.

Date resolution used (call date 2026-10-06, Tue):
- „do czwartku” = 2026-10-08; „piątek” = 2026-10-09; „poniedziałek” = 2026-10-12
- „dzisiaj / dziś / po callu / zaraz po rozmowie” = 2026-10-06
- „w tym tygodniu” = by 2026-10-09 (working week; at the latest 2026-10-11)
- „w przyszłym tygodniu” = 2026-10-12..2026-10-16 (due = 2026-10-16)
- „przyszły czwartek, piętnastego” = 2026-10-15
- Kasia's vacation „od dziewiętnastego do dwudziestego trzeciego” = 2026-10-19..2026-10-23 (Mon–Fri)

Statuses: todo | waiting_for_client | parked | do_not_do.

## Items

### R01 — Ręczny test A/B wstępu (dwie wersje, wybiera Kasia)
- type: config_change
- owner: Marek (uruchomienie); Kasia (tekst obu wersji)
- status: waiting_for_client
- due: none (start nie wcześniej niż 2026-10-12; nie w tygodniu 2026-10-19..23)
- condition / blocked_by: Kasia przysyła obie wersje tekstu; nie w tym tygodniu (Kasia odsłuchuje starą bazę); nic nowego w czasie urlopu Kasi
- constraints: Marek nie pisze tekstu za Kasię; dwie wersje (obecna + krótsza), nie jedna „lepsza” wybrana przez Rinvo; krótsza nadal mówi, że to wirtualna asystentka i że rozmowa jest nagrywana; podział na dwa dni albo na dwa miasta (Toruń / Włocławek); wybór wersji należy do Kasi; Paweł nie zatwierdza tekstu wstępu
- evidence: `Tylko ja chcę to zobaczyć na dwóch wersjach, a nie na jednej, którą wy uznacie za lepszą.`; `Tekst napiszę ja. W tym tygodniu tego nie puszczajcie`
- note: tło — agent „jedzie z formułką” i nie daje wejść w słowo. Marek: formułka musi być dokończona, „przepraszam” zostaje; jego „zobaczę, czy początek da się skrócić” zostaje wchłonięte przez wersję krótszą, którą pisze Kasia.

### R02 — Przypomnienie o tekstach wstępu (jedno)
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-08 (jeśli do czwartku nie przyjdą obie wersje; przypomnienie po upływie terminu)
- condition / blocked_by: tylko jeśli Kasia nie wyśle obu wersji do 2026-10-08
- constraints: przypomnieć tylko raz
- evidence: `Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.`; `Jak do czwartku nic nie przyjdzie, przypomnę.`

### R03 — Agent drugi raz pyta o model (sytuacja od Oli)
- type: bug
- owner: Marek
- status: parked
- due: none
- condition / blocked_by: brak nagrania / numeru — Ola nie podała
- constraints: bez nagrania nie da się znaleźć; nie zgadywać
- evidence: `drugi raz zapytała o model`; `bez nagrania nie znajdę. Ola nie dała numeru.`

### R04 — Wbudowane testy A/B w panelu (self-service)
- type: feature_request
- owner: product team (Marek zapisuje prośbę)
- status: todo (backlog, bez terminu)
- due: none
- condition / blocked_by: —
- constraints: termin nieobiecany; nie tylko wstęp, też kolejność pytań; miernik sukcesu = więcej pełnych rozmów (telefon + model + salon), NIE mniej rozłączeń
- evidence: `Czyli testy A/B wbudowane w panel, które sama ustawiasz i sama czytasz wyniki.`; `Więcej pełnych rozmów.`
- note: Marek: „nie jesteście pierwsi” — prośba powtarza się u innych klientów.

### R05 — Nieaktualny adres salonu we Włocławku w bazie wiedzy
- type: bug
- owner: Marek
- status: todo
- due: 2026-10-06
- condition / blocked_by: —
- constraints: Kapitulna → Toruńska 120 (Włocławek); Toruń bez zmian
- evidence: `A my od sierpnia jesteśmy na Toruńskiej.`; `Podaj mi nowy adres, poprawię dzisiaj.`

### R06 — Godziny salonów podawane przez agenta: sobota do 15:00, oba salony
- type: config_change
- owner: Marek
- status: todo
- due: 2026-10-06 (razem z adresem)
- condition / blocked_by: —
- constraints: sobota 9–15 dla OBU salonów (Toruń i Włocławek), nie 9–14 jak Kasia podała wcześniej; Włocławek w tygodniu 9–18
- evidence: `A co z godzinami salonu, które agent podaje klientom? Też mam zmienić na piętnastą?`; `Tak, dla obu salonów.`

### R07 — Napisać Kasi, gdy adres i godziny są poprawione
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-06
- condition / blocked_by: po R05/R06
- constraints: NIE wysyłać nagrania testowego — Kasia przetestuje sama; wystarczy wiadomość
- evidence: `Nie musisz mi wysyłać, puszczę sobie test sama. Tylko napisz, jak będzie poprawione.`; `Dobra, napiszę.`

### R08 — Drugi telefon tego samego dnia po rozłączeniu w ciągu 3 s
- type: bug
- owner: Marek
- status: todo
- due: 2026-10-06 („zaraz po rozmowie”)
- condition / blocked_by: —
- constraints: punkt startowy: 2026-10-05, 16:40, numer kończy się na 14, ta sama kampania, 6 przypadków po południu; nie ruszać przy okazji limitu 5 prób
- evidence: `Ustawialiśmy, że jak ktoś się rozłączy w ciągu trzech sekund, to agent nie dzwoni do niego drugi raz tego samego dnia.`; `Pierwszy był o 16:40, numer kończy się na 14`

### R09 — Limit 5 prób zostaje
- type: decision
- owner: Marek
- status: do_not_do
- due: none
- condition / blocked_by: —
- constraints: nie zmieniać na 3 (Kasia tylko przekazała pytanie kogoś innego)
- evidence: `Zostaw pięć. Nie kazałam schodzić do trzech.`; `No, zostaje pięć.`

### R10 — Godziny dzwonienia: pn–pt 9–19, sobota 9–15, niedziela bez dzwonienia
- type: config_change
- owner: Marek
- status: todo
- due: 2026-10-06 („zmienię po callu”)
- condition / blocked_by: —
- constraints: obecnie 9–20 pn–sob; sobota ostatecznie do 15:00 (korekta z 14:00 pod koniec rozmowy); niedziela bez zmian (i tak nie dzwoni)
- evidence: `To skróćcie do dziewiętnastej.`; `Sobotę jednak zostaw do piętnastej, nie do czternastej.`

### R11 — Klientka na urlopie to lead, nie odmowa
- type: decision
- owner: Marek (klasyfikacja/raportowanie); doradca dealera (oddzwonienie)
- status: todo
- due: none (klientka prosiła o kontakt w tygodniu 2026-10-12..16 — po stronie doradcy)
- condition / blocked_by: —
- constraints: nie oznaczać jako „niezainteresowany”; pytanie bota „kiedy zadzwonić” wystarcza
- evidence: `To jest lead, nie odmowa. Doradca ma zadzwonić, jak ona wróci.`; `Bot zapytał, kiedy zadzwonić, i to wystarczy.`

### R12 — Success story (lead z lipca → telefon w piątek → Peugeot 208 w sobotę), bez nazwy
- type: commitment
- owner: Marek
- status: todo
- due: none (wolno od razu)
- condition / blocked_by: tylko w wersji bez nazwy firmy i bez nazwiska klienta
- constraints: nazwa firmy dopiero po zatwierdzeniu przez Pawła; pokazać przypadek 208 na spotkaniu z Pawłem
- evidence: `nazwę firmy musi zatwierdzić Paweł. Bez nazwy możesz od razu.`; `Dobra, na razie bez nazwy. O nazwę zapytam przy Pawle.`

### R13 — Zgoda na użycie nazwy firmy w success story
- type: client_dependency
- owner: Paweł (decyzja); Marek pyta na spotkaniu
- status: waiting_for_client
- due: 2026-10-15 (spotkanie z Pawłem, jeśli potwierdzone)
- condition / blocked_by: R37 (spotkanie z Pawłem)
- constraints: do tego czasu bez nazwy
- evidence: `O nazwę zapytam przy Pawle.`; `I na tym spotkaniu możesz pokazać tę 208.`

### R14 — Przesunięcie prób na porę obiadową / po 17:00
- type: parked
- owner: Marek
- status: parked
- due: none
- condition / blocked_by: najpierw wyniki na świeżych leadach (stara baza nie jest reprezentatywna)
- constraints: nie zmieniać teraz harmonogramu prób
- evidence: `Może, ale nie teraz. To była stara baza, na świeżych może być inaczej.`; `Jasne, zostawiam.`

### R15 — Opel nie jest włączany
- type: parked
- owner: Kasia (decyzja); Marek
- status: do_not_do
- due: none
- condition / blocked_by: wyniki na świeżych leadach z ostatniego miesiąca; decyzja czeka na Kasię (Paweł nie zatwierdza Opla podczas jej urlopu)
- constraints: nawet jeśli Paweł napisze, że kazał — najpierw telefon do Kasi, nic nie klikać
- evidence: `Opel czeka, aż zobaczymy wyniki na leadach z ostatniego miesiąca.`; `Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.`

### R16 — Plik ze świeżymi leadami (ostatni miesiąc, strona + Facebook)
- type: client_dependency
- owner: Kasia (plik); Marek (uruchomienie)
- status: waiting_for_client
- due: 2026-10-12 (nie piątek — zamknięcie miesiąca)
- condition / blocked_by: plik od Kasi; wystarczy numer + Toruń/Włocławek; brak startu w tygodniu 2026-10-19..23
- constraints: bez pliku nic nie uruchamiać; NIE wysyłać wzoru pliku; przyjąć brzydki eksport („field 1”, model w treści); starej bazy nie puszczać drugi raz
- evidence: `Piątku nie obiecuję, bo zamykamy miesiąc. Powiedzmy poniedziałek.`; `Jak będzie numer i to, czy Toruń, czy Włocławek, to puszczajcie.`

### R17 — Jedno przypomnienie o pliku, jeśli nie przyjdzie w poniedziałek
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-12
- condition / blocked_by: tylko jeśli pliku nie ma w poniedziałek
- constraints: jeden mail, nie trzy
- evidence: `Jak nie wyślę, napisz jeden mail, nie trzy.`; `Jak w poniedziałek nic nie będzie, napiszę raz.`

### R18 — Starej bazy nie puszczać drugi raz
- type: decision
- owner: Marek
- status: do_not_do
- due: none
- condition / blocked_by: —
- constraints: dotyczy starej bazy 70 numerów
- evidence: `Starej bazy drugi raz nie puszczajcie.`; `Starej bazy drugi raz nie puszczam`

### R19 — Przegląd zakwalifikowany jako lead sprzedażowy (sprawa Oli)
- type: client_dependency
- owner: Kasia (przekazać sprawę); Marek (analiza po otrzymaniu)
- status: waiting_for_client
- due: none
- condition / blocked_by: Ola musi znaleźć maila, Kasia go przesyła
- constraints: nie zgadywać, która to kampania; nie ruszać bez wiadomości od Kasi; nie pisać do Oli
- evidence: `Jak nie, to nie zgadujcie, która to kampania.`; `A tego przeglądu, co Ola ma w skrzynce, nie ruszajcie bez wiadomości ode mnie.`

### R20 — Mail po walidacji: model i salon na górze
- type: feature_request
- owner: Marek
- status: parked
- due: none
- condition / blocked_by: wrócić, gdy ruszą świeże leady; nie w tym tygodniu (zamknięcie miesiąca)
- constraints: nie zmieniać teraz; ustalenia tylko z Kasią, nie z Olą
- evidence: `model i salon na górze, żeby nie musieli szukać w tej ścianie.`; `Wrócimy do tego, jak pójdą świeże leady.`

### R21 — Nie kontaktować się z Olą bezpośrednio
- type: decision
- owner: Marek
- status: do_not_do
- due: none
- condition / blocked_by: —
- constraints: wszystko ustalane z Kasią
- evidence: `I do Oli nie piszę, ustalam wszystko z tobą.`

### R22 — Filtr statusu „zainteresowany” na liście kontaktów nie zawęża
- type: bug
- owner: Marek
- status: todo
- due: 2026-10-06 („zaraz po rozmowie”)
- condition / blocked_by: —
- constraints: filtr daty działa; nie mieszać z klikalnym kafelkiem (R23)
- evidence: `Na liście kontaktów filtr „zainteresowany” też nie zawęża.`; `Widzę: data działa, a filtr statusu nie. To sprawdzę u nas po callu.`

### R23 — Klikalny kafelek „zainteresowani” na dashboardzie walidacji
- type: feature_request
- owner: product team (Marek)
- status: todo (backlog, bez terminu)
- due: none
- condition / blocked_by: —
- constraints: to brakująca funkcja, nie bug; terminu nie obiecano
- evidence: `Klikam w tę dziewiątkę. Nic.`; `filtr jest zepsuty, a klikania w kafelek nigdy nie zrobiliśmy. Na to klikanie terminu ci nie podam.`

### R24 — Kolumna „nazwisko” zaraz po statusie na liście kontaktów
- type: feature_request
- owner: Marek
- status: todo (warunkowo)
- due: none
- condition / blocked_by: tylko jeśli poprawka filtra (R22) i tak dotyka tej listy
- constraints: bez osobnej roboty pod kolumnę; jeśli problem z filtrem jest gdzie indziej — kolumn nie ruszać
- evidence: `Jak w tym tygodniu listy nie ruszacie, nie róbcie osobnej roboty pod kolumnę.`; `Jak się okaże, że problem z filtrem siedzi gdzie indziej, to kolumn osobno nie ruszam.`

### R25 — Cotygodniowy raport mailowy do Pawła (poniedziałek rano)
- type: feature_request
- owner: product team (Marek zapisuje)
- status: todo (backlog, bez terminu)
- due: none
- condition / blocked_by: —
- constraints: termin nieobiecany; zakres: ile zadzwoniono, ile odebrało, ilu zainteresowanych
- evidence: `Da się, żeby to samo do niego przychodziło? W poniedziałek rano, na przykład.`; `Ale to jest coś, o co pyta więcej klientów, więc zapiszę. Nie obiecuję terminu.`

### R26 — Agent po godzinach (jeden agent na wszystkie numery)
- type: parked
- owner: Kasia (decyzja o powrocie do tematu)
- status: parked
- due: none
- condition / blocked_by: nie w tym miesiącu; wraca tylko, gdy Kasia sama powie; Paweł tylko pyta, nie zlecił
- constraints: zakres zapisany do przyszłego projektu — sprzedaż jak walidacja → lead; serwis bez umawiania, zebrać imię/telefon/model/salon/opis, bez pytania o VIN, BOK oddzwania rano; części tak samo + przypomnieć o VIN na rano; assistance: podać numer marki, bez zakładania sprawy; reszta (np. kluczyki) do BOK na rano
- evidence: `Jak salon jest zamknięty, ma odbierać jeden agent, na wszystkie numery.`; `Jak sama nie powiem, że wracamy do tematu, to nie wracamy.`

### R27 — Numery assistance i lista pól: przechować, nie podpinać
- type: client_dependency
- owner: Kasia (przysyła, kiedy znajdzie chwilę); Marek (przechowuje)
- status: do_not_do
- due: none
- condition / blocked_by: przysłanie materiałów NIE jest zielonym światłem
- constraints: trzymać u siebie, nic nie podpinać; jeśli ktoś napisze „Kasia mówiła, że po godzinach od wtorku” — nie wierzyć, odpisać, że czekamy na Kasię
- evidence: `ale to nie jest zielone światło. Jak wyślę, trzymajcie u siebie, nie podpinajcie.`; `I jak ktoś ode mnie napisze „Kasia mówiła, że po godzinach od wtorku”, nie wierzcie.`

### R28 — Serwis w ciągu dnia przez agenta
- type: parked
- owner: Kasia
- status: do_not_do
- due: none
- condition / blocked_by: osobny temat, „może za pół roku”
- constraints: nie ruszać
- evidence: `Serwisu w ciągu dnia tym agentem nie ruszamy. To osobny temat, może za pół roku.`

### R29 — Przekazać Michałowi sprawę korekty faktury za wrzesień
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-06
- condition / blocked_by: —
- constraints: faktura wystawiona na „Grupa Auto Tama sp. z o.o.”, umowa z „Auto Tama Toruń sp. z o.o.”
- evidence: `Faktury wystawia Michał, przekażę mu dziś.`; `a umowa jest podpisana z „Auto Tama Toruń sp. z o.o.”`

### R30 — Faktura korygująca za wrzesień
- type: billing
- owner: Michał
- status: todo
- due: 2026-10-16 („w przyszłym tygodniu”)
- condition / blocked_by: R29
- constraints: korekta na podmiot z umowy (Auto Tama Toruń sp. z o.o.); księgowa (pani Grażyna) bez niej nie zaksięguje
- evidence: `Ona potrzebuje korekty, inaczej tego nie zaksięguje.`; `Korekta powinna przyjść w przyszłym tygodniu.`

### R31 — Jak rozliczane są połączenia 3-sekundowe (sekunda vs rozpoczęta minuta)
- type: billing
- owner: Marek
- status: todo
- due: none
- condition / blocked_by: —
- constraints: —
- evidence: `Te połączenia, gdzie ktoś się rozłącza po trzech sekundach, też liczycie jako minutę?`; `Szczerze, nie pamiętam, czy liczymy od pierwszej sekundy, czy za rozpoczętą minutę. Sprawdzę.`

### R32 — Odjąć koszt podwójnych telefonów i podać Kasi ich liczbę
- type: billing
- owner: Marek (Michał przy fakturze)
- status: todo
- due: none
- condition / blocked_by: jeśli podwójne telefony to błąd Rinvo (R08)
- constraints: liczbę przypadków przekazać razem z informacją o błędzie (Paweł będzie pytał)
- evidence: `A jeśli te podwójne telefony to nasz błąd, to ich nie powinniście płacić. Odejmiemy je.`; `Napiszę razem z informacją, co z tym błędem.`

### R33 — Cena SMS-ów (po dwóch nieudanych próbach)
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-09 („w tym tygodniu”)
- condition / blocked_by: —
- constraints: wysłać samą cenę; treść SMS pisze Kasia (Marek oferował przykładowy tekst — Kasia poprosiła tylko o cenę)
- evidence: `Przyślij cenę. Wszystko, co kosztuje, i tak musi zatwierdzić Paweł. Treść napiszę sama`; `Dobra, cenę wyślę w tym tygodniu.`

### R34 — SMS po dwóch nieudanych próbach (funkcja)
- type: feature_request
- owner: Paweł (zatwierdzenie kosztu)
- status: waiting_for_client
- due: none
- condition / blocked_by: zatwierdzenie kosztu przez Pawła po otrzymaniu ceny (R33)
- constraints: SMS-y płatne osobno; treść pisze Kasia
- evidence: `Jak bot dwa razy nie dodzwoni się do kogoś, to czy nie mógłby wysłać SMS-a?`; `Technicznie się da, ale SMS-y kosztują osobno, za każdą wiadomość.`

### R35 — Konkurencja: VoiceDesk (taniej, integracja z CRM)
- type: risk_signal
- owner: Marek
- status: todo
- due: none
- condition / blocked_by: —
- constraints: nie obiecywać integracji z „systemem” w tym kwartale; odpowiedź = rozmowa bezpośrednio z Pawłem (R37)
- evidence: `Dwa tygodnie temu była u Pawła firma VoiceDesk.`; `Integracji z waszym systemem teraz nie mamy i nie chcę obiecywać, że będzie w tym kwartale.`

### R36 — Paweł chciał wszystko wyłączyć (ryzyko odejścia)
- type: risk_signal
- owner: Marek
- status: todo
- due: none
- condition / blocked_by: —
- constraints: Paweł patrzy na liczby (9/70), nie na nagrania; kontekst: 23 pełne na 41 odebranych na starej bazie
- evidence: `Paweł zobaczył tylko te dziewięć na siedemdziesiąt i chciał wszystko wyłączyć.`; `Paweł patrzy na liczby, nie na nagrania`

### R37 — Spotkanie z Pawłem: czwartek 2026-10-15, 10:00 (Paweł w Toruniu)
- type: commitment
- owner: Kasia (przekazuje i potwierdza); Marek (zaproszenie po potwierdzeniu)
- status: waiting_for_client
- due: 2026-10-15
- condition / blocked_by: potwierdzenie od Kasi
- constraints: zaproszenie wysłać dopiero po potwierdzeniu; ~30 min; pokazać przypadek 208; zapytać o nazwę firmy do success story
- evidence: `Zaproponuj przyszły czwartek o dziesiątej, on wtedy jest w Toruniu. Ja mu to przekażę i potwierdzę.`; `Czwartek, piętnastego, dziesiąta. Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.`

### R38 — Ściąga (jedna strona) ze znaczeniem statusów dla handlowców
- type: commitment
- owner: Marek
- status: todo
- due: none
- condition / blocked_by: —
- constraints: wysłać do Kasi (nie do handlowców bezpośrednio)
- evidence: `Mogę też przygotować jedną stronę ze ściągą, co znaczy który status.`; `Ściągę ci wyślę`

### R39 — Szkolenie handlowców (kwadrans, online)
- type: parked
- owner: Kasia (termin); Marek (prowadzi)
- status: waiting_for_client
- due: none
- condition / blocked_by: dopiero gdy ruszą świeże leady; termin ustala Kasia
- constraints: nie wcześniej
- evidence: `Szkolenie dopiero, jak pójdą świeże, nie wcześniej, bo zapomną. Termin ustalę ja.`; `szkolenie czeka na twój termin`

### R40 — Agent nie sprzedaje; bez propozycji aut używanych
- type: decision
- owner: Marek
- status: do_not_do
- due: none
- condition / blocked_by: —
- constraints: przy „już kupiłem” / „rozmyśliłem się” — podziękować i się rozłączyć; odrzucona prośba Oli o auta używane; groźba wyłączenia, jeśli zacznie sprzedawać
- evidence: `Ola chciała, żeby przy odmowie proponował auto używane. Nie.`; `Używanych nie dokładam.`

### R41 — Zamrożenie na czas urlopu Kasi (2026-10-19..2026-10-23)
- type: decision
- owner: Marek
- status: do_not_do
- due: 2026-10-19 (początek okresu)
- condition / blocked_by: —
- constraints: nic nowego nie startuje, nawet jeśli plik ze świeżymi leadami już będzie i coś się wysypie; w pilnych sprawach telefon do Pawła; Paweł NIE zatwierdza Opla ani tekstu wstępu
- evidence: `W tym czasie nic nowego nie odpalajcie, nawet jak plik ze świeżymi leadami już będzie i coś się wysypie.`; `Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.`

Total: 41 items (R01–R41).

## Traps

- [ ] **Sobota: korekta 14:00 → 15:00.** Godziny dzwonienia w sobotę ostatecznie 9–15 (nie 9–14, które padło wcześniej). `Sobotę jednak zostaw do piętnastej, nie do czternastej.`
- [ ] **Ta sama korekta dotyczy godzin salonu podawanych przez agenta — dla OBU salonów**, nie tylko Włocławka (wcześniej padło „Toruń bez zmian”). `Tak, dla obu salonów. Dobrze, że pytasz.`
- [ ] **Godziny dzwonienia w tygodniu: 9–19** (było 9–20); niedziela bez zmian. `Czyli sobota dziewiąta–piętnasta, tydzień dziewiąta–dziewiętnasta.`
- [ ] **Opel zostaje wyłączony, nawet jeśli Paweł napisze.** `Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.`
- [ ] **Agent po godzinach to nie zielone światło**, nawet gdy przyjdą numery assistance; nie podpinać; nie wierzyć „Kasia mówiła, że od wtorku”. `Numery assistance i listę pól wam wyślę, jak znajdę chwilę, ale to nie jest zielone światło.`
- [ ] **Zamrożenie 2026-10-19..23**: nic nowego nie startuje (także świeże leady i test wstępu); do Pawła tylko, gdy się pali. `Jakby się naprawdę paliło, dzwońcie do Pawła.`
- [ ] **Paweł nie zatwierdza Opla ani tekstu wstępu** w czasie urlopu Kasi. `Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.`
- [ ] **Klientka na urlopie to lead, nie odmowa** — nie klasyfikować jako „niezainteresowany”. `To jest lead, nie odmowa.`
- [ ] **Filtr statusu (bug) ≠ klikalny kafelek (brakująca funkcja)** — dwa osobne itemy, różne typy. `Nie mieszałbym tych dwóch rzeczy: filtr jest zepsuty, a klikania w kafelek nigdy nie zrobiliśmy.`
- [ ] **Kolumna „nazwisko” tylko przy okazji** poprawki listy; bez osobnej pracy. `Jak w tym tygodniu listy nie ruszacie, nie róbcie osobnej roboty pod kolumnę.`
- [ ] **Limit 5 prób zostaje** — nie zmieniać na 3, to nie było polecenie. `Zostaw pięć. Nie kazałam schodzić do trzech.`
- [ ] **Miernik testu A/B = więcej pełnych rozmów**, nie mniej rozłączeń. `Rozłączenia mogą być, jak ktoś po prostu nie chce.`
- [ ] **Test wstępu: dwie wersje, tekst pisze Kasia, nie w tym tygodniu, przypomnienie tylko raz.** `Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.`
- [ ] **Krótszy wstęp nadal musi ujawniać AI i nagrywanie.** `Druga krótsza, ale dalej ma mówić, że jest wirtualną asystentką i że rozmowa jest nagrywana.`
- [ ] **Success story tylko bez nazwy firmy**, dopóki Paweł nie zatwierdzi; bez nazwiska klienta. `Mnie to nie przeszkadza, ale nazwę firmy musi zatwierdzić Paweł.`
- [ ] **Konkurent VoiceDesk** — sygnał ryzyka (taniej ~30%, integracja z CRM); bez obietnicy integracji w tym kwartale. `Paweł mówił coś o „jakieś trzydzieści procent taniej”, ale nie wiem, od czego.`
- [ ] **Billing: rozliczanie połączeń 3-sekundowych + zwrot za podwójne telefony** (warunkowo — jeśli to błąd Rinvo) i podanie ich liczby. `Bo jak tak, to te podwójne telefony, o których mówiłam, kosztują nas dwa razy.`
- [ ] **Korekta faktury: robi Michał, nie Marek**; Marek tylko przekazuje dziś. `Faktury wystawia Michał, przekażę mu dziś.`
- [ ] **Spotkanie z Pawłem 2026-10-15 10:00 — zaproszenie dopiero po potwierdzeniu Kasi.** `Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.`
- [ ] **Plik świeżych leadów: poniedziałek 2026-10-12 (nie piątek), jeden mail, bez wzoru pliku.** `I nie przysyłaj mi wzoru pliku.`
- [ ] **Starej bazy nie puszczać drugi raz.** `Starej bazy drugi raz nie puszczajcie.`
- [ ] **Sprawa przeglądu od Oli: nie zgadywać kampanii, czekać na Kasię.** `Jak nie, to nie zgadujcie, która to kampania.`
- [ ] **Nie pisać do Oli** — wszystko przez Kasię. `I do Oli nie piszę, ustalam wszystko z tobą.`
- [ ] **Nie wysyłać nagrania testowego po poprawce adresu** — tylko wiadomość. `Nie musisz mi wysyłać, puszczę sobie test sama.`
- [ ] **SMS: tylko cena, bez przykładowego tekstu**; sama funkcja czeka na Pawła (koszt). `Treść napiszę sama, tak jak ze wstępem.`
- [ ] **Mail do handlowców (model i salon na górze) — odłożony do świeżych leadów.** `Ale nie w tym tygodniu.`
- [ ] **Przesunięcie prób na porę obiadową — odłożone**, to tylko obserwacja ze starej bazy. `Może, ale nie teraz.`
- [ ] **Szkolenie handlowców dopiero po świeżych leadach, termin Kasi; ściąga od razu.** `Ściągę tak. Szkolenie dopiero, jak pójdą świeże, nie wcześniej`
- [ ] **Agent nie sprzedaje, bez aut używanych** — prośba Oli odrzucona. `Jak zacznie sprzedawać, wyłączę go.`
- [ ] **„Drugi raz o model” nie da się zbadać** bez nagrania — nie tworzyć zadania „napraw”, tylko zaparkować. `Ola nie dała numeru.`
- [ ] **Serwis w ciągu dnia — nie ruszać** (osobny temat, nie część projektu po godzinach). `Serwisu w ciągu dnia tym agentem nie ruszamy.`
- [ ] **Paweł ≠ Kasia jako źródło decyzji**: Paweł decyduje o markach, budżecie i kosztach, ale Opel i wstęp czekają na Kasię; agent po godzinach „Paweł nie powiedział „róbcie”, on tylko pyta”. `Paweł nie powiedział „róbcie”, on tylko pyta.`
- [ ] **Rzeczy, których Marek wprost NIE zrobi**: nie pisze tekstu wstępu (`Tekstu za ciebie nie piszę.`), nie puszcza nic bez pliku (`Bez pliku nic nie puszczam.`), nie podepnie numerów assistance (`Jak wyślesz numery, odłożę je i nic nie podepnę.`), nie rusza sprawy przeglądu bez danych (`Bez tego nie ruszam.`), nie włącza Opla (`Opla nie włączam.`), nie dokłada używanych (`Używanych nie dokładam.`), nie rusza limitu prób (`Limitu pięciu prób przy okazji nie ruszam`), nie wysyła wzoru pliku (`wzoru ci nie wysyłam`).

## Second transcript (druga-rozmowa.md) — expected items

Source: `examples/druga-rozmowa.md` — DentaVita × Rinvo, 2026-10-13 (wtorek). Fictional. Perspective: Rinvo (Marek).
Date resolution: „w piątek” (przeszły) = 2026-10-09; „w poniedziałek” (przeszły) = 2026-10-12; „do czwartku” = 2026-10-15; „dzisiaj” = 2026-10-13; „w przyszłym tygodniu” = 2026-10-19..23; „wyniki za październik” = dostępne po 2026-10-31.

### S01 — Odwołane wizyty mają w panelu status „potwierdzona”
- type: bug
- owner: Marek
- status: todo
- due: 2026-10-15
- condition / blocked_by: —
- constraints: punkt startowy: rozmowy z 2026-10-09 (Oliwa), wizyty 2026-10-12 na 8:00, 8:30, 9:00, gabinet dr Kani; sprawdzić też inne dni
- evidence: `W piątek trzy osoby z Oliwy odwołały wizytę w rozmowie z agentem, a w panelu mają status „potwierdzona”.`; `Wszystkie trzy były na poniedziałek na ósmą, ósmą trzydzieści i dziewiątą, gabinet doktor Kani.`

### S02 — Do czwartku dać znać, co się stało i czy dotyczy innych dni
- type: commitment
- owner: Marek
- status: todo
- due: 2026-10-15
- condition / blocked_by: —
- constraints: przekazać wyniki bez wysyłania nagrań mailem (S04)
- evidence: `Do czwartku dam ci znać, co się stało i czy w innych dniach też tak było.`

### S03 — Godziny dzwonienia: do 17:30 w obu klinikach
- type: config_change
- owner: Marek
- status: todo
- due: 2026-10-13
- condition / blocked_by: —
- constraints: ostateczna wartość 17:30 (korekta z 18:00 pod koniec rozmowy; obecnie 19:00); jedno ustawienie dla Oliwy i Wrzeszcza
- evidence: `Nie do osiemnastej, tylko do siedemnastej trzydzieści`; `Czyli dzwonimy do siedemnastej trzydzieści, w obu klinikach.`

### S04 — Nie przesyłać nagrań mailem
- type: decision
- owner: Marek
- status: do_not_do
- due: none
- condition / blocked_by: —
- constraints: nawet na prośbę w pośpiechu; dane medyczne; odsłuch tylko w panelu
- evidence: `I nagrań mi nie przesyłajcie mailem, nawet jak poproszę w pośpiechu.`; `Jasne, żadnych nagrań mailem.`

### S05 — Agent proponuje nowy termin przy odwołaniu
- type: feature_request
- owner: product team (Marek zapisuje)
- status: todo (backlog, bez terminu)
- due: none
- condition / blocked_by: wymaga dostępu do grafiku kliniki (brak integracji)
- constraints: termin nieobiecany
- evidence: `Chciałabym, żeby od razu proponował nowy termin z grafiku.`; `Zapisuję jako prośbę, ale terminu nie podam.`

### S06 — Gdynia nie jest włączana
- type: parked
- owner: dr Tomasz Lis (decyzja)
- status: do_not_do
- due: none
- condition / blocked_by: dr Lis widzi wyniki za październik z Oliwy i Wrzeszcza i sam decyduje
- constraints: oferta Marka „w przyszłym tygodniu” odrzucona; nie wierzyć wiadomościom, że Agnieszka się zgodziła
- evidence: `Gdyni nie włączamy, dopóki doktor Lis nie zobaczy wyników za październik z Oliwy i Wrzeszcza.`; `I jak ktoś napisze, że ja się zgodziłam na Gdynię, nie wierzcie.`

### S07 — Czy płacą za minutę, gdy agent trafia na pocztę głosową
- type: billing
- owner: Marek (z Michałem)
- status: todo
- due: none
- condition / blocked_by: —
- constraints: —
- evidence: `Jak agent trafia na pocztę głosową i się rozłącza, to płacimy za to minutę?`; `Sprawdzę z Michałem i odpiszę.`

Total: 7 items (S01–S07).

### Second transcript traps

- [ ] Godziny dzwonienia: wartość końcowa 17:30, nie 18:00. `Pomyliłam się. Nie do osiemnastej`
- [ ] Gdynia: propozycja Marka nie jest zobowiązaniem — została odrzucona. `Mogę ją podpiąć nawet w przyszłym tygodniu.`
- [ ] „Przekażę rejestracji” to obecne zachowanie agenta, nie zobowiązanie Rinvo. `Jak pacjent odwołuje, agent mówi tylko „przekażę rejestracji”.`
