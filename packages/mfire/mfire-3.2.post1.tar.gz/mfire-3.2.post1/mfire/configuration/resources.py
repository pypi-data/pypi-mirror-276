"""
Pydantic models for custom Configs
"""
from abc import ABC
from typing import Literal, Optional

from pydantic import BaseModel, field_validator

from mfire.composite.serialized_types import s_path
from mfire.utils.date import Datetime


class _ResourceHandlerConfig(BaseModel, ABC):
    """Abstract ResourceHandler for handling basic promethee resources"""

    # Section
    role: Optional[str] = None
    fatal: Optional[bool] = False
    now: Optional[bool] = True
    # Resource
    kind: str
    # Provider
    vapp: str
    vconf: str
    namespace: str
    experiment: str
    block: str
    # Container
    format: str
    local: s_path


class _DataResourceHandlerConfig(_ResourceHandlerConfig, ABC):
    """Abstract ResourceHandler specific for meteorological data"""

    # Resource
    model: str
    date: str
    nativefmt: str
    geometry: str
    cutoff: str
    origin: str

    @field_validator("date")
    def init_date(cls, date: str) -> Datetime:
        return Datetime(date)


class GridPointRHConfig(_DataResourceHandlerConfig):
    """ResourceHandler specific for GridPoint data (raw model in grib files)"""

    # Resource
    kind: Literal["gridpoint"]
    term: int


class PrometheeGridPointRHConfig(_DataResourceHandlerConfig):
    """ResourceHandler specific for GridPoint data (raw model in grib files)"""

    # Resource
    kind: Literal["promethee_gridpoint"]
    param: str
    begintime: int
    endtime: int
    step: int


class MaskRHConfig(_ResourceHandlerConfig):
    """ResourceHandler specific for promethee's masks"""

    # Resource
    kind: Literal["promethee_mask"]
    promid: str
    version: Optional[str] = None
