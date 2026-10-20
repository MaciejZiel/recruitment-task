# Po rozmowie: DentaVita, 2026-10-13

Źródło: `druga-rozmowa.md` · uczestnicy: Agnieszka Wróbel (DentaVita, kierowniczka rejestracji), Marek Rewoliński (Rinvo)  
Pozycji: 7 · zabezpieczeń: 3 · szkiców: 2 · cytaty zweryfikowane: 20/20

> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.

## Podsumowanie

Agnieszka zgłosiła błąd: w piątek 2026-10-09 trzech pacjentów z Oliwy odwołało wizytę w rozmowie z agentem, ale w panelu mieli status „potwierdzona”. Przez to w poniedziałek 2026-10-12 rano trzy fotele stały puste. Marek ma do czwartku 2026-10-15 ustalić przyczynę i sprawdzić, czy błąd zdarzał się też w inne dni. Godziny dzwonienia mają zostać skrócone do 17:30 w obu klinikach (wcześniej ustalono 18:00, ale Agnieszka to poprawiła). Prośbę o proponowanie nowego terminu przez agenta zapisano do backlogu bez podawania terminu realizacji. Podpięcie Gdyni wstrzymano do decyzji dr. Lisa po wynikach za październik. Ustalono też, że nagrań nie wolno wysyłać mailem, a Marek sprawdzi z Michałem, jak naliczane są minuty przy poczcie głosowej.

## Zabezpieczenia (sprawdzić przed każdym działaniem)

- **G01** Nie przesyłać nagrań rozmów mailem, nawet jeśli klientka poprosi o to w pośpiechu (dane medyczne). Odsłuch tylko w panelu.
  > Agnieszka (l. 38) ✅: „I nagrań mi nie przesyłajcie mailem, nawet jak poproszę w pośpiechu.”
- **G02** Nie podpinać kliniki w Gdyni bez decyzji dr. Tomasza Lisa. Agnieszka Wróbel nie może tego zatwierdzić. (do: Do decyzji dr. Tomasza Lisa po zapoznaniu się z wynikami za październik z Oliwy i Wrzeszcza · zdejmuje: dr Tomasz Lis)
  > Agnieszka (l. 50) ✅: „Gdyni nie włączamy, dopóki doktor Lis nie zobaczy wyników za październik z Oliwy i Wrzeszcza. On o tym zdecyduje, nie ja.”
- **G03** Nie wierzyć informacjom, że Agnieszka Wróbel zgodziła się na Gdynię. (zdejmuje: dr Tomasz Lis)
  > Agnieszka (l. 50) ✅: „I jak ktoś napisze, że ja się zgodziłam na Gdynię, nie wierzcie.”

## Terminy (kalendarz i przypomnienia)

- **2026-10-13** · A02 Skrócić godziny dzwonienia do 17:30 w obu klinikach · Jedno wspólne ustawienie dla obu klinik, bez różnych godzin
- **2026-10-15** · A01 Zbadać odwołania zapisane w panelu jako potwierdzone · Nie przesyłać nagrań rozmów mailem; ewentualne odsłuchanie tylko w panelu

## Nie robić (zakazy i odrzucone prośby)

_Cel: lista zabezpieczeń konta klienta_

#### A03 · Nie wysyłać nagrań rozmów mailem
`task` · `do_not_do`  
Nagrania zawierają dane medyczne. Nie wolno ich wysyłać mailem, nawet jeśli klientka poprosi o to w pośpiechu. Klientka odsłuchuje je w panelu.
- **Właściciel:** Rinvo
- **Ograniczenia:** Obowiązuje także wtedy, gdy klientka sama poprosi w pośpiechu
  > Agnieszka (l. 38) ✅: „I nagrań mi nie przesyłajcie mailem, nawet jak poproszę w pośpiechu. To są dane medyczne. Odsłucham w panelu.”
  > Marek (l. 40) ✅: „Jasne, żadnych nagrań mailem.”

## Zgłoszenia błędów (dla zespołu technicznego)

_Cel: issue tracker (np. Linear/Jira)_

