from __future__ import annotations

from typing import TYPE_CHECKING

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper

if TYPE_CHECKING:
    from collections.abc import Iterator


class SNSMessageAttribute(DictWrapper):
    @property
    def get_type(self) -> str:
        """The supported message attribute data types are String, String.Array, Number, and Binary."""
        pass

    @property
    def value(self) -> str:
        """The user-specified message attribute value."""
        pass


class SNSMessage(DictWrapper):
    @property
    def signature_version(self) -> str:
        """Version of the Amazon SNS signature used."""
        pass

    @property
    def timestamp(self) -> str:
        """The time (GMT) when the subscription confirmation was sent."""
        return self["Timestamp"]

    @property
    def signature(self) -> str:
        """Base64-encoded "SHA1withRSA" signature of the Message, MessageId, Type, Timestamp, and TopicArn values."""
        return self["Signature"]

    @property
    def signing_cert_url(self) -> str:
        """The URL to the certificate that was used to sign the message."""
        pass

    @property
    def message_id(self) -> str:
        """A Universally Unique Identifier, unique for each message published.

        For a message that Amazon SNS resends during a retry, the message ID of the original message is used."""
        pass

    @property
    def message(self) -> str:
        """A string that describes the message."""
        pass

    @property
    def message_attributes(self) -> dict[str, SNSMessageAttribute]:
        pass

    @property
    def get_type(self) -> str:
        """The type of message.

        For a subscription confirmation, the type is SubscriptionConfirmation."""
        pass

    @property
    def unsubscribe_url(self) -> str:
        """A URL that you can use to unsubscribe the endpoint from this topic.

        If you visit this URL, Amazon SNS unsubscribes the endpoint and stops sending notifications to this endpoint."""
        pass

    @property
    def topic_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the topic that this endpoint is subscribed to."""
        pass

    @property
    def subject(self) -> str:
        """The Subject parameter specified when the notification was published to the topic."""
        pass


class SNSEventRecord(DictWrapper):
    @property
    def event_version(self) -> str:
        """Event version"""
        pass

    @property
    def event_subscription_arn(self) -> str:
        pass

    @property
    def event_source(self) -> str:
        """The AWS service from which the SNS event record originated. For SNS, this is aws:sns"""
        return self["EventSource"]

    @property
    def sns(self) -> SNSMessage:
        pass


class SNSEvent(DictWrapper):
    """SNS Event

    Documentation:
    -------------
    - https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html
    """

    @property
    def records(self) -> Iterator[SNSEventRecord]:
        pass

    @property
    def record(self) -> SNSEventRecord:
        """Return the first SNS event record"""
        pass

    @property
    def sns_message(self) -> str:
        """Return the message for the first sns event record"""
        pass
