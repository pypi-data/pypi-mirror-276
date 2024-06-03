from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Literal, Optional, Union

import numpy as np
from pydantic import field_validator

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseComposite
from mfire.composite.serialized_types import s_Datetime
from mfire.composite.level import LevelComposite
from mfire.composite.period import Period
from mfire.composite.weather import WeatherComposite
from mfire.settings import get_logger
from mfire.utils.date import Datetime
from mfire.utils.exception import LoaderError
from mfire.utils.xr import Loader

# Logging
LOGGER = get_logger(name="components.mod", bind="components")


class TypeComponent(str, Enum):
    """Enumeration class containing the types of components"""

    RISK = "risk"
    SYNTHESIS = "text"


class AbstractComponentComposite(BaseComposite, ABC):
    """
    This abstract class implements the ComponentComposite design pattern,
    which is used to create components of type text or risk.

    Inherits: BaseComposite
    """

    period: Period
    id: str
    type: TypeComponent
    name: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    geos: Optional[List[str]] = None
    production_id: str
    production_name: str
    production_datetime: s_Datetime
    configuration_datetime: Optional[s_Datetime] = Datetime()
    time_dimension: Optional[str] = "valid_time"

    @field_validator("production_datetime", "configuration_datetime", mode="before")
    def init_dates(cls, date_config: str) -> Datetime:
        return Datetime(date_config)

    @abstractmethod
    def alt_area_name(self, geo_id: str) -> str:
        """
        Get the alt area name associated with the given geo_id from the weather dataset.

        Args:
            geo_id (str): Geo ID

        Returns:
            str: Alt area name
        """

    @abstractmethod
    def area_name(self, geo_id: str) -> str:
        """
        Get the area name associated with the given geo_id from the weather dataset.

        Args:
            geo_id (str): Geo ID

        Returns:
            str: Area name
        """

    def compute(self, **kwargs) -> Any:
        try:
            return super().compute(**kwargs)
        except LoaderError as err:
            LOGGER.error(
                "Missing data to make the component.",
                production_id=self.production_id,
                production_name=self.production_name,
                component_id=self.id,
                component_name=self.name,
                component_type=self.type,
                msg=str(err),
            )
            return None


class SynthesisComponentComposite(AbstractComponentComposite):
    """
    This class creates a Component object of type text.

    Inherits: AbstractComponentComposite

    Returns:
        BaseModel: Component object
    """

    _keep_data = True

    type: Literal[TypeComponent.SYNTHESIS] = TypeComponent.SYNTHESIS
    product_comment: bool
    weathers: List[WeatherComposite]

    def _compute(self, **_kwargs) -> Optional[Union[xr.DataArray, xr.Dataset]]:
        """
        Compute the weather dataset by merging the computed weather data
        for each weather in the list.

        Returns:
            xr.Dataset: Merged weather dataset
        """
        return xr.merge([weather.compute() for weather in self.weathers])

    def alt_area_name(self, geo_id: str) -> str:
        """
        Get the alt area name associated with the given geo_id from the weather dataset.

        Args:
            geo_id (str): Geo ID

        Returns:
            str: Area name
        """
        return str(self.compute().sel(id=geo_id)["altAreaName"].values)

    def area_name(self, geo_id: str) -> str:
        """
        Get the area name associated with the given geo_id from the weather dataset.

        Args:
            geo_id (str): Geo ID

        Returns:
            str: Area name
        """
        return str(self.compute().sel(id=geo_id)["areaName"].values)

    @property
    def weather_period(self) -> Period:
        """Get the period covered by the summary text.

        Returns:
            Period: Period without an associated name (it will be computed by CDPPeriod)
        """
        # The period name will be automatically computed by CDPPeriod,
        # so no need to set it here.
        return Period(
            id=self.period.id,
            start=self.period.start,
            stop=self.period.stop,
        )


