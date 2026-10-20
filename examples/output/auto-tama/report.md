# Po rozmowie: Grupa Auto Tama, 2026-10-06

Źródło: `transkrypcja-spotkanie.md` · uczestnicy: Kasia Malinowska (Grupa Auto Tama, BDC), Marek Rewoliński (Rinvo)  
Pozycji: 42 · zabezpieczeń: 20 · szkiców: 8 · cytaty zweryfikowane: 131/131

> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.

## Podsumowanie

Call statusowy w sprawie walidacji leadów (Peugeot i Citroën, Toruń i Włocławek). Ustalono na dziś poprawki: adres salonu we Włocławku (Toruńska 120), sobotnie godziny salonów (do 15:00), godziny dzwonienia (pn–pt 9–19, sob 9–15), a także diagnozę dwóch błędów: ponownego połączenia po rozłączeniu w ciągu 3 sekund oraz niedziałającego filtra statusu „zainteresowany”. Na ruch klienta czekają: teksty do ręcznego testu A/B wstępu, plik ze świeżymi leadami (poniedziałek 12.10, jedno przypomnienie) i potwierdzenie spotkania z Pawłem 15.10 o 10:00. Opel, nowy format maila do handlowców, agent po godzinach i szkolenie handlowców są wstrzymane do sygnału od Kasi. Od 19 do 23.10 obowiązuje zamrożenie zmian. Dla konta są dwa ryzyka: konkurencja ze strony VoiceDesk (taniej, z integracją z CRM) i to, że Paweł chciał wyłączyć usługę.

## Zabezpieczenia (sprawdzić przed każdym działaniem)

- **G01** Nie uruchamiać testu wersji wstępu w bieżącym tygodniu (do: Do 2026-10-11 włącznie i do otrzymania obu tekstów od Kasi · zdejmuje: Kasia Malinowska)
  > Kasia (l. 58) ✅: „W tym tygodniu tego nie puszczajcie, bo odsłuchuję starą bazę i wszystko mi się zleje.”
- **G02** Tekst wstępu pisze i zatwierdza wyłącznie Kasia; Rinvo go nie pisze, a Paweł nie może go zatwierdzić (zdejmuje: Kasia Malinowska (nie Paweł))
  > Marek (l. 60) ✅: „Tekstu za ciebie nie piszę.”
  > Kasia (l. 228) ✅: „Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.”
- **G03** O tekstach wstępu przypomnieć Kasi tylko raz
  > Kasia (l. 58) ✅: „Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.”
- **G04** Nie zmieniać limitu pięciu prób (zdejmuje: Kasia Malinowska)
  > Kasia (l. 94) ✅: „Zostaw pięć. Nie kazałam schodzić do trzech.”
- **G05** Nie włączać Opla; nawet jeśli Paweł napisze, że kazał, najpierw zadzwonić do Kasi (do: Do decyzji Kasi po wynikach na świeżych leadach · zdejmuje: Kasia Malinowska (Paweł nie może zatwierdzić))
  > Marek (l. 132) ✅: „Opla nie włączam. Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.”
  > Kasia (l. 228) ✅: „Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.”
- **G06** Nie puszczać drugi raz starej bazy (zdejmuje: Kasia Malinowska)
  > Kasia (l. 134) ✅: „Starej bazy drugi raz nie puszczajcie.”
- **G07** Bez pliku ze świeżymi leadami niczego nie uruchamiać; nie wysyłać Kasi wzoru pliku; przypomnieć tylko jednym mailem (do: Do otrzymania pliku)
  > Kasia (l. 134) ✅: „Jak nie wyślę, napisz jeden mail, nie trzy. I nie przysyłaj mi wzoru pliku.”
  > Marek (l. 136) ✅: „Dobra. Bez pliku nic nie puszczam.”
- **G08** Nie zgadywać kampanii i nie ruszać sprawy przeglądu z maila Oli bez wiadomości od Kasi (do: Do przesłania przypadku przez Kasię · zdejmuje: Kasia Malinowska)
  > Kasia (l. 138) ✅: „Jak znajdzie, prześlę. Jak nie, to nie zgadujcie, która to kampania.”
  > Kasia (l. 240) ✅: „A tego przeglądu, co Ola ma w skrzynce, nie ruszajcie bez wiadomości ode mnie.”
- **G09** Nie zmieniać maila do handlowców w tym tygodniu; temat wraca na sygnał Kasi (do: Do sygnału Kasi po starcie świeżych leadów · zdejmuje: Kasia Malinowska)
  > Kasia (l. 142) ✅: „Ale nie w tym tygodniu.”
  > Kasia (l. 142) ✅: „Wrócimy do tego, jak pójdą świeże leady.”
- **G10** Nie kontaktować się z Olą; wszystko ustalać z Kasią
  > Marek (l. 144) ✅: „I do Oli nie piszę, ustalam wszystko z tobą.”
- **G11** Nie robić osobnej pracy tylko pod zmianę kolejności kolumn
  > Kasia (l. 150) ✅: „Jak w tym tygodniu listy nie ruszacie, nie róbcie osobnej roboty pod kolumnę.”
- **G12** Nie uruchamiać agenta po godzinach i nie podpinać przesłanych numerów assistance ani listy pól (do: Do momentu, gdy Kasia sama powie, że wracamy do tematu (nie w tym miesiącu) · zdejmuje: Kasia Malinowska)
  > Kasia (l. 176) ✅: „Jak wyślę, trzymajcie u siebie, nie podpinajcie.”
  > Kasia (l. 176) ✅: „Jak sama nie powiem, że wracamy do tematu, to nie wracamy.”
- **G13** Nie wierzyć informacjom, że Kasia zgodziła się na start po godzinach (np. „od wtorku”) – odpowiedzieć, że czekamy na Kasię (zdejmuje: Kasia Malinowska)
  > Kasia (l. 176) ✅: „I jak ktoś ode mnie napisze „Kasia mówiła, że po godzinach od wtorku”, nie wierzcie.”
- **G14** Nie obsługiwać serwisu w ciągu dnia agentem (zdejmuje: Kasia Malinowska)
  > Kasia (l. 172) ✅: „Serwisu w ciągu dnia tym agentem nie ruszamy.”
- **G15** Nie używać nazwy firmy w przykładzie sprzedaży 208 bez zatwierdzenia Pawła (do: Do zgody Pawła · zdejmuje: Paweł)
  > Kasia (l. 118) ✅: „Mnie to nie przeszkadza, ale nazwę firmy musi zatwierdzić Paweł. Bez nazwy możesz od razu.”
