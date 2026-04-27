from __future__ import annotations

from datetime import datetime, tzinfo
from typing import Any

from dateutil.tz import gettz

from aws_lambda_powertools.utilities.feature_flags.constants import HOUR_MIN_SEPARATOR
from aws_lambda_powertools.utilities.feature_flags.schema import ModuloRangeValues, TimeValues


def _get_now_from_timezone(timezone: tzinfo | None) -> datetime:
    """
    Returns now in the specified timezone. Defaults to UTC if not present.
    At this stage, we already validated that the passed timezone string is valid, so we assume that
    gettz() will return a tzinfo object.
    """
    pass


def compare_days_of_week(context_value: Any, condition_value: dict) -> bool:
    pass


def compare_datetime_range(context_value: Any, condition_value: dict) -> bool:
    pass


def compare_time_range(context_value: Any, condition_value: dict) -> bool:
    pass


def compare_modulo_range(context_value: int, condition_value: dict) -> bool:
    """
    Returns for a given context 'a' and modulo condition 'b' -> b.start <= a % b.base <= b.end
    """
    pass


def compare_any_in_list(context_value: list, condition_value: list) -> bool:
    """Comparator for ANY_IN_VALUE action

    Parameters
    ----------
    context_value : list
        user-defined context for flag evaluation
    condition_value : list
        schema value available for condition being evaluated

    Returns
    -------
    bool
        Whether any list item in context_value is available in condition_value
    """
    pass


def compare_all_in_list(context_value: list, condition_value: list) -> bool:
    """Comparator for ALL_IN_VALUE action

    Parameters
    ----------
    context_value : list
        user-defined context for flag evaluation
    condition_value : list
        schema value available for condition being evaluated

    Returns
    -------
    bool
        Whether all list items in context_value are available in condition_value
    """
    pass


def compare_none_in_list(context_value: list, condition_value: list) -> bool:
    """Comparator for NONE_IN_VALUE action

    Parameters
    ----------
    context_value : list
        user-defined context for flag evaluation
    condition_value : list
        schema value available for condition being evaluated

    Returns
    -------
    bool
        Whether list items in context_value are **not** available in condition_value
    """
    pass
