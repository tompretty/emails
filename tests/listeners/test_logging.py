from typing import List

from emails.listeners import LoggingListener
from emails.models import Email


def test_logging_listener_logs_all_emails():
    emails = [
        Email(
            sender="sender@example.com",
            receiver="receiver@example.com",
            subject="First one!",
            body="The first email",
        ),
        Email(
            sender="sender@example.com",
            receiver="receiver@example.com",
            subject="Second one!",
            body="The second email",
        ),
    ]
    listener = LoggingListener()

    listener.notify(emails[0])
    listener.notify(emails[1])

    assert listener.log == emails