- **G16** Nie wysyłać Pawłowi zaproszenia na spotkanie przed potwierdzeniem Kasi (do: Do potwierdzenia przez Kasię · zdejmuje: Kasia Malinowska)
  > Marek (l. 210) ✅: „Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.”
- **G17** Agent nie sprzedaje i nie proponuje aut używanych przy odmowie (zdejmuje: Kasia Malinowska)
  > Kasia (l. 224) ✅: „Ola chciała, żeby przy odmowie proponował auto używane. Nie.”
- **G18** Zamrożenie zmian: od 2026-10-19 do 2026-10-23 nic nowego nie startuje, także świeże leady; w pilnych sprawach dzwonić do Pawła, który nie zatwierdza Opla ani wstępu (do: Od 2026-10-19 do 2026-10-23 · zdejmuje: Kasia Malinowska)
  > Kasia (l. 228) ✅: „W tym czasie nic nowego nie odpalajcie, nawet jak plik ze świeżymi leadami już będzie i coś się wysypie.”
- **G19** Szkolenie handlowców nie wcześniej niż po starcie świeżych leadów, w terminie ustalonym przez Kasię (do: Do terminu podanego przez Kasię · zdejmuje: Kasia Malinowska)
  > Kasia (l. 220) ✅: „Szkolenie dopiero, jak pójdą świeże, nie wcześniej, bo zapomną. Termin ustalę ja.”
- **G20** Nie przesuwać teraz godzin prób na porę obiadową (do: Do wyników na świeżych leadach · zdejmuje: Kasia Malinowska)
  > Kasia (l. 126) ✅: „Może, ale nie teraz.”

## Ostrzeżenia walidacji

- **A02**: termin opisany słownie („w tym tygodniu tego nie puszczajcie”) bez daty
- **A17**: termin opisany słownie („Powiedzmy poniedziałek”) bez daty
- **A24**: pozycja warunkowa oznaczona jako do zrobienia teraz
- **A31**: pozycja warunkowa oznaczona jako do zrobienia teraz
- **A32**: pozycja warunkowa oznaczona jako do zrobienia teraz
- **D07**: szkic używa względnej daty („dziś”)

## Terminy (kalendarz i przypomnienia)

- **2026-10-06** · A06 Poprawić adres salonu we Włocławku w bazie wiedzy
- **2026-10-06** · A07 Zaktualizować godziny salonów podawane przez agenta
- **2026-10-06** · A08 Napisać Kasi, że adres i godziny są poprawione · Nie wysyłać nagrania testowego – Kasia sama puści test
- **2026-10-06** · A09 Zdiagnozować ponowne połączenia po rozłączeniu w ciągu 3 sekund · Przy okazji nie zmieniać limitu pięciu prób
- **2026-10-06** · A11 Zmienić godziny dzwonienia agenta · W niedzielę bez połączeń
- **2026-10-06** · A22 Naprawić filtr statusu „zainteresowany” na liście kontaktów
- **2026-10-06** · A28 Przekazać Michałowi prośbę o korektę faktury za wrzesień
- **2026-10-09** · A03 Przypomnieć Kasi raz o tekstach wstępu · Przypomnieć tylko raz
- **2026-10-09** · A33 Wysłać Kasi cenę SMS-ów · Bez przykładowego tekstu – treść pisze Kasia
- **2026-10-13** · A18 Wysłać jedno przypomnienie o pliku ze świeżymi leadami · Jeden mail, nie trzy; Nie dołączać wzoru pliku
- **2026-10-15** · A37 Spotkanie z Pawłem 15.10 o 10:00 – czekać na potwierdzenie · Zaproszenie wysłać dopiero po potwierdzeniu Kasi
- **2026-10-16** · A29 Wystawić korektę faktury za wrzesień

## Nie robić (zakazy i odrzucone prośby)

_Cel: lista zabezpieczeń konta klienta_

#### A10 · Nie zmniejszać limitu prób do trzech
`config_change` · `do_not_do`  
Limit pięciu prób zostaje. Kasia nie prosiła o zejście do trzech, tylko wspomniała, że ktoś ją o to pytał.
- **Zatwierdza:** Kasia Malinowska
- **Wersja ostateczna:** Limit 5 prób
- **Ograniczenia:** Limit prób pozostaje 5
  > Marek (l. 92) ✅: „Limitu pięciu prób przy okazji nie ruszam, to inna sprawa.”
  > Kasia (l. 94) ✅: „Zostaw pięć. Nie kazałam schodzić do trzech.”
  > Marek (l. 96) ✅: „No, zostaje pięć.”

#### A16 · Nie włączać Opla
`config_change` · `do_not_do`  
Opel nie jest podpinany, dopóki nie będzie wyników ze świeżych leadów z ostatniego miesiąca. Jeśli Paweł napisze, że kazał włączyć, najpierw zadzwonić do Kasi.
- **Warunek:** Do decyzji Kasi po wynikach na świeżych leadach
- **Zatwierdza:** Kasia Malinowska (nie Paweł)
- **Ograniczenia:** Nawet na polecenie Pawła nie włączać – najpierw telefon do Kasi; Paweł nie zatwierdza Opla
  > Kasia (l. 130) ✅: „Peugeot i Citroën zostają, Opel czeka, aż zobaczymy wyniki na leadach z ostatniego miesiąca.”
  > Marek (l. 132) ✅: „Opla nie włączam. Nawet jak Paweł napisze, że kazał, to najpierw zadzwonię do ciebie, a nie będę tego klikał.”
  > Kasia (l. 228) ✅: „Ale Paweł nie zatwierdza ani Opla, ani tekstu wstępu. To czeka na mnie.”

#### A19 · Nie puszczać drugi raz starej bazy
`task` · `do_not_do`  
Stara baza leadów sprzed 2–3 miesięcy nie może być ponownie wykorzystana w kampanii.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie puszczać starej bazy ponownie
  > Kasia (l. 134) ✅: „Starej bazy drugi raz nie puszczajcie.”
  > Marek (l. 136) ✅: „Starej bazy drugi raz nie puszczam i wzoru ci nie wysyłam.”

