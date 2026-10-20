# Po rozmowie: DentaVita, 2026-10-13

Źródło: `druga-rozmowa.md` · uczestnicy: Agnieszka Wróbel (DentaVita, kierowniczka rejestracji), Marek Rewoliński (Rinvo)  
Pozycji: 6 · zabezpieczeń: 3 · szkiców: 3 · cytaty zweryfikowane: 19/19

> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.

## Podsumowanie

Call statusowy z DentaVita. Klientka zgłosiła błąd: w piątek trzy wizyty w Oliwie zostały odwołane w rozmowie z agentem, ale w panelu mają status „potwierdzona”. Przez to w poniedziałek trzy fotele stały puste. Marek ma do czwartku 15.10 przekazać diagnozę i sprawdzić, czy problem wystąpił też w inne dni. Godziny dzwonienia ostatecznie skracamy do 17:30 w obu klinikach (wcześniej ustalono 18:00). Obowiązuje bezwzględny zakaz wysyłania nagrań mailem. Prośbę o proponowanie nowego terminu przez agenta wpisujemy do backlogu bez terminu. Gdyni nie włączamy, dopóki dr Lis nie zobaczy wyników za październik i sam nie zdecyduje. Pytanie księgowości o naliczanie minut przy poczcie głosowej Marek wyjaśni z Michałem.

## Zabezpieczenia (sprawdzić przed każdym działaniem)

- **G01** Nie wysyłać nagrań rozmów mailem (dane medyczne), także na pilną prośbę klientki.
  > Agnieszka (l. 38) ✅: „I nagrań mi nie przesyłajcie mailem, nawet jak poproszę w pośpiechu.”
- **G02** Nie włączać agenta w klinice w Gdyni bez decyzji dr. Tomasza Lisa. (do: Do decyzji dr. Lisa po zapoznaniu się z wynikami za październik z Oliwy i Wrzeszcza · zdejmuje: dr Tomasz Lis)
  > Agnieszka (l. 50) ✅: „Gdyni nie włączamy, dopóki doktor Lis nie zobaczy wyników za październik z Oliwy i Wrzeszcza.”
  > Agnieszka (l. 50) ✅: „On o tym zdecyduje, nie ja.”
- **G03** Nie uznawać informacji, że Agnieszka Wróbel zgodziła się na Gdynię. Ona nie może tego zatwierdzić. (zdejmuje: dr Tomasz Lis)
  > Agnieszka (l. 50) ✅: „I jak ktoś napisze, że ja się zgodziłam na Gdynię, nie wierzcie.”

## Ostrzeżenia walidacji

- **D01**: szkic używa względnej daty („wczorajszym”)

## Terminy (kalendarz i przypomnienia)

- **2026-10-13** · A02 Skrócić godziny dzwonienia do 17:30 w obu klinikach · Jedno wspólne ustawienie dla obu klinik, bez różnych godzin
- **2026-10-15** · A01 Zdiagnozować błędne statusy odwołanych wizyt w Oliwie · Sprawdzić także inne dni, nie tylko te trzy wizyty

## Nie robić (zakazy i odrzucone prośby)

_Cel: lista zabezpieczeń konta klienta_

#### A03 · Nie wysyłać nagrań rozmów mailem
`info` · `do_not_do`  
Nagrania zawierają dane medyczne. Nie wolno ich wysyłać mailem, nawet jeśli klientka poprosi o to w pośpiechu. Klientka odsłuchuje nagrania w panelu.
- **Ograniczenia:** Bez wyjątków, także na pilną prośbę klientki; Nagrań nie dołączać do żadnych wiadomości
  > Agnieszka (l. 38) ✅: „I nagrań mi nie przesyłajcie mailem, nawet jak poproszę w pośpiechu.”
  > Marek (l. 40) ✅: „Jasne, żadnych nagrań mailem.”

