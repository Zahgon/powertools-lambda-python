from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper
from aws_lambda_powertools.utilities.data_classes.shared_functions import base64_decode

if TYPE_CHECKING:
    from collections.abc import Iterator


class ActiveMQMessage(DictWrapper):
    @property
    def message_id(self) -> str:
        """Unique identifier for the message"""
        pass

    @property
    def message_type(self) -> str:
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
        pass

    @property
    def connection_id(self) -> str:
        pass

    @property
    def redelivered(self) -> bool:
        """true if the message is being resent to the consumer"""
        pass

    @property
    def timestamp(self) -> int:
        """Time in milliseconds."""
        return self["timestamp"]

    @property
    def broker_in_time(self) -> int:
        """Time stamp (in milliseconds) for when the message arrived at the broker."""
        pass

    @property
    def broker_out_time(self) -> int:
        """Time stamp (in milliseconds) for when the message left the broker."""
        pass

    @property
    def properties(self) -> dict:
        """Custom properties"""
        pass

    @property
    def destination_physicalname(self) -> str:
        pass

    @property
    def delivery_mode(self) -> int | None:
        """persistent or non-persistent delivery"""
        pass

    @property
    def correlation_id(self) -> str | None:
        """User defined correlation id"""
        pass

    @property
    def reply_to(self) -> str | None:
        """User defined reply to"""
        pass

    @property
    def get_type(self) -> str | None:
        """User defined message type"""
        pass

    @property
    def expiration(self) -> int | None:
        """Expiration attribute whose value is given in milliseconds"""
        pass

    @property
    def priority(self) -> int | None:
        """
        JMS defines a ten-level priority value, with 0 as the lowest priority and 9
        as the highest. In addition, clients should consider priorities 0-4 as
        gradations of normal priority and priorities 5-9 as gradations of expedited
        priority.

        JMS does not require that a provider strictly implement priority ordering
        of messages; however, it should do its best to deliver expedited messages
        ahead of normal messages.
        """
        pass


class ActiveMQEvent(DictWrapper):
    """Represents an Active MQ event sent to Lambda

    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html
    - https://aws.amazon.com/blogs/compute/using-amazon-mq-as-an-event-source-for-aws-lambda/
    """

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self._messages: Iterator[ActiveMQMessage] | None = None

    @property
    def event_source(self) -> str:
        return self["eventSource"]

    @property
    def event_source_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the event source"""
        pass

    @property
    def messages(self) -> Iterator[ActiveMQMessage]:
        pass

    @property
    def message(self) -> ActiveMQMessage:
        """
        Returns the next ActiveMQ message using an iterator

        Returns
        -------
        ActiveMQMessage
            The next activemq message.

        Raises
        ------
        StopIteration
            If there are no more records available.

        """
        pass
