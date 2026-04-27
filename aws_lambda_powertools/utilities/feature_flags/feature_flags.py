from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from aws_lambda_powertools.utilities.feature_flags import schema
from aws_lambda_powertools.utilities.feature_flags.comparators import (
    compare_all_in_list,
    compare_any_in_list,
    compare_datetime_range,
    compare_days_of_week,
    compare_modulo_range,
    compare_none_in_list,
    compare_time_range,
)
from aws_lambda_powertools.utilities.feature_flags.exceptions import ConfigurationStoreError

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.logging import Logger
    from aws_lambda_powertools.utilities.feature_flags.base import StoreProvider
    from aws_lambda_powertools.utilities.feature_flags.types import JSONType, P, T


RULE_ACTION_MAPPING: dict[str, Callable[..., bool]] = {
    schema.RuleAction.EQUALS.value: lambda a, b: a == b,
    schema.RuleAction.NOT_EQUALS.value: lambda a, b: a != b,
    schema.RuleAction.KEY_GREATER_THAN_VALUE.value: lambda a, b: a > b,
    schema.RuleAction.KEY_GREATER_THAN_OR_EQUAL_VALUE.value: lambda a, b: a >= b,
    schema.RuleAction.KEY_LESS_THAN_VALUE.value: lambda a, b: a < b,
    schema.RuleAction.KEY_LESS_THAN_OR_EQUAL_VALUE.value: lambda a, b: a <= b,
    schema.RuleAction.STARTSWITH.value: lambda a, b: a.startswith(b),
    schema.RuleAction.ENDSWITH.value: lambda a, b: a.endswith(b),
    schema.RuleAction.IN.value: lambda a, b: a in b,
    schema.RuleAction.NOT_IN.value: lambda a, b: a not in b,
    schema.RuleAction.KEY_IN_VALUE.value: lambda a, b: a in b,
    schema.RuleAction.KEY_NOT_IN_VALUE.value: lambda a, b: a not in b,
    schema.RuleAction.VALUE_IN_KEY.value: lambda a, b: b in a,
    schema.RuleAction.VALUE_NOT_IN_KEY.value: lambda a, b: b not in a,
    schema.RuleAction.ALL_IN_VALUE.value: compare_all_in_list,
    schema.RuleAction.ANY_IN_VALUE.value: compare_any_in_list,
    schema.RuleAction.NONE_IN_VALUE.value: compare_none_in_list,
    schema.RuleAction.SCHEDULE_BETWEEN_TIME_RANGE.value: compare_time_range,
    schema.RuleAction.SCHEDULE_BETWEEN_DATETIME_RANGE.value: compare_datetime_range,
    schema.RuleAction.SCHEDULE_BETWEEN_DAYS_OF_WEEK.value: compare_days_of_week,
    schema.RuleAction.MODULO_RANGE.value: compare_modulo_range,
}


