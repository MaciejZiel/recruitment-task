# Po rozmowie: Grupa Auto Tama, 2026-10-13

Źródło: `auto-tama-followup.md` · uczestnicy: Kasia Malinowska (Grupa Auto Tama, BDC), Tomek Wrona (Grupa Auto Tama, BDC), Marek Rewoliński (Rinvo)  
Pozycji: 17 · zabezpieczeń: 2 · szkiców: 4 · cytaty zweryfikowane: 34/34

> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.

## Podsumowanie

Na callu kontrolnym Kasia potwierdziła, że adres i godziny podawane przez agenta są poprawne. Przekazała też zmianę: od 17.10 soboty w obu salonach będą do 14:00. Zarówno godziny dzwonienia, jak i godziny podawane klientom trzeba przestawić w piątek 16.10, nie wcześniej. Rinvo poprawiło błąd z drugim telefonem po rozłączeniu. Podwójnych połączeń było 11, a nie 6, i zostaną odjęte z faktury za październik. Marek wyśle to Kasi mailem jeszcze dziś. Ustalono też: ręczne miesięczne podsumowanie liczb (pierwsze 2.11), zaproszenie dla Pawła na spotkanie w czwartek 15.10 o 10:00 w Toruniu, wysyłkę ściągi ze statusami do Oli oraz ocenę jej prośby o model i salon na górze maila po walidacji. Tomek, w imieniu Pawła, zlecił włączenie Opla we Włocławku od 19.10. Agent po godzinach czeka na numery assistance. Test wstępu ruszy od 21.10, jeśli Kasia wyśle teksty, a Marek przypomni jej o nich w poniedziałek 19.10.

## Zabezpieczenia (sprawdzić przed każdym działaniem)

- **G01** Nie przestawiać sobotnich godzin (dzwonienie i godziny podawane klientom) na 14:00 przed piątkiem 16.10 (do: 2026-10-16 (piątek) · zdejmuje: Kasia Malinowska)
  > Kasia (l. 32) ✅: „Przestaw w piątek, nie wcześniej, bo w tę sobotę jeszcze jest do piętnastej.”
- **G02** Na spotkaniu z Pawłem pokazywać przykład 208 bez nazwy firmy
  > Marek (l. 58) ✅: „Wyślę dziś. Pokażę tę 208, bez nazwy firmy.”

## Terminy (kalendarz i przypomnienia)

- **2026-10-13** · A05 Wysłać Kasi maila o podwójnych telefonach · Adresat: Kasia
- **2026-10-13** · A06 Puścić plik ze świeżymi leadami po otrzymaniu
- **2026-10-13** · A13 Wysłać Pawłowi zaproszenie na spotkanie
- **2026-10-15** · A14 Spotkanie z Pawłem w Toruniu – pokazać przykład 208 · Pokazać przykład 208 bez nazwy firmy
- **2026-10-16** · A01 Przestawić soboty na 14:00 w obu salonach · Nie przestawiać przed piątkiem 16.10; Dotyczy obu salonów; Zmienić obie rzeczy: godziny dzwonienia i godziny podawane klientom
- **2026-10-19** · A07 Włączyć walidację leadów Opla we Włocławku · Leady Opla w tym samym pliku, marka w osobnej kolumnie
- **2026-10-19** · A10 Przypomnieć Kasi o tekstach wstępu w poniedziałek · Przypomnieć tylko jeszcze raz (jedno przypomnienie)
- **2026-10-21** · A11 Uruchomić test wstępu od środy 21.10 · Nie wcześniej niż 21.10
- **2026-11-02** · A12 Przygotowywać ręczne miesięczne podsumowanie liczb · Do Kasi, mailem; Pierwszy dzień roboczy każdego miesiąca; Raport ręczny, nie automatyczny

## Zmiany konfiguracji agenta

_Cel: panel konfiguracji agenta (zmiana po zatwierdzeniu)_

