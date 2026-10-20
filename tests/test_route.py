from datetime import date

import pytest
from conftest import make_extraction, make_item

from callflow.route import Inbox, inbox_for, route
from callflow.schema import Kind, State


@pytest.mark.parametrize(
    ("kind", "state", "expected"),
    [
        (Kind.bug, State.do_now, Inbox.tickets),
        (Kind.config_change, State.scheduled, Inbox.config_changes),
        (Kind.feature_request, State.scheduled, Inbox.backlog),
        (Kind.task, State.do_now, Inbox.tasks),
        (Kind.feature_request, State.do_not_do, Inbox.do_not_do),
        (Kind.feature_request, State.on_hold, Inbox.on_hold),
        (Kind.risk, State.no_action, Inbox.risks),
        (Kind.task, State.waiting_on_client, Inbox.waiting_on_client),
        (Kind.bug, State.no_action, Inbox.no_action),
    ],
)
def test_inbox_for(kind, state, expected):
    assert inbox_for(make_item(kind=kind, state=state)) == expected


def test_rejected_request_never_reaches_backlog():
    routed = route(make_extraction(items=[make_item(kind=Kind.feature_request, state=State.do_not_do)]))
    assert routed.inboxes[Inbox.backlog] == []
    assert len(routed.inboxes[Inbox.do_not_do]) == 1


def test_reminders_only_for_dated_client_dependencies_sorted_by_date():
    items = [
        make_item(id="A01", state=State.waiting_on_client, due_date=date(2026, 10, 15)),
        make_item(id="A02", state=State.waiting_on_client, due_date=date(2026, 10, 14)),
        make_item(id="A03", state=State.waiting_on_client, due_date=None),
        make_item(id="A04", state=State.on_hold, due_date=date(2026, 10, 20)),
    ]
    routed = route(make_extraction(items=items))
    assert [item.id for item in routed.reminders] == ["A02", "A01"]


def test_every_item_lands_in_exactly_one_inbox():
    items = [make_item(id=f"A{i:02d}", kind=kind) for i, kind in enumerate(Kind, 1)]
    routed = route(make_extraction(items=items))
    assert sum(len(bucket) for bucket in routed.inboxes.values()) == len(items)