#### A27 · Nie obsługiwać serwisu w ciągu dnia agentem
`feature_request` · `do_not_do`  
Agent nie obsługuje serwisu w godzinach pracy salonu. To osobny temat, ewentualnie za pół roku.
- **Zatwierdza:** Kasia Malinowska
  > Kasia (l. 172) ✅: „Serwisu w ciągu dnia tym agentem nie ruszamy. To osobny temat, może za pół roku.”

#### A40 · Nie dodawać proponowania aut używanych przy odmowie
`feature_request` · `do_not_do`  
Prośba Oli została odrzucona. Agent nie sprzedaje – gdy ktoś mówi „już kupiłem” albo „rozmyśliłem się”, agent dziękuje i kończy rozmowę.
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Agent nie sprzedaje
  > Kasia (l. 224) ✅: „Ola chciała, żeby przy odmowie proponował auto używane. Nie.”
  > Marek (l. 226) ✅: „Jasne, niech nie sprzedaje. Jak ktoś mówi, że kupił, dziękujemy i koniec. Używanych nie dokładam.”

#### A42 · Nie uruchamiać niczego nowego w czasie urlopu Kasi
`task` · `do_not_do`  
Od 19 do 23.10.2026 nic nowego nie startuje, nawet jeśli plik ze świeżymi leadami już będzie. W pilnej sytuacji dzwonić do Pawła, ale Paweł nie zatwierdza Opla ani tekstu wstępu.
- **Termin:** bez daty („od dziewiętnastego do dwudziestego trzeciego”)
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Zamrożenie zmian 2026-10-19–2026-10-23; W pilnych sprawach kontakt z Pawłem; Paweł nie zatwierdza Opla ani tekstu wstępu
  > Kasia (l. 228) ✅: „W tym czasie nic nowego nie odpalajcie, nawet jak plik ze świeżymi leadami już będzie i coś się wysypie.”
  > Marek (l. 230) ✅: „Dobra. Tydzień od dziewiętnastego nic nowego nie startuje. Jak się pali, dzwonię do Pawła, ale Opel i wstęp czekają na ciebie.”

## Zgłoszenia błędów (dla zespołu technicznego)

_Cel: issue tracker (np. Linear/Jira)_

#### A06 · Poprawić adres salonu we Włocławku w bazie wiedzy
`bug` · `scheduled`  
Agent podaje stary adres przy ul. Kapitulnej, a salon od sierpnia jest przy ul. Toruńskiej 120. To błąd po stronie Rinvo (nieaktualna baza wiedzy).
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („poprawię dzisiaj”)
- **Wersja ostateczna:** Włocławek: ul. Toruńska 120
  > Kasia (l. 78) ✅: „A my od sierpnia jesteśmy na Toruńskiej.”
  > Marek (l. 80) ✅: „O, to jest nasz błąd, ewidentnie nieaktualna baza wiedzy. Podaj mi nowy adres, poprawię dzisiaj.”
  > Kasia (l. 82) ✅: „Toruńska 120.”

#### A09 · Zdiagnozować ponowne połączenia po rozłączeniu w ciągu 3 sekund
`bug` · `scheduled`  
Zgodnie z ustawieniem agent nie powinien dzwonić drugi raz tego samego dnia do osoby, która rozłączyła się w ciągu 3 sekund. 5.10 zdarzyło się to 6 razy w tej samej kampanii po południu. Pierwszy przypadek był o 16:40, numer kończy się na 14.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („zaraz po rozmowie”)
- **Ograniczenia:** Przy okazji nie zmieniać limitu pięciu prób
  > Kasia (l. 90) ✅: „Ustawialiśmy, że jak ktoś się rozłączy w ciągu trzech sekund, to agent nie dzwoni do niego drugi raz tego samego dnia. Wczoraj i tak zadzwonił.”
  > Kasia (l. 90) ✅: „Pierwszy był o 16:40, numer kończy się na 14, słyszałam obie próby jedna po drugiej.”
  > Marek (l. 242) ✅: „Drugi telefon i filtr biorę zaraz po rozmowie, adres i godziny dzisiaj.”

#### A22 · Naprawić filtr statusu „zainteresowany” na liście kontaktów
`bug` · `scheduled`  
Filtr „zainteresowany” nie zawęża listy i pokazuje także nieodebrane połączenia i odpowiedzi „kupiłem gdzie indziej”. Filtr daty działa.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („zaraz po rozmowie”)
  > Kasia (l. 146) ✅: „Na liście kontaktów filtr „zainteresowany” też nie zawęża.”
  > Marek (l. 148) ✅: „Widzę: data działa, a filtr statusu nie. To sprawdzę u nas po callu.”

## Zmiany konfiguracji agenta

_Cel: panel konfiguracji agenta (zmiana po zatwierdzeniu)_

#### A07 · Zaktualizować godziny salonów podawane przez agenta
`config_change` · `scheduled`  
W bazie wiedzy ustawić sobotę 9:00–15:00 dla obu salonów. Włocławek w tygodniu bez zmian (9:00–18:00), pozostałe godziny Torunia bez zmian.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („poprawię razem z adresem”)
- **Wersja ostateczna:** Oba salony: sobota 9:00–15:00; Włocławek pn–pt 9:00–18:00
- **Zastępuje:** Godziny bez zmian: sobota 9:00–14:00, Toruń bez zmian
  > Kasia (l. 82) ✅: „Godziny bez zmian, w tygodniu dziewiąta–osiemnasta, sobota dziewiąta–czternasta. Toruń bez zmian.”
  > Marek (l. 234) ✅: „A co z godzinami salonu, które agent podaje klientom? Też mam zmienić na piętnastą?”
  > Kasia (l. 236) ✅: „Tak, dla obu salonów. Dobrze, że pytasz.”
  > Marek (l. 238) ✅: „Dobra, poprawię razem z adresem.”

