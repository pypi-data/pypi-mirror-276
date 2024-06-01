""" Configuration des noms des algorithmes et des variables
"""

from pathlib import Path

_sg_dir = Path(__file__).absolute().parent / "sit_gen"

# Lien entre les noms d'algorithmes et les champs à traiter pour le texte
TEXT_ALGO = {
    "wind": {
        "generic": {
            "params": {
                "wind": {"field": "FF__HAUTEUR10", "default_units": "km/h"},
                "gust": {"field": "RAF__HAUTEUR10", "default_units": "km/h"},
                "direction": {"field": "DD__HAUTEUR10", "default_units": "°"},
            }
        }
    },
    "sitgen_fronts": {
        "generic": {
            "params": {
                "t2m": {"field": "T__HAUTEUR2", "default_units": "°C"},
                "r_700": {"field": "HU__ISOBARE700", "default_units": "%"},
                "msl": {"field": "P__MER", "default_units": "hPa"},
                "u10": {"field": "U__HAUTEUR10", "default_units": "km/h"},
                "v10": {"field": "V__HAUTEUR10", "default_units": "km/h"},
                "wbpt_850": {"field": "THETAPW__ISOBARE850", "default_units": "°C"},
            },
            "normalizer": _sg_dir / "mean_std.csv",
            "model": _sg_dir
            / "training_models_SG/train_fronts_/imagettes_128p_3811566",
            "generator": {
                "patches_h": 128,
                "patches_w": 128,
                "lat_min": 15,
                "lon_min": -50,
                "lat_max": 80,
                "lon_max": 60,
                "covering": 20,
            },
            "output": [
                "front quasi-stationnaire",
                "front froid",
                "front occlus",
                "front chaud",
            ],
            "segmentation": "ContourSegmentation",
            "threshold": 0.2,
        }
    },
    "sitgen_ad": {
        "generic": {
            "params": {
                "msl": {"field": "P__MER", "default_units": "hPa"},
                "u_850": {"field": "U__ISOBARE850", "default_units": "km/h"},
                "v_850": {"field": "V__ISOBARE850", "default_units": "km/h"},
            },
            "normalizer": _sg_dir / "mean_std.csv",
            "model": _sg_dir / "training_models_SG/train_ad_/short_4000_1079776",
            "generator": {
                "patches_h": 128,
                "patches_w": 128,
                "lat_min": 15,
                "lon_min": -50,
                "lat_max": 80,
                "lon_max": 60,
                "covering": 20,
            },
            "output": ["anticyclone", "depression"],
            "segmentation": "BlobSegmentation",
            "threshold": 0.5,
        }
    },
    "tempe": {
        "generic": {
            "params": {"tempe": {"field": "T__HAUTEUR2", "default_units": "°C"}}
        }
    },
    "weather": {
        "generic": {
            "params": {
                "wwmf": {"field": "WWMF__SOL", "default_units": "Code WWMF"},
                "precip": {"field": "PRECIP__SOL", "default_units": "mm"},
                "rain": {"field": "EAU__SOL", "default_units": "mm"},
                "snow": {"field": "NEIPOT__SOL", "default_units": "cm"},
                "lpn": {"field": "LPN__SOL", "default_units": "m"},
            }
        }
    },
    "wwmf": {
        "generic": {
            "params": {
                "wwmf": {"field": "WWMF__SOL", "default_units": "Code WWMF"},
                "precip": {"field": "PRECIP__SOL", "default_units": "mm"},
                "rain": {"field": "EAU__SOL", "default_units": "mm"},
                "snow": {"field": "NEIPOT__SOL", "default_units": "cm"},
                "lpn": {"field": "LPN__SOL", "default_units": "m"},
            }
        }
    },
    "thunder": {
        "generic": {
            "params": {
                "orage": {"field": "RISQUE_ORAGE__SOL", "default_units": "%"},
                "gust": {"field": "RAF__HAUTEUR10", "default_units": "m/s"},
            }
        }
    },
    "visibility": {
        "generic": {
            "params": {
                "visi": {"field": "VISI__SOL", "default_units": "m"},
                "type_fg": "TYPE_FG__SOL",
            }
        }
    },
    "nebulosity": {
        "generic": {
            "params": {"nebul": {"field": "NEBUL__SOL", "default_units": "octa"}}
        }
    },
    "rainfall": {
        "generic": {
            "params": {
                "precip": {"field": "PRECIP__SOL", "default_units": "mm"},
                "rain": {"field": "EAU__SOL", "default_units": "mm"},
                "snow": {"field": "NEIPOT__SOL", "default_units": "cm"},
                "lpn": {"field": "LPN__SOL", "default_units": "m"},
            }
        }
    },
    "snow": {
        "generic": {
            "params": {
                "snow": {"field": "NEIPOT__SOL", "default_units": "cm"},
                "lpn": {"field": "LPN__SOL", "default_units": "m"},
            }
        }
    },
}

# Liste des variables potentielles
PREFIX_TO_VAR = {
    "FF": "wind",
    "RAF": "gust",
    "NEIGE": "snow",
    "NEIPOT": "snow",
    "PRECIP": "precip",
    "EAU": "rain",
    "NEBUL": "nebul",
    "T": "temperature",
    "TMAX": "temperature",
    "TMIN": "temperature",
}
