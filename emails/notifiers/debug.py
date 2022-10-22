from typing import List

from ..models import Email
from .notifier import EmailNotifier


class DebugNotifier(EmailNotifier):
    def __init__(self, emails: List[Email]):
        super().__init__()
        self._emails = emails

    def start(self):
        for email in self._emails:
            self.notify(email)