#### A11 · Zmienić godziny dzwonienia agenta
`config_change` · `scheduled`  
Skrócić okno dzwonienia, bo klient skarżył się na telefon o 19:30, a gdy ktoś oddzwania po zamknięciu salonu, nikt nie odbiera. W niedzielę agent nie dzwoni.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („Zmienię po callu”)
- **Wersja ostateczna:** Pn–pt 9:00–19:00, sobota 9:00–15:00, niedziela bez połączeń
- **Zastępuje:** Pn–sob 9:00–20:00 (obecne ustawienie); Pn–pt 9:00–19:00, sobota 9:00–14:00
- **Ograniczenia:** W niedzielę bez połączeń
  > Marek (l. 100) ✅: „Tak, od dziewiątej do dwudziestej, od poniedziałku do soboty.”
  > Marek (l. 104) ✅: „Dobra. Tydzień dziewiąta–dziewiętnasta, sobota dziewiąta–czternasta. Zmienię po callu.”
  > Kasia (l. 232) ✅: „Sobotę jednak zostaw do piętnastej, nie do czternastej.”
  > Marek (l. 234) ✅: „Czyli sobota dziewiąta–piętnasta, tydzień dziewiąta–dziewiętnasta.”
  > Kasia (l. 106) ✅: „I w niedzielę oczywiście w ogóle.”

#### A24 · Przesunąć kolumnę nazwiska za status (tylko przy pracy nad listą)
`config_change` · `do_now`  
Na liście kontaktów nazwisko ma być zaraz po statusie. Zmianę zrobić tylko wtedy, gdy przy naprawie filtra i tak będzie się zmieniać tę listę.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Tylko jeśli naprawa filtra (A22) wymaga zmian w liście kontaktów
- **Ograniczenia:** Nie robić osobnej pracy pod kolumnę
- **Zależy od:** A22
  > Kasia (l. 150) ✅: „Na liście kontaktów chcę mieć nazwisko zaraz po statusie.”
  > Kasia (l. 150) ✅: „Jak w tym tygodniu listy nie ruszacie, nie róbcie osobnej roboty pod kolumnę.”
  > Marek (l. 152) ✅: „Jak się okaże, że problem z filtrem siedzi gdzie indziej, to kolumn osobno nie ruszam.”

## Zadania zespołu

_Cel: lista zadań właściciela_

#### A03 · Przypomnieć Kasi raz o tekstach wstępu
`task` · `scheduled`  
Jeśli do czwartku nie przyjdą obie wersje tekstu, wysłać Kasi jedno przypomnienie.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-09 („Jak do czwartku nie wyślę obu wersji, przypomnij mi”)
- **Warunek:** Brak obu wersji tekstu (klient: do czwartku 2026-10-08)
- **Ograniczenia:** Przypomnieć tylko raz
- **Zależy od:** A02
  > Kasia (l. 58) ✅: „Jak do czwartku nie wyślę obu wersji, przypomnij mi. Raz.”
  > Marek (l. 60) ✅: „Jak do czwartku nic nie przyjdzie, przypomnę.”

#### A08 · Napisać Kasi, że adres i godziny są poprawione
`task` · `scheduled`  
Po wprowadzeniu poprawek dać Kasi znać wiadomością. Nagrania testowego nie wysyłać, bo Kasia sprawdzi to sama.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („Tylko napisz, jak będzie poprawione”)
- **Warunek:** Po wprowadzeniu poprawek A06 i A07
- **Wersja ostateczna:** Tylko wiadomość o poprawce, bez nagrania testowego
- **Zastępuje:** Marek wysyła nagranie testowe
- **Ograniczenia:** Nie wysyłać nagrania testowego – Kasia sama puści test
- **Zależy od:** A06, A07
  > Marek (l. 84) ✅: „Wyślę ci potem nagranie testowe, żebyś usłyszała, że mówi dobrze.”
  > Kasia (l. 86) ✅: „Nie musisz mi wysyłać, puszczę sobie test sama. Tylko napisz, jak będzie poprawione.”
  > Marek (l. 88) ✅: „Dobra, napiszę.”

#### A14 · Wykorzystać przypadek sprzedaży Peugeota 208 jako przykład (bez nazwy)
`task` · `do_now`  
Lead z lipca, telefon bota w piątek, sprzedaż w sobotę. Można to od razu pokazywać bez nazwy firmy i bez nazwiska. O zgodę na użycie nazwy zapytać Pawła na spotkaniu.
- **Właściciel:** Marek Rewoliński
- **Zatwierdza:** Paweł (nazwa firmy)
- **Ograniczenia:** Bez nazwiska klienta; Bez nazwy firmy, dopóki nie zatwierdzi jej Paweł
- **Zależy od:** A37
  > Kasia (l. 114) ✅: „Jeden z tych dziewięciu, pan z Torunia, w sobotę przyjechał i kupił Peugeota 208.”
  > Kasia (l. 118) ✅: „Mnie to nie przeszkadza, ale nazwę firmy musi zatwierdzić Paweł. Bez nazwy możesz od razu.”
  > Marek (l. 120) ✅: „Dobra, na razie bez nazwy. O nazwę zapytam przy Pawle.”

#### A18 · Wysłać jedno przypomnienie o pliku ze świeżymi leadami
`task` · `scheduled`  
Jeśli w poniedziałek plik nie przyjdzie, wysłać Kasi jeden mail, bez wzoru pliku.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-13 („Jak w poniedziałek nic nie będzie, napiszę raz”)
- **Warunek:** Brak pliku (klient: poniedziałek 2026-10-12)
- **Ograniczenia:** Jeden mail, nie trzy; Nie dołączać wzoru pliku
- **Zależy od:** A17
  > Kasia (l. 134) ✅: „Jak nie wyślę, napisz jeden mail, nie trzy. I nie przysyłaj mi wzoru pliku.”
  > Marek (l. 136) ✅: „Jak w poniedziałek nic nie będzie, napiszę raz.”

#### A28 · Przekazać Michałowi prośbę o korektę faktury za wrzesień
`task` · `scheduled`  
Faktura za wrzesień została wystawiona na „Grupa Auto Tama sp. z o.o.”, a umowa jest z „Auto Tama Toruń sp. z o.o.”. Księgowa dealera (pani Grażyna) potrzebuje korekty, żeby ją zaksięgować.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-06 („przekażę mu dziś”)
  > Kasia (l. 180) ✅: „Faktura za wrzesień przyszła na „Grupa Auto Tama sp. z o.o.”, a umowa jest podpisana z „Auto Tama Toruń sp. z o.o.”.”
  > Marek (l. 182) ✅: „Faktury wystawia Michał, przekażę mu dziś.”

#### A29 · Wystawić korektę faktury za wrzesień
`task` · `scheduled`  
Korekta z prawidłowym nabywcą „Auto Tama Toruń sp. z o.o.”. Według Marka powinna dotrzeć do klienta w przyszłym tygodniu.
- **Właściciel:** Michał (Rinvo)
- **Termin:** 2026-10-16 („Korekta powinna przyjść w przyszłym tygodniu”)
- **Zależy od:** A28
  > Marek (l. 182) ✅: „Korekta powinna przyjść w przyszłym tygodniu.”

