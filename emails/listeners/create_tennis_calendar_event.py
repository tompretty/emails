import re

from ..models import CalendarEvent, Email
from ..services import GoogleCalendarService
from .listener import EmailListener


class CreateTennisCalendarEventListener(EmailListener):
    def __init__(self, calendar: GoogleCalendarService) -> None:
        super().__init__()
        self._calendar = calendar

    def notify(self, email: Email):
        if _is_chandos_booking_email(email):
            self._create_calendar_event(email)

    def _create_calendar_event(self, email):
        event = _get_event(email)
        self._calendar.create_event(event)


# ---- Helpers ---- #


def _is_chandos_booking_email(email: Email) -> bool:
    return _is_from_chandos(email.sender) and _is_booking_subject(email.subject)


def _is_from_chandos(sender: str) -> bool:
    return sender == "chandosltc@clubsolution.co.uk"


def _is_booking_subject(subject: str) -> bool:
    return subject.startswith("Booking Confirmation") or subject.startswith(
        "Your Online Booking"
    )


def _get_event(email: Email):
    opponent = _get_opponent(email.body)
    court = _get_court(email.body)
    start, end = _get_time(email.body)

    return CalendarEvent(
        summary=f"Tennis - {opponent} (court {court})",
        location=CHANDOS_LOCATION,
        start=start,
        end=end,
    )


def _get_opponent(body: str) -> str:
    match = re.search(OPPONENT_REGEX, body)
    return match.groups()[0]


def _get_court(body: str) -> str:
    match = re.search(COURT_REGEX, body)
    return match.groups()[0]


def _get_time(body: str) -> str:
    match = re.search(TIME_REGEX, body)
    day, month, year, start, end = match.groups()

    return (
        f"{year}-{month}-{day}T{start}:00:00",
        f"{year}-{month}-{day}T{end}:00:00",
    )


# ---- Regexes ---- #

OPPONENT_REGEX = "\r\n.*, (.*) has added the following"

COURT_REGEX = r"COURT (\d) (:?INDOOR)?"

TIME_REGEX = r"Date: (\d\d)-(\d\d)-(\d\d\d\d) at (\d\d):00 - (\d\d):00"

# ---- Consts ---- #

CHANDOS_LOCATION = "Chandos Lawn Tennis 120 East End Road, London, N2 0RZ, England"
