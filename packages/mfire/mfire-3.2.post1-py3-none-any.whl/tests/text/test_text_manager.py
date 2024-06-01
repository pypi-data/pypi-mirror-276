from functools import partial
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
)
from mfire.settings import Settings
from mfire.text.text_manager import TextManager
from mfire.utils import recursive_format
from mfire.utils.date import Datetime
from mfire.utils.json import JsonFile
from tests.composite.factories import (
    PeriodFactory,
    RiskComponentCompositeFactory,
    SynthesisComponentCompositeFactory,
    WeatherCompositeFactory,
    WeatherCompositeInterfaceFactory,
)
from tests.text.base.factories import BaseBuilderFactory


class TestTextManager:
    @pytest.mark.parametrize(
        "period_start,production_datetime",
        [
            (Datetime("20230301T07"), Datetime("20230102")),
            (Datetime("20230102"), Datetime("20230301T06")),
        ],
    )
    def test_compute_empty(
        self, period_start, production_datetime, assert_equals_result
    ):
        period = PeriodFactory(start=period_start, stop=Datetime("20230302T06"))
        component = SynthesisComponentCompositeFactory(
            period=period, production_datetime=production_datetime
        )

        assert_equals_result(
            {
                language: TextManager(component=component).compute(geo_id="geo_id")
                for language in Settings.iter_languages()
            }
        )

    def test_compute_risk(self):
        manager = TextManager(
            component=RiskComponentCompositeFactory(),
            builders={
                "risk": partial(BaseBuilderFactory, compute_factory="RiskBuilder Text")
            },
        )
        assert manager.compute(geo_id="") == "RiskBuilder Text"

    def test_compute_synthesis_text(self, assert_equals_result):
        manager = TextManager(
            component=SynthesisComponentCompositeFactory(
                weathers=[
                    WeatherCompositeFactory(id="tempe"),
                    WeatherCompositeFactory(id="weather"),
                    # WeatherCompositeFactory(id="wind"),
                ],
            ),
            builders={
                "tempe": partial(
                    BaseBuilderFactory, compute_factory="Temperature Text"
                ),
                "weather": partial(BaseBuilderFactory, compute_factory="Weather Text"),
                # "wind": partial(BaseBuilderFactory, compute_factory="Wind Text"),
            },
        )
        assert_equals_result(
            {
                language: manager.compute(geo_id="")
                for language in Settings.iter_languages()
            }
        )


@pytest.mark.validation
class TestTextManagerValidation:
    inputs_dir: Path = Path(__file__).parent / "inputs" / "text_manager"

    @pytest.mark.parametrize("language", ["fr", "en", "es"])
    @pytest.mark.parametrize("period", ["20230309", "20230319", "20230401", "20230402"])
    @patch(
        "mfire.composite.weather.TEXT_ALGO",
        {
            "weather": {
                "generic": {
                    "params": {
                        "wwmf": {"field": "WWMF__SOL", "default_units": "Code WWMF"}
                    }
                }
            },
            "tempe": {
                "generic": {
                    "params": {"tempe": {"field": "T__HAUTEUR2", "default_units": "°C"}}
                }
            },
            "wind": {
                "generic": {
                    "params": {
                        "wind": {"field": "FF__HAUTEUR10", "default_units": "km/h"},
                        "gust": {"field": "RAF__HAUTEUR10", "default_units": "km/h"},
                        "direction": {"field": "DD__HAUTEUR10", "default_units": "°"},
                    }
                }
            },
        },
    )  # this patch avoids to have to use all (useless) data files for weather
    def test_compute_synthesis(self, language, period, assert_equals_result):
        Settings.set_language(language)

        inputs_dir = self.inputs_dir / "synthesis"
        config = JsonFile(inputs_dir / f"prod_task_config_{period}.json").load()

        # Replace "test_data_dir" by appropriate values
        data: dict = recursive_format(
            config,
            values={
                "data_dir": str(inputs_dir / period),
                "masks_dir": str(inputs_dir / "masks"),
            },
        )

        result = {}
        for value in data.values():
            component = SynthesisComponentComposite(**value["components"][0])

            # Handling the interface between risk and synthesis
            for weather in component.weathers:
                weather.interface = WeatherCompositeInterfaceFactory()

            # Computation
            for geo_id in component.geos:
                text_manager = TextManager(component=component)
                result[f"{component.name} > {geo_id}"] = text_manager.compute(
                    geo_id=geo_id
                )

        assert_equals_result(result)

    @pytest.mark.parametrize("language", ["fr", "en", "es"])
    @pytest.mark.parametrize("period", ["20220401T070000", "20210115T130000"])
    def test_compute_risk(self, language, period, root_path_cwd, assert_equals_result):
        np.random.seed(0)
        Settings.set_language(language)

        inputs_dir = self.inputs_dir / "risk"
        config = JsonFile(inputs_dir / period / "prod_task_config.json").load()

        result = {}

        # Replace "test_data_dir" by appropriate values
        data: dict = recursive_format(
            config,
            values={
                "inputs_dir": str(inputs_dir),
                "altitudes_dir": (
                    root_path_cwd / "mfire" / "settings" / "geos" / "altitudes"
                ),
            },
        )

        for production in data.values():
            for component in production["components"]:
                risk_component = RiskComponentComposite(**component)
                risk_component.compute()
                text_manager = TextManager(component=risk_component)
                for geo_id in risk_component.geos:
                    result[
                        f"{risk_component.name} > {risk_component.hazard_name} > "
                        f"{risk_component.area_name(geo_id)}"
                    ] = text_manager.compute(geo_id=geo_id)

        assert_equals_result(result)