#### A30 · Sprawdzić sposób naliczania minut za krótkie połączenia
`task` · `do_now`  
Ustalić, czy minuty liczone są od pierwszej sekundy, czy za każdą rozpoczętą minutę. Klient pyta, czy połączenia rozłączone po 3 sekundach są liczone jako minuta.
- **Właściciel:** Marek Rewoliński
  > Kasia (l. 184) ✅: „Te połączenia, gdzie ktoś się rozłącza po trzech sekundach, też liczycie jako minutę?”
  > Marek (l. 186) ✅: „Szczerze, nie pamiętam, czy liczymy od pierwszej sekundy, czy za rozpoczętą minutę. Sprawdzę.”

#### A31 · Odjąć z rozliczenia podwójne połączenia, jeśli to błąd Rinvo
`task` · `do_now`  
Jeśli diagnoza potwierdzi, że ponowne połączenia po rozłączeniu w ciągu 3 sekund wynikały z błędu Rinvo, klient za nie nie płaci.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Jeśli podwójne połączenia okażą się błędem Rinvo (wynik A09)
- **Zależy od:** A09, A30
  > Marek (l. 186) ✅: „A jeśli te podwójne telefony to nasz błąd, to ich nie powinniście płacić. Odejmiemy je.”

#### A32 · Napisać Kasi, ile było podwójnych połączeń i co z błędem
`task` · `do_now`  
Przekazać Kasi liczbę podwójnych połączeń razem z informacją o przyczynie i stanie błędu, bo Paweł będzie o to pytał.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Po diagnozie błędu (A09) i sprawdzeniu naliczania (A30)
- **Zależy od:** A09, A30, A31
  > Kasia (l. 188) ✅: „To napisz mi, ile tego było, bo Paweł będzie pytał.”
  > Marek (l. 190) ✅: „Napiszę razem z informacją, co z tym błędem.”

#### A33 · Wysłać Kasi cenę SMS-ów
`task` · `scheduled`  
Podać koszt SMS-a wysyłanego po dwóch nieudanych próbach połączenia. Tylko cenę – treść SMS-a napisze Kasia.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-09 („cenę wyślę w tym tygodniu”)
- **Wersja ostateczna:** Tylko cena
- **Zastępuje:** Cena i przykładowy tekst SMS
- **Ograniczenia:** Bez przykładowego tekstu – treść pisze Kasia
  > Marek (l. 194) ✅: „Mogę ci przysłać cenę i przykładowy tekst.”
  > Kasia (l. 196) ✅: „Przyślij cenę. Wszystko, co kosztuje, i tak musi zatwierdzić Paweł. Treść napiszę sama, tak jak ze wstępem.”
  > Marek (l. 198) ✅: „Dobra, cenę wyślę w tym tygodniu.”

#### A38 · Przygotować i wysłać Kasi ściągę ze statusami
`task` · `do_now`  
Jedna strona dla handlowców z wyjaśnieniem statusów, m.in. „zainteresowany”, „oddzwonić”, „niezweryfikowany”.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Wysłać Kasi, nie bezpośrednio handlowcom
  > Marek (l. 218) ✅: „Mogę też przygotować jedną stronę ze ściągą, co znaczy który status.”
  > Kasia (l. 220) ✅: „Ściągę tak.”
  > Marek (l. 222) ✅: „Dobra. Ściągę ci wyślę, a szkolenie czeka na twój termin.”

## Backlog produktu (prośby o funkcje)

_Cel: tablica produktowa_

#### A05 · Zapisać w backlogu prośbę o testy A/B w panelu
`feature_request` · `do_now`  
Kasia chce sama ustawiać w panelu 2–3 warianty początku i przebiegu rozmowy (np. kolejność pytań), z automatycznym podziałem połączeń i wynikami po tygodniu. Za wynik uznaje większą liczbę pełnych rozmów (telefon, model, salon), a nie mniejszą liczbę rozłączeń.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie podawać terminu
  > Marek (l. 64) ✅: „Czyli testy A/B wbudowane w panel, które sama ustawiasz i sama czytasz wyniki.”
  > Marek (l. 68) ✅: „A to, żebyś mogła sama, zapisuję jako prośbę. Terminu ci teraz nie dam, ale pytam, bo nie jesteście pierwsi.”
  > Kasia (l. 70) ✅: „Ważne, ilu dochodzi do końca z telefonem, modelem i salonem.”

#### A23 · Zapisać w backlogu przejście z kafelka KPI do listy kontaktów
`feature_request` · `do_now`  
Kliknięcie w kafelek „zainteresowani” na dashboardzie walidacji ma prowadzić do listy tych osób. Takiej funkcji nigdy nie było – to coś innego niż błąd filtra.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie podawać terminu
  > Kasia (l. 146) ✅: „Klikam w tę dziewiątkę. Nic.”
  > Marek (l. 148) ✅: „A to, żeby kliknięcie w dziewiątkę przenosiło cię do tych ludzi, to osobna sprawa, tego po prostu nie ma.”
  > Marek (l. 148) ✅: „Na to klikanie terminu ci nie podam.”

#### A25 · Zapisać w backlogu cotygodniowy raport mailowy
`feature_request` · `do_now`  
Automatyczny mail do Pawła, np. w poniedziałek rano, z liczbą połączeń, odebranych i zainteresowanych. Takiej funkcji dziś nie ma, a pytają o nią także inni klienci.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie obiecywać terminu
  > Kasia (l. 154) ✅: „Da się, żeby to samo do niego przychodziło? W poniedziałek rano, na przykład.”
  > Marek (l. 156) ✅: „Raportu mailowego teraz nie mamy. Ale to jest coś, o co pyta więcej klientów, więc zapiszę. Nie obiecuję terminu.”

#### A36 · Zapisać potrzebę integracji z CRM dealera
`feature_request` · `do_now`  
Handlowczynie przepisują dane z maili do CRM („systemu”). Integracji dziś nie ma. Nie obiecywać jej w tym kwartale – omówić z Pawłem, czego mu faktycznie brakuje.
- **Właściciel:** Marek Rewoliński
- **Ograniczenia:** Nie obiecywać integracji w tym kwartale
  > Kasia (l. 204) ✅: „Bardziej go kręci to łączenie z systemem, bo dziewczyny teraz przepisują wszystko z maili.”
  > Marek (l. 206) ✅: „Integracji z waszym systemem teraz nie mamy i nie chcę obiecywać, że będzie w tym kwartale.”