#### A05 · Nie podpinać kliniki w Gdyni
`feature_request` · `do_not_do`  
Marek zaproponował podpięcie Gdyni w przyszłym tygodniu, ale klientka odmówiła. O Gdyni zdecyduje dr Tomasz Lis po zapoznaniu się z wynikami za październik z Oliwy i Wrzeszcza. Agnieszka nie może tego zatwierdzić.
- **Warunek:** Dopiero po decyzji dr. Lisa, podjętej po zapoznaniu się z wynikami za październik z Oliwy i Wrzeszcza
- **Zatwierdza:** dr Tomasz Lis (nie Agnieszka Wróbel)
- **Wersja ostateczna:** Gdynia pozostaje niepodpięta do decyzji dr. Lisa
- **Zastępuje:** Propozycja Marka: podpięcie Gdyni w przyszłym tygodniu
- **Ograniczenia:** Nie uznawać zgody Agnieszki Wróbel, ona nie może zatwierdzić Gdyni; Nie wierzyć informacjom, że Agnieszka zgodziła się na Gdynię
  > Marek (l. 48) ✅: „Mogę ją podpiąć nawet w przyszłym tygodniu.”
  > Agnieszka (l. 50) ✅: „Gdyni nie włączamy, dopóki doktor Lis nie zobaczy wyników za październik z Oliwy i Wrzeszcza.”
  > Marek (l. 52) ✅: „Dobra, Gdynia czeka na doktora Lisa i wyniki za październik.”

## Zgłoszenia błędów (dla zespołu technicznego)

_Cel: issue tracker (np. Linear/Jira)_

#### A01 · Zdiagnozować błędne statusy odwołanych wizyt w Oliwie
`bug` · `scheduled`  
Trzy wizyty z Oliwy (poniedziałek 12.10, godz. 8:00, 8:30 i 9:00, gabinet dr Kani) pacjenci odwołali w piątkowych rozmowach z agentem, a w panelu mają status „potwierdzona”. Rejestracja ich nie przepisała i fotele stały puste. Trzeba ustalić przyczynę i sprawdzić, czy to samo działo się w inne dni, a potem przekazać wynik Agnieszce.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Termin:** 2026-10-15 („Do czwartku”)
- **Ograniczenia:** Sprawdzić także inne dni, nie tylko te trzy wizyty
  > Agnieszka (l. 26) ✅: „W piątek trzy osoby z Oliwy odwołały wizytę w rozmowie z agentem, a w panelu mają status „potwierdzona”.”
  > Agnieszka (l. 30) ✅: „Wszystkie trzy były na poniedziałek na ósmą, ósmą trzydzieści i dziewiątą, gabinet doktor Kani.”
  > Marek (l. 32) ✅: „Do czwartku dam ci znać, co się stało i czy w innych dniach też tak było.”

## Zmiany konfiguracji agenta

_Cel: panel konfiguracji agenta (zmiana po zatwierdzeniu)_

#### A02 · Skrócić godziny dzwonienia do 17:30 w obu klinikach
`config_change` · `scheduled`  
Agent ma dzwonić najpóźniej do 17:30, zarówno w Oliwie, jak i we Wrzeszczu. Pacjenci oddzwaniają na rejestrację, a rejestracja w Oliwie zamyka się teraz wcześniej. Klientka nie chce dwóch różnych ustawień.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Termin:** 2026-10-13 („dzisiaj”)
- **Wersja ostateczna:** Dzwonienie do 17:30 w Oliwie i we Wrzeszczu
- **Zastępuje:** Obecnie do 19:00; Do 18:00 (ustalone wcześniej w trakcie rozmowy, potem poprawione przez klientkę)
- **Ograniczenia:** Jedno wspólne ustawienie dla obu klinik, bez różnych godzin
  > Marek (l. 36) ✅: „Dobra, do osiemnastej. Zmienię dzisiaj.”
  > Agnieszka (l. 58) ✅: „Nie do osiemnastej, tylko do siedemnastej trzydzieści, bo rejestracja w Oliwie zamyka się teraz wcześniej, a nie chcę dwóch różnych ustawień.”
  > Marek (l. 60) ✅: „Czyli dzwonimy do siedemnastej trzydzieści, w obu klinikach.”

