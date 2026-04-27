from __future__ import annotations

from functools import cached_property
from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper
from aws_lambda_powertools.utilities.data_classes.shared_functions import base64_decode


class BasicProperties(DictWrapper):
    @property
    def content_type(self) -> str:
        pass

    @property
    def content_encoding(self) -> str:
        pass

    @property
    def headers(self) -> dict[str, Any]:
        pass

    @property
    def delivery_mode(self) -> int:
        pass

    @property
    def priority(self) -> int:
        pass

    @property
    def correlation_id(self) -> str:
        pass

    @property
    def reply_to(self) -> str:
        pass

    @property
    def expiration(self) -> str:
        pass

    @property
    def message_id(self) -> str:
        pass

    @property
    def timestamp(self) -> str:
        return self["timestamp"]

    @property
    def get_type(self) -> str:
        pass

    @property
    def user_id(self) -> str:
        pass

    @property
    def app_id(self) -> str:
        pass

    @property
    def cluster_id(self) -> str:
        pass

    @property
    def body_size(self) -> int:
        pass


class RabbitMessage(DictWrapper):
    @property
    def basic_properties(self) -> BasicProperties:
        pass

    @property
    def redelivered(self) -> bool:
        pass

    @property
    def data(self) -> str:
        pass

    @property
    def decoded_data(self) -> str:
        """Decodes the data as a str"""
        pass

    @cached_property
    def json_data(self) -> Any:
        """Parses the data as json"""
        pass


class RabbitMQEvent(DictWrapper):
    """Represents a Rabbit MQ event sent to Lambda

    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html
    - https://aws.amazon.com/blogs/compute/using-amazon-mq-for-rabbitmq-as-an-event-source-for-lambda/
    """

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self._rmq_messages_by_queue = {
            key: [RabbitMessage(message) for message in messages]
            for key, messages in self["rmqMessagesByQueue"].items()
        }

    @property
    def event_source(self) -> str:
        return self["eventSource"]

    @property
    def event_source_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the event source"""
        pass

    @property
    def rmq_messages_by_queue(self) -> dict[str, list[RabbitMessage]]:
        pass