## Czekamy na klienta

_Cel: przypomnienia w kalendarzu_

#### A02 · Uruchomić ręczny test dwóch wersji wstępu
`config_change` · `waiting_on_client`  
Test dwóch wersji wstępu: obecnej i krótszej, w której agent nadal mówi, że jest wirtualną asystentką i że rozmowa jest nagrywana. Test ma trwać dwa dni albo być rozdzielony na dwa miasta (Toruń i Włocławek). Wersję do zostawienia wybiera Kasia. Teksty pisze wyłącznie Kasia.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („w tym tygodniu tego nie puszczajcie”)
- **Warunek:** Po otrzymaniu od Kasi tekstów obu wersji (klient: do czwartku 2026-10-08); nie wcześniej niż po bieżącym tygodniu
- **Zatwierdza:** Kasia Malinowska (nie Paweł)
- **Wersja ostateczna:** Dwie wersje (obecna i krótsza, napisana przez Kasię), test przez 2 dni albo na 2 miasta, wybór należy do Kasi
- **Zastępuje:** Marek sam sprawdza po callu, czy da się skrócić początek, i wdraża jedną wersję
- **Ograniczenia:** Nie uruchamiać w tym tygodniu (do 2026-10-11), bo Kasia odsłuchuje starą bazę; Tekstu nie pisze Rinvo – pisze go Kasia; Obie wersje muszą zawierać informację o wirtualnej asystentce i nagrywaniu rozmowy; Nie uruchamiać w dniach 2026-10-19–2026-10-23 (urlop Kasi); Paweł nie może zatwierdzić tekstu wstępu
  > Marek (l. 56) ✅: „Mogę po callu zobaczyć, czy sam początek da się skrócić, żeby szybciej doszła do pytania.”
  > Kasia (l. 58) ✅: „Tylko ja chcę to zobaczyć na dwóch wersjach, a nie na jednej, którą wy uznacie za lepszą.”
  > Kasia (l. 58) ✅: „Puśćcie to na dwa dni albo na dwa miasta, Toruń i Włocławek, a ja sama wybiorę, którą zostawiamy.”
  > Marek (l. 60) ✅: „Jak przyślesz obie, puścimy i sobie wybierzesz. Tekstu za ciebie nie piszę.”

#### A17 · Uruchomić kampanię na świeżych leadach po otrzymaniu pliku
`task` · `waiting_on_client`  
Leady z ostatniego miesiąca (strona i Facebook). Kampanię można puścić, jeśli plik zawiera numer i informację, czy chodzi o Toruń, czy o Włocławek. Bez pliku nic nie uruchamiać.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („Powiedzmy poniedziałek”)
- **Warunek:** Po otrzymaniu pliku od Kasi (klient: poniedziałek 2026-10-12)
- **Ograniczenia:** Bez pliku nic nie puszczać; Nie wysyłać Kasi wzoru pliku; Wystarczy numer i miasto (Toruń/Włocławek); Nie uruchamiać w dniach 2026-10-19–2026-10-23
  > Kasia (l. 134) ✅: „Plik wyślę. Piątku nie obiecuję, bo zamykamy miesiąc. Powiedzmy poniedziałek.”
  > Kasia (l. 134) ✅: „Jak będzie numer i to, czy Toruń, czy Włocławek, to puszczajcie.”
  > Marek (l. 136) ✅: „Dobra. Bez pliku nic nie puszczam.”

#### A20 · Sprawdzić zgłoszenie przeglądu zakwalifikowanego jako lead sprzedażowy
`bug` · `waiting_on_client`  
Klient chciał umówić przegląd, a w CRM Oli wpadło to jako lead sprzedażowy. Nie wiadomo, czy agent źle zakwalifikował rozmowę, czy Ola nie doczytała maila. Sprawdzić dopiero, gdy Kasia prześle przypadek.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Po przesłaniu przez Kasię przypadku, który Ola ma w skrzynce
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie zgadywać, która to kampania; Nie ruszać bez wiadomości od Kasi; Nie kontaktować się z Olą
  > Kasia (l. 138) ✅: „Wczoraj dostała taki mail i dopiero na samym dole przeczytała, że pan chciał umówić przegląd. A u niej w systemie wpadło to jako lead sprzedażowy.”
  > Kasia (l. 138) ✅: „Jak znajdzie, prześlę. Jak nie, to nie zgadujcie, która to kampania.”
  > Marek (l. 140) ✅: „Jak mi tego nie prześlesz, to nie wiem, czy agent źle to zakwalifikował, czy ona nie doczytała. Bez tego nie ruszam.”

#### A34 · SMS po dwóch nieudanych próbach – czeka na decyzję Pawła
`feature_request` · `waiting_on_client`  
Paweł pyta o SMS do osób, do których bot dwa razy się nie dodzwonił. Technicznie da się to zrobić, ale SMS-y są płatne osobno, więc potrzebna jest zgoda Pawła. Treść pisze Kasia.
- **Warunek:** Po przesłaniu ceny (A33) i zatwierdzeniu kosztu przez Pawła
- **Zatwierdza:** Paweł
- **Ograniczenia:** Treść SMS pisze Kasia
- **Zależy od:** A33
  > Kasia (l. 192) ✅: „Jak bot dwa razy nie dodzwoni się do kogoś, to czy nie mógłby wysłać SMS-a?”
  > Marek (l. 194) ✅: „Technicznie się da, ale SMS-y kosztują osobno, za każdą wiadomość.”

#### A37 · Spotkanie z Pawłem 15.10 o 10:00 – czekać na potwierdzenie
`task` · `waiting_on_client`  
Półgodzinne spotkanie z Pawłem: pokazać, co ma Rinvo, ustalić, czego mu brakuje, i pokazać przypadek Peugeota 208. Kasia przekaże propozycję i potwierdzi termin. Zaproszenie wysłać dopiero po jej potwierdzeniu.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-15 („przyszły czwartek o dziesiątej”)
- **Warunek:** Po potwierdzeniu terminu przez Kasię
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Zaproszenie wysłać dopiero po potwierdzeniu Kasi
  > Kasia (l. 208) ✅: „Zaproponuj przyszły czwartek o dziesiątej, on wtedy jest w Toruniu. Ja mu to przekażę i potwierdzę.”
  > Marek (l. 210) ✅: „Czwartek, piętnastego, dziesiąta. Czekam na potwierdzenie od ciebie, zaproszenie wyślę dopiero wtedy.”
  > Kasia (l. 212) ✅: „I na tym spotkaniu możesz pokazać tę 208.”

