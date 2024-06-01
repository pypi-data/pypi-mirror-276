import random
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union, cast

import numpy as np

import mfire.utils.mfxarray as xr
from mfire.utils.string import _
from mfire.composite.aggregation import Aggregation, AggregationMethod, AggregationType
from mfire.composite.base import BaseComposite
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
)
from mfire.composite.event import (
    Category,
    EventAccumulationComposite,
    EventComposite,
    Threshold,
)
from mfire.composite.field import FieldComposite, Selection
from mfire.composite.geo import AltitudeComposite, GeoComposite
from mfire.composite.level import LevelComposite, LocalisationConfig
from mfire.composite.operator import ComparisonOperator, LogicalOperator
from mfire.composite.period import Period
from mfire.composite.production import ProductionComposite
from mfire.composite.serialized_types import s_Datetime, s_path, s_slice
from mfire.composite.weather import WeatherComposite, WeatherCompositeInterface
from mfire.settings import SETTINGS_DIR
from mfire.utils.date import Datetime


class PeriodFactory(Period):
    id: str = "period_id"
    name: Optional[str] = "period_name"
    start: s_Datetime = Datetime(2023, 3, 1)
    stop: s_Datetime = Datetime(2023, 3, 5)


class AggregationFactory(Aggregation):
    method: AggregationMethod = AggregationMethod.MEAN
    kwargs: dict = {}


class SelectionFactory(Selection):
    sel: dict = {"id": random.randint(0, 42)}
    islice: dict[str, s_slice | float] = {
        "valid_time": slice(random.randint(0, 42), random.randint(0, 42))
    }
    isel: dict = {"latitude": random.randint(0, 42)}
    slice: dict[str, s_slice] = {
        "longitude": slice(random.randint(0, 42), random.randint(0, 42))
    }


class BaseCompositeFactory(BaseComposite):
    """Base composite factory class."""

    data_factory: Any = None
    cached_attrs_factory: Optional[dict] = None

    def compute(self, **kwargs) -> Any:
        if self.data_factory is None:
            return super().compute(**kwargs)
        return self.data_factory

    @property
    def cached_attrs(self) -> dict:
        if self.cached_attrs_factory is None:
            return super().cached_attrs
        return self.cached_attrs_factory


class ProductionCompositeFactory(BaseCompositeFactory, ProductionComposite):
    id: str = "production_id"
    name: str = "production_name"
    config_hash: str = "production_config_hash"
    prod_hash: str = "production_hash"
    mask_hash: str = "production_mask_hash"
    components: List[Union[RiskComponentComposite, SynthesisComponentComposite]] = []


class FieldCompositeFactory(BaseCompositeFactory, FieldComposite):
    """Field composite factory class."""

    file: Union[Path, List[Path]] = Path("field_composite_path")
    grid_name: str = "franxl1s100"
    name: str = "field_name"

    def compute(self, **kwargs) -> xr.DataArray:
        data = super().compute(**kwargs)
        if data.name is None:
            data.name = self.name
        return data


class GeoCompositeFactory(BaseCompositeFactory, GeoComposite):
    """Geo composite factory class."""

    file: s_path = Path("geo_composite_file")
    mask_id: Optional[Union[List[str], str]] = "mask_id"
    grid_name: Optional[str] = "franxl1s100"

    mask_da_factory: Optional[xr.DataArray] = None
    all_sub_areas_factory: Optional[List[str]] = None

    def compute(self, **kwargs) -> Optional[Union[xr.DataArray, xr.Dataset]]:
        if self.data_factory is None:
            return super().compute(**kwargs)
        result = self.data_factory
        if (ids := kwargs.get("mask_id", self.mask_id)) is not None:
            result = result.sel(id=ids)
        return result

    @property
    def mask_da(self) -> xr.DataArray:
        if self.mask_da_factory is None:
            return super().mask_da
        return self.mask_da_factory

    def all_sub_areas(self, area_id: str) -> List[str]:
        if self.all_sub_areas_factory is None:
            return super().all_sub_areas(area_id)
        return self.all_sub_areas_factory


class AltitudeCompositeFactory(BaseCompositeFactory, AltitudeComposite):
    """Altitude composite factory class."""

    filename: s_path = Path(SETTINGS_DIR / "geos/altitudes/franxl1s100.nc")
    grid_name: str = "franxl1s100"
    name: str = "name"


class EventCompositeFactory(BaseCompositeFactory, EventComposite):
    """Factory class for creating EventComposite objects."""

    field: FieldComposite = FieldCompositeFactory()
    category: Category = Category.BOOLEAN
    altitude: AltitudeComposite = AltitudeCompositeFactory()
    geos: Union[GeoComposite, xr.DataArray] = GeoCompositeFactory()
    time_dimension: Optional[str] = "valid_time"
    plain: Optional[Threshold] = Threshold(
        threshold=20, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
    )
    aggregation: Optional[Aggregation] = AggregationFactory()
    aggregation_aval: Optional[Aggregation] = None

    mask_factory: Optional[xr.DataArray] = None

    @property
    def mask(self) -> Optional[xr.MaskAccessor]:
        if self.mask_factory is None:
            return super().mask
        return self.mask_factory.mask


class EventAccumulationCompositeFactory(
    EventCompositeFactory, EventAccumulationComposite
):
    """Factory class for creating EventAccumulationComposite objects."""

    field_1: FieldComposite = FieldCompositeFactory()
    cum_period: int = 6


