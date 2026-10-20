# Po rozmowie: Grupa Auto Tama, 2026-10-06

Źródło: `transkrypcja-spotkanie.md` · uczestnicy: Kasia Malinowska (BDC, Grupa Auto Tama), Marek Rewoliński (Rinvo)  
Pozycji: 37 · zabezpieczeń: 11 · szkiców: 8 · cytaty zweryfikowane: 108/108

> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.

## Podsumowanie

Call statusowy dotyczył walidacji leadów (Peugeot i Citroën, Toruń i Włocławek). Wyszły trzy błędy: nieaktualny adres salonu we Włocławku, ponowne połączenie po rozłączeniu w ciągu 3 sekund i filtr statusu, który nie zawęża listy kontaktów. Ustalono nowe godziny dzwonienia (pon–pt 9–19, sobota 9–15) i sobotnie godziny salonów (9–15). Ustalono też test wstępu w dwóch wersjach, który ruszy dopiero po otrzymaniu tekstów od Kasi. Opel, agent po godzinach, nowy format maila do handlowców i szkolenie są wstrzymane do decyzji Kasi. Do tego Rinvo przekaże korektę faktury za wrzesień, wyśle cenę SMS-ów i ściągę statusów oraz zaproponuje Pawłowi spotkanie 15.10 o 10:00 z powodu konkurencji VoiceDesk. Od 19 do 23.10 Kasia jest na urlopie i w tym czasie nic nowego nie startuje.

## Zabezpieczenia (sprawdzić przed każdym działaniem)

- **G01** Nie włączać Opla. Paweł nie może tego zatwierdzić; jeśli napisze, że kazał, najpierw zadzwonić do Kasi. (do: Wyniki na świeżych leadach i decyzja Kasi · zdejmuje: Kasia Malinowska)
  > Marek (l. 132) ✅: „Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.”
  > Kasia (l. 228) ✅: „Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.”
- **G02** Nie uruchamiać testu wstępu w tygodniu spotkania. Tekst pisze i zatwierdza tylko Kasia, nie Paweł. (do: Koniec tygodnia 2026-10-11 i otrzymanie tekstów od Kasi · zdejmuje: Kasia Malinowska)
  > Kasia (l. 58) ✅: „Tekst napiszę ja. W tym tygodniu tego nie puszczajcie, bo odsłuchuję starą bazę i wszystko mi się zleje.”
- **G03** Nie puszczać starej bazy drugi raz. Bez pliku ze świeżymi leadami nic nie uruchamiać. (zdejmuje: Kasia Malinowska)
  > Kasia (l. 134) ✅: „Starej bazy drugi raz nie puszczajcie.”
  > Marek (l. 136) ✅: „Bez pliku nic nie puszczam.”
- **G04** Agent po godzinach: nie podpinać numerów assistance ani listy pól. Nie wierzyć wiadomościom, że Kasia zgodziła się na start (np. „od wtorku”), tylko odpisać, że czekamy na Kasię. (do: Kasia sama zgłosi powrót do tematu (nie w październiku) · zdejmuje: Kasia Malinowska)
  > Kasia (l. 176) ✅: „I jak ktoś ode mnie napisze „Kasia mówiła, że po godzinach od wtorku”, nie wierzcie.”
  > Kasia (l. 176) ✅: „Jak wyślę, trzymajcie u siebie, nie podpinajcie.”
- **G05** Agent nie sprzedaje i nie proponuje aut używanych. Przy odmowie dziękuje i kończy rozmowę. (zdejmuje: Kasia Malinowska)
  > Kasia (l. 224) ✅: „Ola chciała, żeby przy odmowie proponował auto używane. Nie. Jak zacznie sprzedawać, wyłączę go.”
- **G06** W czasie urlopu Kasi nic nowego nie uruchamiać. W pilnych sprawach dzwonić do Pawła, ale on nie zatwierdza Opla ani tekstu wstępu. (do: 2026-10-23 · zdejmuje: Kasia Malinowska)
  > Kasia (l. 228) ✅: „W tym czasie nic nowego nie odpalajcie, nawet jak plik ze świeżymi leadami już będzie i coś się wysypie.”
- **G07** Nie kontaktować się z Olą ani z handlowcami bezpośrednio, wszystko ustalać z Kasią.
  > Marek (l. 144) ✅: „I do Oli nie piszę, ustalam wszystko z tobą.”
- **G08** Nie ruszać sprawy przeglądu z maila Oli bez wiadomości od Kasi i nie zgadywać, która to kampania. (do: Kasia prześle sprawę · zdejmuje: Kasia Malinowska)
  > Kasia (l. 240) ✅: „A tego przeglądu, co Ola ma w skrzynce, nie ruszajcie bez wiadomości ode mnie.”
  > Kasia (l. 138) ✅: „Jak nie, to nie zgadujcie, która to kampania.”
- **G09** Nie używać nazwy firmy w przykładzie sprzedaży Peugeota 208 bez zgody Pawła. (do: Zgoda Pawła · zdejmuje: Paweł)
  > Kasia (l. 118) ✅: „Mnie to nie przeszkadza, ale nazwę firmy musi zatwierdzić Paweł. Bez nazwy możesz od razu.”
- **G10** Nie zmieniać limitu pięciu prób połączenia. (zdejmuje: Kasia Malinowska)
  > Kasia (l. 94) ✅: „Zostaw pięć. Nie kazałam schodzić do trzech.”
- **G11** Nie wysyłać zaproszenia na spotkanie z Pawłem przed potwierdzeniem od Kasi. (do: Potwierdzenie od Kasi · zdejmuje: Kasia Malinowska)
  > Marek (l. 210) ✅: „Czwartek, piętnastego, dziesiąta. Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.”

