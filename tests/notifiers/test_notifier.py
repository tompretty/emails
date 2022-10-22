from emails.listeners import EmailListener
from emails.models import Email
from emails.notifiers import EmailNotifier


class WasNotifiedListener(EmailListener):
    def __init__(self) -> None:
        super().__init__()
        self.was_notified = False

    def notify(self, email: Email) -> None:
        self.was_notified = True


def test_notifier_notifies_all_listeners():
    notifier = EmailNotifier()
    l1 = WasNotifiedListener()
    l2 = WasNotifiedListener()
    notifier.subscribe(l1)
    notifier.subscribe(l2)
    email = (
        Email(
            sender="sender@example.com",
            receiver="receiver@example.com",
            subject="Subject",
            body="Body",
        ),
    )

    notifier.notify(email)

    assert l1.was_notified
    assert l2.was_notified
