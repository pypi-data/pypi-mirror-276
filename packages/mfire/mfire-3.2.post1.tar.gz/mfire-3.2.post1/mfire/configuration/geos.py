import abc
import re
import warnings
from typing import Any, List, Literal, Optional, Tuple, Union

import geojson
import shapely.geometry as sh
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    model_validator,
    field_validator,
)

from mfire.composite.serialized_types import s_path
from mfire.configuration.resources import MaskRHConfig
from mfire.settings import get_logger
from mfire.utils.hash import MD5

LOGGER = get_logger(name="geos.mod", bind="config_processor")


# =====================================
# Custom types
# =====================================
NumType = Union[float, int]
Position = Tuple[NumType, NumType]

# =====================================
# Geometries
# =====================================


class _GeometryBaseConfig(BaseModel, abc.ABC):
    """Base class for geometry models"""

    coordinates: Any  # will be constrained in child classes

    @property
    def __geo_interface__(self):
        return self.model_dump()


class PointConfig(_GeometryBaseConfig):
    """Point Model"""

    type: Literal["Point"] = "Point"
    coordinates: Position


class MultiPointConfig(_GeometryBaseConfig):
    """MultiPoint Model"""

    type: Literal["MultiPoint"] = "MultiPoint"
    coordinates: List[Position] = Field(..., min_length=1)


class LineStringConfig(_GeometryBaseConfig):
    """LineString Model"""

    type: Literal["LineString"] = "LineString"
    coordinates: List[Position] = Field(..., min_length=2)


class MultiLineStringConfig(_GeometryBaseConfig):
    """MultiLineString Model"""

    type: Literal["MultiLineString"] = "MultiLineString"
    coordinates: List[List[Position]] = Field(..., min_length=1)

    @field_validator("coordinates")
    def check_coordinates(cls, multilinestring):
        """Validate that MultiLineString coordinates pass the GeoJSON spec"""
        if any(len(linestring) < 2 for linestring in multilinestring):
            raise ValueError("All linestrings must have at least 2 Postion items")
        return multilinestring


class PolygonConfig(_GeometryBaseConfig):
    """Polygon Model"""

    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[Position]] = Field(..., min_length=1)

    @field_validator("coordinates")
    def check_coordinates(cls, polygon):
        """Validate that Polygon coordinates pass the GeoJSON spec"""
        if any(len(ring) < 4 for ring in polygon):
            raise ValueError("All linear rings must have four or more coordinates")
        if any(ring[-1] != ring[0] for ring in polygon):
            raise ValueError("All linear rings have the same start and end coordinates")
        return polygon


class MultiPolygonConfig(_GeometryBaseConfig):
    """MultiPolygon Model"""

    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: List[List[List[Position]]] = Field(..., min_length=1)

    @field_validator("coordinates")
    def check_coordinates(cls, multipolygon):
        """Validate that MultiPolygon coordinates pass the GeoJSON spec"""
        if any(len(polygon) == 0 for polygon in multipolygon):
            raise ValueError("Polygons must have at least one ring")
        if any(any(len(ring) < 4 for ring in polygon) for polygon in multipolygon):
            raise ValueError("All linear rings must have four or more coordinates")
        if any(
            any(ring[-1] != ring[0] for ring in polygon) for polygon in multipolygon
        ):
            raise ValueError("All linear rings have the same start and end coordinates")
        return multipolygon


GeometryConfig = Union[
    PointConfig,
    MultiPointConfig,
    LineStringConfig,
    MultiLineStringConfig,
    PolygonConfig,
    MultiPolygonConfig,
]


class GeometryCollectionConfig(BaseModel):
    """GeometryCollection Model"""

    type: Literal["GeometryCollection"] = "GeometryCollection"
    geometries: List[GeometryConfig] = Field(..., min_length=1)

    def __iter__(self):
        """iterate over geometries"""
        return iter(self.geometries)

    def __len__(self):
        """return geometries length"""
        return len(self.geometries)

    def __getitem__(self, index):
        """get geometry at a given index"""
        return self.geometries[index]


