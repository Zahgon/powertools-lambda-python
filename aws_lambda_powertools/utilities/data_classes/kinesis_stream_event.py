from __future__ import annotations

import base64
import json
import zlib
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.utilities.data_classes.cloud_watch_logs_event import (
    CloudWatchLogsDecodedData,
)
from aws_lambda_powertools.utilities.data_classes.common import DictWrapper

if TYPE_CHECKING:
    from collections.abc import Iterator


class KinesisStreamRecordPayload(DictWrapper):
    @property
    def approximate_arrival_timestamp(self) -> float:
        """The approximate time that the record was inserted into the stream"""
        pass

    @property
    def data(self) -> str:
        """The data blob"""
        pass

    @property
    def kinesis_schema_version(self) -> str:
        """Schema version for the record"""
        pass

    @property
    def partition_key(self) -> str:
        """Identifies which shard in the stream the data record is assigned to"""
        pass

    @property
    def sequence_number(self) -> str:
        """The unique identifier of the record within its shard"""
        pass

    def data_as_bytes(self) -> bytes:
        """Decode binary encoded data as bytes"""
        pass

    def data_as_text(self) -> str:
        """Decode binary encoded data as text"""
        pass

    def data_as_json(self) -> dict:
        """Decode binary encoded data as json"""
        pass

    def data_zlib_compressed_as_json(self) -> dict:
        """Decode binary encoded data as bytes"""
        pass


class KinesisStreamRecord(DictWrapper):
    @property
    def aws_region(self) -> str:
        """AWS region where the event originated eg: us-east-1"""
        pass

    @property
    def event_id(self) -> str:
        """A globally unique identifier for the event that was recorded in this stream record."""
        pass

    @property
    def event_name(self) -> str:
        """Event type eg: aws:kinesis:record"""
        pass

    @property
    def event_source(self) -> str:
        """The AWS service from which the Kinesis event originated. For Kinesis, this is aws:kinesis"""
        return self["eventSource"]

    @property
    def event_source_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the event source"""
        pass

    @property
    def event_version(self) -> str:
        """The eventVersion key value contains a major and minor version in the form <major>.<minor>."""
        pass

    @property
    def invoke_identity_arn(self) -> str:
        """The ARN for the identity used to invoke the Lambda Function"""
        pass

    @property
    def kinesis(self) -> KinesisStreamRecordPayload:
        """Underlying Kinesis record associated with the event"""
        pass


class KinesisStreamWindow(DictWrapper):
    @property
    def start(self) -> str:
        """The time window started"""
        pass

    @property
    def end(self) -> str:
        """The time window will end"""
        pass


class KinesisStreamEvent(DictWrapper):
    """Kinesis stream event

    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html
    - https://docs.aws.amazon.com/lambda/latest/dg/services-kinesis-windows.html
    """

    @property
    def records(self) -> Iterator[KinesisStreamRecord]:
        pass

    @property
    def window(self) -> KinesisStreamWindow | None:
        pass

    @property
    def state(self) -> dict[str, Any]:
        pass

    @property
    def shard_id(self) -> str | None:
        pass

    @property
    def event_source_arn(self) -> str | None:
        pass

    @property
    def is_final_invoke_for_window(self) -> bool | None:
        pass

    @property
    def is_window_terminated_early(self) -> bool | None:
        pass


def extract_cloudwatch_logs_from_event(event: KinesisStreamEvent) -> list[CloudWatchLogsDecodedData]:
    pass


def extract_cloudwatch_logs_from_record(record: KinesisStreamRecord) -> CloudWatchLogsDecodedData:
    pass
