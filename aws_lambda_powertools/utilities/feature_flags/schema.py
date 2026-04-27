from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from dateutil import tz

from aws_lambda_powertools.utilities.feature_flags.base import BaseValidator
from aws_lambda_powertools.utilities.feature_flags.exceptions import SchemaValidationError

if TYPE_CHECKING:
    from aws_lambda_powertools.logging import Logger

from aws_lambda_powertools.utilities.feature_flags.constants import (
    CONDITION_ACTION,
    CONDITION_KEY,
    CONDITION_VALUE,
    CONDITIONS_KEY,
    FEATURE_DEFAULT_VAL_KEY,
    FEATURE_DEFAULT_VAL_TYPE_KEY,
    RULE_MATCH_VALUE,
    RULES_KEY,
    TIME_RANGE_FORMAT,
    TIME_RANGE_PATTERN,
)

LOGGER: logging.Logger | Logger = logging.getLogger(__name__)


class RuleAction(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    KEY_GREATER_THAN_VALUE = "KEY_GREATER_THAN_VALUE"
    KEY_GREATER_THAN_OR_EQUAL_VALUE = "KEY_GREATER_THAN_OR_EQUAL_VALUE"
    KEY_LESS_THAN_VALUE = "KEY_LESS_THAN_VALUE"
    KEY_LESS_THAN_OR_EQUAL_VALUE = "KEY_LESS_THAN_OR_EQUAL_VALUE"
    STARTSWITH = "STARTSWITH"
    ENDSWITH = "ENDSWITH"
    IN = "IN"
    NOT_IN = "NOT_IN"
    KEY_IN_VALUE = "KEY_IN_VALUE"
    KEY_NOT_IN_VALUE = "KEY_NOT_IN_VALUE"
    VALUE_IN_KEY = "VALUE_IN_KEY"
    VALUE_NOT_IN_KEY = "VALUE_NOT_IN_KEY"
    ALL_IN_VALUE = "ALL_IN_VALUE"
    ANY_IN_VALUE = "ANY_IN_VALUE"
    NONE_IN_VALUE = "NONE_IN_VALUE"
    SCHEDULE_BETWEEN_TIME_RANGE = "SCHEDULE_BETWEEN_TIME_RANGE"  # hour:min 24 hours clock
    SCHEDULE_BETWEEN_DATETIME_RANGE = "SCHEDULE_BETWEEN_DATETIME_RANGE"  # full datetime format, excluding timezone
    SCHEDULE_BETWEEN_DAYS_OF_WEEK = "SCHEDULE_BETWEEN_DAYS_OF_WEEK"  # MONDAY, TUESDAY, .... see TimeValues enum
    MODULO_RANGE = "MODULO_RANGE"


class TimeKeys(Enum):
    """
    Possible keys when using time rules
    """

    CURRENT_TIME = "CURRENT_TIME"
    CURRENT_DAY_OF_WEEK = "CURRENT_DAY_OF_WEEK"
    CURRENT_DATETIME = "CURRENT_DATETIME"


class TimeValues(Enum):
    """
    Possible values when using time rules
    """

    START = "START"
    END = "END"
    TIMEZONE = "TIMEZONE"
    DAYS = "DAYS"
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"

    @classmethod
    @lru_cache(maxsize=1)
    def days(cls) -> list[str]:
        pass


class ModuloRangeValues(Enum):
    """
    Possible values when using modulo range rule
    """

    BASE = "BASE"
    START = "START"
    END = "END"


class SchemaValidator(BaseValidator):
    """Validates feature flag schema configuration

    Raises
    ------
    SchemaValidationError
        When schema doesn't conform with feature flag schema

    Schema
    ------

    **Feature object**

    A dictionary containing default value and rules for matching.
    The value MUST be an object and MIGHT contain the following members:

    * **default**: `bool | JSONType`. Defines default feature value. This MUST be present
    * **boolean_type**: bool. Defines whether feature has non-boolean value (`JSONType`). This MIGHT be present
    * **rules**: `dict[str, dict]`. Rules object. This MIGHT be present

    `JSONType` being any JSON primitive value: `str | int | float | bool | None | dict[str, Any] | list[Any]`

    ```json
    {
        "my_feature": {
            "default": true,
            "rules": {}
        },
        "my_non_boolean_feature": {
            "default": {"group": "read-only"},
            "boolean_type": false,
            "rules": {}
        }
    }
    ```

    **Rules object**

    A dictionary with each rule and their conditions that a feature might have.
    The value MIGHT be present, and when defined it MUST contain the following members:

    * **when_match**: `bool | JSONType`. Defines value to return when context matches conditions
    * **conditions**: `list[dict]`. Conditions object. This MUST be present

    ```json
    {
        "my_feature": {
            "default": true,
            "rules": {
                "tenant id equals 345345435": {
                    "when_match": false,
                    "conditions": []
                }
            }
        },
        "my_non_boolean_feature": {
            "default": {"group": "read-only"},
            "boolean_type": false,
            "rules": {
                "tenant id equals 345345435": {
                    "when_match": {"group": "admin"},
                    "conditions": []
                }
            }
        }
    }
    ```

    **Conditions object**

    A list of dictionaries containing conditions for a given rule.
    The value MUST contain the following members:

    * **action**: `str`. Operation to perform to match a key and value.
    The value MUST be either EQUALS, STARTSWITH, ENDSWITH,
    KEY_IN_VALUE KEY_NOT_IN_VALUE VALUE_IN_KEY VALUE_NOT_IN_KEY

    * **key**: `str`. Key in given context to perform operation
    * **value**: `Any`. Value in given context that should match action operation.

    ```json
    {
        "my_feature": {
            "default": true,
            "rules": {
                "tenant id equals 345345435": {
                    "when_match": false,
                    "conditions": [
                        {
                            "action": "EQUALS",
                            "key": "tenant_id",
                            "value": "345345435",
                        }
                    ]
                }
            }
        }
    }
    ```
    """

    def __init__(self, schema: dict[str, Any], logger: logging.Logger | Logger | None = None):
        self.schema = schema
        self.logger = logger or LOGGER

        # Validators are designed for modular testing
        # therefore we link the custom logger with global LOGGER
        # so custom validators can use them when necessary
        SchemaValidator._link_global_logger(self.logger)

    def validate(self) -> None:
        self.logger.debug("Validating schema")
        if not isinstance(self.schema, dict):
            raise SchemaValidationError(f"Features must be a dictionary, schema={str(self.schema)}")

        features = FeaturesValidator(schema=self.schema, logger=self.logger)
        features.validate()

    @staticmethod
    def _link_global_logger(logger: logging.Logger | Logger):
        global LOGGER
        LOGGER = logger


class FeaturesValidator(BaseValidator):
    """Validates each feature and calls RulesValidator to validate its rules"""

    def __init__(self, schema: dict, logger: logging.Logger | Logger | None = None):
        self.schema = schema
        self.logger = logger or LOGGER

    def validate(self):
        for name, feature in self.schema.items():
            self.logger.debug(f"Attempting to validate feature '{name}'")
            boolean_feature: bool = self.validate_feature(name, feature)
            rules = RulesValidator(feature=feature, boolean_feature=boolean_feature, logger=self.logger)
            rules.validate()

    # returns True in case the feature is a regular feature flag with a  boolean default value
    @staticmethod
    def validate_feature(name, feature) -> bool:
        if not feature or not isinstance(feature, dict):
            raise SchemaValidationError(f"Feature must be a non-empty dictionary, feature={name}")

        default_value: Any = feature.get(FEATURE_DEFAULT_VAL_KEY)
        boolean_feature: bool = feature.get(FEATURE_DEFAULT_VAL_TYPE_KEY, True)
        # if feature is boolean_feature, default_value must be a boolean type.
        # default_value must exist
        # Maintenance: Revisit before going GA. We might to simplify customers on-boarding by not requiring it
        # for non-boolean flags.
        if default_value is None or (not isinstance(default_value, bool) and boolean_feature):
            raise SchemaValidationError(f"feature 'default' boolean key must be present, feature={name}")
        return boolean_feature


class RulesValidator(BaseValidator):
    """Validates each rule and calls ConditionsValidator to validate each rule's conditions"""

    def __init__(
        self,
        feature: dict[str, Any],
        boolean_feature: bool,
        logger: logging.Logger | Logger | None = None,
    ):
        self.feature = feature
        self.feature_name = next(iter(self.feature))
        self.rules: dict | None = self.feature.get(RULES_KEY)
        self.logger = logger or LOGGER
        self.boolean_feature = boolean_feature

    def validate(self):
        if not self.rules:
            self.logger.debug("Rules are empty, ignoring validation")
            return

        if not isinstance(self.rules, dict):
            self.logger.debug(f"Feature rules must be a dictionary, feature={self.feature_name}")
            raise SchemaValidationError(f"Feature rules must be a dictionary, feature={self.feature_name}")

        for rule_name, rule in self.rules.items():
            self.logger.debug(f"Attempting to validate rule={rule_name} and feature={self.feature_name}")
            self.validate_rule(
                rule=rule,
                rule_name=rule_name,
                feature_name=self.feature_name,
                boolean_feature=self.boolean_feature,
            )
            conditions = ConditionsValidator(rule=rule, rule_name=rule_name, logger=self.logger)
            conditions.validate()

    @staticmethod
    def validate_rule(rule: dict, rule_name: str, feature_name: str, boolean_feature: bool = True):
        if not rule or not isinstance(rule, dict):
            raise SchemaValidationError(f"Feature rule must be a dictionary, feature={feature_name}")

        RulesValidator.validate_rule_name(rule_name=rule_name, feature_name=feature_name)
        RulesValidator.validate_rule_default_value(rule=rule, rule_name=rule_name, boolean_feature=boolean_feature)

    @staticmethod
    def validate_rule_name(rule_name: str, feature_name: str):
        if not rule_name or not isinstance(rule_name, str):
            raise SchemaValidationError(f"Rule name key must have a non-empty string, feature={feature_name}")

    @staticmethod
    def validate_rule_default_value(rule: dict, rule_name: str, boolean_feature: bool):
        rule_default_value = rule.get(RULE_MATCH_VALUE)
        if boolean_feature and not isinstance(rule_default_value, bool):
            raise SchemaValidationError(f"'rule_default_value' key must have be bool, rule={rule_name}")


class ConditionsValidator(BaseValidator):
    def __init__(self, rule: dict[str, Any], rule_name: str, logger: logging.Logger | Logger | None = None):
        self.conditions: list[dict[str, Any]] = rule.get(CONDITIONS_KEY, {})
        self.rule_name = rule_name
        self.logger = logger or LOGGER

    def validate(self):
        if not self.conditions or not isinstance(self.conditions, list):
            self.logger.debug(f"Condition is empty or invalid for rule={self.rule_name}")
            raise SchemaValidationError(f"Invalid condition, rule={self.rule_name}")

        for condition in self.conditions:
            # Condition can contain PII data; do not log condition value
            self.logger.debug(f"Attempting to validate condition for {self.rule_name}")
            self.validate_condition(rule_name=self.rule_name, condition=condition)

    @staticmethod
    def validate_condition(rule_name: str, condition: dict[str, str]) -> None:
        if not condition or not isinstance(condition, dict):
            raise SchemaValidationError(f"Feature rule condition must be a dictionary, rule={rule_name}")

        ConditionsValidator.validate_condition_action(condition=condition, rule_name=rule_name)
        ConditionsValidator.validate_condition_key(condition=condition, rule_name=rule_name)
        ConditionsValidator.validate_condition_value(condition=condition, rule_name=rule_name)

    @staticmethod
    def validate_condition_action(condition: dict[str, Any], rule_name: str):
        action = condition.get(CONDITION_ACTION, "")
        if action not in RuleAction.__members__:
            allowed_values = [_action.value for _action in RuleAction]
            raise SchemaValidationError(
                f"'action' value must be either {allowed_values}, rule_name={rule_name}, action={action}",
            )

    @staticmethod
    def validate_condition_key(condition: dict[str, Any], rule_name: str):
        key = condition.get(CONDITION_KEY, "")
        if not key or not isinstance(key, str):
            raise SchemaValidationError(f"'key' value must be a non empty string, rule={rule_name}")

        action = condition.get(CONDITION_ACTION, "")

        # To allow for growth and prevent if/elif chains, we align extra validators based on the action name.
        # for example:
        #
        # SCHEDULE_BETWEEN_DAYS_OF_WEEK_KEY
        # - extra validation: `_validate_schedule_between_days_of_week_key`
        #
        # maintenance: we should split to separate file/classes for better organization, e.g., visitor pattern.

        custom_validator = getattr(ConditionsValidator, f"_validate_{action.lower()}_key", None)

        # ~90% of actions available don't require a custom validator
        # logging a debug statement for no-match will increase CPU cycles for most customers
        # for that reason only, we invert and log only when extra validation is found.
        if custom_validator is None:
            return

        LOGGER.debug(f"{action} requires key validation. Running '{custom_validator}' validator.")
        custom_validator(key, rule_name)

    @staticmethod
    def validate_condition_value(condition: dict[str, Any], rule_name: str):
        value = condition.get(CONDITION_VALUE)
        if value is None:
            raise SchemaValidationError(f"'value' key must not be null, rule={rule_name}")
        action = condition.get(CONDITION_ACTION, "")

        # To allow for growth and prevent if/elif chains, we align extra validators based on the action name.
        # for example:
        #
        # SCHEDULE_BETWEEN_DAYS_OF_WEEK_KEY
        # - extra validation: `_validate_schedule_between_days_of_week_value`
        #
        # maintenance: we should split to separate file/classes for better organization, e.g., visitor pattern.

        custom_validator = getattr(ConditionsValidator, f"_validate_{action.lower()}_value", None)

        # ~90% of actions available don't require a custom validator
        # logging a debug statement for no-match will increase CPU cycles for most customers
        # for that reason only, we invert and log only when extra validation is found.
        if custom_validator is None:
            return

        LOGGER.debug(f"{action} requires value validation. Running '{custom_validator}' validator.")

        custom_validator(value, rule_name)

    @staticmethod
    def _validate_schedule_between_days_of_week_key(key: str, rule_name: str):
        pass

    @staticmethod
    def _validate_schedule_between_days_of_week_value(value: dict, rule_name: str):
        pass

    @staticmethod
    def _validate_schedule_between_time_range_key(key: str, rule_name: str):
        pass

    @staticmethod
    def _validate_schedule_between_time_range_value(value: dict, rule_name: str):
        pass

    @staticmethod
    def _validate_schedule_between_datetime_range_key(key: str, rule_name: str):
        pass

    @staticmethod
    def _validate_schedule_between_datetime_range_value(value: dict, rule_name: str):
        pass

    @staticmethod
    def _validate_modulo_range_value(value: dict, rule_name: str):
        pass

    @staticmethod
    def _validate_all_in_value_value(value: list, rule_name: str):
        pass

    @staticmethod
    def _validate_any_in_value_value(value: list, rule_name: str):
        pass

    @staticmethod
    def _validate_none_in_value_value(value: list, rule_name: str):
        pass

    @staticmethod
    def _validate_datetime(datetime_str: str, rule_name: str):
        pass

    @staticmethod
    def _validate_timezone(rule: str, timezone: str | None = None):
        pass