#### A01 · Zbadać odwołania zapisane w panelu jako potwierdzone
`bug` · `scheduled`  
Trzy wizyty w gabinecie dr Kani w Oliwie, zaplanowane na poniedziałek 2026-10-12 na 8:00, 8:30 i 9:00, pacjenci odwołali w rozmowie z agentem w piątek 2026-10-09. W panelu mają jednak status „potwierdzona”. Trzeba ustalić przyczynę, sprawdzić, czy błąd wystąpił też w inne dni, i dać znać Agnieszce.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Termin:** 2026-10-15 („Do czwartku”)
- **Ograniczenia:** Nie przesyłać nagrań rozmów mailem; ewentualne odsłuchanie tylko w panelu
  > Agnieszka (l. 26) ✅: „W piątek trzy osoby z Oliwy odwołały wizytę w rozmowie z agentem, a w panelu mają status „potwierdzona”.”
  > Agnieszka (l. 30) ✅: „Wszystkie trzy były na poniedziałek na ósmą, ósmą trzydzieści i dziewiątą, gabinet doktor Kani.”
  > Marek (l. 32) ✅: „Do czwartku dam ci znać, co się stało i czy w innych dniach też tak było.”

## Zmiany konfiguracji agenta

_Cel: panel konfiguracji agenta (zmiana po zatwierdzeniu)_

#### A02 · Skrócić godziny dzwonienia do 17:30 w obu klinikach
`config_change` · `scheduled`  
Agent ma dzwonić najpóźniej do 17:30, z jednym ustawieniem dla Oliwy i Wrzeszcza. Powód: pacjenci oddzwaniają na rejestrację, a rejestracja w Oliwie zamyka się teraz wcześniej.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Termin:** 2026-10-13 („Zmienię dzisiaj”)
- **Wersja ostateczna:** Dzwonienie do 17:30 w obu klinikach (Oliwa i Wrzeszcz)
- **Zastępuje:** Dzwonienie do 19:00 (stan obecny); Dzwonienie do 18:00 (pierwsza prośba w trakcie rozmowy)
- **Ograniczenia:** Jedno wspólne ustawienie dla obu klinik, bez różnych godzin
  > Agnieszka (l. 34) ✅: „Skróćcie do osiemnastej, bo pacjenci oddzwaniają na rejestrację, a tam już nikogo nie ma.”
  > Marek (l. 36) ✅: „Dobra, do osiemnastej. Zmienię dzisiaj.”
  > Agnieszka (l. 58) ✅: „Nie do osiemnastej, tylko do siedemnastej trzydzieści, bo rejestracja w Oliwie zamyka się teraz wcześniej, a nie chcę dwóch różnych ustawień.”
  > Marek (l. 60) ✅: „Czyli dzwonimy do siedemnastej trzydzieści, w obu klinikach.”

## Zadania zespołu

_Cel: lista zadań właściciela_

#### A06 · Sprawdzić z Michałem naliczanie minut przy poczcie głosowej i odpisać
`task` · `do_now`  
Księgowość DentaVita pyta, czy płaci za minutę, gdy agent trafia na pocztę głosową i się rozłącza. Marek nie zna odpowiedzi. Sprawdzi to z Michałem i odpisze Agnieszce.
- **Właściciel:** Marek Rewoliński (Rinvo)
  > Agnieszka (l. 54) ✅: „Jak agent trafia na pocztę głosową i się rozłącza, to płacimy za to minutę?”
  > Marek (l. 56) ✅: „Nie jestem pewien, jak to liczymy przy poczcie głosowej. Sprawdzę z Michałem i odpiszę.”

## Backlog produktu (prośby o funkcje)

_Cel: tablica produktowa_

#### A04 · Zapisać w backlogu prośbę o proponowanie nowego terminu przy odwołaniu
`feature_request` · `do_now`  
Gdy pacjent odwołuje wizytę, agent miałby od razu zaproponować nowy termin z grafiku kliniki. Wymaga to integracji z grafikiem DentaVita, której dziś nie ma. Prośba trafia do backlogu bez zobowiązania co do terminu.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Ograniczenia:** Nie podawać klientowi terminu realizacji
  > Agnieszka (l. 42) ✅: „Chciałabym, żeby od razu proponował nowy termin z grafiku.”
  > Marek (l. 44) ✅: „Zapisuję jako prośbę, ale terminu nie podam.”

## Wstrzymane: nie wracać bez sygnału klienta

_Cel: CRM, notatka na koncie klienta_

