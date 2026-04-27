from __future__ import annotations

import enum
import re
import warnings
from typing import Any, overload

from typing_extensions import deprecated, override

from aws_lambda_powertools.utilities.data_classes.common import (
    BaseRequestContext,
    BaseRequestContextV2,
    CaseInsensitiveDict,
    DictWrapper,
)
from aws_lambda_powertools.utilities.data_classes.shared_functions import (
    get_header_value,  # ty: ignore[deprecated]
)
from aws_lambda_powertools.warnings import PowertoolsDeprecationWarning


class APIGatewayRouteArn:
    """A parsed route arn"""

    def __init__(
        self,
        region: str,
        aws_account_id: str,
        api_id: str,
        stage: str,
        http_method: str | None,
        resource: str,
        partition: str = "aws",
        is_websocket_authorizer: bool = False,
    ):
        self.partition = partition
        self.region = region
        self.aws_account_id = aws_account_id
        self.api_id = api_id
        self.stage = stage
        self.http_method = http_method
        # Remove matching "/" from `resource`.
        self.resource = resource.lstrip("/")
        self.is_websocket_authorizer = is_websocket_authorizer

    @property
    def arn(self) -> str:
        """Build an arn from its parts
        eg: arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/request"""
        pass


def parse_api_gateway_arn(arn: str, is_websocket_authorizer: bool = False) -> APIGatewayRouteArn:
    """Parses a gateway route arn as a APIGatewayRouteArn class

    Parameters
    ----------
    arn : str
        ARN string for a methodArn or a routeArn
    is_websocket_authorizer: bool
        If it's a API Gateway Websocket

    Returns
    -------
    APIGatewayRouteArn
    """
    pass


class APIGatewayAuthorizerTokenEvent(DictWrapper):
    """API Gateway Authorizer Token Event Format 1.0

    Documentation:
    -------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
    """

    @property
    def get_type(self) -> str:
        pass

    @property
    def authorization_token(self) -> str:
        pass

    @property
    def method_arn(self) -> str:
        """ARN of the incoming method request and is populated by API Gateway in accordance with the Lambda authorizer
        configuration"""
        pass

    @property
    def parsed_arn(self) -> APIGatewayRouteArn:
        """Convenient property to return a parsed api gateway method arn"""
        pass


class APIGatewayAuthorizerRequestEvent(DictWrapper):
    """API Gateway Authorizer Request Event Format 1.0

    Documentation:
    -------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    """

    @property
    def version(self) -> str:
        return self["version"]

    @property
    def get_type(self) -> str:
        pass

    @property
    def method_arn(self) -> str:
        pass

    @property
    def parsed_arn(self) -> APIGatewayRouteArn:
        pass

    @property
    def identity_source(self) -> str:
        pass

    @property
    def authorization_token(self) -> str:
        pass

    @property
    def resource(self) -> str:
        return self["resource"]

    @property
    def path(self) -> str:
        pass

    @property
    def http_method(self) -> str:
        pass

    @property
    def headers(self) -> dict[str, str]:
        pass

    @property
    def query_string_parameters(self) -> dict[str, str]:
        pass

    @property
    def path_parameters(self) -> dict[str, str]:
        pass

    @property
    def stage_variables(self) -> dict[str, str]:
        pass

    @property
    def request_context(self) -> BaseRequestContext:
        pass

    @overload
    def get_header_value(
        self,
        name: str,
        default_value: str,
        case_sensitive: bool = False,
    ) -> str: ...

    @overload
    def get_header_value(
        self,
        name: str,
        default_value: str | None = None,
        case_sensitive: bool = False,
    ) -> str | None: ...

    @deprecated(
        "`get_header_value` function is deprecated; Access headers directly using event.headers.get('HeaderName')",
        category=None,
    )
    def get_header_value(
        self,
        name: str,
        default_value: str | None = None,
        case_sensitive: bool = False,
    ) -> str | None:
        """Get header value by name
        Parameters
        ----------
        name: str
            Header name
        default_value: str, optional
            Default value if no value was found by name
        case_sensitive: bool
            Whether to use a case-sensitive look up
        Returns
        -------
        str, optional
            Header value
        """
        pass