#### A01 · Przestawić soboty na 14:00 w obu salonach
`config_change` · `scheduled`  
Zmienić sobotnie godziny dzwonienia oraz godziny, które agent podaje klientom, z 15:00 na 14:00, dla Torunia i Włocławka. Paweł skrócił soboty w salonach od 17.10. Zmianę trzeba zrobić w piątek 16.10, nie wcześniej.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-16 („w piątek szesnastego”)
- **Wersja ostateczna:** Sobota do 14:00 (dzwonienie i godziny podawane klientom) w obu salonach od 17.10, zmiana w piątek 16.10
- **Zastępuje:** Sobota do 15:00 (ustawione w czwartek 8.10)
- **Ograniczenia:** Nie przestawiać przed piątkiem 16.10; Dotyczy obu salonów; Zmienić obie rzeczy: godziny dzwonienia i godziny podawane klientom
  > Kasia (l. 32) ✅: „Paweł skrócił salonowi soboty, od siedemnastego znowu do czternastej.”
  > Kasia (l. 32) ✅: „Przestaw w piątek, nie wcześniej, bo w tę sobotę jeszcze jest do piętnastej.”
  > Marek (l. 34) ✅: „Dobra, w piątek szesnastego przestawiam obie rzeczy na czternastą.”

#### A07 · Włączyć walidację leadów Opla we Włocławku
`config_change` · `scheduled`  
Na polecenie Pawła, przekazane przez Tomka, włączyć Opla we Włocławku od poniedziałku 19.10. Leady Opla będą w tym samym pliku co pozostałe, a marka będzie w osobnej kolumnie.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-19 („Od poniedziałku dziewiętnastego”)
- **Zatwierdza:** Paweł (przekazane przez Tomka)
- **Ograniczenia:** Leady Opla w tym samym pliku, marka w osobnej kolumnie
  > Tomek (l. 64) ✅: „Paweł kazał włączyć Opla. Mówi, że adres już jest dobry, to nie ma na co czekać. Od poniedziałku dziewiętnastego.”
  > Marek (l. 66) ✅: „Opel we Włocławku od dziewiętnastego. Leady z Opla będą w tym samym pliku?”
  > Tomek (l. 68) ✅: „W tym samym, marka jest w osobnej kolumnie.”

## Zadania zespołu

_Cel: lista zadań właściciela_

#### A04 · Odjąć 11 podwójnych telefonów z faktury za październik
`task` · `do_now`  
Przy wystawianiu faktury za październik odjąć 11 podwójnych połączeń wynikających z błędu reguły trzech sekund.
- **Właściciel:** Rinvo (Marek Rewoliński)
- **Termin:** bez daty („z faktury za październik”)
- **Wersja ostateczna:** 11 połączeń
- **Zastępuje:** 6 połączeń
- **Zależy od:** A03
  > Marek (l. 38) ✅: „Podwójnych telefonów było jedenaście, nie sześć. Odejmiemy je z faktury za październik.”

#### A05 · Wysłać Kasi maila o podwójnych telefonach
`task` · `scheduled`  
Opisać na piśmie przyczynę błędu, datę poprawki, liczbę 11 podwójnych połączeń i odjęcie ich z faktury za październik. Paweł chce mieć to na piśmie.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-13 („dziś”)
- **Ograniczenia:** Adresat: Kasia
- **Zależy od:** A03, A04
  > Kasia (l. 40) ✅: „To napisz mi to mailem, Paweł będzie chciał na piśmie.”
  > Marek (l. 42) ✅: „Napiszę dziś.”

#### A10 · Przypomnieć Kasi o tekstach wstępu w poniedziałek
`task` · `scheduled`  
Na prośbę Tomka przypomnieć Kasi o tekstach wstępu w poniedziałek 19.10. Marek przypominał jej już w piątek.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-19 („w poniedziałek”)
- **Ograniczenia:** Przypomnieć tylko jeszcze raz (jedno przypomnienie)
- **Zależy od:** A09
  > Tomek (l. 80) ✅: „I przypomnijcie jej jeszcze raz o tych tekstach w poniedziałek, bo zapomni.”
  > Marek (l. 82) ✅: „Mogę.”

