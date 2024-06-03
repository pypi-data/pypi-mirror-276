import random
from typing import Optional

from mfire.composite.serialized_types import s_slice
from mfire.utils.selection import Selection


class SelectionFactory(Selection):
    sel: Optional[dict] = {"id": random.randint(0, 42)}
    islice: Optional[dict[str, s_slice | float]] = {
        "valid_time": slice(random.randint(0, 42), random.randint(0, 42))
    }
    isel: Optional[dict] = {"latitude": random.randint(0, 42)}
    slice: Optional[dict[str, s_slice]] = {
        "longitude": slice(random.randint(0, 42), random.randint(0, 42))
    }