## Terminy (kalendarz i przypomnienia)

- **2026-10-06** · A05 Poprawić adres salonu we Włocławku w bazie wiedzy · Nie wysyłać nagrania testowego, Kasia przetestuje sama; Napisać do Kasi, gdy będzie poprawione
- **2026-10-06** · A06 Zmienić sobotnie godziny salonów podawane przez agenta na 9–15 · Dotyczy obu salonów
- **2026-10-06** · A09 Zmienić godziny dzwonienia na pon–pt 9–19, sobota 9–15 · Niedziela bez połączeń
- **2026-10-06** · A28 Przekazać Michałowi prośbę o korektę faktury za wrzesień
- **2026-10-08** · A01 Uruchomić test wstępu w dwóch wersjach po otrzymaniu tekstów · Tekst pisze wyłącznie Kasia, Rinvo nie pisze go za nią; Nie uruchamiać w tym tygodniu (Kasia odsłuchuje starą bazę); Obie wersje muszą informować o wirtualnej asystentce i nagrywaniu; Nie uruchamiać w dniach 19–23.10 (urlop Kasi); Wybór wersji należy do Kasi
- **2026-10-09** · A02 Przypomnieć raz o tekstach wstępu · Przypomnieć tylko raz
- **2026-10-09** · A30 Wysłać Kasi cenę SMS-ów · Nie wysyłać przykładowej treści SMS
- **2026-10-12** · A16 Uruchomić walidację świeżych leadów po otrzymaniu pliku · Bez pliku nic nie uruchamiać; Nie wysyłać wzoru pliku; Wystarczy numer i miasto; Nie uruchamiać w dniach 19–23.10
- **2026-10-13** · A17 Wysłać jeden mail-przypomnienie o pliku ze świeżymi leadami · Tylko jeden mail; Nie dołączać wzoru pliku
- **2026-10-15** · A33 Wysłać zaproszenie na spotkanie z Pawłem po potwierdzeniu Kasi · Nie wysyłać zaproszenia przed potwierdzeniem od Kasi
- **2026-10-16** · A29 Wystawić korektę faktury na Auto Tama Toruń sp. z o.o.

## Nie robić (zakazy i odrzucone prośby)

_Cel: lista zabezpieczeń konta klienta_

#### A08 · Nie zmieniać limitu pięciu prób
`config_change` · `do_not_do`  
Limit prób zostaje na 5. Kasia nie prosiła o zejście do 3, tylko wspomniała, że ktoś ją o to pytał.
- **Właściciel:** Marek Rewoliński
- **Zatwierdza:** Kasia Malinowska
- **Wersja ostateczna:** 5 prób
- **Ograniczenia:** Limit zostaje 5
  > Kasia (l. 94) ✅: „Zostaw pięć. Nie kazałam schodzić do trzech.”
  > Marek (l. 92) ✅: „Limitu pięciu prób przy okazji nie ruszam, to inna sprawa.”

#### A15 · Nie włączać Opla
`config_change` · `do_not_do`  
Opel czeka na wyniki walidacji świeżych leadów z ostatniego miesiąca. Nawet jeśli Paweł napisze, że kazał go włączyć, najpierw trzeba zadzwonić do Kasi.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Wyniki na świeżych leadach i decyzja Kasi.
- **Zatwierdza:** Kasia Malinowska (Paweł NIE może zatwierdzić)
- **Ograniczenia:** Paweł nie może zatwierdzić Opla; Przy prośbie od Pawła najpierw zadzwonić do Kasi
  > Kasia (l. 130) ✅: „Peugeot i Citroën zostają, Opel czeka, aż zobaczymy wyniki na leadach z ostatniego miesiąca.”
  > Marek (l. 132) ✅: „Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.”
  > Kasia (l. 228) ✅: „Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.”

#### A18 · Nie puszczać starej bazy drugi raz
`task` · `do_not_do`  
Stara baza leadów sprzed 2–3 miesięcy była już raz przedzwoniona i nie może być puszczona ponownie.
- **Właściciel:** Marek Rewoliński
  > Kasia (l. 134) ✅: „Starej bazy drugi raz nie puszczajcie.”
  > Marek (l. 136) ✅: „Starej bazy drugi raz nie puszczam i wzoru ci nie wysyłam.”

#### A26 · Nie podpinać numerów assistance ani listy pól
`task` · `do_not_do`  
Kasia może przysłać numery assistance i listę pól. To nie jest zgoda na start; materiały trzeba odłożyć i niczego nie podpinać.
- **Właściciel:** Marek Rewoliński
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Przechowywać, nie podpinać
- **Zależy od:** A25
  > Kasia (l. 176) ✅: „Numery assistance i listę pól wam wyślę, jak znajdę chwilę, ale to nie jest zielone światło.”
  > Marek (l. 178) ✅: „Jak wyślesz numery, odłożę je i nic nie podepnę. W tym miesiącu tego nie ruszamy.”

#### A27 · Nie używać agenta do serwisu w ciągu dnia
`feature_request` · `do_not_do`  
Obsługa serwisu w godzinach pracy salonu przez agenta to osobny temat, ewentualnie za pół roku.
- **Termin:** bez daty („może za pół roku”)
- **Zatwierdza:** Kasia Malinowska
  > Kasia (l. 172) ✅: „Serwisu w ciągu dnia tym agentem nie ruszamy.”

