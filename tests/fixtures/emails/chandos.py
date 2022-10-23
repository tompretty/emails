from dataclasses import dataclass
from datetime import datetime

from emails.models import Email


@dataclass
class Person:
    first_name: str
    last_name: str


def get_booking_created_indoor(opponent: Person, court: int, start: datetime) -> Email:
    return Email(
        sender="chandosltc@clubsolution.co.uk",
        receiver="tompretty2@gmail.com",
        subject="Your Online Booking - Order no. 100000",
        body=f"To Pretty, Tom\r\n\r\nWe confirm your online booking\r\nBooking\r\nCTS 1 - 4 INDOOR /  GYM: COURT {court} INDOOR  - All names of players\r\n{_get_date(start)} £  12.00 \r\nTOTAL £  12.00 \r\nPaid Online Today\r\nReference: 100000 \r\n\r\n\r\n\r\nSpecification of booking\r\nLocation: CTS 1 - 4 INDOOR /  GYM: COURT {court} INDOOR  - All names of players \r\nDate: {_get_date(start)} \r\nOpponent: {opponent.last_name}, {opponent.first_name} \r\nPrice: £  12.00 \r\nYou will only get a refund if booking is deleted up to 48 hours before booking start. \r\nClub terms and conditions applies to all court bookings.You are responsible for leaving the court appropriately when your court time is finished. \r\n\r\n\r\nPlease  note there will be a late cancellation and no show fee applicable on outdoor courts see club rule 4.1 \r\n \r\n\r\n\r\n\r\nRegards,\r\nChandos LTC\r\n120 East End Road\r\nN2 0RZ \r\nPhone: 020 8343 1755.  020 8346 2856\r\nCompany Reg.: 12345679\r\n\r\n\r\n \r\n\r\n\r\n",
    )


def get_booking_confirmation_outdoor():
    pass


def get_booking_added_indoor(opponent: Person, court: int, start: datetime) -> Email:
    date = start.strftime("%d-%m-%Y")

    return Email(
        sender="chandosltc@clubsolution.co.uk",
        receiver="tompretty2@gmail.com",
        subject="Booking Confirmation",
        body=f"To Pretty, Tom\r\n{opponent.last_name}, {opponent.first_name} has added the following booking with you as opponent:\r\nLocation: CTS 1 - 4 INDOOR /  GYM: COURT {court} INDOOR  - All names of players \r\nDate: {date} at {str(start.hour).zfill(2)}:00 - {str(start.hour + 1).zfill(2)}:00 \r\nPrice: £  12.00 \r\nYou will only get a refund if booking is deleted up to 48 hours before booking start. \r\nClub terms and conditions applies to all court bookings.You are responsible for leaving the court appropriately when your court time is finished. \r\n\r\nPlease  note there will be a late cancellation and no show fee applicable on outdoor courts see club rule 4.1 \r\n\r\n\r\n\r\nRegards,\r\nChandos LTC\r\n120 East End Road\r\nN2 0RZ \r\nPhone: 020 8343 1755.  020 8346 2856\r\nCompany Reg.: 12345679\r\n\r\n \r\n\r\n\r\n\r\n",
    )


def get_booking_added_outdoor(opponent: Person, court: int, start: datetime):
    date = start.strftime("%d-%m-%Y")

    return Email(
        sender="chandosltc@clubsolution.co.uk",
        receiver="tompretty2@gmail.com",
        subject="Booking Confirmation",
        body=f"To Pretty, Tom\r\n{opponent.last_name}, {opponent.first_name} has added the following booking with you as opponent:\r\nLocation: CTS 5 - 8 OUTDOOR / MINI TENNIS: COURT {court} -YOU  WILL be charged IF YOU DO NOT CANCEL \r\nDate: {date} at {str(start.hour).zfill(2)}:00 - {str(start.hour + 1).zfill(2)}:00 \r\nClub terms and conditions applies to all court bookings.You are responsible for leaving the court appropriately when your court time is finished. \r\n\r\nPlease  note there will be a late cancellation and no show fee applicable on outdoor courts see club rule 4.1 \r\n\r\n\r\n\r\nRegards,\r\nChandos LTC\r\n120 East End Road\r\nN2 0RZ \r\nPhone: 020 8343 1755.  020 8346 2856\r\nCompany Reg.: 12345679\r\n\r\n \r\n\r\n\r\n\r\n",
    )


def _get_date(start: datetime) -> str:
    return f"{start.strftime('%d-%m-%Y')} at {str(start.hour).zfill(2)}:00 - {str(start.hour + 1).zfill(2)}:00"
