from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Creates a simple event in the user's calendar.
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename="credentials.json", scopes=SCOPES
    )

    try:
        service = build("calendar", "v3", credentials=credentials)

        event = {
            "summary": "Tennis - Test (court 5)",
            "location": "Chandos Lawn Tennis 120 East End Road, London, N2 0RZ, England",
            "start": {
                "dateTime": "2022-09-20T08:00:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": "2022-09-20T10:00:00",
                "timeZone": "Europe/London",
            },
            "reminders": {
                "useDefault": True,
            },
        }
        # Call the Calendar API
        print("Creating an event")
        event_result = (
            service.events()
            .insert(calendarId="tompretty2@gmail.com", body=event)
            .execute()
        )

        print("Event created: %s" % (event_result.get("htmlLink")))

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