#### A12 · Przygotowywać ręczne miesięczne podsumowanie liczb
`task` · `scheduled`  
Raz w miesiącu wysyłać Kasi mailem podsumowanie: liczbę połączeń, odebranych i zainteresowanych. Termin to pierwszy dzień roboczy miesiąca. Automatycznego raportu nie ma, więc Marek będzie go robił ręcznie. Pierwsze podsumowanie 2.11.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-11-02 („Pierwszy drugiego listopada”)
- **Ograniczenia:** Do Kasi, mailem; Pierwszy dzień roboczy każdego miesiąca; Raport ręczny, nie automatyczny
  > Kasia (l. 52) ✅: „Paweł chce raz w miesiącu podsumowanie liczb: ile zadzwoniliśmy, ile odebrało, ilu zainteresowanych. Do mnie, mailem, pierwszego dnia roboczego miesiąca.”
  > Marek (l. 54) ✅: „Automatycznego raportu nie mamy, ale ręcznie raz w miesiącu zrobię. Pierwszy drugiego listopada.”

#### A13 · Wysłać Pawłowi zaproszenie na spotkanie
`task` · `scheduled`  
Wysłać na adres pawel@autotama.pl zaproszenie na spotkanie w czwartek 15.10 o 10:00 w Toruniu. Paweł potwierdził termin.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-13 („dziś”)
  > Kasia (l. 56) ✅: „I Paweł potwierdził czwartek, dziesiąta, w Toruniu. Wyślij mu zaproszenie, pawel@autotama.pl.”
  > Marek (l. 58) ✅: „Wyślę dziś. Pokażę tę 208, bez nazwy firmy.”

#### A14 · Spotkanie z Pawłem w Toruniu – pokazać przykład 208
`task` · `scheduled`  
Na spotkaniu w czwartek 15.10 o 10:00 w Toruniu Marek pokaże przykład „208” bez nazwy firmy.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-15 („czwartek, dziesiąta, w Toruniu”)
- **Ograniczenia:** Pokazać przykład 208 bez nazwy firmy
- **Zależy od:** A13
  > Marek (l. 58) ✅: „Wyślę dziś. Pokażę tę 208, bez nazwy firmy.”

#### A15 · Wysłać Oli ściągę ze statusami
`task` · `do_now`  
Ola prosiła, żeby wysłać jej ściągę ze statusami bezpośrednio na adres ola.nowak@autotama.pl. Marek ma ją prawie gotową.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Gdy ściąga będzie gotowa
- **Ograniczenia:** Wysłać bezpośrednio do Oli: ola.nowak@autotama.pl
  > Tomek (l. 84) ✅: „Prosiła, żebyście jej wysłali ściągę ze statusami bezpośrednio, ola.nowak@autotama.pl.”
  > Marek (l. 86) ✅: „Ściągę mam prawie gotową. Z mailem zobaczę, czy da się szybko.”

## Backlog produktu (prośby o funkcje)

_Cel: tablica produktowa_

#### A16 · Ocenić dodanie modelu i salonu na górze maila po walidacji
`feature_request` · `do_now`  
Ola chce, żeby mail po walidacji miał na górze model i salon, i to od razu, a nie za miesiąc. Marek sprawdzi, czy da się to zrobić szybko. Nie złożył zobowiązania co do terminu.
- **Właściciel:** Marek Rewoliński
- **Termin:** bez daty („już, nie za miesiąc”)
- **Ograniczenia:** Brak zobowiązania terminowego – tylko ocena, czy da się szybko
  > Tomek (l. 84) ✅: „I żeby mail po walidacji miał model i salon na górze. Ona by to chciała już, nie za miesiąc.”
  > Marek (l. 86) ✅: „Ściągę mam prawie gotową. Z mailem zobaczę, czy da się szybko.”

## Czekamy na klienta

_Cel: przypomnienia w kalendarzu_