#### A36 · Nie dodawać sprzedaży ani propozycji aut używanych
`feature_request` · `do_not_do`  
Agent nie sprzedaje. Przy „już kupiłem” lub „rozmyśliłem się” dziękuje i kończy rozmowę. Prośba Oli o proponowanie aut używanych została odrzucona.
- **Zatwierdza:** Kasia Malinowska
  > Kasia (l. 224) ✅: „Ola chciała, żeby przy odmowie proponował auto używane. Nie. Jak zacznie sprzedawać, wyłączę go.”
  > Marek (l. 226) ✅: „Używanych nie dokładam.”

#### A37 · Nic nowego nie uruchamiać w czasie urlopu Kasi (19–23.10)
`info` · `do_not_do`  
W tym tygodniu nic nowego nie startuje, nawet jeśli plik ze świeżymi leadami już będzie. W pilnych sprawach dzwonić do Pawła, ale Opel i tekst wstępu czekają na Kasię.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („od dziewiętnastego do dwudziestego trzeciego”)
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Pilne sprawy: telefon do Pawła; Paweł nie zatwierdza Opla ani tekstu wstępu
  > Kasia (l. 228) ✅: „W tym czasie nic nowego nie odpalajcie, nawet jak plik ze świeżymi leadami już będzie i coś się wysypie.”
  > Marek (l. 230) ✅: „Jak się pali, dzwonię do Pawła, ale Opel i wstęp czekają na ciebie.”

## Zgłoszenia błędów (dla zespołu technicznego)

_Cel: issue tracker (np. Linear/Jira)_

#### A05 · Poprawić adres salonu we Włocławku w bazie wiedzy
`bug` · `scheduled`  
Agent podaje stary adres przy ul. Kapitulnej. Salon Peugeot i Citroën we Włocławku jest od sierpnia przy ul. Toruńskiej 120. Po poprawce trzeba napisać do Kasi, bez wysyłania nagrania testowego.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („poprawię dzisiaj”)
- **Wersja ostateczna:** Toruńska 120, Włocławek
- **Zastępuje:** Marek wyśle nagranie testowe
- **Ograniczenia:** Nie wysyłać nagrania testowego, Kasia przetestuje sama; Napisać do Kasi, gdy będzie poprawione
  > Marek (l. 80) ✅: „O, to jest nasz błąd, ewidentnie nieaktualna baza wiedzy. Podaj mi nowy adres, poprawię dzisiaj.”
  > Kasia (l. 82) ✅: „Toruńska 120. Godziny bez zmian, w tygodniu dziewiąta–osiemnasta, sobota dziewiąta–czternasta. Toruń bez zmian.”
  > Kasia (l. 86) ✅: „Nie musisz mi wysyłać, puszczę sobie test sama. Tylko napisz, jak będzie poprawione.”

#### A07 · Zbadać ponowne połączenia po rozłączeniu w ciągu 3 sekund
`bug` · `do_now`  
Według ustawień po rozłączeniu w ciągu 3 sekund agent nie powinien dzwonić drugi raz tego samego dnia. 5.10 po południu w tej samej kampanii zdarzyło się to 6 razy. Pierwszy przypadek: 16:40, numer kończący się na 14.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („zaraz po rozmowie”)
- **Ograniczenia:** Nie zmieniać przy okazji limitu pięciu prób
  > Kasia (l. 90) ✅: „Ustawialiśmy, że jak ktoś się rozłączy w ciągu trzech sekund, to agent nie dzwoni do niego drugi raz tego samego dnia. Wczoraj i tak zadzwonił.”
  > Kasia (l. 90) ✅: „Pierwszy był o 16:40, numer kończy się na 14, słyszałam obie próby jedna po drugiej.”
  > Marek (l. 92) ✅: „Dobra, sprawdzę po spotkaniu na tej kampanii, nie będziemy teraz w tym grzebać.”

#### A21 · Naprawić filtr statusu na liście kontaktów
`bug` · `do_now`  
Filtr „zainteresowany” na liście kontaktów nie zawęża wyników i pokazuje także nieodebrane oraz „kupiłem gdzie indziej”. Filtr daty działa poprawnie.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („zaraz po rozmowie”)
  > Kasia (l. 146) ✅: „Na liście kontaktów filtr „zainteresowany” też nie zawęża.”
  > Marek (l. 148) ✅: „Widzę: data działa, a filtr statusu nie. To sprawdzę u nas po callu.”

## Zmiany konfiguracji agenta

_Cel: panel konfiguracji agenta (zmiana po zatwierdzeniu)_

#### A06 · Zmienić sobotnie godziny salonów podawane przez agenta na 9–15
`config_change` · `scheduled`  
Od tego miesiąca oba salony (Toruń i Włocławek) są w sobotę czynne do 15:00. Godziny w tygodniu bez zmian, dla Włocławka 9–18. Poprawić razem z adresem.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („adres i godziny dzisiaj”)
- **Wersja ostateczna:** Sobota 9:00–15:00 dla obu salonów, w tygodniu bez zmian
- **Zastępuje:** Godziny bez zmian (sobota 9:00–14:00)
- **Ograniczenia:** Dotyczy obu salonów
  > Marek (l. 234) ✅: „A co z godzinami salonu, które agent podaje klientom? Też mam zmienić na piętnastą?”
  > Kasia (l. 236) ✅: „Tak, dla obu salonów. Dobrze, że pytasz.”
  > Marek (l. 238) ✅: „Dobra, poprawię razem z adresem.”

