from typing import Optional

from mfire.composite.weather import WeatherComposite
from mfire.text.synthesis.reducer import SynthesisReducer
from mfire.text.synthesis.temperature import TemperatureBuilder
from mfire.text.synthesis.weather import WeatherBuilder
from tests.composite.factories import WeatherCompositeFactory
from tests.text.base.factories import BaseBuilderFactory, BaseReducerFactory


class SynthesisReducerFactory(SynthesisReducer, BaseReducerFactory):
    composite: Optional[WeatherComposite] = WeatherCompositeFactory()


class WeatherBuilderFactory(WeatherBuilder, BaseBuilderFactory):
    composite: Optional[WeatherComposite] = WeatherCompositeFactory()


class TemperatureBuilderFactory(TemperatureBuilder, BaseBuilderFactory):
    composite: Optional[WeatherComposite] = WeatherCompositeFactory()
