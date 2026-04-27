from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CloudWatchAlarmState(DictWrapper):
    @property
    def value(self) -> Literal["OK", "ALARM", "INSUFFICIENT_DATA"]:
        """
        Overall state of the alarm.
        """
        pass

    @property
    def reason(self) -> str:
        """
        Reason why alarm was changed to this state.
        """
        pass

    @property
    def reason_data(self) -> str:
        """
        Additional data to back up the reason, usually contains the evaluated data points,
        the calculated threshold and timestamps.
        """
        pass

    @cached_property
    def reason_data_decoded(self) -> Any | None:
        """
        Deserialized version of reason_data.
        """
        pass

    @property
    def actions_suppressed_by(self) -> Literal["Alarm", "ExtensionPeriod", "WaitPeriod"] | None:
        """
        Describes why the actions when the value is `ALARM` are suppressed in a composite
        alarm.
        """
        pass

    @property
    def actions_suppressed_reason(self) -> str | None:
        """
        Captures the reason for action suppression.
        """
        pass

    @property
    def timestamp(self) -> str:
        """
        Timestamp of this state change in ISO-8601 format.
        """
        return self["timestamp"]


class CloudWatchAlarmMetric(DictWrapper):
    @property
    def metric_id(self) -> str:
        """
        Unique ID of the alarm metric.
        """
        pass

    @property
    def expression(self) -> str | None:
        """
        Optional expression of the alarm metric.
        """
        pass

    @property
    def label(self) -> str | None:
        """
        Optional label of the alarm metric.
        """
        pass

    @property
    def return_data(self) -> bool:
        """
        Whether this metric data is used to determine the state of the alarm or not.
        """
        pass

    @property
    def metric_stat(self) -> CloudWatchAlarmMetricStat:
        pass


class CloudWatchAlarmMetricStat(DictWrapper):
    @property
    def period(self) -> int | None:
        """
        Metric evaluation period, in seconds.
        """
        pass

    @property
    def stat(self) -> str | None:
        """
        Statistical aggregation of metric points, e.g. Average, SampleCount, etc.
        """
        pass

    @property
    def unit(self) -> str | None:
        """
        Unit for metric.
        """
        pass

    @property
    def metric(self) -> dict:
        """
        Metric details
        """
        pass


class CloudWatchAlarmData(DictWrapper):
    @property
    def alarm_name(self) -> str:
        """
        Alarm name.
        """
        pass

    @property
    def state(self) -> CloudWatchAlarmState:
        """
        The current state of the Alarm.
        """
        pass

    @property
    def previous_state(self) -> CloudWatchAlarmState:
        """
        The previous state of the Alarm.
        """
        pass

    @property
    def configuration(self) -> CloudWatchAlarmConfiguration:
        """
        The configuration of the Alarm.
        """
        pass


class CloudWatchAlarmConfiguration(DictWrapper):
    @property
    def description(self) -> str | None:
        """
        Optional description for the Alarm.
        """
        pass

    @property
    def alarm_rule(self) -> str | None:
        """
        Optional description for the Alarm rule in case of composite alarm.
        """
        pass

    @property
    def alarm_actions_suppressor(self) -> str | None:
        """
        Optional action suppression for the Alarm rule in case of composite alarm.
        """
        pass

    @property
    def alarm_actions_suppressor_wait_period(self) -> str | None:
        """
        Optional action suppression wait period for the Alarm rule in case of composite alarm.
        """
        pass

    @property
    def alarm_actions_suppressor_extension_period(self) -> str | None:
        """
        Optional action suppression extension period for the Alarm rule in case of composite alarm.
        """
        pass

    @property
    def metrics(self) -> list[CloudWatchAlarmMetric]:
        """
        The metrics evaluated for the Alarm.
        """
        pass


class CloudWatchAlarmEvent(DictWrapper):
    @property
    def source(self) -> Literal["aws.cloudwatch"]:
        """
        Source of the triggered event.
        """
        pass

    @property
    def alarm_arn(self) -> str:
        """
        The ARN of the CloudWatch Alarm.
        """
        pass

    @property
    def region(self) -> str:
        """
        The AWS region in which the Alarm is active.
        """
        pass

    @property
    def source_account_id(self) -> str:
        """
        The AWS Account ID that the Alarm is deployed to.
        """
        pass

    @property
    def timestamp(self) -> str:
        """
        Alarm state change event timestamp in ISO-8601 format.
        """
        return self["time"]

    @property
    def alarm_data(self) -> CloudWatchAlarmData:
        """
        Contains basic data about the Alarm and its current and previous states.
        """
        pass