## Ryzyka klienta (notatka do CRM)

_Cel: CRM, notatka na koncie klienta_

#### A13 · Ryzyko: Paweł chciał wyłączyć usługę
`risk` · `no_action`  
Paweł, patrząc tylko na 9 zainteresowanych z 70 numerów, chciał wszystko wyłączyć. Kasia go powstrzymała, tłumacząc, że to była stara baza.
  > Kasia (l. 114) ✅: „Paweł zobaczył tylko te dziewięć na siedemdziesiąt i chciał wszystko wyłączyć.”

#### A35 · Ryzyko: oferta konkurencji VoiceDesk
`risk` · `no_action`  
VoiceDesk był u Pawła z ofertą bota do leadów – podobno około 30% taniej i z integracją z CRM dealera. Paweł się zainteresował, a bardziej niż cena przyciąga go integracja.
  > Kasia (l. 200) ✅: „Powiedzieli, że są tańsi i że łączą się z systemem, więc leady same wpadają handlowcom. Paweł się tym zainteresował.”
  > Kasia (l. 204) ✅: „Paweł mówił coś o „jakieś trzydzieści procent taniej”, ale nie wiem, od czego.”

#### A41 · Ryzyko: wyłączenie agenta, jeśli zacznie sprzedawać
`risk` · `no_action`  
Kasia zapowiedziała, że wyłączy agenta, jeśli zacznie on sprzedawać.
  > Kasia (l. 224) ✅: „Jak zacznie sprzedawać, wyłączę go.”

## Wstrzymane: nie wracać bez sygnału klienta

_Cel: CRM, notatka na koncie klienta_

#### A15 · Wstrzymać przesunięcie prób na porę obiadową
`config_change` · `on_hold`  
Na starej bazie najwięcej osób odbierało około 12–13 i po 17, a przed 10 prawie nikt. Przesunięcie prób czeka na wyniki ze świeżych leadów.
- **Warunek:** Po wynikach na świeżych leadach
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie zmieniać teraz
- **Zależy od:** A17
  > Kasia (l. 122) ✅: „Najwięcej ludzi odbierało w okolicach dwunastej, trzynastej i po siedemnastej.”
  > Kasia (l. 126) ✅: „Może, ale nie teraz. To była stara baza, na świeżych może być inaczej. Najpierw zobaczmy świeże.”
  > Marek (l. 128) ✅: „Jasne, zostawiam.”

#### A21 · Wstrzymać zmianę maila do handlowców (model i salon na górze)
`feature_request` · `on_hold`  
Mail po walidacji to ściana tekstu z transkrypcją. Kasia chce mieć model i salon na górze. Temat wraca, gdy ruszą świeże leady – sygnał daje Kasia.
- **Warunek:** Kasia wróci do tematu, gdy ruszą świeże leady
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie w tym tygodniu; Nie pisać do Oli – ustalenia tylko z Kasią
  > Kasia (l. 142) ✅: „A co do samego maila: model i salon na górze, żeby nie musieli szukać w tej ścianie.”
  > Kasia (l. 142) ✅: „Wrócimy do tego, jak pójdą świeże leady.”
  > Marek (l. 144) ✅: „I do Oli nie piszę, ustalam wszystko z tobą.”

#### A26 · Wstrzymać agenta po godzinach
`feature_request` · `on_hold`  
Jeden agent na wszystkie numery, gdy salon jest zamknięty. Sprzedaż obsługiwana jak walidacja, z której powstaje lead. Serwis: bez umawiania, zebrać imię, telefon, model, salon i opis problemu, bez pytania o VIN, rano oddzwania BOK. Części: tak samo plus prośba o przygotowanie VIN na rano. Assistance: tylko podać numer danej marki. Pozostałe sprawy idą do BOK na rano. Temat wraca tylko na sygnał Kasi.
- **Termin:** bez daty („Nie w tym miesiącu”)
- **Warunek:** Kasia sama powie, że wracamy do tematu
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie w tym miesiącu; Numery assistance i listę pól po otrzymaniu tylko przechować, nie podpinać; Przesłanie numerów nie jest zielonym światłem; Nie wierzyć informacjom, że Kasia zgodziła się na start po godzinach
  > Kasia (l. 168) ✅: „Jak salon jest zamknięty, ma odbierać jeden agent, na wszystkie numery.”
  > Kasia (l. 176) ✅: „Jak sama nie powiem, że wracamy do tematu, to nie wracamy.”
  > Kasia (l. 176) ✅: „Numery assistance i listę pól wam wyślę, jak znajdę chwilę, ale to nie jest zielone światło.”
  > Marek (l. 178) ✅: „Dobra. Jak wyślesz numery, odłożę je i nic nie podepnę. W tym miesiącu tego nie ruszamy.”

#### A39 · Wstrzymać szkolenie handlowców do terminu od Kasi
`task` · `on_hold`  
Kwadrans online dla handlowców o statusach. Szkolenie dopiero po starcie świeżych leadów. Termin ustala Kasia.
- **Warunek:** Kasia poda termin po starcie świeżych leadów
- **Zatwierdza:** Kasia Malinowska
- **Ograniczenia:** Nie wcześniej niż po starcie świeżych leadów; Termin ustala Kasia
- **Zależy od:** A17
  > Kasia (l. 216) ✅: „Moglibyście im zrobić krótkie szkolenie? Kwadrans, online.”
  > Kasia (l. 220) ✅: „Szkolenie dopiero, jak pójdą świeże, nie wcześniej, bo zapomną. Termin ustalę ja.”

## Informacje i sprawy bez działania

_Cel: CRM, notatka na koncie klienta_

