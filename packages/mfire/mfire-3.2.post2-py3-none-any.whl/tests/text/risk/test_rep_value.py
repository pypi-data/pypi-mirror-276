from collections import defaultdict
from itertools import product
import numpy as np
import pytest

from mfire.composite.operator import ComparisonOperator
from mfire.settings import Settings
from mfire.text.risk.rep_value import (
    AltitudeRepValueReducer,
    FFRafRepValueBuilder,
    FFRafRepValueReducer,
    FFRepValueBuilder,
    FFRepValueReducer,
    PrecipitationRepValueBuilder,
    PrecipitationRepValueReducer,
    RainRepValueBuilder,
    RainRepValueReducer,
    RepValueBuilder,
    RepValueReducer,
    SnowRepValueBuilder,
    SnowRepValueReducer,
    TemperatureRepValueBuilder,
    TemperatureRepValueReducer,
)
from mfire.utils.string import _
from tests.text.risk.factories import (
    AltitudeRepValueBuilderFactory,
    AltitudeRepValueReducerFactory,
    AccumulationRepValueBuilderFactory,
    AccumulationRepValueReducerFactory,
    create_rep_value_test_data_altitude,
    FFRafRepValueBuilderFactory,
    FFRafRepValueReducerFactory,
    FFRepValueBuilderFactory,
    FFRepValueReducerFactory,
    PrecipitationRepValueBuilderFactory,
    PrecipitationRepValueReducerFactory,
    RainRepValueBuilderFactory,
    RainRepValueReducerFactory,
    RepValueBuilderFactory,
    RepValueReducerFactory,
    RepValueTestFactory,
    SnowRepValueBuilderFactory,
    SnowRepValueReducerFactory,
    TemperatureRepValueBuilderFactory,
    TemperatureRepValueReducerFactory,
)


# Test data
REP_VALUE_TEST_DATA: list[dict] = RepValueTestFactory().run()
REP_VALUE_TEST_DATA_ALTITUDE: list[dict] = create_rep_value_test_data_altitude(
    REP_VALUE_TEST_DATA
)


def format_data(data: dict, units: str) -> dict:
    data = data.copy()
    if "plain" in data:
        data["plain"]["units"] = units
    if "mountain" in data:
        data["mountain"]["units"] = units
    return data


def build_expected_result(input_data: dict, output_data: dict) -> dict:
    res = {}
    res.update({"input": input_data})
    res.update({"output": output_data})
    return res


