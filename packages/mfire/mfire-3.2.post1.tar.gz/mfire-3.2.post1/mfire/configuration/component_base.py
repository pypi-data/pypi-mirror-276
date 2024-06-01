from typing import List, Optional, Union

import shapely.geometry as sh
from pydantic import BaseModel
from shapely.geometry import (
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from mfire.composite.period import PeriodCollection
from mfire.configuration.datas import RHManager
from mfire.configuration.geos import MaskConfig

Geometry_used = Union[
    Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString
]


class ComponentManager:
    def __init__(self, rhmanager: RHManager, configuration_datetime):
        self.rhmanager = rhmanager
        self.configuration_datetime = configuration_datetime

    def useable_geometries(self, geo_config: Geometry_used) -> List[str]:
        """useable_geometries : Returns the useable geometries with
        a geographical zone according to its configuration.

        Args:
            geo_config (FeatureConfig): Geograpghical zone's configuration

        Returns:
            List[str] : list of useable geometries's names.
        """
        if not isinstance(geo_config, Geometry_used):
            return []
        return [
            gname
            for gname, bounds in self.rhmanager.rules.get_bounds()
            if sh.box(*bounds).contains(geo_config)
        ]


class CompoBase(BaseModel):
    single_data_config: Optional[dict] = None
    single_mask_config: Optional[MaskConfig] = None
    processed_periods: Optional[PeriodCollection] = None
    processed_hazards: Optional[dict] = None
    all_shapes: Optional[dict] = None
