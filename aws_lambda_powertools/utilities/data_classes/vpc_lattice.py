from __future__ import annotations

from functools import cached_property
from typing import Any

from aws_lambda_powertools.shared.headers_serializer import (
    BaseHeadersSerializer,
    HttpApiHeadersSerializer,
)
from aws_lambda_powertools.utilities.data_classes.common import (
    BaseProxyEvent,
    CaseInsensitiveDict,
    DictWrapper,
)
from aws_lambda_powertools.utilities.data_classes.shared_functions import base64_decode


class VPCLatticeEventBase(BaseProxyEvent):
    # is_base64_encoded and path are inherited from BaseProxyEvent class.

    @property
    def body(self) -> str:
        """The VPC Lattice body."""
        pass

    @cached_property
    def json_body(self) -> Any:
        """Parses the submitted body as json"""
        pass

    @property
    def headers(self) -> dict[str, str]:
        """The VPC Lattice event headers."""
        pass

    @property
    def decoded_body(self) -> str:
        """Dynamically base64 decode body as a str"""
        pass

    @property
    def method(self) -> str:
        """The VPC Lattice method used. Valid values include: DELETE, GET, HEAD, OPTIONS, PATCH, POST, and PUT."""
        pass

    @property
    def http_method(self) -> str:
        """The HTTP method used. Valid values include: DELETE, GET, HEAD, OPTIONS, PATCH, POST, and PUT."""
        pass

    def header_serializer(self) -> BaseHeadersSerializer:
        # When using the VPC Lattice integration, we have multiple HTTP Headers.
        return HttpApiHeadersSerializer()


class VPCLatticeEvent(VPCLatticeEventBase):
    @property
    def raw_path(self) -> str:
        """The raw VPC Lattice request path."""
        pass

    @property
    def is_base64_encoded(self) -> bool:
        """A boolean flag to indicate if the applicable request payload is Base64-encode"""
        pass

    # VPCLattice event has no path field
    # Added here for consistency with the BaseProxyEvent class
    @property
    def path(self) -> str:
        pass

    @property
    def query_string_parameters(self) -> dict[str, str]:
        """The request query string parameters."""
        pass

    @cached_property
    def resolved_headers_field(self) -> dict[str, Any]:
        pass


class vpcLatticeEventV2Identity(DictWrapper):
    @property
    def source_vpc_arn(self) -> str | None:
        """The VPC Lattice v2 Event requestContext Identity sourceVpcArn"""
        pass

    @property
    def get_type(self) -> str | None:
        """The VPC Lattice v2 Event requestContext Identity type"""
        pass

    @property
    def principal(self) -> str | None:
        """The VPC Lattice v2 Event requestContext principal"""
        pass

    @property
    def principal_org_id(self) -> str | None:
        """The VPC Lattice v2 Event requestContext principalOrgID"""
        pass

    @property
    def session_name(self) -> str | None:
        """The VPC Lattice v2 Event requestContext sessionName"""
        pass

    @property
    def x509_subject_cn(self) -> str | None:
        """The VPC Lattice v2 Event requestContext X509SubjectCn"""
        pass

    @property
    def x509_issuer_ou(self) -> str | None:
        """The VPC Lattice v2 Event requestContext X509IssuerOu"""
        pass

    @property
    def x509_san_dns(self) -> str | None:
        """The VPC Lattice v2 Event requestContext X509SanDns"""
        pass

    @property
    def x509_san_uri(self) -> str | None:
        """The VPC Lattice v2 Event requestContext X509SanUri"""
        pass

    @property
    def x509_san_name_cn(self) -> str | None:
        """The VPC Lattice v2 Event requestContext X509SanNameCn"""
        pass


class vpcLatticeEventV2RequestContext(DictWrapper):
    @property
    def service_network_arn(self) -> str:
        """The VPC Lattice v2 Event requestContext serviceNetworkArn"""
        pass

    @property
    def service_arn(self) -> str:
        """The VPC Lattice v2 Event requestContext serviceArn"""
        pass

    @property
    def target_group_arn(self) -> str:
        """The VPC Lattice v2 Event requestContext targetGroupArn"""
        pass

    @property
    def identity(self) -> vpcLatticeEventV2Identity:
        """The VPC Lattice v2 Event requestContext identity"""
        pass

    @property
    def region(self) -> str:
        """The VPC Lattice v2 Event requestContext serviceNetworkArn"""
        pass

    @property
    def time_epoch(self) -> float:
        """The VPC Lattice v2 Event requestContext timeEpoch"""
        pass


class VPCLatticeEventV2(VPCLatticeEventBase):
    @property
    def version(self) -> str:
        """The VPC Lattice v2 Event version"""
        return self["version"]

    @property
    def request_context(self) -> vpcLatticeEventV2RequestContext:
        """The VPC Lattice v2 Event request context."""
        pass

    @cached_property
    def query_string_parameters(self) -> dict[str, str]:
        """The request query string parameters.

        For VPC Lattice V2, the queryStringParameters will contain a dict[str, list[str]]
        so to keep compatibility with existing utilities, we merge all the values with a comma.
        """
        pass

    @property
    def resolved_headers_field(self) -> dict[str, str]:
        pass
