# Logi pracy z AI

Eksport sesji Claude Code użytych przy tym zadaniu, przekonwertowany z plików JSONL do Markdown.

| Plik | Zawartość |
|---|---|
| `01-setup-session.md` | Sesja przygotowania środowiska przed otrzymaniem zadania. |
| `02-main-session.md` | Główna sesja zadania: analiza, plan, implementacja, testy, commity. Jest kontynuacją sesji 1, więc powtórzonych wpisów z sesji 1 nie ma. |
| `03-reviewer-session.md` | Osobna sesja recenzenta pracującego tylko w trybie odczytu. |

## Co zostało skrócone

- Wiadomości użytkownika i odpowiedzi tekstowe asystenta są pełne, w kolejności chronologicznej, z czasem lokalnym (UTC+2).
- Każde wywołanie narzędzia jest streszczone w jednej linii (nazwa narzędzia i skrócony opis lub polecenie, do ok. 200 znaków).
- Wyniki narzędzi są pominięte, zostaje tylko status (ok/błąd i długość). Wyjątek stanowią raporty subagentów i wiadomości między sesjami, które zostawiono w takiej postaci, w jakiej pojawiły się w transkrypcie.
- Ukryte rozumowanie modelu (thinking) i wpisy techniczne (załączniki kontekstu, metadane) są pominięte.

## Co zostało zredagowane

- Tokeny i klucze API (Atlassian, Anthropic, GitHub) zastąpiono `[REDACTED-TOKEN]`, a niepuste wartości `JIRA_API_TOKEN=` niebędące placeholderami — `[REDACTED]`. Skan przed eksportem nie znalazł w sesjach żadnej prawdziwej wartości tego typu.
- Adres e-mail konta Claude zastąpiono `[e-mail konta Claude]`, a adres e-mail autora `[e-mail autora]`, żeby nie publikować danych kontaktowych.

Poza tym treść nie była zmieniana.

## Czego tu nie ma

Rozmów z dodatkowymi doradcami (Fable, GPT Astra) nie ma w tym katalogu. Ich wnioski widać tylko tam, gdzie zostały wklejone do sesji głównej. Rozmowy z doradcami można dodać osobno.
