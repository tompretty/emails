from __future__ import print_function

import base64
import os.path
import re
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ..models import Email
from .gmail_emails import GmailEmailsService


class GmailApiEmailsService(GmailEmailsService):
    def __init__(self):
        self.service = build("gmail", "v1", credentials=_get_api_credentials())

    def fetch_emails(self, history_id: str):
        emails = []
        message_ids = self._get_message_ids(history_id)
        for message_id in message_ids:
            email = self._get_message(message_id)
            emails.append(email)
        return emails

    def _get_message_ids(self, history_id: str):
        message_ids = []
        history = self._get_history(history_id)
        for entry in history:
            messages = entry.get("messages", [])
            for message in messages:
                message_ids.append(message["id"])
        return message_ids

    def _get_message(self, message_id: str) -> Email:
        result = (
            self.service.users().messages().get(userId="me", id=message_id).execute()
        )
        payload = result["payload"]
        return _parse_email_from_payload(payload)

    def _get_history(self, history_id: str):
        results = (
            self.service.users()
            .history()
            .list(userId="me", startHistoryId=history_id)
            .execute()
        )

        return results.get("history", [])


# ---- Helpers ---- #


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _get_api_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def _parse_email_from_payload(payload):
    headers = _parse_email_headers_from_payload(payload)
    body = _parse_email_body_from_payload(payload)

    return Email(
        sender=headers.sender,
        receiver=headers.receiver,
        subject=headers.subject,
        body=body,
    )


def _parse_email_body_from_payload(payload):
    if "parts" in payload:
        data = payload["parts"][0]["body"]["data"]
    else:
        data = payload["body"]["data"]
    return base64.urlsafe_b64decode((data)).decode("utf-8")


@dataclass
class EmailHeaders:
    sender: str
    receiver: str
    subject: str


def _parse_email_headers_from_payload(payload):
    sender = ""
    receiver = ""
    subject = ""
    for header in payload["headers"]:
        if header["name"] == "From":
            sender = _parse_email_from_mailbox(header["value"])
        if header["name"] == "To":
            receiver = _parse_email_from_mailbox(header["value"])
        if header["name"] == "Subject":
            subject = header["value"]

    return EmailHeaders(sender=sender, receiver=receiver, subject=subject)


def _parse_email_from_mailbox(mailbox: str) -> str:
    match = re.match(MAILBOX_REGEX, mailbox)
    if match:
        return match.group(1)
    else:
        return mailbox


MAILBOX_REGEX = r".*<(.*)>.*"