class RiskComponentComposite(AbstractComponentComposite):
    """
    This class creates a Component object of type risk.

    Args:
        baseModel: Pydantic model

    Returns:
        baseModel: Component object
    """

    type: Literal[TypeComponent.RISK] = TypeComponent.RISK
    levels: List[LevelComposite]
    hazard_id: str
    hazard_name: str
    product_comment: bool
    other_names: Optional[Union[str, List[str]]] = None

    _risk_ds: xr.Dataset = xr.Dataset()
    _final_risk_da: xr.DataArray = xr.DataArray()

    def __init__(self, risk_ds: xr.Dataset = xr.Dataset(), **data: Any):
        super().__init__(**data)
        self._risk_ds = risk_ds

    @property
    def risk_ds(self) -> xr.Dataset:
        """
        Get the risks dataset.

        Returns:
            xr.Dataset: Aleas dataset
        """
        return self._risk_ds

    @property
    def final_risk_da(self) -> xr.DataArray:
        """
        Get the final risk DataArray.

        Returns:
            xr.DataArray: Final risk DataArray
        """
        return self._final_risk_da

    @property
    def cached_attrs(self) -> dict:
        """
        Get the cached attributes.

        Returns:
            dict: Cached attributes
        """
        return {
            "data": Loader,
            "risk_ds": Loader,
            "final_risk_da": Loader,
        }

    @staticmethod
    def _special_merge(d1: xr.Dataset, d2: xr.Dataset) -> xr.Dataset:
        """
        Merges "non-mergeable" variables in datasets.

        Args:
            d1 (xr.Dataset): First dataset to merge.
            d2 (xr.Dataset): Second dataset to merge.

        Returns:
            xr.Dataset: Merged dataset.
        """
        dout = xr.Dataset()

        # Iterate over the intersection of non-mergeable variables in the two datasets.
        inter = (
            {
                "summarized_density",
                "risk_summarized_density",
                "occurrence",
                "occurrence_plain",
                "occurrence_mountain",
            }
            .intersection(d1.data_vars)
            .intersection(d2.data_vars)
        )

        for var in inter:
            lev1 = set(d1[var].risk_level.values)
            lev2 = set(d2[var].risk_level.values)
            lev_inter = lev2.intersection(lev1)

            # If there is an intersection of risk levels, merge the variables.
            if lev_inter != set():
                d2_var_new = d2[var].broadcast_like(d1[var]).fillna(0.0)
                d1_var_new = d1[var].broadcast_like(d2_var_new).fillna(0.0)
                dout[var] = np.fmax(d1_var_new, d2_var_new)

                d1 = d1.drop_vars(var)
                d2 = d2.drop_vars(var)

        dout = xr.merge([d1, d2, dout])

        # Transform occurrences to booleans since it was converted into float during
        # the merge operation.
        dout["occurrence"] = dout.occurrence.mask.bool
        if "occurrence_plain" in dout:
            dout["occurrence_plain"] = dout["occurrence_plain"].mask.bool
        if "occurrence_mountain" in dout:
            dout["occurrence_mountain"] = dout["occurrence_mountain"].mask.bool

        return dout

    @staticmethod
    def _replace_middle(x: np.ndarray, axis: Optional[int] = None) -> np.ndarray:
        """
        Replaces the middle value of a risk if it is lower than its neighbors.

        This function scans and replaces the values. For example:
        [2,1,2] => [2,2,2]
        [5,1,4] => [5,4,4]
        [5,4,1] => [5,4,1]

        This function fills in the gaps. It doesn't matter if the other values are not
        consistent.

        Args:
            x (np.ndarray):
                Array containing the risks to fill in. This array must be passed through
                a rolling operation (over 3 time dimensions). The resulting array has
                one additional dimension compared to the original.
            axis (int):
                Axis along which the rolling operation was performed.

        Returns:
            np.ndarray: Array with the original dimension (before rolling).
        """
        if isinstance(axis, tuple) and len(axis) == 1:
            axis = axis[0]
        x_borders = np.min(x.take([0, 2], axis=axis), axis=axis)
        x_middle = x.take(1, axis=axis)
        x_out = np.nanmax([x_borders, x_middle], axis=0)
        return x_out

    def _compute(self, **_kwargs) -> xr.Dataset:
        """
        Compute the risks dataset.

        Returns:
            xr.Dataset: Aleas dataset
        """
        # Computing of the risk
        self._risk_ds = xr.Dataset()
        for level in self.levels:
            level_risk_da = level.compute()
            level_risk_da.attrs["level"] = int(level.level)
            level_risk_da = level_risk_da.expand_dims(dim="risk_level").assign_coords(
                risk_level=[int(level.level)]
            )
            try:
                self._risk_ds = self._special_merge(self._risk_ds, level_risk_da)
            except (Exception, xr.MergeError) as excpt:
                LOGGER.error(
                    "Error in merging dataset",
                    hazard=self.hazard_id,
                    bulletin=self.production_id,
                    func="Component.compute",
                    exc_info=True,
                )
                raise ValueError(str(excpt)) from excpt

        # Computing of the final risk
        if not self.is_risks_empty:
            self._final_risk_da = (
                (self.risk_ds["occurrence"] * self.risk_ds.risk_level)
                .max(dim="risk_level", skipna=True)
                .rolling({self.time_dimension: 3}, center=True, min_periods=1)
                .reduce(self._replace_middle)
            ).astype("float32", copy=False)
        return self._risk_ds

    def get_comparison(self, level: int = 1) -> dict:
        """
        Get the comparison dictionary for the specified risk level as follows:

            {
                "T__HAUTEUR2": {
                    "plain": Threshold(...),
                    "mountain": Threshold(...),
                    "category": ...,
                    "mountain_altitude": ...,
                    "aggregation": ...,
                },
                "NEIPOT1__SOL": {...},
            }

        Args:
            level (int, optional): The risk level. Defaults to 1.

        Returns:
            dict: Comparison dictionary
        """
        # Retrieve the comparison dictionary for the desired level
        d1_comp = self.risks_of_level(level=level)[0].get_comparison()

        # Iterate over each variable and check for identical variables in other levels
        for variable in d1_comp:
            other_level = self.risks_of_level(level=level + 1)
            if not other_level:
                continue

            d2_comp = other_level[0].get_comparison()
            if variable in d1_comp and variable in d2_comp:
                if "plain" in d1_comp[variable] and "plain" in d2_comp[variable]:
                    d1_comp[variable]["plain"].update_next_critical(
                        d2_comp[variable]["plain"]
                    )
                if "mountain" in d1_comp[variable] and "mountain" in d2_comp[variable]:
                    d1_comp[variable]["mountain"].update_next_critical(
                        d2_comp[variable]["mountain"]
                    )
        return d1_comp

    @property
    def is_risks_empty(self) -> bool:
        """
        Check if the risks dataset is empty.

        Returns:
            bool: True if the risks dataset is empty, False otherwise
        """
        return not bool(self.risk_ds)

    def risks_of_level(self, level: float) -> List[LevelComposite]:
        """
        Returns the list of levels that match the specified risk level.

        Args:
            level (int): The required risk level.

        Returns:
            list: List of LevelComposite objects
        """
        return [lvl for lvl in self.levels if lvl.level == level]

    def final_risk_max_level(self, geo_id: str) -> int:
        """
        Return the maximum risk level for a given area.

        Args:
            geo_id (str): The area ID

        Returns:
            int: The maximum risk level
        """
        if self.is_risks_empty:
            return 0
        return int(max(self.final_risk_da.sel(id=geo_id).values))

    def final_risk_min_level(self, geo_id: str) -> int:
        """
        Return the minimum risk level for a given area.

        Args:
            geo_id (str): The area ID

        Returns:
            int: The minimum risk level
        """
        if self.is_risks_empty:
            return 0
        return min(self.final_risk_da.sel(id=geo_id).values)

    def alt_area_name(self, geo_id: str) -> str:
        """
        Get the alt name of the geographical area based on its ID.

        Args:
            geo_id (str): The ID of the geographical area

        Returns:
            str: The name of the geographical area, or "N.A" if no risks are available.
        """
        if not self.is_risks_empty:
            return str(self.risk_ds.sel(id=geo_id)["altAreaName"].data)
        return "N.A"

    def area_name(self, geo_id: str) -> str:
        """
        Get the name of the geographical area based on its ID.

        Args:
            geo_id (str): The ID of the geographical area

        Returns:
            str: The name of the geographical area, or "N.A" if no risks are available.
        """
        if not self.is_risks_empty:
            return str(self.risk_ds.sel(id=geo_id)["areaName"].data)
        return "N.A"

    def has_risk(self, ids: List[str], valid_time_slice: slice) -> Optional[bool]:
        """
        Checks if any of the provided IDs have a risk within the specified time slice.

        Args:
            ids (List[str]): A list of IDs to check for risks.
            valid_time_slice (slice): A time slice object representing the valid time
                range to consider.

        Returns:
            Optional[bool]:
                - True if at least one ID has a risk within the time slice.
                - False if none of the IDs have a risk within the time slice.
                - None if there are no entries for the provided IDs.
        """
        occurrence = self.final_risk_da.where(
            self.final_risk_da.id.isin(ids), drop=True
        ).sel(valid_time=valid_time_slice)
        return occurrence.any().item() if occurrence.size > 0 else None
