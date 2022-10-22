from dataclasses import dataclass


@dataclass
class Email:
    sender: str
    receiver: str
    subject: str
    body: str
