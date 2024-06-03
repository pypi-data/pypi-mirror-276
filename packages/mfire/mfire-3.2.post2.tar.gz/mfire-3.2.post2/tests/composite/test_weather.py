import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.level import LocalisationConfig
from mfire.utils.date import Datetime
from tests.composite.factories import (
    AltitudeCompositeFactory,
    EventCompositeFactory,
    FieldCompositeFactory,
    GeoCompositeFactory,
    WeatherCompositeFactory,
)
from tests.functions_test import assert_identically_close


class TestWeatherComposite:
    def test_wrong_field(self):
        with pytest.raises(
            ValueError,
            match="Wrong field: [], expected ['wwmf', 'precip', 'rain', 'snow', "
            "'lpn']",
        ):
            WeatherCompositeFactory(
                id="weather",
                params={},
            )

    def test_init_datetime(self):
        weather_compo = WeatherCompositeFactory(production_datetime="2023-03-01")
        assert weather_compo.production_datetime == Datetime(2023, 3, 1)

    def test_check_condition_without_condition(self):
        weather_compo = WeatherCompositeFactory()
        assert weather_compo.check_condition("geo_id") is True

    def test_check_condition(self):
        ids = ["geo_id1", "geo_id2"]
        lon, lat = [15], [30, 31]
        valid_time = [Datetime(2023, 3, i).as_np_dt64 for i in range(1, 3)]

        field = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [[[15, 16], [15, 21]]],
                coords={"longitude": lon, "latitude": lat, "valid_time": valid_time},
                attrs={"units": "mm"},
            )
        )
        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[1, 1]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[True, False]], [[False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        evt = EventCompositeFactory(field=field, geos=geos, altitude=altitude)
        weather_compo = WeatherCompositeFactory(condition=evt)

        assert weather_compo.check_condition("geo_id1") is False
        assert weather_compo.check_condition("geo_id2") is True

    def test_altitudes(self):
        weather_compo = WeatherCompositeFactory(
            id="tempe",
            params={"tempe": FieldCompositeFactory(grid_name="franxl1s100")},
        )

        assert weather_compo.altitudes("weather") is None

        alt = weather_compo.altitudes("tempe")
        assert isinstance(alt, xr.DataArray)
        assert alt.name == "franxl1s100"

    def test_geos_data(self):
        geos = GeoCompositeFactory(
            data_factory=xr.DataArray([1, 2], coords={"id": ["id_1", "id_2"]}),
            mask_id=["id_1", "id_2"],
        )
        weather_compo = WeatherCompositeFactory(geos=geos)
        assert_identically_close(
            weather_compo.geos_data(),
            xr.DataArray([1, 2], coords={"id": ["id_1", "id_2"]}),
        )
        assert_identically_close(
            weather_compo.geos_data(geo_id="id_1"),
            xr.DataArray(1, coords={"id": "id_1"}),
        )

    @pytest.mark.parametrize("test_file_path", [{"extension": "nc"}], indirect=True)
    def test_geos_descriptive(self, test_file_path):
        lon, lat = [31], [40]
        ids = ["id_axis", "id_1", "id_2", "id_axis_altitude", "id_axis_compass"]
        ds = xr.Dataset(
            {
                "A": (
                    ["longitude", "latitude", "id"],
                    [[[True, True, False, True, False]]],
                ),
            },
            coords={
                "id": ids,
                "longitude": lon,
                "latitude": lat,
                "areaType": (
                    ["id"],
                    ["areaTypeAxis", "areaType1", "areaType2", "Altitude", "compass"],
                ),
            },
        )
        ds.to_netcdf(test_file_path)

        weather_compo = WeatherCompositeFactory(
            geos=GeoCompositeFactory(file=test_file_path, grid_name="A"),
            localisation=LocalisationConfig(
                geos_descriptive=["id_1", "id_2"],
                compass_split=True,
                altitude_split=True,
            ),
        )
        assert_identically_close(
            weather_compo.geos_descriptive("id_axis"),
            xr.DataArray(
                [[[1.0, np.nan, 1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2", "id_axis_altitude", "id_axis_compass"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["unknown", "unknown", "unknown", "unknown"]),
                    "altAreaName": (
                        ["id"],
                        ["unknown", "unknown", "unknown", "unknown"],
                    ),
                    "areaType": (
                        ["id"],
                        ["areaType1", "areaType2", "Altitude", "compass"],
                    ),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )

        weather_compo.localisation.compass_split = False
        weather_compo.localisation.altitude_split = False
        assert_identically_close(
            weather_compo.geos_descriptive("id_axis"),
            xr.DataArray(
                [[[1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["unknown", "unknown"]),
                    "altAreaName": (["id"], ["unknown", "unknown"]),
                    "areaType": (["id"], ["areaType1", "areaType2"]),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )

    def test_compute(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        field = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[np.nan, 20.0, 30.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[True, False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo = WeatherCompositeFactory(
            id="tempe", params={"tempe": field}, altitude=altitude, geos=geos
        )

        assert_equals_result(weather_compo.compute().to_dict())

    def test_compute_with_small_geos(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        field = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[30.0, 40.0, 50.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[True]]], coords={"id": ids, "longitude": lon, "latitude": [41]}
            ),
            mask_id=ids,
        )

        weather_compo = WeatherCompositeFactory(
            id="tempe", params={"tempe": field}, altitude=altitude, geos=geos
        )

        assert_equals_result(weather_compo.compute().to_dict())