#### A06 · Puścić plik ze świeżymi leadami po otrzymaniu
`task` · `waiting_on_client`  
Kasia nie wysłała pliku w poniedziałek. Eksport jest gotowy i wyśle go dziś po południu, a Marek puści leady, gdy plik przyjdzie.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-13 („dziś po południu”)
- **Warunek:** Otrzymanie pliku od Kasi
  > Kasia (l. 44) ✅: „Eksport jest gotowy, wyślę dziś po południu.”
  > Marek (l. 46) ✅: „Jak przyjdzie, puszczam.”

#### A08 · Skonfigurować agenta po godzinach po otrzymaniu numerów assistance
`config_change` · `waiting_on_client`  
Według Tomka Kasia zgodziła się na uruchomienie nocnego agenta. Marek nie dostał jeszcze numerów assistance i zacznie konfigurację, gdy przyjdą. Tomek obiecał wysłać je dziś.
- **Właściciel:** Marek Rewoliński
- **Warunek:** Otrzymanie numerów assistance od Tomka (obiecane na dziś)
  > Tomek (l. 72) ✅: „Kasia mówiła, że po godzinach od wtorku. Że możecie już ustawiać tego nocnego agenta, a numery assistance ja wam podeślę.”
  > Marek (l. 74) ✅: „Numery assistance jeszcze do mnie nie doszły. Jak przyjdą, siadam do tego.”
  > Tomek (l. 76) ✅: „Podeślę dziś.”

#### A09 · Czekać na teksty wstępu od Kasi
`task` · `waiting_on_client`  
Teksty wstępu leżą u Kasi w szkicu. Kasia nie zdąży ich wysłać w tym tygodniu.
- **Właściciel:** Kasia Malinowska
- **Termin:** bez daty („W tym tygodniu nie zdążę”)
- **Warunek:** Kasia wyśle teksty wstępu
  > Kasia (l. 48) ✅: „Leżą u mnie w szkicu. W tym tygodniu nie zdążę.”

#### A11 · Uruchomić test wstępu od środy 21.10
`task` · `waiting_on_client`  
Gdy Kasia wyśle teksty wstępu, puścić test od środy 21.10. Tomek będzie wtedy słuchał nagrań.
- **Właściciel:** Marek Rewoliński
- **Termin:** 2026-10-21 („od środy dwudziestego pierwszego”)
- **Warunek:** Kasia wyśle teksty wstępu
- **Ograniczenia:** Nie wcześniej niż 21.10
- **Zależy od:** A09
  > Tomek (l. 76) ✅: „I test tego wstępu: jak Kasia wyśle teksty, puśćcie od środy dwudziestego pierwszego.”
  > Marek (l. 78) ✅: „Środa, dwudziesty pierwszy. Dobra.”

## Informacje i sprawy bez działania

_Cel: CRM, notatka na koncie klienta_

#### A02 · Weryfikacja adresu zakończona
`info` · `no_action`  
Kasia sprawdziła w czwartek testowym połączeniem na swój numer, że agent podaje adres Toruńska 120 i sobotę do 15:00. Potwierdziła, że jest dobrze.
  > Kasia (l. 28) ✅: „Adres sprawdziłam w czwartek, testem na swój numer. Mówi Toruńska 120, sobota do piętnastej. Dobrze.”

#### A03 · Błąd drugiego telefonu po rozłączeniu – naprawiony
`bug` · `no_action`  
Reguła trzech sekund działała tylko przy pierwszej próbie, przez co agent dzwonił drugi raz po rozłączeniu. Błąd poprawiono w czwartek 8.10. Podwójnych połączeń było 11, nie 6.
- **Właściciel:** Marek Rewoliński
- **Wersja ostateczna:** 11 podwójnych telefonów
- **Zastępuje:** 6 podwójnych telefonów
  > Marek (l. 38) ✅: „Reguła trzech sekund działała tylko przy pierwszej próbie. Poprawione w czwartek.”

