from emails.listeners import ConsoleLoggingListener, LoggingListener
from emails.notifiers import GmailNotifier
from emails.services import GmailApiEmailsService, GmailApiSubscriberService

notifier = GmailNotifier(GmailApiSubscriberService(), GmailApiEmailsService())
notifier.subscribe(LoggingListener())
notifier.subscribe(ConsoleLoggingListener())
notifier.start()
