"""mfire.configuration module

This module handles version related to the configuration Handling

"""

from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from mfire.utils.date import Datetime
from mfire.composite.serialized_types import s_datetime


class ConfigGlobal:
    def __init__(
        self,
        experiment,
        config_hash,
        settings,
        rules,
        get_geo,
        list_components_configs,
    ):
        self.experiment = experiment
        self.config_hash = config_hash
        self.settings = settings
        self.rules = rules
        self.get_geo = get_geo
        self.list_components_configs = list_components_configs


class VersionConfig(BaseModel):
    """objet qui contient la version de la configuration

    Inheritance : BaseModel

    Returns:
        BaseModel : objet VersionConfig
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    version: str
    drafting_datetime: s_datetime
    reference_datetime: s_datetime
    production_datetime: s_datetime
    configuration_datetime: s_datetime

    @field_validator(
        "drafting_datetime",
        "reference_datetime",
        "production_datetime",
        "configuration_datetime",
        mode="before",
    )
    def check_datetimes(cls, v: Any) -> Datetime:
        return Datetime(v)
