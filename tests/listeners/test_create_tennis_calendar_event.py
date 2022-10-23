from datetime import datetime

from emails.listeners import CreateTennisCalendarEventListener
from emails.models import CalendarEvent, Email
from emails.services import GoogleCalendarService

from ..fixtures.emails.chandos import (
    Person,
    get_booking_added_indoor,
    get_booking_added_outdoor,
    get_booking_created_indoor,
)


class FakeGoogleCalendarService(GoogleCalendarService):
    def __init__(self) -> None:
        super().__init__()
        self.event = None

    def create_event(self, event: CalendarEvent) -> None:
        self.event = event


def test_create_tennis_calendar_event_listener_ignores_emails_that_are_not_from_chandos():
    email = Email(
        sender="sender@example.com",
        receiver="receiver@example.com",
        subject="First one!",
        body="The first email",
    )
    fake_calendar = FakeGoogleCalendarService()
    listener = CreateTennisCalendarEventListener(fake_calendar)

    listener.notify(email)

    assert fake_calendar.event == None


def test_create_tennis_calendar_event_creates_an_event_for_a_created_indoor_booking():
    email = get_booking_created_indoor(
        opponent=Person(first_name="First", last_name="Last"),
        court=1,
        start=datetime(2022, 1, 1, 9),
    )
    fake_calendar = FakeGoogleCalendarService()
    listener = CreateTennisCalendarEventListener(fake_calendar)

    listener.notify(email)

    assert fake_calendar.event != None
    assert fake_calendar.event.summary == "Tennis - First (court 1)"
    assert fake_calendar.event.start == "2022-01-01T09:00:00"
    assert fake_calendar.event.end == "2022-01-01T10:00:00"


def test_create_tennis_calendar_event_creates_an_event_for_an_added_indoor_booking():
    email = get_booking_added_indoor(
        opponent=Person(first_name="First", last_name="Last"),
        court=1,
        start=datetime(2022, 1, 1, 9),
    )
    fake_calendar = FakeGoogleCalendarService()
    listener = CreateTennisCalendarEventListener(fake_calendar)

    listener.notify(email)

    assert fake_calendar.event != None
    assert fake_calendar.event.summary == "Tennis - First (court 1)"
    assert fake_calendar.event.start == "2022-01-01T09:00:00"
    assert fake_calendar.event.end == "2022-01-01T10:00:00"


def test_create_tennis_calendar_event_creates_an_event_for_an_added_outdoor_booking():
    email = get_booking_added_outdoor(
        opponent=Person(first_name="First", last_name="Last"),
        court=5,
        start=datetime(2022, 1, 1, 9),
    )
    fake_calendar = FakeGoogleCalendarService()
    listener = CreateTennisCalendarEventListener(fake_calendar)

    listener.notify(email)

    assert fake_calendar.event != None
    assert fake_calendar.event.summary == "Tennis - First (court 5)"
    assert fake_calendar.event.start == "2022-01-01T09:00:00"
    assert fake_calendar.event.end == "2022-01-01T10:00:00"


# test cases:
# 1. opponent added multiple (inside & outisde?)
# 1. me added inside
# 1. me added outside
# 1. me added multiple
# 1. non chandos booking email
