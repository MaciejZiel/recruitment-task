"""Deterministic routing of extracted items to the inboxes that act on them."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from callflow.schema import ActionItem, Kind, MeetingExtraction, State


class Inbox(StrEnum):
    """Where an item goes; the value is the section title in the report."""

    do_not_do = "Nie robić (zakazy i odrzucone prośby)"
    tickets = "Zgłoszenia błędów (dla zespołu technicznego)"
    config_changes = "Zmiany konfiguracji agenta"
    tasks = "Zadania zespołu"
    backlog = "Backlog produktu (prośby o funkcje)"
    waiting_on_client = "Czekamy na klienta"
    risks = "Ryzyka klienta (notatka do CRM)"
    on_hold = "Wstrzymane: nie wracać bez sygnału klienta"
    no_action = "Informacje i sprawy bez działania"


# Report order: what must not happen first, then what to do now, then what waits.
INBOX_ORDER = list(Inbox)

TARGET_SYSTEM = {
    Inbox.do_not_do: "lista zabezpieczeń konta klienta",
    Inbox.tickets: "issue tracker (np. Linear/Jira)",
    Inbox.config_changes: "panel konfiguracji agenta (zmiana po zatwierdzeniu)",
    Inbox.tasks: "lista zadań właściciela",
    Inbox.backlog: "tablica produktowa",
    Inbox.waiting_on_client: "przypomnienia w kalendarzu",
    Inbox.risks: "CRM, notatka na koncie klienta",
    Inbox.on_hold: "CRM, notatka na koncie klienta",
    Inbox.no_action: "CRM, notatka na koncie klienta",
}

_ACTIVE_BY_KIND = {
    Kind.bug: Inbox.tickets,
    Kind.config_change: Inbox.config_changes,
    Kind.feature_request: Inbox.backlog,
}


def inbox_for(item: ActionItem) -> Inbox:
    if item.state == State.do_not_do:
        return Inbox.do_not_do
    if item.state == State.on_hold:
        return Inbox.on_hold
    if item.kind == Kind.risk:
        return Inbox.risks
    if item.state == State.waiting_on_client:
        return Inbox.waiting_on_client
    if item.state == State.no_action:
        return Inbox.no_action
    return _ACTIVE_BY_KIND.get(item.kind, Inbox.tasks)


@dataclass
class RoutedMeeting:
    extraction: MeetingExtraction
    inboxes: dict[Inbox, list[ActionItem]] = field(default_factory=dict)
    reminders: list[ActionItem] = field(default_factory=list)


def route(extraction: MeetingExtraction) -> RoutedMeeting:
    routed = RoutedMeeting(extraction, {inbox: [] for inbox in INBOX_ORDER})
    for item in extraction.items:
        routed.inboxes[inbox_for(item)].append(item)
        # on_hold items deliberately get no reminder: the client said they will come back themselves.
        if item.state == State.waiting_on_client and item.due_date:
            routed.reminders.append(item)
    routed.reminders.sort(key=lambda item: item.due_date)
    return routed
