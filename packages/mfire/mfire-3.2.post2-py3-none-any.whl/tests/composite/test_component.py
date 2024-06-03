from pathlib import Path

import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.aggregation import AggregationMethod, AggregationType
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
)
from mfire.composite.event import Category, Threshold
from mfire.composite.operator import ComparisonOperator
from mfire.composite.period import Period
from mfire.utils.date import Datetime
from mfire.utils.json import JsonFile
from tests.composite.factories import (
    AggregationFactory,
    AltitudeCompositeFactory,
    EventCompositeFactory,
    FieldCompositeFactory,
    GeoCompositeFactory,
    LevelCompositeFactory,
    RiskComponentCompositeFactory,
    SynthesisComponentCompositeFactory,
    WeatherCompositeFactory,
)
from tests.functions_test import assert_identically_close


class TestAbstractComponentComposite:
    def test_init_dates(self):
        component = SynthesisComponentCompositeFactory(
            production_datetime="2023-03-01", configuration_datetime="2023-03-02"
        )
        assert component.production_datetime == Datetime(2023, 3, 1)
        assert component.configuration_datetime == Datetime(2023, 3, 2)


class TestSynthesisComponentComposite:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_weather_period(self):
        compo = SynthesisComponentCompositeFactory()
        assert compo.weather_period == Period(
            id="period_id",
            start=Datetime(2023, 3, 1),
            stop=Datetime(2023, 3, 5),
        )

    def test_alt_area_name(self):
        ds = xr.Dataset(
            {"altAreaName": (["id"], ["area1", "area2"]), "id": ["id1", "id2"]}
        )
        text_compo = SynthesisComponentCompositeFactory(data_factory=ds)

        assert text_compo.alt_area_name("id1") == "area1"
        assert text_compo.alt_area_name("id2") == "area2"

    def test_area_name(self):
        ds = xr.Dataset(
            {"areaName": (["id"], ["area1", "area2"]), "id": ["id1", "id2"]}
        )
        text_compo = SynthesisComponentCompositeFactory(data_factory=ds)

        assert text_compo.area_name("id1") == "area1"
        assert text_compo.area_name("id2") == "area2"

    def test_compute(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[np.nan, 20.0, 30.0]], coords={"longitude": lon, "latitude": lat}
            )
        )

        # First weather risk_component
        field1 = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            ),
            name="T__HAUTEUR2",
        )
        geos1 = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[True, False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo1 = WeatherCompositeFactory(
            id="tempe", params={"tempe": field1}, altitude=altitude, geos=geos1
        )

        # Second weather risk_component
        field2 = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [[4.0, 5.0, 6.0]], coords={"longitude": lon, "latitude": lat}
            ),
            name="T__SOL",
        )
        geos2 = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[True, True, False]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo2 = WeatherCompositeFactory(
            id="tempe", params={"tempe": field2}, altitude=altitude, geos=geos2
        )

        # Text Component
        text_compo = SynthesisComponentCompositeFactory(
            geos=["id"], weathers=[weather_compo1, weather_compo2]
        )
        assert_equals_result(text_compo.compute().to_dict())

    def test_integration(self, assert_equals_result, root_path_cwd):
        data = JsonFile(self.inputs_dir / "small_conf_text.json").load()
        data_prod = next(iter(data.values()))
        component = data_prod["components"][0]
        compo = SynthesisComponentComposite(**component)

        assert_equals_result(compo)


