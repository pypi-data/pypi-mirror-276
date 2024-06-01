from __future__ import annotations

import numpy as np
import xarray as xr

from mfire.text.wind.reducers.base_param_force import BaseParamForce
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_period import WindPeriod
from mfire.utils.date import Datetime, Period


class WindForce(BaseParamForce):
    """WindForce class."""

    DEFAULT_PRECISION: int = 5
    PERCENTILE_NUM: int = 95

    def __init__(self, force: float, precision: int = DEFAULT_PRECISION):
        super().__init__(force, precision)

    def __add__(self, other: WindForce) -> WindForce:
        """Add 2 WindForce instances."""
        lower_bound: int = min(self.interval[0], other.interval[0])
        upper_bound: int = max(self.interval[1], other.interval[1])
        precision: int = upper_bound - lower_bound

        return WindForce(lower_bound, precision)

    @classmethod
    def data_array_to_value(cls, data_array: xr.DataArray) -> float:
        """Find the value which represents the input DataArray."""
        return float(np.percentile(data_array.values, cls.PERCENTILE_NUM))


class WindForcePeriod(WindPeriod[WindForce]):
    """WindForcePeriod class."""

    def update(self, date: Datetime, wind_element: WindForce) -> bool:
        """Update the period with a Datetime and a WindForce."""
        if wind_element != self._wind_element:
            return False

        if date < self.begin_time:
            self._period.begin_time = date
        elif date > self.begin_time:
            self._period.end_time = date
        return True

    @property
    def period(self) -> Period:
        return self._period

    def has_same_force_than(self, other: WindForcePeriod) -> bool:
        return self.wind_element == other.wind_element

    def is_juxtaposed_with(self, other: WindForcePeriod):
        wf1: WindForce = self.wind_element
        wf2: WindForce = other.wind_element
        precision: int = WindForce.DEFAULT_PRECISION

        if (wf1.precision, wf2.precision) != (precision, precision):
            return False

        if wf1.repr_value == wf2.repr_value + precision:
            return True
        if wf2.repr_value == wf1.repr_value + precision:
            return True
        return False

    def __add__(self, other: WindForcePeriod) -> WindForcePeriod:
        """Add 2 WindForcePeriod instances."""
        return WindForcePeriod(
            min(self.begin_time, other.begin_time),
            max(self.end_time, other.end_time),
            self.wind_element + other.wind_element,
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(begin_time={self.begin_time}, "
            f"end_time={self.end_time}), wind_force={self.wind_element}"
        )

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the WindForcePeriod instance."""
        summary: dict = super().summarize(reference_datetime)
        summary[self.WF_INTERVAL] = self.wind_element.interval

        return summary
