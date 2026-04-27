from __future__ import annotations

from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


def get_invoke_event(
    invoking_event: dict,
) -> AWSConfigConfigurationChanged | AWSConfigScheduledNotification | AWSConfigOversizedConfiguration:
    """
    Returns the corresponding event object based on the messageType in the invoking event.

    Parameters
    ----------
    invoking_event: dict
        The invoking event received.

    Returns
    -------
    AWSConfigConfigurationChanged | AWSConfigScheduledNotification | AWSConfigOversizedConfiguration:
        The event object based on the messageType in the invoking event.
    """
    pass


class AWSConfigConfigurationChanged(DictWrapper):
    @property
    def configuration_item_diff(self) -> dict:
        """The configuration item diff of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_item(self) -> AWSConfigConfigurationItemChanged:
        """The configuration item of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def raw_configuration_item(self) -> dict:
        """The raw configuration item of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def record_version(self) -> str:
        """The record version of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def message_type(self) -> str:
        """The message type of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def notification_creation_time(self) -> str:
        """The notification creation time of the ConfigurationItemChangeNotification event."""
        pass


class AWSConfigConfigurationItemChanged(DictWrapper):
    @property
    def related_events(self) -> list:
        """The related events of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def relationships(self) -> list:
        """The relationships of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration(self) -> dict:
        """The configuration of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def supplementary_configuration(self) -> dict:
        """The supplementary configuration of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def tags(self) -> dict:
        """The tags of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_item_version(self) -> str:
        """The configuration item version of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_item_capture_time(self) -> str:
        """The configuration item capture time of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_state_id(self) -> str:
        """The configuration state id of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def accountid(self) -> str:
        """The accountid of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_item_status(self) -> str:
        """The configuration item status of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def resource_type(self) -> str:
        """The resource type of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def resource_id(self) -> str:
        """The resource id of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def resource_name(self) -> str:
        """The resource name of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def resource_arn(self) -> str:
        """The resource arn of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def region(self) -> str:
        """The region of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def availability_zone(self) -> str:
        """The availability zone of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def configuration_state_md5_hash(self) -> str:
        """The md5 hash of the state of the ConfigurationItemChangeNotification event."""
        pass

    @property
    def resource_creation_time(self) -> str:
        """The resource creation time of the ConfigurationItemChangeNotification event."""
        pass


class AWSConfigScheduledNotification(DictWrapper):
    @property
    def accountid(self) -> str:
        """The accountid of the ScheduledNotification event."""
        pass

    @property
    def notification_creation_time(self) -> str:
        """The notification creation time of the ScheduledNotification event."""
        pass

    @property
    def record_version(self) -> str:
        """The record version of the ScheduledNotification event."""
        pass

    @property
    def message_type(self) -> str:
        """The message type of the ScheduledNotification event."""
        pass


class AWSConfigOversizedConfiguration(DictWrapper):
    @property
    def configuration_item_summary(self) -> AWSConfigOversizedConfigurationItemSummary:
        """The configuration item summary of the OversizedConfiguration event."""
        pass

    @property
    def raw_configuration_item_summary(self) -> str:
        """The raw configuration item summary of the OversizedConfiguration event."""
        pass

    @property
    def message_type(self) -> str:
        """The message type of the OversizedConfiguration event."""
        pass

    @property
    def notification_creation_time(self) -> str:
        """The notification creation time of the OversizedConfiguration event."""
        pass

    @property
    def record_version(self) -> str:
        """The record version of the OversizedConfiguration event."""
        pass


class AWSConfigOversizedConfigurationItemSummary(DictWrapper):
    @property
    def change_type(self) -> str:
        """The change type of the OversizedConfiguration event."""
        pass

    @property
    def configuration_item_version(self) -> str:
        """The configuration item version of the OversizedConfiguration event."""
        pass

    @property
    def configuration_item_capture_time(self) -> str:
        """The configuration item capture time of the OversizedConfiguration event."""
        pass

    @property
    def configuration_state_id(self) -> str:
        """The configuration state id of the OversizedConfiguration event."""
        pass

    @property
    def accountid(self) -> str:
        """The accountid of the OversizedConfiguration event."""
        pass

    @property
    def configuration_item_status(self) -> str:
        """The configuration item status of the OversizedConfiguration event."""
        pass

    @property
    def resource_type(self) -> str:
        """The resource type of the OversizedConfiguration event."""
        pass

    @property
    def resource_id(self) -> str:
        """The resource id of the OversizedConfiguration event."""
        pass

    @property
    def resource_name(self) -> str:
        """The resource name of the OversizedConfiguration event."""
        pass

    @property
    def resource_arn(self) -> str:
        """The resource arn of the OversizedConfiguration event."""
        pass

    @property
    def region(self) -> str:
        """The region of the OversizedConfiguration event."""
        pass

    @property
    def availability_zone(self) -> str:
        """The availability zone of the OversizedConfiguration event."""
        pass

    @property
    def configuration_state_md5_hash(self) -> str:
        """The state md5 hash  of the OversizedConfiguration event."""
        pass

    @property
    def resource_creation_time(self) -> str:
        """The resource creation time of the OversizedConfiguration event."""
        pass


class AWSConfigRuleEvent(DictWrapper):
    """Events for AWS Config Rules
    Documentation:
    --------------
    - https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_lambda-functions.html
    """

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self._invoking_event: Any | None = None
        self._rule_parameters: Any | None = None

    @property
    def version(self) -> str:
        """The version of the event."""
        return self["version"]

    @property
    def invoking_event(
        self,
    ) -> AWSConfigConfigurationChanged | AWSConfigScheduledNotification | AWSConfigOversizedConfiguration:
        """The invoking payload of the event."""
        pass

    @property
    def raw_invoking_event(self) -> str:
        """The raw invoking payload of the event."""
        pass

    @property
    def rule_parameters(self) -> dict:
        """The parameters of the event."""
        pass

    @property
    def result_token(self) -> str:
        """The result token of the event."""
        pass

    @property
    def event_left_scope(self) -> bool:
        """The left scope of the event."""
        pass

    @property
    def execution_role_arn(self) -> str:
        """The execution role arn of the event."""
        pass

    @property
    def config_rule_arn(self) -> str:
        """The arn of the rule of the event."""
        pass

    @property
    def config_rule_name(self) -> str:
        """The name of the rule of the event."""
        pass

    @property
    def config_rule_id(self) -> str:
        """The id of the rule of the event."""
        pass

    @property
    def accountid(self) -> str:
        """The accountid of the event."""
        pass

    @property
    def evalution_mode(self) -> str | None:
        """The evalution mode of the event."""
        pass