#### A09 · Zmienić godziny dzwonienia na pon–pt 9–19, sobota 9–15
`config_change` · `scheduled`  
Obecnie agent dzwoni pon–sob 9–20. Klient skarżył się na telefon o 19:30. Wieczorem i w sobotę po zamknięciu salonu nikt nie odbierze oddzwaniających klientów, dlatego godziny mają się pokrywać z pracą salonu. W niedzielę agent nie dzwoni.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („Zmienię po callu / adres i godziny dzisiaj”)
- **Zatwierdza:** Kasia Malinowska
- **Wersja ostateczna:** Pon–pt 9:00–19:00, sobota 9:00–15:00, niedziela brak
- **Zastępuje:** Pon–sob 9:00–20:00 (stan obecny); Pon–pt 9:00–19:00, sobota 9:00–14:00
- **Ograniczenia:** Niedziela bez połączeń
  > Kasia (l. 102) ✅: „To skróćcie do dziewiętnastej.”
  > Marek (l. 104) ✅: „Dobra. Tydzień dziewiąta–dziewiętnasta, sobota dziewiąta–czternasta. Zmienię po callu.”
  > Kasia (l. 232) ✅: „Sobotę jednak zostaw do piętnastej, nie do czternastej.”
  > Marek (l. 234) ✅: „Czyli sobota dziewiąta–piętnasta, tydzień dziewiąta–dziewiętnasta.”

## Zadania zespołu

_Cel: lista zadań właściciela_

#### A02 · Przypomnieć raz o tekstach wstępu
`task` · `scheduled`  
Jeśli do końca czwartku 8.10 Kasia nie przyśle obu wersji wstępu, wysłać jej jedno przypomnienie.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-09 („Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.”)
- **Warunek:** Brak obu wersji tekstu do końca czwartku 2026-10-08.
- **Ograniczenia:** Przypomnieć tylko raz
- **Zależy od:** A01
  > Kasia (l. 58) ✅: „Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.”
  > Marek (l. 60) ✅: „Jak do czwartku nic nie przyjdzie, przypomnę.”

#### A10 · Sprawdzić, jak naliczane są minuty za krótkie połączenia
`task` · `do_now`  
Paweł i księgowa pytają, czy połączenia przerwane po 3 sekundach są liczone jako pełna minuta. Marek nie pamięta, czy rozliczenie idzie od pierwszej sekundy, czy za rozpoczętą minutę.
- **Właściciel:** Marek Rewoliński
  > Kasia (l. 184) ✅: „Te połączenia, gdzie ktoś się rozłącza po trzech sekundach, też liczycie jako minutę?”
  > Marek (l. 186) ✅: „Szczerze, nie pamiętam, czy liczymy od pierwszej sekundy, czy za rozpoczętą minutę. Sprawdzę.”

#### A11 · Odjąć podwójne połączenia z rozliczenia i podać Kasi ich liczbę
`task` · `do_now`  
Jeśli podwójne połączenia to błąd Rinvo, nie będą one płatne i zostaną odjęte. Kasi trzeba napisać, ile ich było, razem z informacją o stanie błędu.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Potwierdzenie, że podwójne połączenia to błąd po stronie Rinvo.
- **Ograniczenia:** Informację o liczbie wysłać razem z informacją o błędzie
- **Zależy od:** A07, A10
  > Marek (l. 186) ✅: „A jeśli te podwójne telefony to nasz błąd, to ich nie powinniście płacić. Odejmiemy je.”
  > Kasia (l. 188) ✅: „To napisz mi, ile tego było, bo Paweł będzie pytał.”
  > Marek (l. 190) ✅: „Napiszę razem z informacją, co z tym błędem.”

#### A13 · Wykorzystać przykład sprzedaży Peugeota 208 bez nazwy firmy
`task` · `do_now`  
Lead z lipca, rozmowa z botem w piątek, zakup Peugeota 208 w sobotę. Przykładu można używać od razu, ale bez nazwy firmy i nazwiska. Na użycie nazwy firmy musi zgodzić się Paweł; Marek zapyta o to na spotkaniu z nim.
- **Właściciel:** Marek Rewoliński
- **Zatwierdza:** Paweł (nazwa firmy)
- **Ograniczenia:** Bez nazwiska klienta; Bez nazwy firmy do czasu zgody Pawła
  > Kasia (l. 118) ✅: „Mnie to nie przeszkadza, ale nazwę firmy musi zatwierdzić Paweł. Bez nazwy możesz od razu.”
  > Marek (l. 120) ✅: „Dobra, na razie bez nazwy. O nazwę zapytam przy Pawle.”

#### A17 · Wysłać jeden mail-przypomnienie o pliku ze świeżymi leadami
`task` · `scheduled`  
Jeśli w poniedziałek 12.10 plik nie przyjdzie, wysłać Kasi jeden mail.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-13 („Jak w poniedziałek nic nie będzie, napiszę raz.”)
- **Warunek:** Brak pliku do końca poniedziałku 2026-10-12.
- **Ograniczenia:** Tylko jeden mail; Nie dołączać wzoru pliku
- **Zależy od:** A16
  > Kasia (l. 134) ✅: „Jak nie wyślę, napisz jeden mail, nie trzy.”
  > Marek (l. 136) ✅: „Jak w poniedziałek nic nie będzie, napiszę raz.”

#### A28 · Przekazać Michałowi prośbę o korektę faktury za wrzesień
`task` · `scheduled`  
Faktura za wrzesień jest wystawiona na „Grupa Auto Tama sp. z o.o.”, a umowa jest z „Auto Tama Toruń sp. z o.o.”. Księgowa potrzebuje korekty, żeby zaksięgować fakturę.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („przekażę mu dziś”)
  > Kasia (l. 180) ✅: „Faktura za wrzesień przyszła na „Grupa Auto Tama sp. z o.o.”, a umowa jest podpisana z „Auto Tama Toruń sp. z o.o.”.”
  > Marek (l. 182) ✅: „Faktury wystawia Michał, przekażę mu dziś. Korekta powinna przyjść w przyszłym tygodniu.”

