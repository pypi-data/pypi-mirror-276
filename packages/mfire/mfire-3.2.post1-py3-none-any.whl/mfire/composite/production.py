from __future__ import annotations

from typing import List, Optional, Union

from mfire.composite.base import BaseComposite
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
    TypeComponent,
)
from mfire.composite.weather import WeatherCompositeInterface
from mfire.settings import get_logger
from mfire.text.text_manager import TextManager

# Logging
LOGGER = get_logger(name="productions.mod", bind="productions")


class ProductionComposite(BaseComposite):
    """
    Represents a ProductionComposite object containing the configuration of the
    Promethee production task.

    Args:
        baseModel: Pydantic base model.

    Returns:
        baseModel: Production object.
    """

    id: str
    name: str
    config_hash: str
    prod_hash: str
    mask_hash: str
    components: List[Union[RiskComponentComposite, SynthesisComponentComposite]]

    @property
    def cached_attrs(self) -> dict:
        return {}

    @property
    def sorted_components(
        self,
    ) -> List[Union[RiskComponentComposite, SynthesisComponentComposite]]:
        risks, synthesis = [], []
        for component in self.components:
            if component.type == TypeComponent.RISK:
                risks.append(component)
            else:
                synthesis.append(component)
        return risks + synthesis

    def has_risk(
        self, hazard_name: str, ids: List[str], valid_time_slice: slice
    ) -> Optional[bool]:
        """
        Checks if a risk with the given hazard name has occurred for any of the provided
        IDs within the specified time slice.

        Args:
            hazard_name (str): The name of the hazard to check for.
            ids (List[str]): A list of IDs to check for risks.
            valid_time_slice (slice): A time slice object representing the valid time
                range to consider.

        Returns:
            Optional[bool]:
                - True if a risk with the specified hazard name is found for any of the
                    IDs within the time slice.
                - False if no risks with the specified hazard name are found for the
                    given IDs and time slice.
                - None if there are no relevant components to check or if there are no
                    entries for the provided IDs.
        """
        for component in self.components:
            if (
                component.type == TypeComponent.SYNTHESIS
                or component.hazard_name != hazard_name
            ):
                continue

            return component.has_risk(ids, valid_time_slice=valid_time_slice)

    def _compute(self, **_kwargs) -> List[dict]:
        """
        Computes the production task by iterating over the components and invoking
        their compute method.
        """
        result = []
        for component in self.sorted_components:
            log_ids = {
                "production_id": self.id,
                "production_name": self.name,
                "component_id": component.id,
                "component_name": component.name,
                "component_type": component.type,
            }

            # Add the interface between risk and synthesis
            if component.type == TypeComponent.SYNTHESIS:
                for weather in component.weathers:
                    weather.interface = WeatherCompositeInterface(
                        has_risk=self.has_risk
                    )

            # Compute the component
            if not bool(component.compute()):
                result.append(None)
                continue

            # Handle of the generation of the text
            text_manager = TextManager(component=component)
            texts = {}
            for geo_id in component.geos:
                try:
                    text = text_manager.compute(geo_id)
                except Exception:
                    LOGGER.error(
                        "Failed to generate text on geo",
                        geo_id=geo_id,
                        **log_ids,
                        exc_info=True,
                    )
                    text = (
                        "Ce commentaire n'a pas pu être produit à cause d'un incident "
                        "technique."
                    )
                texts[geo_id] = text

            result.append(texts)

        return result
