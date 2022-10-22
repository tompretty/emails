from ..models import Email
from .listener import EmailListener


class ConsoleLoggingListener(EmailListener):
    def notify(self, email: Email):
        print(
            f"""
 Received email:
     from:       {email.sender}
     to:         {email.receiver}
     subject:    {email.subject}
     body:
          {email.body}
"""
        )