#### A17 · Tomek Wrona zastępuje Kasię w BDC
`info` · `no_action`  
Tomek pracuje w BDC od tego tygodnia i będzie zastępował Kasię. Od wczoraj ma dostęp do panelu. Pozostałe tematy z tego calla Kasia przekazała Tomkowi.
  > Kasia (l. 24) ✅: „To Tomek, od tego tygodnia u nas w BDC, będzie mnie zastępował.”
  > Kasia (l. 60) ✅: „Tomek ma od wczoraj dostęp do panelu, resztę z nim.”

## Szkice wiadomości (do zatwierdzenia)

- **D01** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Podwójne telefony po rozłączeniu – podsumowanie i korekta faktury” · wysłać: Dziś, 2026-10-13 · [drafts/D01-kasia-malinowska.md](drafts/D01-kasia-malinowska.md)
- **D02** do: Paweł &lt;pawel@autotama.pl&gt; · „Zaproszenie: spotkanie Grupa Auto Tama × Rinvo – czwartek 15.10, 10:00, Toruń” · wysłać: Dziś, 2026-10-13 · [drafts/D02-pawel.md](drafts/D02-pawel.md)
- **D03** do: Ola Nowak &lt;ola.nowak@autotama.pl&gt; · „Ściąga ze statusami walidacji leadów” · wysłać: Gdy ściąga będzie gotowa (Marek ma ją prawie gotową) · [drafts/D03-ola-nowak.md](drafts/D03-ola-nowak.md)
- **D04** do: Kasia Malinowska &lt;kasia.malinowska@autotama.pl&gt; · „Przypomnienie: teksty wstępu” · wysłać: Poniedziałek 2026-10-19, jednorazowo, tylko jeśli teksty nie przyszły wcześniej · [drafts/D04-kasia-malinowska.md](drafts/D04-kasia-malinowska.md)

## Założenia przyjęte przy analizie

- Wypowiedzi Kasi o sobotach są sprzeczne. Mówi „od siedemnastego znowu do czternastej”, ale też „w tę sobotę jeszcze jest do piętnastej”, a najbliższa sobota po 13.10 to właśnie 17.10. Przyjęto wersję, którą Marek potwierdził i której Kasia nie skorygowała: zmiana w piątek 16.10, obowiązuje od soboty 17.10. Warto potwierdzić to z Kasią lub Tomkiem przed przestawieniem.
- „Czwartek, dziesiąta” to najbliższy czwartek po callu, czyli 2026-10-15.
- „Poprawione w czwartek” odnosi się do czwartku 2026-10-08.
- Pierwszy dzień roboczy listopada to poniedziałek 2026-11-02, bo 1.11 to niedziela. Kolejne podsumowania także w pierwszy dzień roboczy każdego miesiąca.
- Polecenie włączenia Opla od 19.10 przekazał Tomek w imieniu Pawła. Paweł nie potwierdził go bezpośrednio na callu, a Kasia nie wypowiadała się o Oplu. Przyjęto je jako obowiązujące, bo Marek je przyjął, a Kasia przekazała resztę tematów Tomkowi.
- Z połączenia ustaleń wynika, że sobotnie godziny do 14:00 dotyczą obu salonów, więc również Opla we Włocławku. To wniosek, nikt tego nie powiedział wprost.
- Informację „po godzinach od wtorku” przekazał Tomek, powołując się na Kasię. Kasia nie wspomniała o tym, gdy była na callu, a Marek nie zobowiązał się do daty uruchomienia. Dlatego nie ustalono terminu, a pozycja czeka na numery assistance.
- Teksty wstępu potraktowano jako waiting_on_client, nie on_hold. Kasia nie zapowiedziała, że sama wróci do tematu, a klient (Tomek) wprost poprosił o przypomnienie.
- „Przypomnijcie jej jeszcze raz” oznacza jedno przypomnienie w poniedziałek 2026-10-19.
- Miesięczne podsumowanie ma iść do Kasi, jak sama wskazała, mimo że Tomek będzie ją zastępował.
- „Ta 208” to przykład, prawdopodobnie nagranie lub lead dotyczący Peugeota 208, który Marek pokaże Pawłowi. Dokładny charakter nie wynika z transkryptu.
