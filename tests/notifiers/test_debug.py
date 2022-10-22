from typing import List

from emails.listeners import LoggingListener
from emails.models import Email
from emails.notifiers import DebugNotifier


def test_debug_notifier_notifies_listeners_with_fake_email_data_on_start():
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

    notifier = DebugNotifier(emails)
    listener = LoggingListener()
    notifier.subscribe(listener)

    notifier.start()

    assert listener.log == emails
