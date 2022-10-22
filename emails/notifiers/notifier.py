from typing import List

from ..listeners import EmailListener
from ..models import Email


class EmailNotifier:
    def __init__(self):
        self._listeners: List[EmailListener] = []

    def subscribe(self, listener: EmailListener) -> None:
        self._listeners.append(listener)

    def notify(self, email: Email):
        for listener in self._listeners:
            listener.notify(email)

    # # todo: make this abstract
    def start(self):
        pass