class APIGatewayAuthorizerEventV2(DictWrapper):
    """API Gateway Authorizer Event Format 2.0

    Documentation:
    -------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    - https://aws.amazon.com/blogs/compute/introducing-iam-and-lambda-authorizers-for-amazon-api-gateway-http-apis/
    """

    @property
    def version(self) -> str:
        """Event payload version should always be 2.0"""
        return self["version"]

    @property
    def get_type(self) -> str:
        """Event type should always be request"""
        pass

    @property
    def route_arn(self) -> str:
        """ARN of the route being called

        eg: arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/request"""
        pass

    @property
    def parsed_arn(self) -> APIGatewayRouteArn:
        """Convenient property to return a parsed api gateway route arn"""
        pass

    @property
    def identity_source(self) -> list[str]:
        """The identity source for which authorization is requested.

        For a REQUEST authorizer, this is optional. The value is a set of one or more mapping expressions of the
        specified request parameters. The identity source can be headers, query string parameters, stage variables,
        and context parameters.
        """
        pass

    @property
    def route_key(self) -> str:
        """The route key for the route. For HTTP APIs, the route key can be either $default,
        or a combination of an HTTP method and resource path, for example, GET /pets."""
        pass

    @property
    def raw_path(self) -> str:
        pass

    @property
    def raw_query_string(self) -> str:
        pass

    @property
    def cookies(self) -> list[str]:
        """Cookies"""
        pass

    @property
    def headers(self) -> dict[str, str]:
        """Http headers"""
        pass

    @property
    def query_string_parameters(self) -> dict[str, str]:
        pass

    @property
    def request_context(self) -> BaseRequestContextV2:
        pass

    @property
    def path_parameters(self) -> dict[str, str]:
        pass

    @property
    def stage_variables(self) -> dict[str, str]:
        pass

    @overload
    def get_header_value(self, name: str, default_value: str, case_sensitive: bool = False) -> str: ...

    @overload
    def get_header_value(
        self,
        name: str,
        default_value: str | None = None,
        case_sensitive: bool = False,
    ) -> str | None: ...

    @deprecated(
        "`get_header_value` function is deprecated; Access headers directly using event.headers.get('HeaderName')",
        category=None,
    )
    def get_header_value(
        self,
        name: str,
        default_value: str | None = None,
        case_sensitive: bool = False,
    ) -> str | None:
        """Get header value by name
        Parameters
        ----------
        name: str
            Header name
        default_value: str, optional
            Default value if no value was found by name
        case_sensitive: bool
            Whether to use a case-sensitive look up
        Returns
        -------
        str, optional
            Header value
        """
        pass


class APIGatewayAuthorizerResponseV2:
    """Api Gateway HTTP API V2 payload authorizer simple response helper

    Parameters
    ----------
    authorize: bool
        authorize is a boolean value indicating if the value in authorizationToken
        is authorized to make calls to the GraphQL API. If this value is
        true, execution of the GraphQL API continues. If this value is false,
        an UnauthorizedException is raised
    context: dict[str, Any], optional
        A JSON object visible as `event.requestContext.authorizer` lambda event

        The context object only supports key-value pairs. Nested keys are not supported.

        Warning: The total size of this JSON object must not exceed 5MB.
    """

    def __init__(
        self,
        authorize: bool = False,
        context: dict[str, Any] | None = None,
    ):
        self.authorize = authorize
        self.context = context

    def asdict(self) -> dict:
        """Return the response as a dict"""
        response: dict = {"isAuthorized": self.authorize}

        if self.context:
            response["context"] = self.context

        return response


