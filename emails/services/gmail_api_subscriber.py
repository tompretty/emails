import json

from google.cloud import pubsub_v1

from .gmail_subscriber import GmailSubscriberService

project_id = "c0e-tennis-emails"
subscription_id = "emails-sub"


class GmailApiSubscriberService(GmailSubscriberService):
    def __init__(self) -> None:
        super().__init__()
        self._callback = None

    def subscribe(self, callback) -> None:
        self._callback = callback

        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        print(f"Listening for messages on {subscription_path}..\n")

        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=self._on_message
        )

        with subscriber:
            streaming_pull_future.result()

    def _on_message(self, message: pubsub_v1.subscriber.message.Message) -> None:
        message.ack()

        data = json.loads(message.data)
        history_id = data["historyId"]

        self._callback(history_id)
