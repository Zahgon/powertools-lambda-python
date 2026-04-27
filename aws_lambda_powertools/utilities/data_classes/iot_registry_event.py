from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper

EVENT_CRUD_OPERATION = Literal["CREATED", "UPDATED", "DELETED"]
EVENT_ADD_REMOVE_OPERATION = Literal["ADDED", "REMOVED"]


class IoTCoreRegistryEventsBase(DictWrapper):
    @property
    def event_id(self) -> str:
        """
        The unique identifier for the event.
        """
        pass

    @property
    def timestamp(self) -> datetime:
        """
        The timestamp of the event.

        The timestamp is in Unix format (seconds or milliseconds).
        If it's 10 digits long, it represents seconds;
        if it's 13 digits, it's in milliseconds and is converted to seconds.
        """
        ts = self["timestamp"]
        return datetime.fromtimestamp(ts / 1000 if ts > 10**10 else ts)


class IoTCoreThingEvent(IoTCoreRegistryEventsBase):
    """
    Thing Created/Updated/Deleted
    The registry publishes event messages when things are created, updated, or deleted.
    """

    @property
    def event_type(self) -> Literal["THING_EVENT"]:
        """
        The event type, which will always be "THING_EVENT".
        """
        pass

    @property
    def operation(self) -> str:
        """
        The operation type for the event (e.g., CREATED, UPDATED, DELETED).
        """
        pass

    @property
    def thing_id(self) -> str:
        """
        The unique identifier for the thing.
        """
        pass

    @property
    def account_id(self) -> str:
        """
        The account ID associated with the event.
        """
        pass

    @property
    def thing_name(self) -> str:
        """
        The name of the thing.
        """
        pass

    @property
    def version_number(self) -> int:
        """
        The version number of the thing.
        """
        pass

    @property
    def thing_type_name(self) -> str | None:
        """
        The thing type name if available, or None if not specified.
        """
        pass

    @property
    def attributes(self) -> dict[str, Any]:
        """
        The dictionary of attributes associated with the thing.
        """
        pass


class IoTCoreThingTypeEvent(IoTCoreRegistryEventsBase):
    """
    Thing Type Created/Updated/Deprecated/Undeprecated/Deleted
    The registry publishes event messages when thing types are created, updated, deprecated, undeprecated, or deleted.
    """

    @property
    def event_type(self) -> str:
        """
        The event type, corresponding to a thing type event.
        """
        pass

    @property
    def operation(self) -> EVENT_CRUD_OPERATION:
        """
        The operation performed on the thing type (e.g., CREATED, UPDATED, DELETED).
        """
        pass

    @property
    def account_id(self) -> str:
        """
        The account ID associated with the event.
        """
        pass

    @property
    def thing_type_id(self) -> str:
        """
        The unique identifier for the thing type.
        """
        pass

    @property
    def thing_type_name(self) -> str:
        """
        The name of the thing type.
        """
        pass

    @property
    def is_deprecated(self) -> bool:
        """
        Whether the thing type is marked as deprecated.
        """
        pass

    @property
    def deprecation_date(self) -> datetime | None:
        """
        The deprecation date of the thing type, or None if not available.
        """
        pass

    @property
    def searchable_attributes(self) -> list[str]:
        """
        The list of attributes that are searchable for the thing type.
        """
        pass

    @property
    def propagating_attributes(self) -> list[dict[str, str]]:
        """
        The list of attributes to propagate for the thing type.
        """
        pass

    @property
    def description(self) -> str:
        """
        The description of the thing type.
        """
        pass


class IoTCoreThingTypeAssociationEvent(IoTCoreRegistryEventsBase):
    """
    The registry publishes event messages when a thing type is associated or disassociated with a thing.
    """

    @property
    def event_type(self) -> str:
        """
        The event type, related to the thing type association event.
        """
        pass

    @property
    def operation(self) -> Literal["THING_TYPE_ASSOCIATION_EVENT"]:
        """
        The operation type, which is always "THING_TYPE_ASSOCIATION_EVENT".
        """
        pass

    @property
    def thing_id(self) -> str:
        """
        The unique identifier for the associated thing.
        """
        pass

    @property
    def thing_name(self) -> str:
        """
        The name of the associated thing.
        """
        pass

    @property
    def thing_type_name(self) -> str:
        """
        The name of the associated thing type.
        """
        pass


