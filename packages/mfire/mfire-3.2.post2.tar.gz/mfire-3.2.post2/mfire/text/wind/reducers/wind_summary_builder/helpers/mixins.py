from mfire.text.wind.reducers.mixins import BaseSummaryBuilderMixin
from mfire.text.wind.selectors import WindSelector

from .wind_enum import WindCase


class WindSummaryBuilderMixin(BaseSummaryBuilderMixin[WindCase]):
    SELECTOR_KEY: str = WindSelector.KEY


class SummaryKeysMixin:
    """SummaryKeysMixin class."""

    BEGIN_TIME_MARKER: str = "begin_time"
    END_TIME_MARKER: str = "end_time"
    TIME_DESC: str = "time_desc"
    TIME_MARKER: str = "time_marker"
    WD: str = "wd"
    WD_PERIOD: str = "wd_period"
    DESC: str = "desc"
    WD_PERIODS: str = "wd_periods"
    WF_INTENSITY: str = "wf_intensity"
    WF_INTERVAL: str = "interval"
    WF_PERIOD: str = "wf_period"
    WF_PERIODS: str = "wf_periods"
    WF_VARIATION_MARKER: str = "var_marker"
