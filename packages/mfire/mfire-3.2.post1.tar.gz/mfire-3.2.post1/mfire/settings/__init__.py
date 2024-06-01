"""mfire.settings module

This module manages the processing of constants and templates

"""

from mfire.settings.algorithms import TEXT_ALGO, PREFIX_TO_VAR
from mfire.settings.constants import (
    RULES_DIR,
    RULES_NAMES,
    LOCAL,
    UNITS_TABLES,
    SETTINGS_DIR,
    ALT_MIN,
    ALT_MAX,
    SPACE_DIM,
    TIME_DIM,
    N_CUTS,
    GAIN_THRESHOLD,
    Dimension,
    SIT_GEN,
)
from mfire.settings.logger import get_logger
from mfire.settings.settings import Settings


__all__ = [
    "TEXT_ALGO",
    "RULES_DIR",
    "RULES_NAMES",
    "PREFIX_TO_VAR",
    "LOCAL",
    "UNITS_TABLES",
    "SETTINGS_DIR",
    "ALT_MIN",
    "ALT_MAX",
    "SPACE_DIM",
    "TIME_DIM",
    "N_CUTS",
    "GAIN_THRESHOLD",
    "Settings",
    "Dimension",
    "get_logger",
    "SIT_GEN",
]