class LevelCompositeFactory(BaseCompositeFactory, LevelComposite):
    level: int = 2
    aggregation: Optional[Aggregation] = None
    aggregation_type: AggregationType = AggregationType.UP_STREAM
    probability: str = "no"
    events: List[Union[EventAccumulationComposite, EventComposite]] = [
        EventCompositeFactory()
    ]
    time_dimension: Optional[str] = "valid_time"
    localisation: LocalisationConfig = LocalisationConfig()

    cover_period_factory: Optional[List[np.datetime64]] = None
    spatial_risk_da_factory: Optional[xr.DataArray] = None

    def __init__(self, **data: Any):
        events = data.get("events")
        if events is not None and data.get("logical_op_list") is None:
            logical_ops = [op.value for op in LogicalOperator]
            data["logical_op_list"] = list(
                np.random.choice(logical_ops, size=len(events) - 1)
            )
        super().__init__(**data)

    @property
    def cover_period(self) -> List[np.datetime64]:
        if self.cover_period_factory is None:
            return super().cover_period
        return self.cover_period_factory

    @property
    def spatial_risk_da(self) -> xr.DataArray:
        if self.spatial_risk_da_factory is None:
            return super().spatial_risk_da
        return self.spatial_risk_da_factory


class SynthesisComponentCompositeFactory(
    BaseCompositeFactory, SynthesisComponentComposite
):
    period: Period = PeriodFactory()
    id: str = "text_component_id"
    name: str = "text_component_name"
    production_id: str = "production_id"
    production_name: str = "production_name"
    production_datetime: s_Datetime = Datetime(2023, 3, 1, 6)

    weathers: List[WeatherComposite] = []
    product_comment: bool = True

    customer_id: Optional[str] = "customer_id"
    customer_name: Optional[str] = "customer_name"

    area_name_factory: Optional[dict] = None

    def area_name(self, geo_id: str) -> str:
        if self.area_name_factory is None:
            return super().area_name(geo_id)
        return self.area_name_factory[geo_id]


class RiskComponentCompositeFactory(BaseCompositeFactory, RiskComponentComposite):
    period: Period = PeriodFactory()
    id: str = "risk_component_id"
    name: str = "risk_component_name"
    production_id: str = "production_id"
    production_name: str = "production_name"
    production_datetime: s_Datetime = Datetime(2023, 3, 1, 6)

    levels: List[LevelComposite] = []
    hazard_id: str = "hazard_id"
    hazard_name: str = "hazard_name"
    product_comment: bool = True

    customer_id: Optional[str] = "customer_id"
    customer_name: Optional[str] = "customer_name"

    final_risk_da_factory: Optional[xr.DataArray] = None

    area_name_factory: Optional[dict] = None

    def area_name(self, geo_id: str) -> str:
        if self.area_name_factory is None:
            return super().area_name(geo_id)
        return self.area_name_factory[geo_id]

    @property
    def final_risk_da(self) -> xr.DataArray:
        if self.final_risk_da_factory is None:
            return super().final_risk_da
        return self.final_risk_da_factory


class WeatherCompositeInterfaceFactory(WeatherCompositeInterface):
    has_risk: Callable[[str, List[str], slice], Optional[bool]] = lambda x, y, z: None


class WeatherCompositeFactory(BaseCompositeFactory, WeatherComposite):
    id: str = "id_weather"
    params: Dict[str, FieldComposite] = {}
    units: Dict[str, Optional[str]] = {}
    localisation: LocalisationConfig = LocalisationConfig()

    geos_descriptive_factory: Optional[xr.DataArray] = None
    altitudes_factory: Optional[xr.DataArray] = None
    check_condition_factory: Optional[bool] = None

    interface: WeatherCompositeInterface = WeatherCompositeInterfaceFactory()

    def geos_descriptive(self, geo_id: str) -> xr.DataArray:
        if self.geos_descriptive_factory is None:
            return super().geos_descriptive(geo_id)
        return self.geos_descriptive_factory

    def altitudes(self, param: str) -> Optional[xr.DataArray]:
        if self.altitudes_factory is None:
            return super().altitudes(param)
        return self.altitudes_factory

    def check_condition(self, geo_id: str) -> bool:
        if self.check_condition_factory is None:
            return super().check_condition(geo_id)
        return self.check_condition_factory

    @classmethod
    def create_factory(
        cls,
        geos_descriptive: list,
        valid_times: list,
        lon: list,
        lat: list,
        data_vars: dict,
        altitude: Optional[list],
        **kwargs,
    ) -> WeatherComposite:
        data_ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                "id": "id_axis",
                "valid_time": valid_times,
                "latitude": lat,
                "longitude": lon,
            },
        )

        ids = list(map(str, list(range(len(geos_descriptive)))))
        compo = cls(
            data_factory=data_ds,
            production_datetime=data_ds.valid_time[0],
            geos_descriptive_factory=xr.DataArray(
                data=geos_descriptive,
                dims=["id", "latitude", "longitude"],
                coords={
                    "id": ids,
                    "latitude": lat,
                    "longitude": lon,
                    "areaType": (["id"], ["Axis"] + (len(ids) - 1) * [""]),
                    "areaName": (
                        ["id"],
                        [f"à localisation N°{i + 1}" for i in range(len(ids))],
                    ),
                },
            ),
            altitudes_factory=xr.DataArray(
                data=altitude,
                dims=["latitude", "longitude"],
                coords={
                    "latitude": lat,
                    "longitude": lon,
                },
            ),
            **kwargs,
        )

        geos_data = (
            compo.geos_descriptive_factory.sum(dim="id").expand_dims(
                {"id": ["id_axis"]}
            )
            > 0
        )
        geos_data["areaType"] = (["id"], ["Axis"])
        geos_data["areaName"] = (["id"], [_("sur tout le domaine")])
        geos_data["altAreaName"] = (["id"], [_("sur tout le domaine")])
        compo.geos = GeoCompositeFactory(
            data_factory=geos_data, mask_da_factory=geos_data, mask_id=None
        )
        return cast(WeatherComposite, compo)