#### A29 · Wystawić korektę faktury na Auto Tama Toruń sp. z o.o.
`task` · `scheduled`  
Korekta faktury za wrzesień na podmiot z umowy powinna dotrzeć do klienta w przyszłym tygodniu.
- **Właściciel:** Michał (Rinvo)
- **Termin:** 2026-10-16 („w przyszłym tygodniu”)
- **Wersja ostateczna:** Nabywca: Auto Tama Toruń sp. z o.o.
- **Zależy od:** A28
  > Marek (l. 182) ✅: „Faktury wystawia Michał, przekażę mu dziś. Korekta powinna przyjść w przyszłym tygodniu.”

#### A30 · Wysłać Kasi cenę SMS-ów
`task` · `scheduled`  
Chodzi o SMS po dwóch nieudanych próbach połączenia. Wysłać wyłącznie cenę, bez przykładowego tekstu, bo treść napisze Kasia.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-09 („w tym tygodniu”)
- **Wersja ostateczna:** Tylko cena
- **Zastępuje:** Cena i przykładowy tekst
- **Ograniczenia:** Nie wysyłać przykładowej treści SMS
  > Marek (l. 194) ✅: „Mogę ci przysłać cenę i przykładowy tekst.”
  > Kasia (l. 196) ✅: „Przyślij cenę. Wszystko, co kosztuje, i tak musi zatwierdzić Paweł. Treść napiszę sama, tak jak ze wstępem.”
  > Marek (l. 198) ✅: „Dobra, cenę wyślę w tym tygodniu.”

#### A34 · Przygotować i wysłać Kasi ściągę statusów
`task` · `do_now`  
Jedna strona z wyjaśnieniem statusów („zainteresowany”, „oddzwonić”, „niezweryfikowany”) dla handlowców.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Wysłać do Kasi, nie bezpośrednio do handlowców
  > Marek (l. 218) ✅: „Mogę też przygotować jedną stronę ze ściągą, co znaczy który status.”
  > Marek (l. 222) ✅: „Dobra. Ściągę ci wyślę, a szkolenie czeka na twój termin.”

## Backlog produktu (prośby o funkcje)

_Cel: tablica produktowa_

#### A04 · Zapisać w backlogu testy A/B wbudowane w panel
`feature_request` · `do_now`  
Kasia chce sama wgrywać 2–3 wersje początku rozmowy lub kolejności pytań. System ma automatycznie dzielić połączenia i pokazywać wyniki. Za wynik uznaje się większą liczbę pełnych rozmów (telefon, model, salon), a nie mniejszą liczbę rozłączeń.
- **Właściciel:** Marek Rewoliński
- **Wersja ostateczna:** Miara sukcesu: więcej pełnych rozmów
- **Ograniczenia:** Nie podawać terminu
  > Kasia (l. 62) ✅: „Chciałabym mieć w panelu coś takiego, że wrzucam dwie albo trzy wersje początku rozmowy, system sam dzieli połowę telefonów na jedną, połowę na drugą, a po tygodniu widzę, przy której ludzie rzadziej się rozłączają i częściej dochodzą do końca.”
  > Marek (l. 68) ✅: „A to, żebyś mogła sama, zapisuję jako prośbę.”
  > Kasia (l. 70) ✅: „Więcej pełnych rozmów.”

#### A22 · Zapisać w backlogu klikalny kafelek „zainteresowani”
`feature_request` · `do_now`  
Kliknięcie w kafelek na dashboardzie walidacji powinno przenosić do listy tych kontaktów. Takiej funkcji nigdy nie było, to osobna sprawa od błędu filtra.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie podawać terminu
  > Kasia (l. 146) ✅: „Klikam w tę dziewiątkę. Nic.”
  > Marek (l. 148) ✅: „A to, żeby kliknięcie w dziewiątkę przenosiło cię do tych ludzi, to osobna sprawa, tego po prostu nie ma.”
  > Marek (l. 148) ✅: „Na to klikanie terminu ci nie podam.”

#### A23 · Przesunąć kolumnę nazwiska zaraz za status (tylko przy okazji filtra)
`feature_request` · `do_now`  
Na liście kontaktów nazwisko ma być bezpośrednio po statusie. Robimy to tylko wtedy, gdy naprawa filtra i tak wymaga zmian w tej liście.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Tylko jeśli naprawa filtra wymaga zmian w liście kontaktów.
- **Ograniczenia:** Nie robić osobnej pracy pod samą kolumnę
- **Zależy od:** A21
  > Kasia (l. 150) ✅: „Na liście kontaktów chcę mieć nazwisko zaraz po statusie.”
  > Kasia (l. 150) ✅: „Jak w tym tygodniu listy nie ruszacie, nie róbcie osobnej roboty pod kolumnę.”
  > Marek (l. 152) ✅: „Jak się okaże, że problem z filtrem siedzi gdzie indziej, to kolumn osobno nie ruszam.”

#### A24 · Zapisać w backlogu cotygodniowy raport mailowy
`feature_request` · `do_now`  
Automatyczny mail z liczbami (ile połączeń, ile odebranych, ilu zainteresowanych) do Pawła, np. w poniedziałek rano.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie obiecywać terminu
  > Kasia (l. 154) ✅: „Da się, żeby to samo do niego przychodziło? W poniedziałek rano, na przykład.”
  > Marek (l. 156) ✅: „Raportu mailowego teraz nie mamy. Ale to jest coś, o co pyta więcej klientów, więc zapiszę. Nie obiecuję terminu.”

## Czekamy na klienta

_Cel: przypomnienia w kalendarzu_