class FeatureFlags:
    def __init__(self, store: StoreProvider, logger: logging.Logger | Logger | None = None):
        """Evaluates whether feature flags should be enabled based on a given context.

        It uses the provided store to fetch feature flag rules before evaluating them.

        Examples
        --------

        ```python
        from aws_lambda_powertools.utilities.feature_flags import FeatureFlags, AppConfigStore

        app_config = AppConfigStore(
            environment="test",
            application="powertools",
            name="test_conf_name",
            max_age=300,
            envelope="features"
        )

        feature_flags: FeatureFlags = FeatureFlags(store=app_config)
        ```

        Parameters
        ----------
        store: StoreProvider
            Store to use to fetch feature flag schema configuration.
        logger: A logging object
            Used to log messages. If None is supplied, one will be created.
        """
        self.store = store
        self.logger = logger or logging.getLogger(__name__)
        self._exception_handlers: dict[Exception, Callable] = {}

    def _match_by_action(self, action: str, condition_value: Any, context_value: Any) -> bool:
        pass

    def _evaluate_conditions(
        self,
        rule_name: str,
        feature_name: str,
        rule: dict[str, Any],
        context: dict[str, Any],
    ) -> bool:
        """Evaluates whether context matches conditions, return False otherwise"""
        pass

    def _evaluate_rules(
        self,
        *,
        feature_name: str,
        context: dict[str, Any],
        feat_default: Any,
        rules: dict[str, Any],
        boolean_feature: bool,
    ) -> bool:
        """Evaluates whether context matches rules and conditions, otherwise return feature default"""
        pass

    def get_configuration(self) -> dict:
        """Get validated feature flag schema from configured store.

        Largely used to aid testing, since it's called by `evaluate` and `get_enabled_features` methods.

        Raises
        ------
        ConfigurationStoreError
            Any propagated error from store
        SchemaValidationError
            When schema doesn't conform with feature flag schema

        Returns
        ------
        dict[str, dict]
            parsed JSON dictionary

        Example
        -------

        ```python
        {
            "premium_features": {
                "default": False,
                "rules": {
                    "customer tier equals premium": {
                        "when_match": True,
                        "conditions": [
                            {
                                "action": "EQUALS",
                                "key": "tier",
                                "value": "premium",
                            }
                        ],
                    }
                },
            },
            "feature_two": {
                "default": False
            }
        }
        ```
        """
        pass

    def evaluate(self, *, name: str, context: dict[str, Any] | None = None, default: JSONType) -> JSONType:
        """Evaluate whether a feature flag should be enabled according to stored schema and input context

        **Logic when evaluating a feature flag**

        1. Feature exists and a rule matches, returns when_match value
        2. Feature exists but has either no rules or no match, return feature default value
        3. Feature doesn't exist in stored schema, encountered an error when fetching -> return default value provided

        ┌────────────────────────┐      ┌────────────────────────┐       ┌────────────────────────┐
        │     Feature flags      │──────▶   Get Configuration    ├───────▶     Evaluate rules     │
        └────────────────────────┘      │                        │       │                        │
                                        │┌──────────────────────┐│       │┌──────────────────────┐│
                                        ││     Fetch schema     ││       ││      Match rule      ││
                                        │└───────────┬──────────┘│       │└───────────┬──────────┘│
                                        │            │           │       │            │           │
                                        │┌───────────▼──────────┐│       │┌───────────▼──────────┐│
                                        ││     Cache schema     ││       ││   Match condition    ││
                                        │└───────────┬──────────┘│       │└───────────┬──────────┘│
                                        │            │           │       │            │           │
                                        │┌───────────▼──────────┐│       │┌───────────▼──────────┐│
                                        ││   Validate schema    ││       ││     Match action     ││
                                        │└──────────────────────┘│       │└──────────────────────┘│
                                        └────────────────────────┘       └────────────────────────┘

        Parameters
        ----------
        name: str
            feature name to evaluate
        context: dict[str, Any] | None
            Attributes that should be evaluated against the stored schema.

            for example: `{"tenant_id": "X", "username": "Y", "region": "Z"}`
        default: JSONType
            default value if feature flag doesn't exist in the schema,
            or there has been an error when fetching the configuration from the store
            Can be boolean or any JSON values for non-boolean features.


        Example
        --------

        ```python
        from aws_lambda_powertools.utilities.feature_flags import AppConfigStore, FeatureFlags
        from aws_lambda_powertools.utilities.typing import LambdaContext

        app_config = AppConfigStore(environment="dev", application="product-catalogue", name="features")

        feature_flags = FeatureFlags(store=app_config)


        def lambda_handler(event: dict, context: LambdaContext):
            # Get customer's tier from incoming request
            ctx = {"tier": event.get("tier", "standard")}

            # Evaluate whether customer's tier has access to premium features
            # based on `has_premium_features` rules
            has_premium_features: bool = feature_flags.evaluate(name="premium_features", context=ctx, default=False)
            if has_premium_features:
                # enable premium features
                ...
        ```

        Returns
        ------
        JSONType
            whether feature should be enabled (bool flags) or JSON value when non-bool feature matches

        Raises
        ------
        SchemaValidationError
            When schema doesn't conform with feature flag schema
        """
        pass

    def get_enabled_features(self, *, context: dict[str, Any] | None = None) -> list[str]:
        """Get all enabled feature flags while also taking into account context
        (when a feature has defined rules)

        Parameters
        ----------
        context: dict[str, Any] | None
            dict of attributes that you would like to match the rules
            against, can be `{'tenant_id: 'X', 'username':' 'Y', 'region': 'Z'}` etc.

        Returns
        ----------
        list[str]
            list of all feature names that either matches context or have True as default

        Example
        -------

        ```python
        ["premium_features", "my_feature_two", "always_true_feature"]
        ```

        Raises
        ------
        SchemaValidationError
            When schema doesn't conform with feature flag schema
        """
        pass

    def validation_exception_handler(self, exc_class: Exception | list[Exception]):
        """Registers function to handle unexpected validation exceptions when evaluating flags.

        It does not override the function of a default flag value in case of network and IAM permissions.
        For example, you won't be able to catch ConfigurationStoreError exception.

        Parameters
        ----------
        exc_class : Exception | list[Exception]
            One or more exceptions to catch

        Example
        -------

        ```python
        feature_flags = FeatureFlags(store=app_config)

        @feature_flags.validation_exception_handler(Exception)  # any exception
        def catch_exception(exc):
            raise TypeError("re-raised") from exc
        ```
        """
        pass

    def _lookup_exception_handler(self, exc: BaseException) -> Callable | None:
        # Use "Method Resolution Order" to allow for matching against a base class
        # of an exception
        pass