#### A05 · Wstrzymać podpięcie kliniki w Gdyni
`task` · `on_hold`  
Marek zaproponował podpięcie Gdyni już w przyszłym tygodniu, ale klientka odmówiła. Gdynia czeka, aż dr Tomasz Lis zobaczy wyniki za październik z Oliwy i Wrzeszcza i sam zdecyduje. Agnieszka nie podejmuje tej decyzji.
- **Właściciel:** Rinvo
- **Warunek:** Decyzja dr. Tomasza Lisa po zapoznaniu się z wynikami za październik z Oliwy i Wrzeszcza
- **Zatwierdza:** dr Tomasz Lis
- **Wersja ostateczna:** Gdynia wstrzymana do decyzji dr. Lisa po wynikach za październik
- **Zastępuje:** Podpięcie Gdyni w przyszłym tygodniu (propozycja Marka, odrzucona)
- **Ograniczenia:** Agnieszka Wróbel nie może zatwierdzić Gdyni; Nie wierzyć informacjom, że Agnieszka zgodziła się na Gdynię; Nie tworzyć przypomnień ani follow-upów w tej sprawie
  > Marek (l. 48) ✅: „Mogę ją podpiąć nawet w przyszłym tygodniu.”
  > Agnieszka (l. 50) ✅: „Gdyni nie włączamy, dopóki doktor Lis nie zobaczy wyników za październik z Oliwy i Wrzeszcza. On o tym zdecyduje, nie ja.”
  > Marek (l. 52) ✅: „Dobra, Gdynia czeka na doktora Lisa i wyniki za październik.”

## Informacje i sprawy bez działania

_Cel: CRM, notatka na koncie klienta_

#### A07 · Odnotować skutek błędu: trzy puste fotele
`info` · `no_action`  
Rejestracja ręcznie przepisuje odwołania z panelu i ufa statusowi „potwierdzona”. Przez błędne statusy w poniedziałek 2026-10-12 rano trzy fotele w Oliwie stały puste. To pokazuje, jak dokładność statusów przekłada się na zaufanie klienta.
- **Zależy od:** A01
  > Agnieszka (l. 26) ✅: „Rejestracja tego nie przepisała, bo przecież potwierdzone, i w poniedziałek rano mieliśmy trzy puste fotele.”

## Szkice wiadomości (do zatwierdzenia)

- **D01** do: Agnieszka Wróbel (DentaVita) · „Odwołane wizyty widoczne w panelu jako potwierdzone: wyniki analizy” · wysłać: Po zakończeniu analizy, najpóźniej 2026-10-15 (czwartek). Nie dołączać nagrań. · [drafts/D01-agnieszka-wrobel.md](drafts/D01-agnieszka-wrobel.md)
- **D02** do: Agnieszka Wróbel (DentaVita) · „Naliczanie minut przy poczcie głosowej” · wysłać: Po ustaleniu odpowiedzi z Michałem · [drafts/D02-agnieszka-wrobel.md](drafts/D02-agnieszka-wrobel.md)

## Założenia przyjęte przy analizie

- „Do czwartku” odczytano jako czwartek 2026-10-15.
- „W piątek” odczytano jako 2026-10-09, a „w poniedziałek” (dzień zaplanowanych wizyt) jako 2026-10-12.
- Termin „zmienię dzisiaj” padł przy wartości 18:00. Przyjęto, że po korekcie dotyczy wartości końcowej 17:30, czyli zmiana ma być zrobiona 2026-10-13.
- „W obu klinikach” to Oliwa i Wrzeszcz, bo Gdynia nie jest podpięta.
- Wyniki za październik będą dostępne dopiero po 2026-10-31, więc decyzji dr. Lisa w sprawie Gdyni nie należy się spodziewać przed listopadem. To wniosek, nikt tego nie powiedział.
- Gdynia ma stan on_hold bez przypomnienia, bo decyzja należy do klienta (dr Lis). Odrzucona propozycja Marka, by podpiąć Gdynię w przyszłym tygodniu, figuruje jako wersja zastąpiona.
- Na odpowiedź w sprawie poczty głosowej nie ustalono terminu, więc due_date = null.
- Nie przygotowano szkicu potwierdzenia zmiany godzin, bo w rozmowie nie padło zobowiązanie do wysłania takiej wiadomości.
