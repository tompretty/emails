import re
from dataclasses import dataclass


@dataclass
class EmailMetadata:
    sender: str
    receiver: str
    subject: str


def parse_gmail_metadata(headers) -> EmailMetadata:
    sender = ""
    receiver = ""
    subject = ""
    for header in headers:
        if header["name"] == "From":
            sender = _parse_email_from_mailbox(header["value"])
        if header["name"] == "To":
            receiver = _parse_email_from_mailbox(header["value"])
        if header["name"] == "Subject":
            subject = header["value"]

    return EmailMetadata(sender=sender, receiver=receiver, subject=subject)


def _parse_email_from_mailbox(mailbox: str) -> str:
    match = re.match(MAILBOX_REGEX, mailbox)
    if match:
        return match.group(1)
    else:
        return mailbox


MAILBOX_REGEX = r".*<(.*)>.*"
