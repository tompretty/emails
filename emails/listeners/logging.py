from typing import List

from ..models import Email
from .listener import EmailListener


class LoggingListener(EmailListener):
    def __init__(self) -> None:
        super().__init__()
        self.log: List[Email] = []

    def notify(self, email: Email):
        self.log.append(email)
