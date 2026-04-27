from __future__ import annotations

from enum import Enum, auto

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class ConnectContactFlowChannel(Enum):
    VOICE = auto()
    CHAT = auto()


class ConnectContactFlowEndpointType(Enum):
    TELEPHONE_NUMBER = auto()


class ConnectContactFlowInitiationMethod(Enum):
    INBOUND = auto()
    OUTBOUND = auto()
    TRANSFER = auto()
    CALLBACK = auto()
    API = auto()


class ConnectContactFlowEndpoint(DictWrapper):
    @property
    def address(self) -> str:
        """The phone number."""
        pass

    @property
    def endpoint_type(self) -> ConnectContactFlowEndpointType:
        """The endpoint type."""
        pass


class ConnectContactFlowQueue(DictWrapper):
    @property
    def arn(self) -> str:
        """The unique queue ARN."""
        pass

    @property
    def name(self) -> str:
        """The queue name."""
        pass


class ConnectContactFlowMediaStreamAudio(DictWrapper):
    @property
    def start_fragment_number(self) -> str | None:
        """The number that identifies the Kinesis Video Streams fragment, in the stream used for Live media streaming,
        in which the customer audio stream started.
        """
        pass

    @property
    def start_timestamp(self) -> str | None:
        """When the customer audio stream started."""
        pass

    @property
    def stream_arn(self) -> str | None:
        """The ARN of the Kinesis Video stream used for Live media streaming that includes the customer data to
        reference.
        """
        pass


class ConnectContactFlowMediaStreamCustomer(DictWrapper):
    @property
    def audio(self) -> ConnectContactFlowMediaStreamAudio:
        pass


class ConnectContactFlowMediaStreams(DictWrapper):
    @property
    def customer(self) -> ConnectContactFlowMediaStreamCustomer:
        pass


class ConnectContactFlowData(DictWrapper):
    @property
    def attributes(self) -> dict[str, str]:
        """These are attributes that have been previously associated with a contact,
        such as when using a Set contact attributes block in a contact flow.
        This map may be empty if there aren't any saved attributes.
        """
        pass

    @property
    def channel(self) -> ConnectContactFlowChannel:
        """The method used to contact your contact center."""
        pass

    @property
    def contact_id(self) -> str:
        """The unique identifier of the contact."""
        pass

    @property
    def customer_endpoint(self) -> ConnectContactFlowEndpoint | None:
        """Contains the customer’s address (number) and type of address."""
        pass

    @property
    def initial_contact_id(self) -> str:
        """The unique identifier for the contact associated with the first interaction between the customer and your
        contact center. Use the initial contact ID to track contacts between contact flows.
        """
        pass

    @property
    def initiation_method(self) -> ConnectContactFlowInitiationMethod:
        """How the contact was initiated."""
        pass

    @property
    def instance_arn(self) -> str:
        """The ARN for your Amazon Connect instance."""
        pass

    @property
    def previous_contact_id(self) -> str:
        """The unique identifier for the contact before it was transferred.
        Use the previous contact ID to trace contacts between contact flows.
        """
        pass

    @property
    def queue(self) -> ConnectContactFlowQueue | None:
        """The current queue."""
        pass

    @property
    def system_endpoint(self) -> ConnectContactFlowEndpoint | None:
        """Contains the address (number) the customer dialed to call your contact center and type of address."""
        pass

    @property
    def media_streams(self) -> ConnectContactFlowMediaStreams:
        pass


class ConnectContactFlowEvent(DictWrapper):
    """Amazon Connect contact flow event

    Documentation:
    -------------
    - https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html
    """

    @property
    def contact_data(self) -> ConnectContactFlowData:
        """This is always passed by Amazon Connect for every contact. Some parameters are optional."""
        pass

    @property
    def parameters(self) -> dict[str, str]:
        """These are parameters specific to this call that were defined when you created the Lambda function."""
        pass
