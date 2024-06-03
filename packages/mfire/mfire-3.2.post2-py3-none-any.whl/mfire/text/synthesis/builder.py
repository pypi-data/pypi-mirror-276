from __future__ import annotations

from abc import abstractmethod
from functools import cached_property
from typing import Optional, Union

import numpy as np

from mfire.composite.weather import WeatherComposite
from mfire.text.base.builder import BaseBuilder


class SynthesisBuilder(BaseBuilder):
    """
    SynthesisBuilder class that must build synthesis texts
    """

    module_name: str = "synthesis"
    composite: Optional[WeatherComposite] = None

    def compute(self) -> Optional[str]:
        """
        Generate the text according to the weather composite

        Args:
            compo (BaseComposite): Composite used to make the reduction.

        Returns:
            str: The built text.
        """
        if not self.composite.check_condition(self.geo_id):
            return None
        return super().compute()

    @property
    @abstractmethod
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """

    @cached_property
    @abstractmethod
    def template_key(self) -> Optional[Union[str, np.ndarray]]:
        """
        Get the template key.

        Returns:
            Union[str, np.ndarray]: The template key.
        """
