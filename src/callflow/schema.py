"""Structured result of analysing one client call; its JSON Schema is what the model must return."""

from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Kind(StrEnum):
    """What the item is."""

    bug = "bug"
    config_change = "config_change"
    task = "task"
    feature_request = "feature_request"
    feedback = "feedback"
    risk = "risk"
    info = "info"


class State(StrEnum):
    """What we do with the item."""

    do_now = "do_now"
    scheduled = "scheduled"
    waiting_on_client = "waiting_on_client"
    on_hold = "on_hold"
    do_not_do = "do_not_do"
    no_action = "no_action"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(StrictModel):
    speaker: str = Field(description="Speaker label exactly as in the transcript, e.g. 'Kasia'.")
    quote: str = Field(
        description="Verbatim fragment of ONE utterance of that speaker, copied character by character."
    )


class ActionItem(StrictModel):
    id: str = Field(description="A01, A02, ...")
    title: str = Field(description="Short imperative title in Polish.")
    details: str = Field(description="1-3 sentences in Polish: what exactly and why.")
    kind: Kind
    state: State
    owner: str | None = Field(description="Who must act (person or team), null if nobody.")
    due_date: date | None = Field(description="Resolved with the provided calendar; null if not stated.")
    due_text: str | None = Field(description="Deadline wording from the call, e.g. 'do czwartku'.")
    condition: str | None = Field(description="What it depends on / what triggers it.")
    constraints: list[str] = Field(description="Explicit limits from the call, e.g. 'przypomnieć tylko raz'.")
    approval_by: str | None = Field(description="Who must approve before acting, if anyone.")
    final_value: str | None = Field(description="For decisions changed during the call: the final version.")
    superseded: list[str] = Field(description="Earlier versions replaced later in the call.")
    depends_on: list[str] = Field(description="Ids of items this one depends on.")
    evidence: list[Evidence] = Field(description="At least one verbatim quote supporting the item.")


class Guardrail(StrictModel):
    rule: str = Field(description="Prohibition or freeze in Polish, e.g. 'Nie włączać Opla'.")
    until: str | None = Field(description="Until when / until what event it holds.")
    approval_by: str | None = Field(description="Who can lift it.")
    evidence: list[Evidence]


class Draft(StrictModel):
    to: str = Field(description="Recipient (person) — only someone the call says we should contact.")
    subject: str
    body: str = Field(description="Message in Polish; no promises beyond what was agreed in the call.")
    send_when: str = Field(description="Condition or date for sending; drafts are never sent automatically.")
    related_items: list[str] = Field(description="Ids of the items this message is about.")


class MeetingExtraction(StrictModel):
    meeting_date: date
    client: str
    participants: list[str]
    summary: str = Field(description="3-5 sentences in Polish.")
    items: list[ActionItem]
    guardrails: list[Guardrail]
    drafts: list[Draft]
    assumptions: list[str] = Field(
        description="Ambiguities you resolved yourself, each with the chosen reading."
    )
