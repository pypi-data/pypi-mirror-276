import xarray as xr

from mfire.utils.date import Datetime
from tests.composite.factories import (
    GeoCompositeFactory,
    WeatherCompositeFactory,
    WeatherCompositeInterfaceFactory,
)
from tests.functions_test import assert_identically_close
from tests.text.synthesis.factories import SynthesisReducerFactory


class TestSynthesisReducer:
    def test_has_risk(self):
        weather_compo = WeatherCompositeFactory(
            data_factory=xr.DataArray(
                [0, 1, 2],
                coords={
                    "valid_time": [Datetime(2023, 3, 1, i).as_np_dt64 for i in range(3)]
                },
            ),
            geos=GeoCompositeFactory(all_sub_areas_factory=["Sub Areas"]),
            interface=WeatherCompositeInterfaceFactory(
                has_risk=lambda x, y, z: (x, y, z)
            ),
        )
        reducer = SynthesisReducerFactory(composite=weather_compo)

        assert_identically_close(
            reducer.has_risk("Risk name"),
            (
                "Risk name",
                ["Sub Areas"],
                slice(
                    Datetime(2023, 3, 1).as_np_dt64, Datetime(2023, 3, 1, 2).as_np_dt64
                ),
            ),
        )
