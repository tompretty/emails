from emails.headers import parse_gmail_metadata


def test_parse_gmail_metadata_parses_sender():
    headers = [
        {"name": "From", "value": "email@example.com"},
    ]

    metadata = parse_gmail_metadata(headers)

    assert metadata.sender == "email@example.com"


def test_parse_gmail_metadata_parses_sender_using_nickname_format():
    headers = [
        {"name": "From", "value": "Sender <email@example.com>"},
    ]

    metadata = parse_gmail_metadata(headers)

    assert metadata.sender == "email@example.com"



def test_parse_gmail_metadata_parses_receiver():
    headers = [
        {"name": "To", "value": "email@example.com"},
    ]

    metadata = parse_gmail_metadata(headers)

    assert metadata.receiver == "email@example.com"

def test_parse_gmail_metadata_parses_receiver_using_nickname_format():
    headers = [
        {"name": "To", "value": "Receiver <email@example.com>"},
    ]

    metadata = parse_gmail_metadata(headers)

    assert metadata.receiver == "email@example.com"


def test_parse_gmail_metadata_parses_subject():
    headers = [
        {"name": "Subject", "value": "Example subject"},
    ]

    metadata = parse_gmail_metadata(headers)

    assert metadata.subject == "Example subject"