class HttpVerb(enum.Enum):
    """Enum of http methods / verbs"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    ALL = "*"


DENY_ALL_RESPONSE = {
    "principalId": "deny-all-user",
    "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "execute-api:Invoke",
                "Effect": "Deny",
                "Resource": ["*"],
            },
        ],
    },
}


class APIGatewayAuthorizerResponse:
    """The IAM Policy Response required for API Gateway REST APIs and HTTP APIs.

    Based on: - https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints/blob/\
    master/blueprints/python/api-gateway-authorizer-python.py

    Documentation:
    -------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
    """

    path_regex = r"^[/.a-zA-Z0-9\-_\*\{\}\+]+$"
    """The regular expression used to validate resource paths for the policy"""

    def __init__(
        self,
        principal_id: str,
        region: str,
        aws_account_id: str,
        api_id: str,
        stage: str,
        context: dict | None = None,
        usage_identifier_key: str | None = None,
        partition: str = "aws",
    ):
        """
        Parameters
        ----------
        principal_id : str
            The principal used for the policy, this should be a unique identifier for the end user
        region : str
            AWS Regions. Beware of using '*' since it will not simply mean any region, because stars will greedily
            expand over '/' or other separators.
            See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more
            details.
        aws_account_id : str
            The AWS account id the policy will be generated for. This is used to create the method ARNs.
        api_id : str
            The API Gateway API id to be used in the policy.
            Beware of using '*' since it will not simply mean any API Gateway API id, because stars will greedily
            expand over '/' or other separators.
            See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more
            details.
        stage : str
            The default stage to be used in the policy.
            Beware of using '*' since it will not simply mean any stage, because stars will
            greedily expand over '/' or other separators.
            See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more
            details.
        context : dict, optional
            Optional, context.
            Note: only names of type string and values of type int, string or boolean are supported
        usage_identifier_key: str, optional
            If the API uses a usage plan (the apiKeySource is set to `AUTHORIZER`), the Lambda authorizer function
            must return one of the usage plan's API keys as the usageIdentifierKey property value.
            > **Note:** This only applies for REST APIs.
        partition: str, optional
            Optional, arn partition.
            See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html
        """
        self.principal_id = principal_id
        self.region = region
        self.aws_account_id = aws_account_id
        self.api_id = api_id
        self.stage = stage
        self.context = context
        self.usage_identifier_key = usage_identifier_key
        self._allow_routes: list[dict] = []
        self._deny_routes: list[dict] = []
        self._resource_pattern = re.compile(self.path_regex)
        self.partition = partition

    @staticmethod
    def from_route_arn(
        arn: str,
        principal_id: str,
        context: dict | None = None,
        usage_identifier_key: str | None = None,
    ) -> APIGatewayAuthorizerResponse:
        pass

    def _add_route(self, effect: str, http_method: str, resource: str, conditions: list[dict] | None = None):
        """Adds a route to the internal lists of allowed or denied routes. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        pass

    @staticmethod
    def _get_empty_statement(effect: str) -> dict[str, Any]:
        """Returns an empty statement object prepopulated with the correct action and the desired effect."""
        return {"Action": "execute-api:Invoke", "Effect": effect.capitalize(), "Resource": []}

    def _get_statement_for_effect(self, effect: str, routes: list[dict]) -> list[dict]:
        """This function loops over an array of objects containing a `resourceArn` and
        `conditions` statement and generates the array of statements for the policy."""
        if not routes:
            return []

        statements: list[dict] = []
        statement = self._get_empty_statement(effect)

        for route in routes:
            resource_arn = route["resourceArn"]
            conditions = route.get("conditions")
            if conditions is not None and len(conditions) > 0:
                conditional_statement = self._get_empty_statement(effect)
                conditional_statement["Resource"].append(resource_arn)
                conditional_statement["Condition"] = conditions
                statements.append(conditional_statement)

            else:
                statement["Resource"].append(resource_arn)

        if len(statement["Resource"]) > 0:
            statements.append(statement)

        return statements

    def allow_all_routes(self, http_method: str = HttpVerb.ALL.value):
        """Adds a '*' allow to the policy to authorize access to all methods of an API

        Parameters
        ----------
        http_method: str
        """
        pass

    def deny_all_routes(self, http_method: str = HttpVerb.ALL.value):
        """Adds a '*' allow to the policy to deny access to all methods of an API

        Parameters
        ----------
        http_method: str
        """
        pass

    def allow_route(self, http_method: str, resource: str, conditions: list[dict] | None = None):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy.

        Optionally includes a condition for the policy statement. More on AWS policy
        conditions here: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        pass

    def deny_route(self, http_method: str, resource: str, conditions: list[dict] | None = None):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy.

        Optionally includes a condition for the policy statement. More on AWS policy
        conditions here: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        pass

    def asdict(self) -> dict[str, Any]:
        """Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy."""
        if len(self._allow_routes) == 0 and len(self._deny_routes) == 0:
            raise ValueError("No statements defined for the policy")

        response: dict[str, Any] = {
            "principalId": self.principal_id,
            "policyDocument": {"Version": "2012-10-17", "Statement": []},
        }

        response["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Allow", self._allow_routes))
        response["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Deny", self._deny_routes))

        if self.usage_identifier_key:
            response["usageIdentifierKey"] = self.usage_identifier_key

        if self.context:
            response["context"] = self.context

        return response


class APIGatewayAuthorizerResponseWebSocket(APIGatewayAuthorizerResponse):
    """The IAM Policy Response required for API Gateway WebSocket APIs

    Based on: - https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints/blob/\
    master/blueprints/python/api-gateway-authorizer-python.py

    Documentation:
    -------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
    """

    @staticmethod
    def from_route_arn(
        arn: str,
        principal_id: str,
        context: dict | None = None,
        usage_identifier_key: str | None = None,
    ) -> APIGatewayAuthorizerResponseWebSocket:
        pass

    # Note: we need ignore[override] because we are removing the http_method field
    @override
    def _add_route(self, effect: str, resource: str, conditions: list[dict] | None = None):  # type: ignore[override]  # ty: ignore[invalid-method-override]
        """Adds a route to the internal lists of allowed or denied routes. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        pass

    @override
    def allow_all_routes(self, http_method: str = HttpVerb.ALL.value):  # type: ignore[override]  # noqa: ARG002
        """Adds a '*' allow to the policy to authorize access to all methods of an API"""
        pass

    @override
    def deny_all_routes(self, http_method: str = HttpVerb.ALL.value):  # type: ignore[override]  # noqa: ARG002
        """Adds a '*' allow to the policy to deny access to all methods of an API"""
        pass

    # Note: we need ignore[override] because we are removing the http_method field
    @override
    def allow_route(self, resource: str, conditions: list[dict] | None = None):  # type: ignore[override]  # ty: ignore[invalid-method-override]
        """
        Add an API Gateway Websocket method to the list of allowed methods for the policy.

        This method adds an API Gateway Websocket method Resource path) to the list of
        allowed methods for the policy. It optionally includes conditions for the policy statement.

        Parameters
        ----------
        resource : str
            The API Gateway resource path to allow.
        conditions : list[dict] | None, optional
            A list of condition dictionaries to apply to the policy statement.
            Default is None.

        Notes
        -----
        For more information on AWS policy conditions, see:
        https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition

        Example
        --------
        >>> policy = APIGatewayAuthorizerResponseWebSocket(...)
        >>> policy.allow_route("/api/users", [{"StringEquals": {"aws:RequestTag/Environment": "Production"}}])
        """
        pass

    # Note: we need ignore[override] because we are removing the http_method field
    @override
    def deny_route(self, resource: str, conditions: list[dict] | None = None):  # type: ignore[override]  # ty: ignore[invalid-method-override]
        """
        Add an API Gateway Websocket method to the list of allowed methods for the policy.

        This method adds an API Gateway Websocket method Resource path) to the list of
        denied methods for the policy. It optionally includes conditions for the policy statement.

        Parameters
        ----------
        resource : str
            The API Gateway resource path to allow.
        conditions : list[dict] | None, optional
            A list of condition dictionaries to apply to the policy statement.
            Default is None.

        Notes
        -----
        For more information on AWS policy conditions, see:
        https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition

        Example
        --------
        >>> policy = APIGatewayAuthorizerResponseWebSocket(...)
        >>> policy.deny_route("/api/users", [{"StringEquals": {"aws:RequestTag/Environment": "Production"}}])
        """
        pass
