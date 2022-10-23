from dataclasses import dataclass


@dataclass
class CalendarEvent:
    summary: str
    location: str
    start: str
    end: str
