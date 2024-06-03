from typing import List, Optional

from mfire.composite.component import RiskComponentComposite
from mfire.composite.serialized_types import s_Datetime
from mfire.localisation.risk_localisation import RiskLocalisation
from mfire.localisation.spatial_localisation import SpatialLocalisation
from mfire.localisation.table_localisation import TableLocalisation
from mfire.utils import mfxarray as xr
from mfire.utils.date import Datetime
from tests.composite.factories import RiskComponentCompositeFactory


class SpatialLocalisationFactory(SpatialLocalisation):
    component: RiskComponentComposite = RiskComponentCompositeFactory()
    geo_id: str = "geo_id"

    localised_risk_ds_factory: Optional[xr.Dataset] = None

    risk_level_factory: Optional[int] = None

    @property
    def localised_risk_ds(self) -> xr.Dataset:
        if self.localised_risk_ds_factory is None:
            return super().localised_risk_ds
        return self.localised_risk_ds_factory

    @property
    def risk_level(self):
        if self.risk_level_factory is None:
            return super().risk_level
        return self.risk_level_factory


class TableLocalisationFactory(TableLocalisation):
    data: xr.DataArray = xr.DataArray(coords={"id": []}, dims=["id"])

    request_time: s_Datetime = Datetime(2023, 3, 1)
    domain: xr.DataArray = xr.DataArray()
    areas: xr.DataArray = xr.DataArray()
    alt_min: int = 100
    alt_max: int = 1000

    name_factory: Optional[str] = None

    @property
    def name(self) -> str:
        return self.name_factory if self.name_factory is not None else super().name


class RiskLocalisationFactory(RiskLocalisation):
    risk_component: RiskComponentCompositeFactory = RiskComponentCompositeFactory()
    risk_level: int = 2
    geo_id: str = "geo_id"
    period: set = {Datetime(2023, 3, 1, 6)}

    template_type_factory: Optional[str] = None
    unique_name_factory: Optional[str] = None
    periods_name_factory: Optional[List] = None
    is_multizone_factory: Optional[bool] = None
    critical_values_factory: Optional[dict] = None

    @property
    def is_multizone(self) -> bool:
        if self.is_multizone_factory is None:
            return super().is_multizone
        return self.is_multizone_factory

    @property
    def periods_name(self) -> list:
        """Get the names of periods."""
        if self.periods_name_factory is None:
            return super().periods_name
        return self.periods_name_factory

    @property
    def template_type(self) -> str:
        if self.template_type_factory is None:
            return super().template_type
        return self.template_type_factory

    @property
    def unique_name(self) -> str:
        if self.unique_name_factory is None:
            return super().unique_name
        return self.unique_name_factory

    @property
    def critical_values(self) -> dict:
        if self.critical_values_factory is None:
            return super().critical_values
        return self.critical_values_factory
