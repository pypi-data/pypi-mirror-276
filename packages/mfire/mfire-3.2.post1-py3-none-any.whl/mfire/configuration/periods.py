from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

from mfire.composite.period import Period, PeriodCollection
from mfire.composite.serialized_types import s_datetime
from mfire.settings import get_logger
from mfire.utils.date import Datetime, Timedelta

LOGGER = get_logger(name=__name__, bind="periods")


class PeriodElementConfig(BaseModel):
    """Cette classe permet de créer un objet PeriodElementConfig

    Inheritance : BaseModel

    Returns:
        baseModel : objet PeriodElementConfig
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    start: Optional[int] = Field(None)
    delta_start: Optional[int] = Field(None, alias="deltaStart")
    absolu_start: Optional[s_datetime] = Field(None, alias="absoluStart")
    stop: Optional[int] = Field(None)
    delta_stop: Optional[int] = Field(None, alias="deltaStop")
    absolu_stop: Optional[s_datetime] = Field(None, alias="absoluStop")
    production_time_until: int = Field(24, ge=0, le=24, alias="productionTime_until")

    @model_validator(mode="before")
    def init_start_stop(cls, values: dict) -> dict:
        """validator to check the given period element consistency"""
        # check start
        start_keys = ("start", "deltaStart", "absoluStart", "Start")
        start_count = sum(key in values for key in start_keys)
        if start_count != 1:
            raise ValueError(f"Exactly one 'start' key expected. {start_count} given.")
        # A bug in Metronome sometimes gives us the "Start" key instead of "start"
        if "Start" in values:
            values["start"] = values.pop("Start")
        if "absoluStart" in values:
            values["absoluStart"] = Datetime(values["absoluStart"])

        # check stop
        stop_keys = ("stop", "deltaStop", "absoluStop", "Stop")
        stop_count = sum(key in values for key in stop_keys)
        if stop_count != 1:
            raise ValueError(f"Exactly one 'stop' key expected. {stop_count} given.")
        # workaround for Stop in config file instead of stop : shift to stop key
        if "Stop" in values:
            values["stop"] = values.pop("Stop")
        if "absoluStop" in values:
            values["absoluStop"] = Datetime(values["absoluStop"])

        return values

    def get_bound_datetime(
        self, production_datetime: Datetime, bound_name: str
    ) -> Datetime:
        """Method creating a datetime out of a given bound_name and
        a reference datetime.
        Example:
        >>> el = PeriodElement(deltaStart=1, stop=32, productionTime_until=16)
        >>> ref_dt = Datetime(2021, 11, 3, 10)
        >>> el.get_bound_datetime(ref_dt, "start")
        Datetime(2021, 11, 3, 11)
        >>> el.get_bound_datetime(ref_dt, "stop")
        Datetime(2021, 11, 4, 8)
        >>> el.get_bound_datetime(Datetime(2021, 11, 3, 17), "stop")
        Datetime(2021, 11, 5, 8)

        >>> el = PeriodElement(
        >>>    start=1, absoluStop=Datetime(2021, 1, 1), productionTime_until=16
        >>> )
        >>> el.get_bound_datetime(ref_dt, "stop")
        Datetime(2021, 1, 1)

        Args:
            production_datetime (Datetime): Reference datetime.
            bound_key (str): Key representing the bound (e.g. "start", "delta_start",
                "absolu_start", etc.)
            bound (Union[int, Datetime]): Value to transform as datetime.
            next_day (bool, optional): Whether we must look forward to the day after the
                given reference one. Only used when bound_key is "start" or "stop".
                    Defaults to False.

        Returns:
            Datetime: datetime corresponding to the given bound and reference datetime.
        """
        bound_key, bound_value = next(
            (
                (key, self.__dict__.get(key))
                for key in self.model_fields.keys()
                if bound_name in key and self.__dict__.get(key) is not None
            ),
            (bound_name, None),
        )
        if bound_value is None:
            LOGGER.error(
                f"(bound_key, bound_value)=({bound_key}, {bound_value}) "
                f"with bound_name={bound_name}",
                **self.model_dump(),
            )

        if bound_key.startswith("absolu"):
            result = bound_value

        elif bound_key.startswith("delta"):
            result = production_datetime + Timedelta(hours=bound_value)

        else:
            # if the production_datetime is 00h and the production goes until 00h,
            # we produce the bulletin for the next period since we're somewhere
            # between 00h and 01h and we don't want to produce bulletin in the past
            if production_datetime.hour >= self.production_time_until:
                nb_days_shift = 1
            else:
                nb_days_shift = 0

            result = production_datetime.midnight + Timedelta(
                days=nb_days_shift, hours=bound_value
            )
        if result < production_datetime:
            LOGGER.warning(
                f"Configured '{bound_name}' datetime ({result}) is before the given "
                f"reference datetime ({production_datetime})."
            )
        return result

    def get_start_stop_datetime(
        self, production_datetime: Datetime
    ) -> Tuple[Datetime, Datetime]:
        """Returns the start and stop datetime corresponding to
        the self configuration and a given reference datetime.

        Args:
            production_datetime (Datetime): Reference datetime

        Returns:
            Tuple[Datetime, Datetime]: Start and stop datetime.
        """
        start = self.get_bound_datetime(production_datetime, "start")
        stop = self.get_bound_datetime(production_datetime, "stop")

        if start > stop:
            LOGGER.warning(
                f"Configured start datetime ({start}) is after the "
                f"configured stop datetime ({stop})."
            )
        return start, stop


class _AbstractPeriodConfig(BaseModel, ABC):
    """Abstract Period class with an id, a name and an abstract method
    get_processed_period"""

    id: str
    name: Optional[str] = None

    @abstractmethod
    def get_processed_period(self, production_datetime: Datetime) -> Period:
        """Returns the processed period (mfire.composite.periods.Period) corresponding
        to the given production datetime.

        Args:
            production_datetime (Datetime): Current production datetime.

        Returns:
            Period: Period with concrete start and stop datetimes.
        """


class PeriodSingleElementConfig(_AbstractPeriodConfig, PeriodElementConfig):
    """PeriodSingleElement class : Period without a list of periodElements"""

    def get_processed_period(self, production_datetime: Datetime) -> Period:
        start, stop = self.get_start_stop_datetime(production_datetime)
        return Period(id=self.id, name=self.name, start=start, stop=stop)


class PeriodMultipleElementConfig(_AbstractPeriodConfig):
    """PeriodMultipleElement: class Period with multiple periodElements"""

    period_elements: List[PeriodElementConfig] = Field(
        ..., min_length=1, alias="periodElements"
    )

    @field_validator("period_elements")
    def sort_elements(
        cls, elements: List[PeriodElementConfig]
    ) -> List[PeriodElementConfig]:
        """validator sorting given period elements"""
        return sorted(elements, key=lambda element: element.production_time_until)

    def get_processed_period(self, production_datetime: Datetime) -> Period:
        # As soon as production_datetime == pt_until, we want to pick the next period
        # because it means that the current hour as already started and we don't want
        # to describe past events
        element = next(
            (
                el
                for el in self.period_elements
                if production_datetime.hour < el.production_time_until
            ),
            self.period_elements[0],
        )
        start, stop = element.get_start_stop_datetime(production_datetime)
        return Period(id=self.id, name=self.name, start=start, stop=stop)


PeriodConfig = Union[PeriodSingleElementConfig, PeriodMultipleElementConfig]


class PeriodCollectionConfig(BaseModel):
    """Cette classe permet de créer un objet PeriodCollectionConfig

    Inheritance : BaseModel

    Returns:
        baseModel : liste d'objet PeriodConfig
    """

    periods: List[PeriodConfig]

    def __iter__(self):
        """iterate over periods"""
        return iter(self.periods)

    def __len__(self):
        """return periods length"""
        return len(self.periods)

    def __getitem__(self, period_id: str) -> PeriodConfig:
        """get periods at a given index"""
        try:
            return next(period for period in self.periods if period.id == period_id)
        except StopIteration as excpt:
            raise KeyError(f"'{period_id}'") from excpt

    def get(self, index: str, default: Any = None) -> PeriodConfig:
        """get period with a default value in case"""
        try:
            return self[index]
        except KeyError:
            return default

    def get_processed_periods(self, production_datetime: Datetime) -> PeriodCollection:
        return PeriodCollection(
            periods=[
                period.get_processed_period(production_datetime)
                for period in self.periods
            ]
        )


def period_factory(configuration: dict) -> PeriodConfig:
    """Factory function for creating the proper PeriodConfig object
    according to the given configuration.

    Args:
        configuration (dict): Configuration dictionary.

    Returns:
        Period: Corresponding period.
    """
    if "periodElements" in configuration:
        return PeriodMultipleElementConfig(**configuration)
    return PeriodSingleElementConfig(**configuration)