#### A01 · Uruchomić test wstępu w dwóch wersjach po otrzymaniu tekstów
`task` · `waiting_on_client`  
Kasia przyśle dwie wersje wstępu: obecną i krótszą. Obie muszą nadal mówić, że to wirtualna asystentka i że rozmowa jest nagrywana. Rinvo puszcza je ręcznie na dwa dni albo na dwa miasta (Toruń i Włocławek), a Kasia sama wybiera wersję, która zostaje.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-08 („do czwartku”)
- **Warunek:** Kasia przysyła obie wersje tekstu (termin: czwartek).
- **Zatwierdza:** Kasia Malinowska (Paweł NIE może zatwierdzić tekstu wstępu)
- **Wersja ostateczna:** Dwie wersje napisane przez Kasię, test ręczny na 2 dni albo na 2 miasta, wybór należy do Kasi
- **Zastępuje:** Marek sam sprawdzi po callu, czy da się skrócić początek wstępu
- **Ograniczenia:** Tekst pisze wyłącznie Kasia, Rinvo nie pisze go za nią; Nie uruchamiać w tym tygodniu (Kasia odsłuchuje starą bazę); Obie wersje muszą informować o wirtualnej asystentce i nagrywaniu; Nie uruchamiać w dniach 19–23.10 (urlop Kasi); Wybór wersji należy do Kasi
  > Kasia (l. 58) ✅: „Puśćcie to na dwa dni albo na dwa miasta, Toruń i Włocławek, a ja sama wybiorę, którą zostawiamy.”
  > Kasia (l. 58) ✅: „Tekst napiszę ja. W tym tygodniu tego nie puszczajcie, bo odsłuchuję starą bazę i wszystko mi się zleje.”
  > Kasia (l. 58) ✅: „Druga krótsza, ale dalej ma mówić, że jest wirtualną asystentką i że rozmowa jest nagrywana.”
  > Marek (l. 56) ✅: „Mogę po callu zobaczyć, czy sam początek da się skrócić, żeby szybciej doszła do pytania.”
  > Marek (l. 60) ✅: „Tekstu za ciebie nie piszę.”

#### A16 · Uruchomić walidację świeżych leadów po otrzymaniu pliku
`task` · `waiting_on_client`  
Kasia wyśle plik ze świeżymi leadami z ostatniego miesiąca (strona i Facebook), najpewniej w poniedziałek. Wystarczy numer telefonu i miasto (Toruń lub Włocławek), wtedy można uruchamiać.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-12 („Powiedzmy poniedziałek.”)
- **Warunek:** Otrzymanie pliku od Kasi.
- **Zatwierdza:** Kasia Malinowska
- **Zastępuje:** Piątek (Kasia nie obiecuje)
- **Ograniczenia:** Bez pliku nic nie uruchamiać; Nie wysyłać wzoru pliku; Wystarczy numer i miasto; Nie uruchamiać w dniach 19–23.10
  > Kasia (l. 134) ✅: „Powiedzmy poniedziałek.”
  > Kasia (l. 134) ✅: „I nie przysyłaj mi wzoru pliku.”
  > Kasia (l. 134) ✅: „Jak będzie numer i to, czy Toruń, czy Włocławek, to puszczajcie.”
  > Marek (l. 136) ✅: „Bez pliku nic nie puszczam.”

#### A19 · Czekać na przypadek przeglądu zakwalifikowanego jako lead sprzedażowy
`bug` · `waiting_on_client`  
Ola dostała mail po walidacji: klient chciał umówić przegląd, a u niej trafiło to jako lead sprzedażowy. Nie wiadomo, czy agent źle to zakwalifikował, czy Ola nie doczytała. Kasia prześle sprawę, jeśli Ola ją znajdzie.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Kasia przesyła sprawę znalezioną przez Olę.
- **Ograniczenia:** Nie zgadywać, która to kampania; Nie ruszać bez wiadomości od Kasi; Nie kontaktować się z Olą
  > Kasia (l. 138) ✅: „Wczoraj dostała taki mail i dopiero na samym dole przeczytała, że pan chciał umówić przegląd.”
  > Kasia (l. 138) ✅: „Jak nie, to nie zgadujcie, która to kampania.”
  > Marek (l. 140) ✅: „Bez tego nie ruszam.”

#### A31 · Czekać na decyzję w sprawie SMS-ów po dwóch nieudanych próbach
`feature_request` · `waiting_on_client`  
Funkcja jest technicznie możliwa, ale SMS-y są płatne osobno. Uruchomienie wymaga zgody Pawła na koszt, a treść przygotuje Kasia.
- **Warunek:** Zgoda Pawła na koszt i treść od Kasi.
- **Zatwierdza:** Paweł
- **Ograniczenia:** Treść pisze Kasia
- **Zależy od:** A30
  > Kasia (l. 192) ✅: „Jak bot dwa razy nie dodzwoni się do kogoś, to czy nie mógłby wysłać SMS-a?”
  > Kasia (l. 196) ✅: „Przyślij cenę. Wszystko, co kosztuje, i tak musi zatwierdzić Paweł. Treść napiszę sama, tak jak ze wstępem.”

#### A33 · Wysłać zaproszenie na spotkanie z Pawłem po potwierdzeniu Kasi
`task` · `waiting_on_client`  
Propozycja: czwartek 15.10 o 10:00, 30 minut. Plan: pokazać, co mamy, ustalić, czego Pawłowi brakuje, pokazać przykład z Peugeotem 208 i zapytać o zgodę na nazwę firmy. Zaproszenie wysyłamy dopiero po potwierdzeniu od Kasi.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-15 („przyszły czwartek o dziesiątej”)
- **Warunek:** Kasia potwierdza termin z Pawłem.
- **Zatwierdza:** Kasia Malinowska (potwierdzenie terminu)
- **Wersja ostateczna:** 2026-10-15, 10:00
- **Ograniczenia:** Nie wysyłać zaproszenia przed potwierdzeniem od Kasi
- **Zależy od:** A13
  > Kasia (l. 208) ✅: „Zaproponuj przyszły czwartek o dziesiątej, on wtedy jest w Toruniu. Ja mu to przekażę i potwierdzę.”
  > Marek (l. 210) ✅: „Czwartek, piętnastego, dziesiąta. Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.”
  > Kasia (l. 212) ✅: „I na tym spotkaniu możesz pokazać tę 208.”

