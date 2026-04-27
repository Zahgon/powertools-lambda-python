from __future__ import annotations

from typing import TYPE_CHECKING

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper

if TYPE_CHECKING:
    from collections.abc import Iterator


class SESMailHeader(DictWrapper):
    @property
    def name(self) -> str:
        pass

    @property
    def value(self) -> str:
        pass


class SESMailCommonHeaders(DictWrapper):
    @property
    def return_path(self) -> str:
        """The values in the Return-Path header of the email."""
        pass

    @property
    def get_from(self) -> list[str]:
        """The values in the From header of the email."""
        pass

    @property
    def date(self) -> str:
        """The date and time when Amazon SES received the message."""
        pass

    @property
    def to(self) -> list[str]:
        """The values in the To header of the email."""
        pass

    @property
    def message_id(self) -> str:
        """The ID of the original message."""
        pass

    @property
    def subject(self) -> str:
        """The value of the Subject header for the email."""
        pass

    @property
    def cc(self) -> list[str]:
        """The values in the CC header of the email."""
        pass

    @property
    def bcc(self) -> list[str]:
        """The values in the BCC header of the email."""
        pass

    @property
    def sender(self) -> list[str]:
        """The values in the Sender header of the email."""
        pass

    @property
    def reply_to(self) -> list[str]:
        """The values in the replyTo header of the email."""
        pass


class SESMail(DictWrapper):
    @property
    def timestamp(self) -> str:
        """String that contains the time at which the email was received, in ISO8601 format."""
        return self["timestamp"]

    @property
    def source(self) -> str:
        """String that contains the email address (specifically, the envelope MAIL FROM address)
        that the email was sent from."""
        pass

    @property
    def message_id(self) -> str:
        """String that contains the unique ID assigned to the email by Amazon SES.

        If the email was delivered to Amazon S3, the message ID is also the Amazon S3 object key that was
        used to write the message to your Amazon S3 bucket."""
        pass

    @property
    def destination(self) -> list[str]:
        """A complete list of all recipient addresses (including To: and CC: recipients)
        from the MIME headers of the incoming email."""
        pass

    @property
    def headers_truncated(self) -> bool:
        """String that specifies whether the headers were truncated in the notification, which will happen
        if the headers are larger than 10 KB. Possible values are true and false."""
        pass

    @property
    def headers(self) -> Iterator[SESMailHeader]:
        """A list of Amazon SES headers and your custom headers.
        Each header in the list has a name field and a value field"""
        pass

    @property
    def common_headers(self) -> SESMailCommonHeaders:
        """A list of headers common to all emails. Each header in the list is composed of a name and a value."""
        pass


class SESReceiptStatus(DictWrapper):
    @property
    def status(self) -> str:
        """Receipt status
        Possible values: 'PASS', 'FAIL', 'GRAY', 'PROCESSING_FAILED', 'DISABLED'
        """
        pass


class SESReceiptAction(DictWrapper):
    @property
    def get_type(self) -> str:
        """String that indicates the type of action that was executed.

        Possible values are S3, SNS, Bounce, Lambda, Stop, and WorkMail
        """
        pass

    @property
    def topic_arn(self) -> str | None:
        """String that contains the Amazon Resource Name (ARN) of the Amazon SNS topic to which the
        notification was published."""
        pass

    @property
    def function_arn(self) -> str:
        """String that contains the ARN of the Lambda function that was triggered.
        Present only for the Lambda action type."""
        pass

    @property
    def invocation_type(self) -> str:
        """String that contains the invocation type of the Lambda function. Possible values are RequestResponse
        and Event. Present only for the Lambda action type."""
        pass


class SESReceipt(DictWrapper):
    @property
    def timestamp(self) -> str:
        """String that specifies the date and time at which the action was triggered, in ISO 8601 format."""
        return self["timestamp"]

    @property
    def processing_time_millis(self) -> int:
        """String that specifies the period, in milliseconds, from the time Amazon SES received the message
        to the time it triggered the action."""
        pass

    @property
    def recipients(self) -> list[str]:
        """A list of recipients (specifically, the envelope RCPT TO addresses) that were matched by the
        active receipt rule. The addresses listed here may differ from those listed by the destination
        field in the mail object."""
        pass

    @property
    def spam_verdict(self) -> SESReceiptStatus:
        """Object that indicates whether the message is spam."""
        pass

    @property
    def virus_verdict(self) -> SESReceiptStatus:
        """Object that indicates whether the message contains a virus."""
        pass

    @property
    def spf_verdict(self) -> SESReceiptStatus:
        """Object that indicates whether the Sender Policy Framework (SPF) check passed."""
        pass

    @property
    def dkim_verdict(self) -> SESReceiptStatus:
        """Object that indicates whether the DomainKeys Identified Mail (DKIM) check passed"""
        pass

    @property
    def dmarc_verdict(self) -> SESReceiptStatus:
        """Object that indicates whether the Domain-based Message Authentication,
        Reporting & Conformance (DMARC) check passed."""
        pass

    @property
    def dmarc_policy(self) -> str | None:
        """Indicates the Domain-based Message Authentication, Reporting & Conformance (DMARC) settings for
        the sending domain. This field only appears if the message fails DMARC authentication.
        Possible values for this field are: none, quarantine, reject"""
        pass

    @property
    def action(self) -> SESReceiptAction:
        """Object that encapsulates information about the action that was executed."""
        return SESReceiptAction(self["action"])


class SESMessage(DictWrapper):
    @property
    def mail(self) -> SESMail:
        pass

    @property
    def receipt(self) -> SESReceipt:
        pass


class SESEventRecord(DictWrapper):
    @property
    def event_source(self) -> str:
        """The AWS service from which the SES event record originated. For SES, this is aws:ses"""
        return self["eventSource"]

    @property
    def event_version(self) -> str:
        """The eventVersion key value contains a major and minor version in the form <major>.<minor>."""
        pass

    @property
    def ses(self) -> SESMessage:
        pass


class SESEvent(DictWrapper):
    """Amazon SES to receive message event trigger

    NOTE: There is a 30-second timeout on RequestResponse invocations.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/lambda/latest/dg/services-ses.html
    - https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda.html
    """

    @property
    def records(self) -> Iterator[SESEventRecord]:
        pass

    @property
    def record(self) -> SESEventRecord:
        pass

    @property
    def mail(self) -> SESMail:
        pass

    @property
    def receipt(self) -> SESReceipt:
        pass
