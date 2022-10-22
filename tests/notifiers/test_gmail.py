from typing import List

from emails.listeners import LoggingListener
from emails.models import Email
from emails.notifiers import GmailNotifier
from emails.services import GmailEmailsService, GmailService, GmailSubscriberService


class FakeGmailSubscriberService(GmailSubscriberService):
    def subscribe(self, callback):
        callback("HISTORY_ID")


class FakeGmailEmailsService(GmailEmailsService):
    def __init__(self, emails: List[Email]):
        super().__init__()
        self.emails = emails

    def fetch_emails(self, history_id: str):
        if history_id == "HISTORY_ID":
            return self.emails
        return []


def test_gmail_notifier_notifies_listeners_with_all_messages_from_the_gmail_service():
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
    notifier = GmailNotifier(
        FakeGmailSubscriberService(), FakeGmailEmailsService(emails)
    )
    listener = LoggingListener()
    notifier.subscribe(listener)

    notifier.start()

    assert listener.log == emails
