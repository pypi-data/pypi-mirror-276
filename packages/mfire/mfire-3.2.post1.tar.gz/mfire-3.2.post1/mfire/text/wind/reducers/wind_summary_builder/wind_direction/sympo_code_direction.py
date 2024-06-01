from __future__ import annotations

from typing import Optional

from mfire.utils.geo import CompassRose16


class SympoCodeDirection:
    """SympoCodeDirection class."""

    @classmethod
    def get_direction_from_sympo_code(cls, sympo_code: Optional[int]) -> str:
        """Get the textual direction from a sympo code."""
        return (
            list(CompassRose16)[sympo_code].description
            if sympo_code is not None
            else ""
        )