## Ryzyka klienta (notatka do CRM)

_Cel: CRM, notatka na koncie klienta_

#### A32 · Ryzyko: konkurencja VoiceDesk
`risk` · `no_action`  
VoiceDesk zaproponował Pawłowi ofertę rzekomo o ok. 30% tańszą i z integracją z CRM dealera. Paweł jest zainteresowany głównie integracją. Rinvo nie ma integracji i nie obiecuje jej w tym kwartale.
- **Ograniczenia:** Nie obiecywać integracji z CRM w tym kwartale
  > Kasia (l. 200) ✅: „Powiedzieli, że są tańsi i że łączą się z systemem, więc leady same wpadają handlowcom.”
  > Marek (l. 206) ✅: „Integracji z waszym systemem teraz nie mamy i nie chcę obiecywać, że będzie w tym kwartale.”

## Wstrzymane: nie wracać bez sygnału klienta

_Cel: CRM, notatka na koncie klienta_

#### A14 · Wstrzymać przesunięcie prób na porę obiadową
`config_change` · `on_hold`  
Na starej bazie najwięcej osób odbierało około 12–13 i po 17. Pomysł przesunięcia pierwszej próby na porę obiadową czeka na wyniki ze świeżych leadów.
- **Warunek:** Najpierw wyniki na świeżych leadach i sygnał od Kasi.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie zmieniać harmonogramu prób teraz
  > Marek (l. 124) ✅: „Wtedy moglibyśmy przesunąć próby tak, żeby pierwsza szła w przerwie obiadowej.”
  > Kasia (l. 126) ✅: „Najpierw zobaczmy świeże.”
  > Marek (l. 128) ✅: „Jasne, zostawiam.”

#### A20 · Wstrzymać zmianę maila do handlowców (model i salon na górze)
`feature_request` · `on_hold`  
Kasia chce, żeby mail po walidacji miał model i salon na górze, a nie tylko transkrypcję. Temat jest wstrzymany do czasu uruchomienia świeżych leadów; Kasia sama do niego wróci.
- **Warunek:** Uruchomienie świeżych leadów i sygnał od Kasi.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie w tym tygodniu; Nie pisać do Oli, wszystko ustalać z Kasią; Nie przypominać
  > Kasia (l. 142) ✅: „A co do samego maila: model i salon na górze, żeby nie musieli szukać w tej ścianie.”
  > Kasia (l. 142) ✅: „Wrócimy do tego, jak pójdą świeże leady.”
  > Marek (l. 144) ✅: „I do Oli nie piszę, ustalam wszystko z tobą.”

#### A25 · Wstrzymać agenta po godzinach do sygnału Kasi
`feature_request` · `on_hold`  
Planowany zakres: jeden agent na wszystkie numery po zamknięciu salonu. Sprzedaż jak w walidacji (lead). Serwis: imię, telefon, model, salon, opis usterki, bez pytania o VIN, rano oddzwania BOK. Części jak serwis, z prośbą o przygotowanie VIN na rano. Assistance: tylko podać numer marki. Sprawy, których nie da się przypisać, trafiają do BOK. Temat wraca wyłącznie, gdy Kasia sama to powie.
- **Termin:** bez daty („Nie w tym miesiącu.”)
- **Warunek:** Kasia sama zgłosi powrót do tematu.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie w tym miesiącu; Nie przypominać ani nie wracać z własnej inicjatywy; Nie wierzyć wiadomościom typu „Kasia mówiła, że od wtorku”, tylko odpisać, że czekamy na Kasię
  > Kasia (l. 168) ✅: „Jak salon jest zamknięty, ma odbierać jeden agent, na wszystkie numery.”
  > Kasia (l. 176) ✅: „Jak sama nie powiem, że wracamy do tematu, to nie wracamy.”
  > Marek (l. 178) ✅: „A jak ktoś napisze, że od wtorku, odpiszę, że czekam na ciebie.”

#### A35 · Wstrzymać szkolenie handlowców do terminu od Kasi
`task` · `on_hold`  
15-minutowe szkolenie online ze statusów. Ma się odbyć dopiero po starcie świeżych leadów, a termin ustala Kasia.
- **Warunek:** Start świeżych leadów i termin podany przez Kasię.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie wcześniej niż po starcie świeżych leadów; Termin ustala Kasia
  > Kasia (l. 220) ✅: „Ściągę tak. Szkolenie dopiero, jak pójdą świeże, nie wcześniej, bo zapomną. Termin ustalę ja.”

## Informacje i sprawy bez działania

_Cel: CRM, notatka na koncie klienta_

#### A03 · Nie szukać przypadku z powtórnym pytaniem o model
`bug` · `no_action`  
Ola zgłosiła rozmowę, w której asystentka przestała reagować na klientkę i drugi raz zapytała o model. Nie ma nagrania ani numeru, więc Rinvo nie jest w stanie znaleźć tej rozmowy.
- **Ograniczenia:** Nie zgadywać, która to rozmowa
  > Kasia (l. 38) ✅: „W drugiej asystentka w środku rozmowy przestała odpowiadać na to, co klientka mówi, i drugi raz zapytała o model.”
  > Marek (l. 60) ✅: „A tej drugiej sytuacji, gdzie pyta drugi raz o model, bez nagrania nie znajdę.”

