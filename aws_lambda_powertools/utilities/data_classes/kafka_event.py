from __future__ import annotations

import base64
from functools import cached_property
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.shared.functions import decode_header_bytes
from aws_lambda_powertools.utilities.data_classes.common import CaseInsensitiveDict, DictWrapper

if TYPE_CHECKING:
    from collections.abc import Iterator


class KafkaEventRecordSchemaMetadata(DictWrapper):
    @property
    def data_format(self) -> str | None:
        """The data format of the Kafka record."""
        pass

    @property
    def schema_id(self) -> str | None:
        """The schema id of the Kafka record."""
        pass


class KafkaEventRecordBase(DictWrapper):
    @property
    def topic(self) -> str:
        """The Kafka topic."""
        pass

    @property
    def partition(self) -> int:
        """The Kafka record parition."""
        pass

    @property
    def offset(self) -> int:
        """The Kafka record offset."""
        pass

    @property
    def timestamp(self) -> int:
        """The Kafka record timestamp."""
        return self["timestamp"]

    @property
    def timestamp_type(self) -> str:
        """The Kafka record timestamp type."""
        pass

    @property
    def key_schema_metadata(self) -> KafkaEventRecordSchemaMetadata | None:
        """The metadata of the Key Kafka record."""
        pass

    @property
    def value_schema_metadata(self) -> KafkaEventRecordSchemaMetadata | None:
        """The metadata of the Value Kafka record."""
        pass


class KafkaEventRecord(KafkaEventRecordBase):
    @property
    def key(self) -> str | None:
        """
        The raw (base64 encoded) Kafka record key.

        This key is optional; if not provided,
        a round-robin algorithm will be used to determine
        the partition for the message.
        """
        pass

    @property
    def decoded_key(self) -> bytes | None:
        """
        Decode the base64 encoded key as bytes.

        If the key is not provided, this will return None.
        """
        pass

    @property
    def value(self) -> str:
        """The raw (base64 encoded) Kafka record value."""
        pass

    @property
    def decoded_value(self) -> bytes:
        """Decodes the base64 encoded value as bytes."""
        pass

    @cached_property
    def json_value(self) -> Any:
        """Decodes the text encoded data as JSON."""
        pass

    @property
    def headers(self) -> list[dict[str, list[int]]]:
        """The raw Kafka record headers."""
        pass

    @cached_property
    def decoded_headers(self) -> dict[str, bytes]:
        """Decodes the headers as a single dictionary."""
        pass


class KafkaEventBase(DictWrapper):
    @property
    def event_source(self) -> str:
        """The AWS service from which the Kafka event record originated."""
        return self["eventSource"]

    @property
    def event_source_arn(self) -> str | None:
        """The AWS service ARN from which the Kafka event record originated, mandatory for AWS MSK."""
        pass

    @property
    def bootstrap_servers(self) -> str:
        """The Kafka bootstrap URL."""
        pass

    @property
    def decoded_bootstrap_servers(self) -> list[str]:
        """The decoded Kafka bootstrap URL."""
        pass


class KafkaEvent(KafkaEventBase):
    """Self-managed or MSK Apache Kafka event trigger
    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html
    - https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html
    """

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self._records: Iterator[KafkaEventRecord] | None = None

    @property
    def records(self) -> Iterator[KafkaEventRecord]:
        """The Kafka records."""
        pass

    @property
    def record(self) -> KafkaEventRecord:
        """
        Returns the next Kafka record using an iterator.

        Returns
        -------
        KafkaEventRecord
            The next Kafka record.

        Raises
        ------
        StopIteration
            If there are no more records available.

        """
        pass