#### A01 · Odnotować uwagi do przebiegu rozmów walidacyjnych
`feedback` · `no_action`  
Według Kasi statystyki wyglądają dobrze, ale z nagrań słychać, że w połowie rozmowy ludzie orientują się, że rozmawiają z robotem, i rozłączają się albo odpowiadają byle jak. Agent nie robi przerwy na początku, więc klient nie może wejść mu w słowo. Końcowe „przepraszam, jest pani w aucie?” Kasia ocenia dobrze.
  > Kasia (l. 38) ✅: „Że w połowie rozmowy ludzie łapią, że to nie człowiek.”
  > Kasia (l. 54) ✅: „To „przepraszam” jest dobre. Złe jest to, że wcześniej nie ma żadnej przerwy, żebym mogła wejść jej w słowo.”

#### A04 · Odnotować zgłoszenie podwójnego pytania o model (bez nagrania)
`bug` · `no_action`  
Ola zgłosiła rozmowę, w której agent przestał reagować na odpowiedzi klientki i drugi raz zapytał o model. Nie ma nagrania ani numeru, więc nie da się tego zdiagnozować.
  > Kasia (l. 42) ✅: „Ola nie spisała numerów, powiedziała tylko „jakaś pani przed południem”.”
  > Marek (l. 60) ✅: „A tej drugiej sytuacji, gdzie pyta drugi raz o model, bez nagrania nie znajdę. Ola nie dała numeru.”

#### A12 · Wyniki kampanii na starej bazie
`info` · `no_action`  
Stara baza: 70 numerów, 41 odebranych, 23 pełne rozmowy, 9 zainteresowanych. Jedna osoba poprosiła o telefon po urlopie – to lead, a nie odmowa, i nie należy jej liczyć jako „niezainteresowanej”.
  > Kasia (l. 110) ✅: „Siedemdziesiąt numerów, odebrało czterdzieści jeden.”
  > Kasia (l. 110) ✅: „Pełne rozmowy, czyli potwierdzony telefon, model i salon: dwadzieścia trzy.”
  > Kasia (l. 110) ✅: „Jak wrzucicie ją w „niezainteresowany”, bo nie umówiła się na jutro, to źle to czytacie.”

## Szkice wiadomości (do zatwierdzenia)

- **D01** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Poprawione: adres salonu we Włocławku i godziny” · wysłać: 2026-10-06, po wprowadzeniu poprawek (A06, A07, A11) · [drafts/D01-kasia-malinowska.md](drafts/D01-kasia-malinowska.md)
- **D02** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Przypomnienie: teksty dwóch wersji wstępu” · wysłać: 2026-10-09, tylko jeśli do 2026-10-08 nie przyszły obie wersje; jednorazowo · [drafts/D02-kasia-malinowska.md](drafts/D02-kasia-malinowska.md)
- **D03** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Plik ze świeżymi leadami” · wysłać: 2026-10-13, tylko jeśli 2026-10-12 plik nie przyszedł; jeden mail, bez wzoru pliku · [drafts/D03-kasia-malinowska.md](drafts/D03-kasia-malinowska.md)
- **D04** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Podwójne połączenia po rozłączeniu – liczba i stan błędu” · wysłać: Po diagnozie błędu (A09) i sprawdzeniu naliczania minut (A30) · [drafts/D04-kasia-malinowska.md](drafts/D04-kasia-malinowska.md)
- **D05** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Cena SMS-ów po nieudanych próbach połączenia” · wysłać: Do 2026-10-09; tylko cena, bez przykładowego tekstu · [drafts/D05-kasia-malinowska.md](drafts/D05-kasia-malinowska.md)
- **D06** do: Michał (Rinvo) · „Korekta faktury za wrzesień – Auto Tama” · wysłać: 2026-10-06 · [drafts/D06-michal.md](drafts/D06-michal.md)
- **D07** do: Paweł (Grupa Auto Tama) · „Spotkanie Rinvo – 15.10.2026, 10:00” · wysłać: Dopiero po potwierdzeniu terminu przez Kasię · [drafts/D07-pawel.md](drafts/D07-pawel.md)
- **D08** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Ściąga: statusy leadów” · wysłać: Po przygotowaniu ściągi · [drafts/D08-kasia-malinowska.md](drafts/D08-kasia-malinowska.md)

## Założenia przyjęte przy analizie

- „Do czwartku” w sprawie tekstów wstępu odczytano jako 2026-10-08, a jednorazowe przypomnienie zaplanowano na 2026-10-09.
- „Powiedzmy poniedziałek” w sprawie pliku ze świeżymi leadami odczytano jako 2026-10-12, a jedyny mail przypominający zaplanowano na 2026-10-13.
- „W tym tygodniu” oznacza 2026-10-06–2026-10-11. Termin wysłania ceny SMS-ów ustawiono na piątek 2026-10-09.
- „W przyszłym tygodniu” dla korekty faktury oznacza 2026-10-12–2026-10-16; due_date ustawiono na 2026-10-16. Użyto sformułowania „powinna”, a nie obietnicy.
- „Przyszły czwartek” to 2026-10-15 (Marek potwierdził: „piętnastego”).
- „Zaraz po rozmowie”, „po callu” i „dzisiaj” odczytano jako 2026-10-06.
- Urlop Kasi „od dziewiętnastego do dwudziestego trzeciego” odczytano jako 2026-10-19–2026-10-23.
- Wniosek z połączenia ustaleń: test wstępu i kampanię na świeżych leadach można uruchomić najwcześniej 2026-10-12, a jeśli nie wystartują przed 2026-10-19, to dopiero po 2026-10-23.
- Wniosek: jeśli plik ze świeżymi leadami zawiera leady Opla, nie należy do nich dzwonić, bo Opel jest wstrzymany.
- Godziny Torunia w tygodniu nie padły w rozmowie; zmieniono tylko sobotę (do 15:00) dla obu salonów, reszta bez zmian.
- Nowe godziny dzwonienia (pn–pt 9–19, sob 9–15) przyjęto dla wszystkich kampanii walidacji.
- Potrzebę integracji z CRM zapisano jako prośbę do backlogu, choć Marek nie powiedział wprost „zapiszę”; potrzeba wynika z rozmowy o VoiceDesk.
- Odjęcie podwójnych połączeń z rozliczenia potraktowano jako warunkowe – tylko jeśli diagnoza potwierdzi błąd Rinvo.
- Prośbę Kasi „nie musisz mi wysyłać” (nagrania testowego) potraktowano jako ograniczenie zadania, a nie zakaz wymagający osobnej reguły.
- Numery assistance i listę pól do agenta po godzinach potraktowano jako część wstrzymanego tematu (A26), a nie osobne zadanie z oczekiwaniem na klienta.
