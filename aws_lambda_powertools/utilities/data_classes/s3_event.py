from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import unquote_plus

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper
from aws_lambda_powertools.utilities.data_classes.event_bridge_event import (
    EventBridgeEvent,
)

if TYPE_CHECKING:
    from collections.abc import Iterator


class S3Identity(DictWrapper):
    @property
    def principal_id(self) -> str:
        pass


class S3RequestParameters(DictWrapper):
    @property
    def source_ip_address(self) -> str:
        pass


class S3EventNotificationEventBridgeBucket(DictWrapper):
    @property
    def name(self) -> str:
        pass


class S3EventBridgeNotificationObject(DictWrapper):
    @property
    def key(self) -> str:
        """Object key"""
        pass

    @property
    def size(self) -> int | None:
        """Object size. Object deletion event doesn't contain size."""
        pass

    @property
    def etag(self) -> str:
        """Object eTag. Object deletion event doesn't contain eTag; we default to empty string"""
        pass

    @property
    def version_id(self) -> str:
        """Object version ID"""
        pass

    @property
    def sequencer(self) -> str:
        """Object key"""
        pass


class S3EventBridgeNotificationDetail(DictWrapper):
    @property
    def version(self) -> str:
        """Get the detail version"""
        return self["version"]

    @property
    def bucket(self) -> S3EventNotificationEventBridgeBucket:
        """Get the bucket name for the S3 notification"""
        pass

    @property
    def object(self) -> S3EventBridgeNotificationObject:  # noqa: A003 # ignore shadowing built-in grammar
        """Get the request-id for the S3 notification"""
        pass

    @property
    def request_id(self) -> str:
        """Get the request-id for the S3 notification"""
        pass

    @property
    def requester(self) -> str:
        """Get the AWS account ID or AWS service principal of requester for the S3 notification"""
        pass

    @property
    def source_ip_address(self) -> str | None:
        """Get the source IP address of S3 request. Only present for events triggered by an S3 request."""
        pass

    @property
    def reason(self) -> str | None:
        """Get the reason for the S3 notification.

        For 'Object Created events', the S3 API used to create the object: `PutObject`, `POST Object`, `CopyObject`, or
        `CompleteMultipartUpload`. For 'Object Deleted' events, this is set to `DeleteObject` when an object is deleted
        by an S3 API call, or 'Lifecycle Expiration' when an object is deleted by an S3 Lifecycle expiration rule.
        """
        pass

    @property
    def deletion_type(self) -> str | None:
        """Get the deletion type for the S3 object in this notification.

        For 'Object Deleted' events, when an unversioned object is deleted, or a versioned object is permanently deleted
        this is set to 'Permanently Deleted'. When a delete marker is created for a versioned object, this is set to
        'Delete Marker Created'.
        """
        pass

    @property
    def restore_expiry_time(self) -> str | None:
        """Get the restore expiry time for the S3 object in this notification.

        For 'Object Restore Completed' events, the time when the temporary copy of the object will be deleted from S3.
        """
        pass

    @property
    def source_storage_class(self) -> str | None:
        """Get the source storage class of the S3 object in this notification.

        For 'Object Restore Initiated' and 'Object Restore Completed' events, the storage class of the object being
        restored.
        """
        pass

    @property
    def destination_storage_class(self) -> str | None:
        """Get the destination storage class of the S3 object in this notification.

        For 'Object Storage Class Changed' events, the new storage class of the object.
        """
        pass

    @property
    def destination_access_tier(self) -> str | None:
        """Get the destination access tier of the S3 object in this notification.

        For 'Object Access Tier Changed' events, the new access tier of the object.
        """
        pass


class S3EventBridgeNotificationEvent(EventBridgeEvent):
    """Amazon S3EventBridge Event

    Documentation:
    --------------
    - https://docs.aws.amazon.com/AmazonS3/latest/userguide/ev-events.html
    """

    @property
    def detail(self) -> S3EventBridgeNotificationDetail:  # type: ignore[override]
        """S3 notification details"""
        pass


class S3Bucket(DictWrapper):
    @property
    def name(self) -> str:
        pass

    @property
    def owner_identity(self) -> S3Identity:
        pass

    @property
    def arn(self) -> str:
        pass