class TestRepValueReducer:
    factory = RepValueReducerFactory()

    @pytest.mark.parametrize(
        "reducer_class",
        [
            FFRepValueReducer,
            FFRafRepValueReducer,
            TemperatureRepValueReducer,
            PrecipitationRepValueReducer,
            RainRepValueReducer,
            SnowRepValueReducer,
        ],
    )
    def test_initialization_failure(self, reducer_class):
        """Test that KeyError raised if if 'var_name' key is missing in data arg."""
        with pytest.raises(KeyError):
            reducer_class(data={})

    def test_def_article(self, assert_equals_result):
        result = defaultdict(lambda: {})
        for feminine in [True, False]:
            for plural in [True, False]:
                factory = RepValueReducerFactory(feminine=feminine, plural=plural)
                for language in Settings.iter_languages():
                    result[f"{feminine=},{plural=}"][language] = factory.def_article
        assert_equals_result(result)

    def test_indef_article(self, assert_equals_result):
        result = defaultdict(lambda: {})
        for feminine in [True, False]:
            for plural in [True, False]:
                factory = RepValueReducerFactory(feminine=feminine, plural=plural)
                for language in Settings.iter_languages():
                    result[f"{feminine=},{plural=}"][language] = factory.indef_article
        assert_equals_result(result)

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            # Plain cases only
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"plain": {"value": 1.5}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"plain": {"value": 2.5}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"plain": {"value": 1.5}},
                False,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"plain": {"value": 2.5}},
                False,
            ),
            # Plain and mountain cases
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 0.5}},
                True,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.INF},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 1.5}},
                True,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.INF},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 0.5}},
                False,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 1.5}},
                False,
            ),
            # Mountain cases only
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 1.5}},
                True,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"mountain": {"value": 2.5}},
                True,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"mountain": {"value": 1.5}},
                False,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 2.5}},
                False,
            ),
            # Special cases
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 3.0}},
                True,
            ),
            ({"mountain": {"value": 3.0}}, {"plain": {"value": 2.0}}, False),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL}},
                {
                    "plain": {"value": 2.0},
                    "mountain": {"value": 1.0},
                },
                False,
            ),
        ],
    )
    def test_compare(self, a, b, expected):
        assert RepValueReducer.compare(a, b) == expected

    @pytest.mark.parametrize("unit,expected", [("cm", "cm"), (None, "")])
    def test_units(self, unit, expected):
        assert self.factory.units(unit) == expected

    @pytest.mark.parametrize(
        "x,expected",
        [(None, None), (1e-7, None), (1e-5, "1e-05"), (10, "10"), (100.258, "100.258")],
    )
    def test_round(self, x, expected):
        assert self.factory.round(x) == expected

    def test_around_word(self, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            {
                language: self.factory.around_word
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "dict_in,expected",
        [  # no operator
            (
                {
                    "operator": None,
                    "next_critical": 12,
                    "value": 10,
                },
                (None, None),
            ),
            # no value
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": 12,
                    "value": None,
                },
                (None, None),
            ),
            # no next_critical
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": None,
                    "value": 10,
                },
                (10, None),
            ),
            # value < next_critical
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": 12,
                    "value": 10,
                },
                (10, None),
            ),
            # value < next_critical
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": 10,
                    "value": 12,
                },
                (9, 12),
            ),
        ],
    )
    def test_replace_critical(self, dict_in, expected):
        assert RepValueReducer.replace_critical(dict_in) == expected

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = RepValueReducerFactory(data=format_data(data, units="UNITS"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestFFRepValueReducer:
    factory = FFRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        assert_equals_result(
            {
                language: {
                    value: self.factory.round(value)
                    for value in [None, 1e-7, 1e-5, 7.5, 12.5]
                }
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = FFRepValueReducerFactory(data=format_data(data, units="km/h"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestTemperatureRepValueReducer:
    factory = TemperatureRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "x,operator,expected",
        [
            (None, ComparisonOperator.INF, None),
            (None, ComparisonOperator.SUP, None),
            (1e-7, ComparisonOperator.INF, "0"),
            (1e-7, ComparisonOperator.SUP, "1"),
            (7.5, ComparisonOperator.INF, "7"),
            (7.5, ComparisonOperator.SUP, "8"),
        ],
    )
    def test_round(self, x, operator, expected):
        assert self.factory.round(x, operator=operator) == expected

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = TemperatureRepValueReducerFactory(data=format_data(data, units="°C"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestFFRafRepValueReducer:
    factory = FFRafRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            (None, None),
            (1e-7, None),
            (1e-5, None),
            (7.5, None),
            (7.5, _("comprises entre")),
        ]
        assert_equals_result(
            {
                language: {
                    str((x, around)): self.factory.round(x, around=around)
                    for x, around in values
                }
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = FFRafRepValueReducerFactory(data=format_data(data, units="km/h"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestAccumulationRepValueReducer:
    @pytest.mark.parametrize(
        "var_name",
        ["NEIPOT1__SOL", "NEIPOT6__SOL", "EAU1__SOL"],
    )
    def test_accumulated_hours(self, var_name, assert_equals_result):
        reducer = AccumulationRepValueReducerFactory(var_name=var_name)
        assert_equals_result(reducer.accumulated_hours)


class TestSnowRepValueReducer:
    factory = SnowRepValueReducerFactory()

    @pytest.mark.parametrize(
        "var_name",
        ["NEIPOT1__SOL", "NEIPOT24__SOL"],
    )
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: SnowRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "var_name",
        ["NEIPOT1__SOL", "NEIPOT24__SOL"],
    )
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: SnowRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [None, 1e-7, 1e-5, 1.5, 4.5, 6.5, 7.5, 12.5, 17.5, 28.1, 113.4]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = SnowRepValueReducerFactory(data=format_data(data, units="cm"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestPrecipitationRepValueReducer:
    factory = PrecipitationRepValueReducerFactory()

    @pytest.mark.parametrize(
        "var_name",
        ["PRECIP3__SOL", "PRECIP1__SOL"],
    )
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: PrecipitationRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "var_name",
        ["PRECIP3__SOL", "PRECIP1__SOL"],
    )
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: PrecipitationRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            None,
            1e-7,
            1e-5,
            1.5,
            4.5,
            7.5,
            12.5,
            17.5,
            22,
            27,
            35,
            45,
            55,
            70,
            90,
            112.2,
            1218.5,
        ]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = PrecipitationRepValueReducerFactory(
            data=format_data(data, units="mm")
        )
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestRainRepValueReducer:
    factory = RainRepValueReducerFactory()

    @pytest.mark.parametrize(
        "var_name",
        ["EAU24__SOL", "EAU1__SOL"],
    )
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: RainRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "var_name,",
        ["EAU24__SOL", "EAU1__SOL"],
    )
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: RainRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            None,
            1e-7,
            1e-5,
            1.5,
            4.5,
            7.5,
            12.5,
            17.5,
            22,
            27,
            35,
            45,
            55,
            70,
            90,
            115,
            1215,
        ]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        reducer = RainRepValueReducerFactory(data=format_data(data, units="cm"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestAltitudeRepValueReducer:
    @pytest.mark.parametrize(
        "var_name",
        [
            "FF__HAUTEUR10",
            "T__HAUTEUR2",
            "RAF__HAUTEUR10",
            "NEIPOT1__SOL",
            "PRECIP1__SOL",
            "EAU12__SOL",
            "OTHER__OTHER",
        ],
    )
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, var_name, data, assert_equals_result):
        np.random.seed(1)
        reducer = AltitudeRepValueReducerFactory(data={var_name: data})
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )

    @pytest.mark.parametrize(
        "var_name,expected_class",
        [
            ("FF__HAUTEUR10", FFRepValueReducer),
            ("T__HAUTEUR2", TemperatureRepValueReducer),
            ("RAF__HAUTEUR10", FFRafRepValueReducer),
            ("PRECIP1__SOL", PrecipitationRepValueReducer),
            ("EAU12__SOL", RainRepValueReducer),
            ("NEIPOT1__SOL", SnowRepValueReducer),
            ("OTHER__OTHER", None),
        ],
    )
    def test_get_reducer(self, var_name, expected_class):
        result = AltitudeRepValueReducer.get_reducer(var_name)
        if expected_class is not None:
            assert result == expected_class
        else:
            assert result is None


class TestRepValueBuilder:
    @pytest.mark.parametrize(
        "var_name,expected_class",
        [
            ("FF__HAUTEUR10", FFRepValueBuilder),
            ("RAF__HAUTEUR10", FFRafRepValueBuilder),
            ("T__HAUTEUR2", TemperatureRepValueBuilder),
            ("PRECIP1__SOL", PrecipitationRepValueBuilder),
            ("EAU12__SOL", RainRepValueBuilder),
            ("NEIPOT1__SOL", SnowRepValueBuilder),
            ("OTHER__OTHER", None),
        ],
    )
    def test_get_builder(self, var_name, expected_class):
        result = RepValueBuilder.get_builder({"var_name": var_name})
        if expected_class is not None:
            assert isinstance(result, expected_class)
        else:
            assert result is None

    def test_template_name(self):
        builder = RepValueBuilderFactory()
        assert builder.template_name == "rep_value_generic"

    @pytest.mark.parametrize(
        "reduction,expected",
        [
            ({}, ""),
            ({"plain_value": ...}, "plain"),
            ({"mountain_value": ...}, "mountain"),
            ({"plain_value": ..., "local_plain_value": ...}, "local_plain"),
            ({"mountain_value": ..., "local_mountain_value": ...}, "local_mountain"),
            ({"plain_value": ..., "mountain_value": ...}, "plain_mountain"),
            (
                {"plain_value": ..., "local_plain_value": ..., "mountain_value": ...},
                "local_plain_mountain",
            ),
            (
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "plain_local_mountain",
            ),
            (
                {
                    "plain_value": ...,
                    "local_plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_local_mountain",
            ),
        ],
    )
    def test_template_key_not_accumulated(self, reduction, expected):
        builder = RepValueBuilderFactory(
            reducer=RepValueReducerFactory(reduction=reduction)
        )
        assert builder.template_key == expected

    @pytest.mark.parametrize(
        "data, reduction, expected",
        [
            ({}, {}, ""),
            ({"plain": ...}, {}, "no_acc_plain"),
            ({"plain": ...}, {"plain_value": ...}, "plain"),
            ({"plain": ...}, {"local_plain_value": ...}, "no_acc_plain_local_plain"),
            (
                {"plain": ...},
                {"plain_value": ..., "local_plain_value": ...},
                "local_plain",
            ),
            ({"mountain": ...}, {}, "no_acc_mountain"),
            ({"mountain": ...}, {"mountain_value": ...}, "mountain"),
            (
                {"mountain": ...},
                {"local_mountain_value": ...},
                "no_acc_mountain_local_mountain",
            ),
            (
                {"mountain": ...},
                {"mountain_value": ..., "local_mountain_value": ...},
                "local_mountain",
            ),
            ({"plain": ..., "mountain": ...}, {}, "no_acc_plain_no_acc_mountain"),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ...},
                "plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ...},
                "no_acc_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_plain_value": ...},
                "no_acc_plain_local_plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_mountain_value": ...},
                "no_acc_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "mountain_value": ...},
                "plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "local_plain_value": ...},
                "local_plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "local_mountain_value": ...},
                "plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ..., "local_plain_value": ...},
                "no_acc_plain_local_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ..., "local_mountain_value": ...},
                "no_acc_plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_plain_value": ..., "local_mountain_value": ...},
                "no_acc_plain_local_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_plain_value": ...,
                },
                "local_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "mountain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "no_acc_plain_local_plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_local_mountain",
            ),
        ],
    )
    def test_template_key_accumulated_var_name(self, data, reduction, expected):
        builder = AccumulationRepValueBuilderFactory(
            reducer=AccumulationRepValueReducerFactory(data=data, reduction=reduction)
        )
        assert builder.template_key == expected

    def test_pre_process(self):
        reduction = {
            "indefinite_var_name": "un cumul de précipitation sur 3 heures",
            "plain_value": "au maximum 3 mm",
            "around": "aux alentours de",
        }
        builder = RepValueBuilderFactory(
            text="On attend {indefinite_var_name} {around} {value}.",
            reducer=RepValueReducerFactory(
                reduction=reduction, data={"var_name": "TEST__VARNAME"}
            ),
        )
        builder.pre_process()

        assert builder.text == "On attend {indefinite_var_name} {around}{value}."
        assert builder.reduction == {
            "indefinite_var_name": "un cumul de précipitation sur 3 heures",
            "plain_value": "au maximum 3 mm",
            "around": "d'",
        }

    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: RepValueBuilderFactory(
                        data=format_data(data, units="UNITS")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )

    @pytest.mark.parametrize(
        "data",
        [
            # Empty data
            {},
            # rep value > next_critical
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "RAF__HAUTEUR10": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                },
            },
            # rep value < threshold
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": False,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": False,
                    },
                    "mountain_altitude": 1300,
                },
            },
            {
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                },
            },
            # Altitude builder same prefixes
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # Altitude builder different prefixes
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # No mountain_altitude
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                },
            },
            {
                "T__HAUTEUR2": {},
                "FF__HAUTEUR10": {},
            },
        ],
    )
    def test_compute_all(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            {
                language: RepValueBuilder.compute_all(data)
                for language in Settings.iter_languages()
            }
        )


class TestFFRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: FFRepValueBuilderFactory(
                        data=format_data(data, units="km/h")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestTemperatureRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: TemperatureRepValueBuilderFactory(
                        data=format_data(data, units="°C")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestFFRafRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: FFRafRepValueBuilderFactory(
                        data=format_data(data, units="km/h")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestSnowRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: SnowRepValueBuilderFactory(
                        data=format_data(data, units="cm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestPrecipitationRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: PrecipitationRepValueBuilderFactory(
                        data=format_data(data, units="mm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestRainRepValueBuilder:
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA)
    def test_compute(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: RainRepValueBuilderFactory(
                        data=format_data(data, units="mm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestAltitudeRepValueBuilder:
    @pytest.mark.parametrize(
        "var_name, unit",
        [
            ("FF__HAUTEUR10", "km/h"),
            ("T__HAUTEUR2", "°C"),
            ("RAF__HAUTEUR10", "km/h"),
            ("NEIPOT1__SOL", "cm"),
            ("PRECIP1__SOL", "cm"),
            ("EAU12__SOL", "cm"),
            ("OTHER__OTHER", "cm"),
        ],
    )
    @pytest.mark.parametrize("data", REP_VALUE_TEST_DATA_ALTITUDE)
    def test_compute(self, var_name, unit, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: AltitudeRepValueBuilderFactory(
                        data={var_name: format_data(data, units=unit)}
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )

    @pytest.mark.parametrize(
        "data1,data2",
        product(REP_VALUE_TEST_DATA_ALTITUDE, repeat=2),
    )
    def test_compute_both(self, data1, data2, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            build_expected_result(
                {"NEIPOT1__SOL": data1, "NEIPOT24__SOL": data2},
                {
                    language: AltitudeRepValueBuilderFactory(
                        data={"NEIPOT1__SOL": data1, "NEIPOT24__SOL": data2}
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )
