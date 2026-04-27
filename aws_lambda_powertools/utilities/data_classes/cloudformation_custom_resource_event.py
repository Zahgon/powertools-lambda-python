from __future__ import annotations

from typing import Any, Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CloudFormationCustomResourceEvent(DictWrapper):
    @property
    def request_type(self) -> Literal["Create", "Update", "Delete"]:
        pass

    @property
    def service_token(self) -> str:
        pass

    @property
    def response_url(self) -> str:
        pass

    @property
    def stack_id(self) -> str:
        pass

    @property
    def request_id(self) -> str:
        pass

    @property
    def logical_resource_id(self) -> str:
        pass

    @property
    def physical_resource_id(self) -> str:
        pass

    @property
    def resource_type(self) -> str:
        pass

    @property
    def resource_properties(self) -> dict[str, Any]:
        pass

    @property
    def old_resource_properties(self) -> dict[str, Any]:
        pass
