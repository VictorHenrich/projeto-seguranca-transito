from typing import Any

from server import App
from server.amqp import AMQPConsumer



@App.amqp.add_consumer(
    "occurrences_integration",
    "queue_occurrences_integration",
    ack=True
)
class ConsumerOccurrencesIntegration(AMQPConsumer):
    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        pass