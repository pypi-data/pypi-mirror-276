import logging
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.oauth2 import service_account
from google.pubsub_v1.types import pubsub
from google.api_core.exceptions import NotFound
from google.auth import default

logger = logging.getLogger(__name__)


class PubSubClient:
    """PubSubClient v0.1.4"""

    def __init__(
        self,
        project_id: str,
        topic_name: str,
        keyfile_path: None | str = None,
        subscription_name: None | str = None,  # publisher에서 필요없음
    ):
        if keyfile_path:
            logger.info("Creating credentials with SA keyfile..")
            self._credentials = service_account.Credentials.from_service_account_file(
                keyfile_path
            )
        else:
            # https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
            logger.info(
                "Creating credentials with Application Default Credentials (ADC).."
            )
            self._credentials, _ = default()

        self._project_id = project_id
        self._topic_name = topic_name
        self._subscription_name = subscription_name

        try:
            logger.info("Creating Pub/Sub topic and subscription if not exist")
            if topic_name:
                logger.info(f"Creating publisher client")
                self._publisher_client: PublisherClient = pubsub_v1.PublisherClient(
                    credentials=self._credentials
                )
                logger.info(f"Creating topic")
                self._create_topic()
            if subscription_name:
                logger.info(f"Creating subscriber client")
                self._subscriber_client: SubscriberClient = pubsub_v1.SubscriberClient(
                    credentials=self._credentials
                )
                logger.info(f"Creating subscription")
                self._create_subscription()
        except Exception:
            logger.exception("Failed to create Pub/Sub topic and subscription")
            raise

    @property
    def _topic_path(self):
        return self._publisher_client.topic_path(self._project_id, self._topic_name)

    @property
    def _subscription_path(self):
        return self._subscriber_client.subscription_path(
            self._project_id, self._subscription_name
        )

    def _create_topic(self):
        # Check if the topic exists, if not, create the topic.
        try:
            self.topic: pubsub.Topic = self._publisher_client.get_topic(
                request={"topic": self._topic_path}
            )
        except NotFound:
            logger.info(
                f"Topic ({self._topic_path=}) hasn't been found. Create the topic..."
            )
            self.topic: pubsub.Topic = self._publisher_client.create_topic(
                request={"name": self._topic_path}
            )
            logger.info(f"{self.topic.name} topic has been created.")
        except Exception:
            logger.exception(f"Failed to get topic ({self._topic_path=})")
            raise

    def _create_subscription(self):
        # Check if the subscription exists, if not, create the subscription.
        try:
            self.subscription = self._subscriber_client.get_subscription(
                request={"subscription": self._subscription_path}
            )
        except NotFound:
            logger.info(
                f"Subscription ({self._subscription_path=}) hasn't been found. Create the subscription..."
            )

            self.subscription = self._subscriber_client.create_subscription(
                request={"name": self._subscription_path, "topic": self._topic_path}
                # request={"name": self._subscription_path, "topic": self._topic_name}
            )
            logger.info(f"{self.subscription.name} subscription has been created.")

        except Exception:
            logger.exception(f"Failed to get subscription ({self._subscription_path=})")
            raise

    def publish(self, msg: str | bytes) -> None:
        # Convert the message data to bytes.
        if isinstance(msg, str):
            msg_bytes: bytes = msg.encode("utf-8")
        else:
            msg_bytes = msg

        # Publish the message to the topic.
        future = self._publisher_client.publish(self._topic_path, data=msg_bytes)

        # block until the message has been published successfully
        message_id = future.result()

        logger.info(
            f"Message '{msg}' published to topic {self._topic_name} with message ID {message_id}"
        )

    def read_pubsub_messages(self, callback: callable) -> None:
        def wrapper(message):
            callback(message)
            # Acknowledge the message to mark it as processed
            message.ack()

        # Subscribe to the specified subscription and start receiving messages
        logger.info(
            f"Subscribing to listen for messages on {self._subscription_path}...\n"
        )
        streaming_pull_future = self._subscriber_client.subscribe(
            self._subscription_path, callback=wrapper
        )

        # Keep the script running to continue receiving messages
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
