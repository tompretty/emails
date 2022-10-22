from ..services import GmailEmailsService, GmailSubscriberService
from .notifier import EmailNotifier


class GmailNotifier(EmailNotifier):
    def __init__(self, subscriber: GmailSubscriberService, emails: GmailEmailsService):
        super().__init__()
        self._subscriber = subscriber
        self._emails = emails

    def start(self):
        self._subscribe()

    def _subscribe(self):
        self._subscriber.subscribe(self._on_notification)

    def _on_notification(self, history_id):
        emails = self._emails.fetch_emails(history_id)
        for email in emails:
            self.notify(email)
