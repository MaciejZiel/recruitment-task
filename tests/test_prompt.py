from datetime import date

from callflow.prompt import build_calendar, build_user_message


def test_calendar_names_weekdays_and_marks_meeting_day():
    calendar = build_calendar(date(2026, 10, 6)).splitlines()

    assert "2026-10-06 wtorek  <- meeting day" in calendar
    assert "2026-10-08 czwartek" in calendar
    assert "2026-10-12 poniedziałek" in calendar
    assert calendar[0] == "2026-09-29 wtorek"


def test_user_message_wraps_transcript_as_data():
    message = build_user_message("**A:** Cześć.", date(2026, 10, 6), vendor="Rinvo")

    assert message.startswith("VENDOR: Rinvo\nMEETING_DATE: 2026-10-06 (wtorek)")
    assert "<<<TRANSCRIPT\n**A:** Cześć.\nTRANSCRIPT>>>" in message


def test_unknown_meeting_date_asks_not_to_guess_and_has_no_calendar():
    message = build_user_message("**A:** x", None, vendor="Rinvo")

    assert "MEETING_DATE: unknown" in message
    assert "CALENDAR" not in message