#### A12 · Wyniki na starej bazie: lead z urlopu to nie odmowa
`info` · `no_action`  
Wyniki: 70 numerów, 41 odebranych, 23 pełne rozmowy, 9 zainteresowanych, w tym jedna osoba z prośbą o kontakt po urlopie, czyli lead, a nie odmowa. Paweł, widząc 9 na 70, chciał wszystko wyłączyć. Kasia tłumaczy, że była to stara, martwa baza.
- **Ograniczenia:** Nie traktować prośby „oddzwońcie po urlopie” jako „niezainteresowany”
  > Kasia (l. 110) ✅: „Siedemdziesiąt numerów, odebrało czterdzieści jeden.”
  > Kasia (l. 110) ✅: „To jest lead, nie odmowa.”
  > Kasia (l. 114) ✅: „Paweł zobaczył tylko te dziewięć na siedemdziesiąt i chciał wszystko wyłączyć.”

## Szkice wiadomości (do zatwierdzenia)

- **D01** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Poprawione: adres we Włocławku i godziny” · wysłać: Po wprowadzeniu poprawek, planowo 2026-10-06. Bez nagrania testowego. · [drafts/D01-kasia-malinowska.md](drafts/D01-kasia-malinowska.md)
- **D02** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Przypomnienie: dwie wersje wstępu” · wysłać: Tylko jeśli do końca czwartku 2026-10-08 nie przyjdą obie wersje. Wysłać raz, 2026-10-09. · [drafts/D02-kasia-malinowska.md](drafts/D02-kasia-malinowska.md)
- **D03** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Plik ze świeżymi leadami” · wysłać: Tylko jeśli plik nie przyjdzie do końca poniedziałku 2026-10-12. Wysłać jeden raz, 2026-10-13, bez wzoru pliku. · [drafts/D03-kasia-malinowska.md](drafts/D03-kasia-malinowska.md)
- **D04** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Ponowne połączenia po rozłączeniu: przyczyna i rozliczenie” · wysłać: Po zdiagnozowaniu błędu i sprawdzeniu sposobu naliczania minut. Zdanie o odliczeniu tylko wtedy, gdy błąd po stronie Rinvo jest potwierdzony. · [drafts/D04-kasia-malinowska.md](drafts/D04-kasia-malinowska.md)
- **D05** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Cena SMS po nieudanych próbach połączenia” · wysłać: Do piątku 2026-10-09. Tylko cena, bez przykładowej treści. · [drafts/D05-kasia-malinowska.md](drafts/D05-kasia-malinowska.md)
- **D06** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Ściąga: co znaczą statusy” · wysłać: Gdy ściąga będzie gotowa (bez konkretnego terminu). · [drafts/D06-kasia-malinowska.md](drafts/D06-kasia-malinowska.md)
- **D07** do: Michał (Rinvo) · „Korekta faktury za wrzesień – Grupa Auto Tama” · wysłać: 2026-10-06 (dziś). · [drafts/D07-michal.md](drafts/D07-michal.md)
- **D08** do: Paweł (Grupa Auto Tama) · „Rinvo – spotkanie 15.10, godz. 10:00” · wysłać: Dopiero po potwierdzeniu terminu przez Kasię. Nie wcześniej. · [drafts/D08-pawel.md](drafts/D08-pawel.md)

## Założenia przyjęte przy analizie

- „Do czwartku” (teksty wstępu) czytam jako 2026-10-08 włącznie, więc jedyne przypomnienie idzie 2026-10-09.
- „Powiedzmy poniedziałek” (plik ze świeżymi leadami) to 2026-10-12, więc jedyny mail-przypomnienie idzie 2026-10-13.
- „W tym tygodniu” (cena SMS) czytam jako do piątku 2026-10-09.
- „W przyszłym tygodniu” (korekta faktury) to 12–16.10, termin ustawiony na 2026-10-16.
- „Przyszły czwartek” to 2026-10-15, co Marek potwierdził słowami „Czwartek, piętnastego”.
- „Adres i godziny dzisiaj” obejmuje zarówno godziny salonów podawane przez agenta, jak i godziny dzwonienia. Termin obu zmian: 2026-10-06.
- „Tydzień” w godzinach dzwonienia rozumiem jako poniedziałek–piątek.
- Wniosek z połączenia decyzji (nikt tego nie powiedział wprost): test wstępu może ruszyć najwcześniej 2026-10-12 i nie w dniach 19–23.10. Jeśli nie wystartuje przed 19.10, czeka do 26.10.
- Wniosek z połączenia decyzji: jeśli plik ze świeżymi leadami dotrze tak, że start wypadłby w dniach 19–23.10, walidacja czeka do powrotu Kasi.
- Nie przewidziano przypomnień o: sprawie przeglądu Oli, potwierdzeniu spotkania z Pawłem, numerach assistance, agencie po godzinach, szkoleniu i nowym mailu do handlowców, bo nic takiego nie ustalono.
- Sprawę przeglądu z maila Oli roboczo oznaczam jako bug. Nie wiadomo, czy to błąd agenta, czy Ola nie doczytała.
- Podwójnych połączeń było co najmniej 6, tyle znalazła Kasia. Dokładną liczbę musi ustalić Rinvo.
- Adres e-mail Pawła nie padł w rozmowie. Szkic zaproszenia trzeba zaadresować po potwierdzeniu przez Kasię.
- Godziny salonu w Toruniu w tygodniu nie zostały podane („Toruń bez zmian”), zmienia się tylko sobota na 9–15 dla obu salonów.
