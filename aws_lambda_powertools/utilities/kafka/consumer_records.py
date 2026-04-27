from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.shared.functions import decode_header_bytes
from aws_lambda_powertools.utilities.data_classes.common import CaseInsensitiveDict
from aws_lambda_powertools.utilities.data_classes.kafka_event import KafkaEventBase, KafkaEventRecordBase
from aws_lambda_powertools.utilities.kafka.deserializer.deserializer import get_deserializer
from aws_lambda_powertools.utilities.kafka.serialization.serialization import serialize_to_output_type

if TYPE_CHECKING:
    from collections.abc import Iterator

    from aws_lambda_powertools.utilities.kafka.schema_config import SchemaConfig

logger = logging.getLogger(__name__)


class ConsumerRecordRecords(KafkaEventRecordBase):
    """
    A Kafka Consumer Record
    """

    def __init__(self, data: dict[str, Any], schema_config: SchemaConfig | None = None):
        super().__init__(data)
        self.schema_config = schema_config

    @cached_property
    def key(self) -> Any:
        pass

    @cached_property
    def value(self) -> Any:
        pass

    @property
    def original_value(self) -> str:
        """The original (base64 encoded) Kafka record value."""
        pass

    @property
    def original_key(self) -> str | None:
        """
        The original (base64 encoded) Kafka record key.

        This key is optional; if not provided,
        a round-robin algorithm will be used to determine
        the partition for the message.
        """
        pass

    @property
    def original_headers(self) -> list[dict[str, list[int]]]:
        """The raw Kafka record headers."""
        pass

    @cached_property
    def headers(self) -> dict[str, bytes]:
        """Decodes the headers as a single dictionary."""
        pass


class ConsumerRecords(KafkaEventBase):
    """Self-managed or MSK Apache Kafka event trigger
    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html
    - https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html
    """

    def __init__(self, data: dict[str, Any], schema_config: SchemaConfig | None = None):
        super().__init__(data)
        self._records: Iterator[ConsumerRecordRecords] | None = None
        self.schema_config = schema_config

    @property
    def records(self) -> Iterator[ConsumerRecordRecords]:
        """The Kafka records."""
        pass

    @property
    def record(self) -> ConsumerRecordRecords:
        """
        Returns the next Kafka record using an iterator.

        Returns
        -------
        ConsumerRecordRecords
            The next Kafka record.

        Raises
        ------
        StopIteration
            If there are no more records available.

        """
        pass
