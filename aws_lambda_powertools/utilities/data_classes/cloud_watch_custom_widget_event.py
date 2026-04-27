from __future__ import annotations

from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class TimeZone(DictWrapper):
    @property
    def label(self) -> str:
        """The time range label. Either 'UTC' or 'Local'"""
        pass

    @property
    def offset_iso(self) -> str:
        """The time range offset in the format +/-00:00"""
        pass

    @property
    def offset_in_minutes(self) -> int:
        """The time range offset in minutes"""
        pass


class TimeRange(DictWrapper):
    @property
    def mode(self) -> str:
        """The time range mode, i.e. 'relative' or 'absolute'"""
        pass

    @property
    def start(self) -> int:
        """The start time within the time range"""
        pass

    @property
    def end(self) -> int:
        """The end time within the time range"""
        pass

    @property
    def relative_start(self) -> int | None:
        """The relative start time within the time range"""
        pass

    @property
    def zoom_start(self) -> int | None:
        """The start time within the zoomed time range"""
        pass

    @property
    def zoom_end(self) -> int | None:
        """The end time within the zoomed time range"""
        pass


class CloudWatchWidgetContext(DictWrapper):
    @property
    def dashboard_name(self) -> str:
        """Get dashboard name, in which the widget is used"""
        pass

    @property
    def widget_id(self) -> str:
        """Get widget ID"""
        pass

    @property
    def domain(self) -> str:
        """AWS domain name"""
        pass

    @property
    def account_id(self) -> str:
        """Get AWS Account ID"""
        pass

    @property
    def locale(self) -> str:
        """Get locale language"""
        pass

    @property
    def timezone(self) -> TimeZone:
        """Timezone information of the dashboard"""
        pass

    @property
    def period(self) -> int:
        """The period shown on the dashboard"""
        pass

    @property
    def is_auto_period(self) -> bool:
        """Whether auto period is enabled"""
        pass

    @property
    def time_range(self) -> TimeRange:
        """The widget time range"""
        pass

    @property
    def theme(self) -> str:
        """The dashboard theme, i.e. 'light' or 'dark'"""
        pass

    @property
    def link_charts(self) -> bool:
        """The widget is linked to other charts"""
        pass

    @property
    def title(self) -> str:
        """Get widget title"""
        return self["title"]

    @property
    def params(self) -> dict[str, Any]:
        """Get widget parameters"""
        pass

    @property
    def forms(self) -> dict[str, Any]:
        """Get widget form data"""
        pass

    @property
    def height(self) -> int:
        """Get widget height"""
        pass

    @property
    def width(self) -> int:
        """Get widget width"""
        pass


class CloudWatchDashboardCustomWidgetEvent(DictWrapper):
    """CloudWatch dashboard custom widget event

    You can use a Lambda function to create a custom widget on a CloudWatch dashboard.

    Documentation:
    -------------
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/add_custom_widget_dashboard_about.html
    """

    @property
    def describe(self) -> bool:
        """Display widget documentation"""
        pass

    @property
    def widget_context(self) -> CloudWatchWidgetContext | None:
        """The widget context"""
        pass
