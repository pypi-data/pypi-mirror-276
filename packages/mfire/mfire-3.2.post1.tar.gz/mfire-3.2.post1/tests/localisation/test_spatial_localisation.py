import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.aggregation import AggregationType
from mfire.composite.event import Category, Threshold
from mfire.composite.level import LocalisationConfig
from mfire.composite.operator import ComparisonOperator
from mfire.utils.date import Datetime
from mfire.utils.exception import LocalisationError, LocalisationWarning
from tests.composite.factories import (
    AggregationFactory,
    AltitudeCompositeFactory,
    EventCompositeFactory,
    FieldCompositeFactory,
    GeoCompositeFactory,
    LevelCompositeFactory,
    RiskComponentCompositeFactory,
)
from tests.functions_test import assert_identically_close
from tests.localisation.factories import SpatialLocalisationFactory


class TestSpatialLocalisation:
    def test_risk_level(self):
        # Empty risk
        loc = SpatialLocalisationFactory(component=RiskComponentCompositeFactory())
        assert loc.risk_level == 0

        # Non-empty risk
        compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [...])}, coords={"B": [...]}),
            final_risk_da_factory=xr.DataArray(
                [[1, 2], [4, 5]], coords={"id": ["id_1", "id_2"], "A": [..., ...]}
            ),
        )
        assert (
            SpatialLocalisationFactory(component=compo, geo_id="id_1").risk_level == 2
        )
        assert (
            SpatialLocalisationFactory(component=compo, geo_id="id_2").risk_level == 5
        )

    @pytest.mark.parametrize("risk_level", [1, 2, 3])
    def test_localised_risk_ds(self, risk_level, assert_equals_result):
        lon, lat = [15], [30, 31, 32, 33]
        ids = ["id"]

        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[10, np.nan, 20, 30]], coords={"longitude": lon, "latitude": lat}
            )
        )

        geos1_da = xr.DataArray(
            [[[False, True, True, True]]],
            coords={"id": ids, "longitude": lon, "latitude": lat},
        )
        geos2_da = xr.DataArray(
            [[[False, True, False, True]]],
            coords={"id": ids, "longitude": lon, "latitude": lat},
        )
        geos1 = GeoCompositeFactory(data_factory=geos1_da)
        geos2 = GeoCompositeFactory(data_factory=geos2_da, grid_name=None)

        field1 = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [
                    [
                        [
                            [1000, 2000],  # masked values by geos
                            [1500, 3000],  # masked values by altitude
                            [1.7, 1.9],  # isn't risked with threshold and geos
                            [1.8, 1.9],
                        ]
                    ]
                ],
                coords={
                    "id": ids,
                    "longitude": lon,
                    "latitude": lat,
                    "valid_time": [
                        Datetime(2023, 3, i).as_np_dt64 for i in range(1, 3)
                    ],
                },
                attrs={"units": "cm"},
            ),
            grid_name="new_grid_name",
            name="NEIPOT24__SOL",
        )
        field2 = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [
                    [
                        [
                            [1500],  # masked values by geos
                            [2000],  # masked values by altitude
                            [1.6],  # isn't risked with threshold
                            [1.9],
                        ]
                    ]
                ],
                coords={
                    "id": ids,
                    "longitude": lon,
                    "latitude": lat,
                    "valid_time": [Datetime(2023, 3, 3).as_np_dt64],
                },
                attrs={"units": "cm"},
            ),
            grid_name="new_grid_name",
            name="NEIPOT1__SOL",
        )
        evt1 = EventCompositeFactory(
            field=field1,
            geos=geos1,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=2.0, comparison_op=ComparisonOperator.SUPEGAL, units="cm"
            ),
            compute_list=["density", "summary", "extrema", "representative"],
        )
        evt2 = EventCompositeFactory(
            field=field1,
            geos=geos2,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=15, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
            ),
            compute_list=["density", "summary", "extrema", "representative"],
        )
        evt3 = EventCompositeFactory(
            field=field2,
            geos=geos2,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=2.0, comparison_op=ComparisonOperator.SUPEGAL, units="cm"
            ),
            mountain=Threshold(
                threshold=12, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
            ),
            mountain_altitude=15,
            compute_list=["density", "summary", "extrema", "representative"],
        )

        lvl1 = LevelCompositeFactory(
            level=1,
            events=[evt1, evt2],
            logical_op_list=["or"],
            aggregation_type=AggregationType.DOWN_STREAM,
            compute_list=["density", "summary"],
            aggregation=AggregationFactory(),
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[evt1, evt2],
            logical_op_list=["and"],
            aggregation_type=AggregationType.DOWN_STREAM,
            compute_list=["density", "summary"],
            aggregation=AggregationFactory(),
        )
        lvl3 = LevelCompositeFactory(
            level=3,
            events=[evt3],
            aggregation_type=AggregationType.DOWN_STREAM,
            compute_list=["density", "summary"],
            aggregation=AggregationFactory(),
        )
        risk_compo = RiskComponentCompositeFactory(levels=[lvl1, lvl2, lvl3])
        loc = SpatialLocalisationFactory(
            component=risk_compo,
            risk_level_factory=risk_level,
            geo_id="id",
            areas=geos1_da,
        )

        assert_equals_result(loc.localised_risk_ds.to_dict())

    @pytest.mark.parametrize(
        "risk_density,expected",
        [
            (None, True),
            ([0.01, 0.2, np.nan], False),
            ([0.011, 0.2, np.nan], True),
            ([0.1, 0.5, np.nan], False),
            ([0.11, 0.5, np.nan], True),
        ],
    )
    def test_areas_with_occurrence(self, risk_density, expected):
        ids = ["id1"]
        valid_time = [Datetime(2023, 3, 1, i).as_np_dt64 for i in range(3)]

        risk_ds = xr.Dataset(
            {
                "occurrence": (
                    ["id", "risk_level", "valid_time"],
                    [[[1.0, 0.0, np.nan]]],
                )
            },
            coords={"id": ids, "risk_level": [1], "valid_time": valid_time},
        )
        if risk_density is not None:
            risk_ds["risk_density"] = (
                ["id", "risk_level", "valid_time"],
                [[risk_density]],
            )

        loc = SpatialLocalisationFactory(localised_risk_ds_factory=risk_ds)

        if expected is True:
            assert_identically_close(
                loc.areas_with_occurrence,
                xr.DataArray(
                    [[1.0, 0.0, np.nan]],
                    coords={"id": ids, "risk_level": 1, "valid_time": valid_time},
                    dims=["id", "valid_time"],
                    name="occurrence",
                ),
            )
        else:
            with pytest.raises(LocalisationWarning, match="No occurrence for the risk"):
                _ = loc.areas_with_occurrence

    @pytest.mark.parametrize(
        "compass,altitude,spatial_risk,expected_areas_id",
        [
            # Test simple area
            (True, True, [[1.0, 0.0], [0.0, 0.0]], [1]),
            # Test combined areas
            (True, True, [[1.0, 0.0], [1.0, 1.0]], [2, 1]),
            # Test compass
            (True, True, [[1.0, 0.0], [1.0, 0.0]], [1, 3]),
            (False, True, [[1.0, 0.0], [1.0, 0.0]], [1, 2]),
            # Test altitude
            (True, True, [[1.0, 0.0], [0.0, 1.0]], [1, 4]),
            (True, False, [[1.0, 0.0], [0.0, 1.0]], [1, 2]),
        ],
    )
    def test_compute_domain_and_areas(
        self, compass, altitude, spatial_risk, expected_areas_id
    ):
        valid_time = [Datetime(2023, 3, 1)]
        ids = ["iddomain" + id for id in ["", "_id1", "_id2", "_id3", "_id4"]]
        lon, lat = [30, 31], [40, 41]
        geos_da = xr.DataArray(
            [
                [[1.0, 1.0], [1.0, 1.0]],
                [[1.0, np.nan], [np.nan, np.nan]],
                [[np.nan, np.nan], [1.0, 1.0]],
                [[np.nan, np.nan], [1.0, np.nan]],
                [[np.nan, np.nan], [np.nan, 1.0]],
            ],
            coords={
                "id": ids,
                "longitude": lon,
                "latitude": lat,
                "areaName": (
                    ["id"],
                    ["domain", "area1", "area2", "area3", "area4"],
                ),
                "altAreaName": (
                    ["id"],
                    ["altDomain", "altArea1", "altArea2", "altArea3", "altArea4"],
                ),
                "areaType": (
                    ["id"],
                    ["domain", "type1", "type2", "compass", "Altitude"],
                ),
            },
            dims=["id", "longitude", "latitude"],
        )
        level = LevelCompositeFactory(
            data_factory=xr.Dataset(),  # to avoid computing
            events=[
                EventCompositeFactory(geos=GeoCompositeFactory(data_factory=geos_da))
            ],
            localisation=LocalisationConfig(
                compass_split=compass, altitude_split=altitude
            ),
            spatial_risk_da_factory=xr.DataArray(
                [[spatial_risk]],
                coords={
                    "id": [ids[0]],
                    "valid_time": valid_time,
                    "longitude": lon,
                    "latitude": lat,
                },
            ),
        )

        loc = SpatialLocalisationFactory(geo_id=ids[0])
        loc._compute_domain_and_areas(level=level, periods=valid_time)

        assert_identically_close(loc.domain, geos_da.isel(id=0))
        if "quantile" in loc.areas.coords:
            loc.areas = loc.areas.drop_vars("quantile")
        assert_identically_close(loc.areas, geos_da.isel(id=expected_areas_id))

    def test_compute_fails_with_risk_level_0(self):
        with pytest.raises(
            LocalisationWarning,
            match="RiskLocalisation is only possible for risk level > 0.",
        ):
            SpatialLocalisationFactory(
                component=RiskComponentCompositeFactory()
            ).compute()

    def test_compute_fails_with_upstream(self):
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        risk_compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            levels=[LevelCompositeFactory(level=1, cover_period_factory=valid_time)],
        )

        with pytest.raises(
            LocalisationWarning,
            match="RiskLocalisation is only possible for downstream risk.",
        ):
            SpatialLocalisationFactory(
                component=risk_compo, risk_level_factory=1
            ).compute()

    def test_compute_fails_with_mask_not_available(self):
        # With GeoComposite as geos
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            levels=[
                LevelCompositeFactory(
                    level=1,
                    cover_period_factory=valid_time,
                    aggregation_type=AggregationType.DOWN_STREAM,
                    aggregation=AggregationFactory(),
                )
            ],
        )
        with pytest.raises(
            LocalisationError,
            match="Mask with id 'geo_id' not available",
        ):
            SpatialLocalisationFactory(component=compo, risk_level_factory=1).compute()

        # With DataArray as geos
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            levels=[
                LevelCompositeFactory(
                    level=1,
                    events=[
                        EventCompositeFactory(
                            geos=xr.DataArray(coords={"id": ["id"]}, dims=["id"])
                        )
                    ],
                    cover_period_factory=valid_time,
                    aggregation_type=AggregationType.DOWN_STREAM,
                    aggregation=AggregationFactory(),
                )
            ],
        )
        with pytest.raises(
            LocalisationError,
            match="Mask with id 'geo_id' not available",
        ):
            SpatialLocalisationFactory(component=compo, risk_level_factory=1).compute()

    def test_compute_fails_without_area(self):
        ids = ["geo_id"]
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        geos = GeoCompositeFactory(
            mask_id=ids,
            data_factory=xr.DataArray(
                [...],
                coords={
                    "id": ids,
                    "areaName": (["id"], ["area1"]),
                    "altAreaName": (["id"], ["altArea1"]),
                    "areaType": (["id"], ["compass"]),
                },
                dims=["id"],
            ),
        )

        compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            levels=[
                LevelCompositeFactory(
                    level=1,
                    cover_period_factory=valid_time,
                    aggregation_type=AggregationType.DOWN_STREAM,
                    aggregation=AggregationFactory(),
                    events=[EventCompositeFactory(geos=geos)],
                    localisation=LocalisationConfig(compass_split=False),
                )
            ],
        )

        with pytest.raises(
            LocalisationWarning,
            match="There is no area for localisation process.",
        ):
            SpatialLocalisationFactory(component=compo, risk_level_factory=1).compute()

    def test_compute_fails_when_whole_zone_is_best_loc(self):
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        lon, lat = [30], [40, 41]
        geos = GeoCompositeFactory(
            mask_id=["iddomain"],
            data_factory=xr.DataArray(
                [[[1.0, 1.0]], [[1.0, 0.0]]],
                coords={
                    "id": ["iddomain", "iddomain_id1"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["Domain", "area1"]),
                    "altAreaName": (["id"], ["Domain", "altArea1"]),
                    "areaType": (["id"], ["domain", "type1"]),
                },
                dims=["id", "longitude", "latitude"],
            ),
        )

        compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["iddomain"], "valid_time": valid_time}
            ),
            levels=[
                LevelCompositeFactory(
                    level=1,
                    data_factory=xr.Dataset(),  # to avoid computing
                    cover_period_factory=valid_time,
                    aggregation_type=AggregationType.DOWN_STREAM,
                    aggregation=AggregationFactory(),
                    events=[EventCompositeFactory(geos=geos)],
                    spatial_risk_da_factory=xr.DataArray(
                        [[[[0.0, 1.0]]]],
                        coords={
                            "id": ["iddomain"],
                            "valid_time": valid_time,
                            "longitude": lon,
                            "latitude": lat,
                            "areaName": (["id"], ["area1"]),
                            "altAreaName": (["id"], ["altArea1"]),
                            "areaType": (["id"], ["type1"]),
                        },
                        dims=["id", "valid_time", "longitude", "latitude"],
                    ),
                )
            ],
        )

        with pytest.raises(
            LocalisationWarning,
            match="The whole zone is the best localisation",
        ):
            SpatialLocalisationFactory(
                component=compo, geo_id="iddomain", risk_level_factory=1
            ).compute()

    def test_compute(self, assert_equals_result):
        valid_time = [Datetime(2023, 3, 1).as_np_dt64]
        lon, lat = [30, 31], [40, 41]
        geos = GeoCompositeFactory(
            mask_id=["iddomain"],
            data_factory=xr.DataArray(
                [[[1.0, 1.0], [1.0, 1.0]], [[1.0, 0.0], [1.0, 0.0]]],
                coords={
                    "id": ["iddomain", "iddomain_id1"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["domain", "area1"]),
                    "altAreaName": (["id"], ["altDomain", "altArea1"]),
                    "areaType": (["id"], ["domain", "type1"]),
                },
                dims=["id", "longitude", "latitude"],
            ),
        )

        risk_compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [[1]], coords={"id": ["iddomain"], "valid_time": valid_time}
            ),
            levels=[
                LevelCompositeFactory(
                    level=1,
                    data_factory=xr.Dataset(),  # to avoid computing
                    cover_period_factory=valid_time,
                    aggregation_type=AggregationType.DOWN_STREAM,
                    aggregation=AggregationFactory(),
                    events=[EventCompositeFactory(geos=geos)],
                    spatial_risk_da_factory=xr.DataArray(
                        [[[[1.0, 0.0], [1.0, 0.0]]]],
                        coords={
                            "id": ["iddomain"],
                            "valid_time": valid_time,
                            "longitude": lon,
                            "latitude": lat,
                            "areaName": (["id"], ["area1"]),
                            "altAreaName": (["id"], ["altArea1"]),
                            "areaType": (["id"], ["type1"]),
                        },
                        dims=["id", "valid_time", "longitude", "latitude"],
                    ),
                )
            ],
        )
        loc = SpatialLocalisationFactory(
            component=risk_compo, geo_id="iddomain", risk_level_factory=1
        ).compute()

        assert_equals_result(
            {"domain": loc.domain.to_dict(), "areas": loc.areas.to_dict()}
        )