## Zadania zespołu

_Cel: lista zadań właściciela_

#### A06 · Wyjaśnić naliczanie minut przy poczcie głosowej i odpisać księgowości
`task` · `do_now`  
Księgowość DentaVita pyta, czy płaci za minutę, gdy agent trafia na pocztę głosową i się rozłącza. Marek nie zna odpowiedzi. Sprawdzi to z Michałem i odpisze klientce.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Ograniczenia:** Nie odpowiadać przed sprawdzeniem z Michałem
  > Agnieszka (l. 54) ✅: „Jak agent trafia na pocztę głosową i się rozłącza, to płacimy za to minutę?”
  > Marek (l. 56) ✅: „Nie jestem pewien, jak to liczymy przy poczcie głosowej. Sprawdzę z Michałem i odpiszę.”

## Backlog produktu (prośby o funkcje)

_Cel: tablica produktowa_

#### A04 · Zapisać w backlogu prośbę o proponowanie nowego terminu przy odwołaniu
`feature_request` · `do_now`  
Klientka chce, żeby agent po odwołaniu wizyty od razu proponował pacjentowi nowy termin z grafiku. Wymagałoby to integracji z grafikiem kliniki, której dziś nie ma. Prośba trafia do backlogu bez terminu.
- **Właściciel:** Marek Rewoliński (Rinvo)
- **Ograniczenia:** Nie podawać klientowi terminu realizacji
  > Agnieszka (l. 42) ✅: „Chciałabym, żeby od razu proponował nowy termin z grafiku.”
  > Marek (l. 44) ✅: „Zapisuję jako prośbę, ale terminu nie podam.”

## Szkice wiadomości (do zatwierdzenia)

- **D01** do: Agnieszka Wróbel · „Godziny dzwonienia zmienione na 17:30” · wysłać: Po faktycznym wprowadzeniu zmiany godzin w konfiguracji (A02). Nie wysyłać automatycznie. · [drafts/D01-agnieszka-wrobel.md](drafts/D01-agnieszka-wrobel.md)
- **D02** do: Agnieszka Wróbel · „Błędne statusy odwołanych wizyt w Oliwie: wyniki analizy” · wysłać: Do czwartku 2026-10-15, dopiero po zakończeniu analizy. Bez załączonych nagrań. · [drafts/D02-agnieszka-wrobel.md](drafts/D02-agnieszka-wrobel.md)
- **D03** do: Agnieszka Wróbel · „Naliczanie minut przy poczcie głosowej” · wysłać: Dopiero po ustaleniu odpowiedzi z Michałem. Bez zgadywania. · [drafts/D03-agnieszka-wrobel.md](drafts/D03-agnieszka-wrobel.md)

## Założenia przyjęte przy analizie

- „Do czwartku” odczytano jako czwartek 2026-10-15, czyli najbliższy czwartek po callu.
- „Zmienię dzisiaj” padło przy wersji 18:00. Przyjęto, że termin 2026-10-13 dotyczy też ostatecznej wersji (17:30).
- „W obu klinikach” odczytano jako Oliwę i Wrzeszcz, bo tylko te dwie kliniki mają włączonego agenta.
- Wyniki za październik będą pełne najwcześniej po 2026-10-31, więc decyzja dr. Lisa w sprawie Gdyni nie zapadnie wcześniej. Nikt nie ustalił, kto i kiedy przekaże dr. Lisowi te wyniki, dlatego nie utworzono takiego zadania ani przypomnienia.
- Prośbę o proponowanie nowego terminu wpisano do backlogu bez terminu, bo Marek wprost odmówił jego podania.
- Pytanie o pocztę głosową nie ma terminu odpowiedzi. Przyjęto, że Marek odpisze po ustaleniu tego z Michałem.