class S3Object(DictWrapper):
    @property
    def key(self) -> str:
        """Object key"""
        pass

    @property
    def size(self) -> int:
        """Object byte size"""
        pass

    @property
    def etag(self) -> str:
        """Object eTag. Object deletion event doesn't contain eTag; we default to empty string"""
        pass

    @property
    def version_id(self) -> str | None:
        """Object version if bucket is versioning-enabled, otherwise null"""
        pass

    @property
    def sequencer(self) -> str:
        """A string representation of a hexadecimal value used to determine event sequence,
        only used with PUTs and DELETEs
        """
        pass


class S3Message(DictWrapper):
    @property
    def s3_schema_version(self) -> str:
        pass

    @property
    def configuration_id(self) -> str:
        """ID found in the bucket notification configuration"""
        pass

    @property
    def bucket(self) -> S3Bucket:
        pass

    @property
    def get_object(self) -> S3Object:
        """Get the `object` property as an S3Object

        Note: IntelligentTiering events use 'get_object' as the actual key name,
        while other S3 events use 'object'. This method handles both cases.
        """
        pass


class S3EventRecordGlacierRestoreEventData(DictWrapper):
    @property
    def lifecycle_restoration_expiry_time(self) -> str:
        """Time when the object restoration will be expired."""
        pass

    @property
    def lifecycle_restore_storage_class(self) -> str:
        """Source storage class for restore"""
        pass


class S3EventRecordGlacierEventData(DictWrapper):
    @property
    def restore_event_data(self) -> S3EventRecordGlacierRestoreEventData:
        """The restoreEventData key contains attributes related to your restore request.

        The glacierEventData key is only visible for s3:ObjectRestore:Completed events
        """
        pass


class S3EventRecordIntelligentTieringEventData(DictWrapper):
    @property
    def destination_access_tier(self) -> str:
        """The new access tier for the object.

        The intelligentTieringEventData key is only visible for IntelligentTiering events.
        """
        pass


class S3EventRecord(DictWrapper):
    @property
    def event_version(self) -> str:
        """The eventVersion key value contains a major and minor version in the form <major>.<minor>."""
        pass

    @property
    def event_source(self) -> str:
        """The AWS service from which the S3 event originated. For S3, this is aws:s3"""
        return self["eventSource"]

    @property
    def aws_region(self) -> str:
        """aws region eg: us-east-1"""
        pass

    @property
    def event_time(self) -> str:
        """The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, when S3 finished
        processing the request"""
        pass

    @property
    def event_name(self) -> str:
        """Event type"""
        pass

    @property
    def user_identity(self) -> S3Identity:
        pass

    @property
    def request_parameters(self) -> S3RequestParameters:
        pass

    @property
    def response_elements(self) -> dict[str, str]:
        """The responseElements key value is useful if you want to trace a request by following up with AWS Support.

        Both x-amz-request-id and x-amz-id-2 help Amazon S3 trace an individual request. These values are the same
        as those that Amazon S3 returns in the response to the request that initiates the events, so they can be
        used to match the event to the request.
        """
        pass

    @property
    def s3(self) -> S3Message:
        pass

    @property
    def glacier_event_data(self) -> S3EventRecordGlacierEventData | None:
        """The glacierEventData key is only visible for s3:ObjectRestore:Completed events."""
        pass

    @property
    def intelligent_tiering_event_data(self) -> S3EventRecordIntelligentTieringEventData | None:
        """The intelligentTieringEventData key is only visible for IntelligentTiering events."""
        pass


class S3Event(DictWrapper):
    """S3 event notification

    Documentation:
    -------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html
    - https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html
    - https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html
    """

    @property
    def records(self) -> Iterator[S3EventRecord]:
        pass

    @property
    def record(self) -> S3EventRecord:
        """Get the first s3 event record"""
        pass

    @property
    def bucket_name(self) -> str:
        """Get the bucket name for the first s3 event record"""
        pass

    @property
    def object_key(self) -> str:
        """Get the object key for the first s3 event record and unquote plus

        Note: IntelligentTiering events use 'get_object' as the key name,
        while other S3 events use 'object'. This method handles both cases.
        """
        pass