class IoTCoreThingGroupEvent(IoTCoreRegistryEventsBase):
    """
    The registry publishes event messages when a thing group is created, updated, or deleted.
    """

    @property
    def event_type(self) -> str:
        """
        The event type, corresponding to the thing group event.
        """
        pass

    @property
    def operation(self) -> EVENT_CRUD_OPERATION:
        """
        The operation type (e.g., CREATED, UPDATED, DELETED) performed on the thing group.
        """
        pass

    @property
    def account_id(self) -> str:
        """
        The account ID associated with the event.
        """
        pass

    @property
    def thing_group_id(self) -> str:
        """
        The unique identifier for the thing group.
        """
        pass

    @property
    def thing_group_name(self) -> str:
        """
        The name of the thing group.
        """
        pass

    @property
    def version_number(self) -> int:
        """
        The version number of the thing group.
        """
        pass

    @property
    def parent_group_name(self) -> str | None:
        """
        The name of the parent group, or None if not applicable.
        """
        pass

    @property
    def parent_group_id(self) -> str | None:
        """
        The ID of the parent group, or None if not applicable.
        """
        pass

    @property
    def description(self) -> str:
        """
        The description of the thing group.
        """
        pass

    @property
    def root_to_parent_thing_groups(self) -> list[dict[str, str]]:
        """
        The list of root-to-parent thing group mappings.
        """
        pass

    @property
    def attributes(self) -> dict[str, Any]:
        """
        The attributes associated with the thing group.
        """
        pass

    @property
    def dynamic_group_mapping_id(self) -> str | None:
        """
        The dynamic group mapping ID if available, or None if not specified.
        """
        pass


class IoTCoreAddOrRemoveFromThingGroupEvent(IoTCoreRegistryEventsBase):
    """
    The registry publishes event messages when a thing is added to or removed from a thing group.
    """

    @property
    def event_type(self) -> str:
        """
        The event type, corresponding to the add/remove from thing group event.
        """
        pass

    @property
    def operation(self) -> EVENT_ADD_REMOVE_OPERATION:
        """
        The operation (ADDED or REMOVED) performed on the thing in the group.
        """
        pass

    @property
    def account_id(self) -> str:
        """
        The account ID associated with the event.
        """
        pass

    @property
    def group_arn(self) -> str:
        """
        The ARN of the group the thing was added to or removed from.
        """
        pass

    @property
    def group_id(self) -> str:
        """
        The unique identifier of the group.
        """
        pass

    @property
    def thing_arn(self) -> str:
        """
        The ARN of the thing being added or removed.
        """
        pass

    @property
    def thing_id(self) -> str:
        """
        The unique identifier for the thing being added or removed.
        """
        pass

    @property
    def membership_id(self) -> str:
        """
        The unique membership ID for the thing within the group.
        """
        pass


class IoTCoreAddOrDeleteFromThingGroupEvent(IoTCoreRegistryEventsBase):
    """
    The registry publishes event messages when a child group is added to or deleted from a parent group.
    """

    @property
    def event_type(self) -> str:
        """
        The event type, corresponding to the add/delete from thing group event.
        """
        pass

    @property
    def operation(self) -> EVENT_ADD_REMOVE_OPERATION:
        """
        The operation (ADDED or REMOVED) performed on the child group.
        """
        pass

    @property
    def account_id(self) -> str:
        """
        The account ID associated with the event.
        """
        pass

    @property
    def thing_group_id(self) -> str:
        """
        The unique identifier of the thing group.
        """
        pass

    @property
    def thing_group_name(self) -> str:
        """
        The name of the thing group.
        """
        pass

    @property
    def child_group_id(self) -> str:
        """
        The unique identifier of the child group being added or removed.
        """
        pass

    @property
    def child_group_name(self) -> str:
        """
        The name of the child group being added or removed.
        """
        pass