def parse_geometry_obj(obj) -> GeometryConfig:
    """
    `obj` is an object that is supposed to represent a GeoJSON geometry.
    This method returns the reads the `"type"` field and returns the
    correct pydantic Geometry model.
    """
    if "type" not in obj:
        raise TypeError("Missing 'type' field in geometry !")
    if obj["type"] == "Point":
        return PointConfig.model_validate(obj)
    if obj["type"] == "MultiPoint":
        return MultiPointConfig.model_validate(obj)
    if obj["type"] == "LineString":
        return LineStringConfig.model_validate(obj)
    if obj["type"] == "MultiLineString":
        return MultiLineStringConfig.model_validate(obj)
    if obj["type"] == "Polygon":
        return PolygonConfig.model_validate(obj)
    if obj["type"] == "MultiPolygon":
        return MultiPolygonConfig.model_validate(obj)
    raise TypeError(f"Unknown type '{obj['type']}' !")


# =====================================
# Features
# =====================================


class FeatureConfig(BaseModel):
    """Feature Model"""

    model_config = ConfigDict(use_enum_values=True)

    id: str | None = None
    properties: dict = {}
    type: Literal["Feature"] = "Feature"
    geometry: GeometryConfig | None

    @field_validator("geometry", mode="before")
    def set_geometry(cls, v: Any, info: ValidationInfo) -> Optional[GeometryConfig]:
        feat_id = info.data.get("id")
        feat_label = dict(info.data.get("properties", {})).get("label")
        # geometry validation
        geometry = v
        if hasattr(v, "__geo_interface__"):
            geometry = v.__geo_interface__

        # geometry's shape validation and geojson
        # because shape add a terminal point if first/last differ
        shape = sh.shape(geometry)
        geodoc = geojson.Feature(geometry=geometry)
        if not shape.is_valid or not geodoc.is_valid:
            LOGGER.error(
                f"geometry's shape not valid (id={feat_id}, label={feat_label}) : "
                f"removed from available zones "
            )
            return None
        lon0, lat0, lon1, lat1 = shape.bounds
        lon_lat_valid = (
            (-180 <= lon0 <= 180)
            and (-180 <= lon1 <= 180)
            and (-90 <= lat0 <= 90)
            and (-90 <= lat1 <= 90)
        )
        if not lon_lat_valid:
            LOGGER.error(
                f"Longitude/Latitude error : (lon, lat, lon, lat) = {shape.bounds}"
                ", while longitude values must be in [-180,180] and latitude values"
                f" must be in [-90, 90]. (id={feat_id}, label={feat_label})."
            )
            return None
        return geometry

    @field_validator("properties")
    def get_name_from_label(cls, v: dict) -> str:
        if v is None or not (v.get("name") is None and "label" in v):
            return v
        v["name"] = v["label"]
        search = re.search(r"^.*_\((.*)$", v["label"])
        if search:
            v["name"] = search.group(1).strip("()")
        return v

    @property
    def shape(self) -> sh.base.BaseGeometry:
        """Returns the equivalent shapely geometry.

        Returns:
            sh.base.BaseGeometry: shapely geometry
        """
        return sh.shape(self.geometry)

    def is_in(self, *bounds) -> bool:
        return sh.box(*bounds).contains(self.shape)

    def intersects(self, *bounds) -> bool:
        return self.shape.intersects(sh.box(*bounds))


class FeatureCollectionConfig(BaseModel):
    """FeatureCollection Model"""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[FeatureConfig]

    def __iter__(self):
        """iterate over features"""
        return iter(self.features)

    def __len__(self):
        """return features length"""
        return len(self.features)

    def __getitem__(self, index):
        """get feature at a given index"""
        return self.features[index]

    def __hash__(self) -> str:
        return MD5(self.model_dump()).hash

    @field_validator("features")
    def set_features(cls, v: []) -> List[FeatureConfig]:
        return [feat for feat in v if feat.geometry is not None]


# =====================================
# Mask configuration model
# =====================================


class MaskConfig(BaseModel):
    """Mask configuration model"""

    file: s_path
    id: str
    name: str
    config_hash: str
    prod_hash: str
    mask_hash: Optional[str] = None
    geos: FeatureCollectionConfig
    resource_handler: MaskRHConfig

    @model_validator(mode="before")
    def check_mask_hash(cls, values: dict):
        # breakpoint()
        geos_hash = values["geos"].__hash__()
        mask_hash = values.get("mask_hash")
        if mask_hash != geos_hash:
            if mask_hash:
                warnings.warn(
                    "Given mask_hash differs from the given geos hash. Changed it."
                )
            values["mask_hash"] = geos_hash
        rh_hash = values["resource_handler"].version
        if rh_hash != geos_hash:
            if rh_hash:
                warnings.warn(
                    "Given version in resource handler differs from the given geos "
                    "hash. Changed it."
                )
            values["resource_handler"].version = geos_hash
        return values
