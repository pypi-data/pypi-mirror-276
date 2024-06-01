from abc import ABC

from mfire.composite.weather import WeatherComposite
from mfire.text.wind.base.builders import BaseBuilder
from mfire.text.wind.base.reducers import BaseReducer


class BaseDirector(ABC):
    """BaseDirector class.

    Its it used to handle the text synthesis generation.
    ."""

    REDUCER: BaseReducer = BaseReducer
    BUILDER: BaseBuilder = BaseBuilder
    WITH_EXTRA: bool = False

    def __init__(self):
        self.reducer = self.REDUCER()
        self.builder = self.BUILDER()

    def _compute_synthesis_elements(
        self, geo_id: str, composite: WeatherComposite
    ) -> tuple:
        """Compute synthesis elements."""

        summary = self.reducer.compute(geo_id, composite)
        return self.builder.compute(summary, self.WITH_EXTRA)

    def compute(self, geo_id: str, composite: WeatherComposite) -> str:
        """Compute synthesis text.

        If extra_content is not none, then text and extra_content are concatenated.
        """
        if not composite.check_condition(geo_id):
            return ""

        text, extra_content = self._compute_synthesis_elements(geo_id, composite)
        if extra_content:
            text += f" {extra_content}"

        return text
