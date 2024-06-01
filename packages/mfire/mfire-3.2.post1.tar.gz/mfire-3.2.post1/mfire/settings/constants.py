from pathlib import Path
from typing import Optional, Sequence, Union

# Paths
CUR_DIR = Path(".")
SETTINGS_DIR = Path(__file__).absolute().parent
LOCALE_DIR = Path(__file__).absolute().parents[1] / "locale"

# Rules
RULES_DIR = SETTINGS_DIR / "rules"
RULES_NAMES = tuple(
    d.name for d in RULES_DIR.iterdir() if d.is_dir() and not d.name.startswith("__")
)


TEMPLATES_FILENAME = {
    "compass": "compass.json",
    "date": "date.json",
    "period": "period.csv",
    "synonyms": "synonyms.json",
    "wwmf_labels": "wwmf_labels.csv",
    "wwmf_labels_no_risk": "wwmf_labels_no_risk.csv",
    "risk/monozone_generic": "risk/monozone.csv",
    "risk/monozone_precip_or_snow": "risk/monozone_precip_or_snow.json",
    "risk/multizone_generic": "risk/multizone.json",
    "risk/multizone_snow": "risk/multizone_snow.json",
    "risk/multizone_precip": "risk/multizone_precip.json",
    "risk/rep_value_generic": "risk/rep_value.json",
    "risk/rep_value_FFRaf": "risk/rep_value_FFRaf.json",
    "risk/rep_value_altitude": "risk/rep_value_altitude.json",
    "synthesis/sit_gen": "synthesis/sit_gen_templates.json",
    "synthesis/temperature": "synthesis/temperature.json",
    "synthesis/weather": "synthesis/weather.json",
}


SIT_GEN = {
    "zones": {
        "front": SETTINGS_DIR / "geos/marine/zones_SG_anticyc_front.geojson",
        "anticyclone": SETTINGS_DIR / "geos/marine/zones_SG_anticyc_front.geojson",
        "depression": SETTINGS_DIR / "geos/marine/zones_SG_depression.geojson",
    },
    "depression": {
        "fast": (8, 16),
        "slow": (4, 8),
        "evol": (2, 4),
        "move": (200, 400),
    },
    "anticyclone": {
        "evol": (8, 16),
        "move": (400, 800),
    },
}

# Data conf
LOCAL = {
    "gridpoint": "[date:stdvortex]/[block]/[geometry:area]/[term:fmth].[format]",
    "promethee_gridpoint": (
        "[date:stdvortex]/[model]/[geometry:area]/"
        "[param].[begintime:fmth]_[endtime:fmth]_[step:fmth].[format]"
    ),
}

# Units
_units_dir = SETTINGS_DIR / "units"
UNITS_TABLES = {
    "pint_extension": _units_dir / "pint_extension.txt",
    "wwmf_w1": _units_dir / "wwmf_w1_correspondence.csv",
}

# Default altitudes min and max
ALT_MIN = -500
ALT_MAX = 10000
EARTH_RADIUS_KM = 6378.137

# Default dimensions used
Dimension = Optional[Union[str, Sequence[str]]]
SPACE_DIM = ("latitude", "longitude")
TIME_DIM = ("valid_time",)

# RiskLocalisation default values
N_CUTS = 3
GAIN_THRESHOLD = 0.001