class TestRiskComponentComposite:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_is_risks_empty(self):
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.is_risks_empty is True

        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [1])}, coords={"B": [2]})
        )
        assert risk_compo.is_risks_empty is False

    def test_risks_of_level(self):
        risk_compo = RiskComponentCompositeFactory(
            levels=[LevelCompositeFactory(level=1)] * 3
            + [LevelCompositeFactory(level=2)] * 5
        )
        assert len(risk_compo.risks_of_level(1)) == 3
        assert len(risk_compo.risks_of_level(2)) == 5
        assert len(risk_compo.risks_of_level(3)) == 0

    def test_final_risk_max_level(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.final_risk_max_level(geo_id="id") == 0

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [...])}, coords={"B": [...]}),
            final_risk_da_factory=xr.DataArray(
                [[1, 2], [4, 5]], coords={"id": ["id_1", "id_2"], "A": [..., ...]}
            ),
        )
        assert risk_compo.final_risk_max_level(geo_id="id_1") == 2
        assert risk_compo.final_risk_max_level(geo_id="id_2") == 5

    def test_final_risk_min_level(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.final_risk_min_level(geo_id="id") == 0

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [...])}, coords={"B": [...]}),
            final_risk_da_factory=xr.DataArray(
                [[1, 2], [4, 5]], coords={"id": ["id_1", "id_2"], "A": [..., ...]}
            ),
        )

        assert risk_compo.final_risk_min_level(geo_id="id_1") == 1
        assert risk_compo.final_risk_min_level(geo_id="id_2") == 4

    def test_alt_area_name(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.area_name(geo_id="id") == "N.A"

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"altAreaName": (["id"], ["area1", "area2"])},
                coords={"id": ["id1", "id2"]},
            )
        )
        assert risk_compo.alt_area_name(geo_id="id1") == "area1"
        assert risk_compo.alt_area_name(geo_id="id2") == "area2"

    def test_area_name(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.area_name(geo_id="id") == "N.A"

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"areaName": (["id"], ["area1", "area2"])},
                coords={"id": ["id1", "id2"]},
            )
        )
        assert risk_compo.area_name(geo_id="id1") == "area1"
        assert risk_compo.area_name(geo_id="id2") == "area2"

    def test_get_comparison(self):
        levels = [
            LevelCompositeFactory(
                level=1,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=13,
                            comparison_op=ComparisonOperator.SUP,
                            units="mm",
                        ),
                        mountain=Threshold(
                            threshold=13,
                            comparison_op=ComparisonOperator.INF,
                            units="mm",
                        ),
                    )
                ],
            ),
            LevelCompositeFactory(
                level=2,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=1.5,
                            comparison_op=ComparisonOperator.SUP,
                            units="cm",
                        ),
                        mountain=Threshold(
                            threshold=1.0,
                            comparison_op=ComparisonOperator.INF,
                            units="cm",
                        ),
                    )
                ],
            ),
            LevelCompositeFactory(
                level=3,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=20,
                            comparison_op=ComparisonOperator.SUPEGAL,
                            units="mm",
                        ),
                        mountain=Threshold(
                            threshold=0.5,
                            comparison_op=ComparisonOperator.INFEGAL,
                            units="cm",
                        ),
                    )
                ],
            ),
        ]

        risk_compo = RiskComponentCompositeFactory(levels=levels)
        assert risk_compo.get_comparison(1) == {
            "field_name": {
                "plain": Threshold(
                    threshold=13,
                    comparison_op=ComparisonOperator.SUP,
                    units="mm",
                    next_critical=15.0,
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=13,
                    comparison_op=ComparisonOperator.INF,
                    units="mm",
                    next_critical=10.0,
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }
        assert risk_compo.get_comparison(2) == {
            "field_name": {
                "plain": Threshold(
                    threshold=1.5,
                    comparison_op=ComparisonOperator.SUP,
                    units="cm",
                    next_critical=2.0,
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=1,
                    comparison_op=ComparisonOperator.INF,
                    units="cm",
                    next_critical=0.5,
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }
        assert risk_compo.get_comparison(3) == {
            "field_name": {
                "plain": Threshold(
                    threshold=20,
                    comparison_op=ComparisonOperator.SUPEGAL,
                    units="mm",
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=0.5,
                    comparison_op=ComparisonOperator.INFEGAL,
                    units="cm",
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }

    @pytest.mark.parametrize(
        "axis,expected",
        [
            (0, [5.0, 1.0, 4.0]),
            (1, [2.0, 4.0, 4.0]),
            ((0,), [5.0, 1.0, 4.0]),
            ((1,), [2.0, 4.0, 4.0]),
        ],
    )
    def test_replace_middle(self, axis, expected):
        x = np.array([[2.0, 1.0, 2.0], [5.0, 1.0, 4.0], [4.0, 4.0, 1.0]])
        result = RiskComponentComposite._replace_middle(x, axis=axis)
        assert_identically_close(result, np.array(expected))

    def test_special_merge(self):
        d1 = xr.Dataset(
            {
                "summarized_density": (["valid_time", "risk_level"], [[0.1, 0.2]]),
                "risk_summarized_density": (
                    [
                        "valid_time",
                        "risk_level",
                    ],
                    [[0.1, 0.2]],
                ),
                "occurrence": (["valid_time", "risk_level"], [[False, True]]),
                "occurrence_plain": (["valid_time", "risk_level"], [[False, True]]),
                "occurrence_mountain": (["valid_time", "risk_level"], [[False, True]]),
            },
            coords={
                "risk_level": [1, 2],
                "valid_time": [
                    np.datetime64("2024-02-01T00:00:00"),
                ],
            },
        )
        d2 = xr.Dataset(
            {
                "summarized_density": (
                    ["valid_time", "risk_level"],
                    [[0.2, 0.1], [0.4, 0.3]],
                ),
                "risk_summarized_density": (
                    ["valid_time", "risk_level"],
                    [[0.2, 0.1], [0.4, 0.3]],
                ),
                "occurrence": (
                    ["valid_time", "risk_level"],
                    [[True, False], [True, False]],
                ),
                "occurrence_plain": (
                    ["valid_time", "risk_level"],
                    [[True, False], [False, True]],
                ),
                "occurrence_mountain": (
                    ["valid_time", "risk_level"],
                    [[True, False], [False, True]],
                ),
            },
            coords={
                "risk_level": [1, 2],
                "valid_time": [
                    np.datetime64("2024-02-01T00:00:00"),
                    np.datetime64("2024-02-02T04:00:00"),
                ],
            },
        )

        result = RiskComponentComposite._special_merge(d1, d2)

        assert_identically_close(
            result,
            xr.Dataset(
                {
                    "summarized_density": (
                        ["valid_time", "risk_level"],
                        [[0.2, 0.2], [0.4, 0.3]],
                    ),
                    "risk_summarized_density": (
                        ["valid_time", "risk_level"],
                        [[0.2, 0.2], [0.4, 0.3]],
                    ),
                    "occurrence": (
                        ["valid_time", "risk_level"],
                        [[True, True], [True, False]],
                    ),
                    "occurrence_plain": (
                        ["valid_time", "risk_level"],
                        [[True, True], [False, True]],
                    ),
                    "occurrence_mountain": (
                        ["valid_time", "risk_level"],
                        [[True, True], [False, True]],
                    ),
                },
                coords={
                    "risk_level": [1, 2],
                    "valid_time": [
                        np.datetime64("2024-02-01T00:00:00"),
                        np.datetime64("2024-02-02T04:00:00"),
                    ],
                },
            ),
        )

    def test_compute(self, assert_equals_result):
        lon, lat = [15], [30, 31, 32, 33]
        ids = ["id"]

        altitude = AltitudeCompositeFactory(
            data_factory=xr.DataArray(
                [[10, np.nan, 20, 30]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos1 = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[False, True, True, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )
        geos2 = GeoCompositeFactory(
            data_factory=xr.DataArray(
                [[[False, True, False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        field1 = FieldCompositeFactory(
            data_factory=xr.DataArray(
                [
                    [
                        [1000, 2000],  # masked values by geos
                        [1500, 3000],  # masked values by altitude
                        [1.7, 1.9],  # isn't risked with threshold and geos
                        [1.8, 1.9],
                    ]
                ],
                coords={
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
                        [1500],  # masked values by geos
                        [2000],  # masked values by altitude
                        [1.6],  # isn't risked with threshold
                        [1.9],
                    ]
                ],
                coords={
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

        risk_compo.compute()
        assert_equals_result(
            {
                "risk_ds": risk_compo.risk_ds.to_dict(),
                "final_risk_da": risk_compo.final_risk_da.to_dict(),
            }
        )

    def test_integration(self, assert_equals_result, root_path_cwd):
        data = JsonFile(self.inputs_dir / "small_conf_risk.json").load()
        data_prod = next(iter(data.values()))
        component = data_prod["components"][0]
        compo = RiskComponentComposite(**component)

        assert_equals_result(compo)

    @pytest.mark.parametrize(
        "final_risk_da,expected",
        [
            # No information about fog
            (
                xr.DataArray(
                    [[1]], coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id3"]}
                ),
                None,
            ),
            (
                xr.DataArray(
                    [[1]], coords={"valid_time": [Datetime(2023, 2, 1)], "id": ["id1"]}
                ),
                None,
            ),
            # Mist without occurrence
            (
                xr.DataArray(
                    [[0]], coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1"]}
                ),
                False,
            ),
            # Mist with occurrence
            (
                xr.DataArray(
                    [[1, 0]],
                    coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1", "id2"]},
                ),
                True,
            ),
            (
                xr.DataArray(
                    [[0, 1]],
                    coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1", "id2"]},
                ),
                True,
            ),
        ],
    )
    def test_has_risk(self, final_risk_da, expected):
        valid_time_slice = slice(Datetime(2023, 3, 1), Datetime(2023, 3, 1, 2))
        assert (
            RiskComponentCompositeFactory(final_risk_da_factory=final_risk_da).has_risk(
                ids=["id1", "id2"],
                valid_time_slice=valid_time_slice,
            )
            == expected
        )
