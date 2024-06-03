from enum import Enum
from typing import Dict, Iterable, Optional, Set, Tuple, Union, List

import mfire.utils.mfxarray as xr
from mfire.settings import Settings
from mfire.utils.string import concatenate_string, decapitalize


class WWMF_FAMILIES(Enum):
    """Enumeration of all families and subfamilies of weather phenomena."""

    VISIBILITY = 0
    RAIN = 1
    SNOW = 2
    SHOWER = 3
    THUNDERSTORM = 4


class WWMF_SUBGRP(Enum):
    """Enumeration of some grouping of labels for weather phenomena."""

    A1 = (40, 50, 51, 52, 53)
    A2 = (58, 60, 61, 62, 63)
    A3 = (70, 71, 72, 73)
    A4 = (77, 78, 80, 81, 82, 83)
    A5 = (90, 91, 92, 93, 97)
    B1 = (49, 59)
    B2 = (84,)
    B3 = (85,)
    B4 = (98,)
    B5 = (99,)

    @classmethod
    @property
    def B_group(cls) -> List[int]:
        return sum(
            (list(b.value) for b in [cls.B1, cls.B2, cls.B3, cls.B4, cls.B5]), start=[]
        )


def is_severe(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code represents a severe weather phenomenon"""
    return (wwmf == 49) | (wwmf == 59) | (wwmf == 85) | (wwmf == 98) | (wwmf == 99)


def is_visibility(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code represents visibility"""
    return (30 <= wwmf) & (wwmf <= 39)


def is_precipitation(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF codes represents precipitation"""
    return (40 <= wwmf) & (wwmf <= 99)


def is_snow(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code belongs to the snow family"""
    return (wwmf == 58) | (60 <= wwmf) & (wwmf <= 63) | (77 <= wwmf) & (wwmf <= 83)


def is_rain(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code belongs to the rain family"""
    return (40 <= wwmf) & (wwmf <= 59) | (70 <= wwmf) & (wwmf <= 78) | (wwmf == 93)


def is_shower(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code belongs to the shower family"""
    return (70 <= wwmf) & (wwmf <= 85) | (wwmf == 92)


def is_thunderstorm(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
    """Check if the given WWMF code belongs to the thunderstorm family"""
    return (wwmf == 84) | (wwmf == 85) | (90 <= wwmf) & (wwmf <= 99)


def wwmf_families(*wwmfs: int) -> Set[WWMF_FAMILIES]:
    """Identify the families of weather phenomena represented by the given WWMF codes"""
    families = set()
    for wwmf in wwmfs:
        if is_visibility(wwmf):
            families.add(WWMF_FAMILIES.VISIBILITY)
        else:
            if is_rain(wwmf):
                families.add(WWMF_FAMILIES.RAIN)
            if is_snow(wwmf):
                families.add(WWMF_FAMILIES.SNOW)
            if is_shower(wwmf):
                families.add(WWMF_FAMILIES.SHOWER)
            if is_thunderstorm(wwmf):
                families.add(WWMF_FAMILIES.THUNDERSTORM)
    return families


def wwmf_subfamilies(*wwmfs: int) -> Tuple[WWMF_SUBGRP, ...]:
    """Identify the subfamilies of weather phenomena represented by the given WWMF
    codes.

    Args:
        *wwmfs: Variable number of WWMF codes to check.

    Returns:
        Tuple[WWMF_SUBGRP, ...]: Tuple of WWMF subfamilies represented by the given
        codes.
    """
    return tuple(
        subgroup for subgroup in WWMF_SUBGRP if set(subgroup.value) & set(wwmfs)
    )


def wwmf_label(
    *wwmfs: int, labels: Optional[Dict] = None, concatenate: bool = True
) -> Optional[str]:
    """Generate a label for the given WWMF codes.

    Args:
        *wwmfs (int): Variable number of WWMF codes to generate a label for.
        labels (Dict): Dictionary mapping a label according code(s) or group(s).
        concatenate (bool): Indicates if the final result should be concatenated labels
            if not found

    Returns:
        Optional[str]: Generated label for the given WWMF codes, or None if no match is
        found.
    """
    if labels is None:
        labels = Settings().wwmf_labels

    if len(wwmfs) == 1:
        return labels.get((wwmfs[0],), None)

    # If we have >= 3 precipitation TS then we regroup some repeated codes
    sorted_args = sorted(wwmfs)
    if len(wwmfs) >= 3 and all(is_precipitation(ts) for ts in sorted_args):
        try:
            return labels[wwmf_subfamilies(*sorted_args)]
        except KeyError:
            pass
    else:
        for key, value in labels.items():
            if len(key) != len(wwmfs):
                continue
            if all(
                arg in key[i] if isinstance(key[i], Iterable) else arg == key[i]
                for i, arg in enumerate(sorted_args)
            ):
                return value

    # Generate labels for each WWMF code and concatenate them
    return (
        concatenate_string(
            [labels[(sorted_args[0],)]]
            + [decapitalize(labels[(arg,)]) for arg in sorted_args[1:]]
        )
        if concatenate
        else None
    )
