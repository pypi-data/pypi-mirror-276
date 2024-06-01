from typing import Optional

from mfire.settings import get_logger
from mfire.text.template import Template

# Logging
LOGGER = get_logger(name="base_builder.mod", bind="base_builder")


class BaseBuilder:
    """BaseBuilder qui doit construire les textes
    (texte de synthèse ou commentaire détaillé)"""

    def __init__(self, template: str = "") -> None:
        self.reset()
        self._text: Template = Template(template)
        self.reduction: Optional[dict] = None

    @property
    def text(self) -> Template:
        """text being built and processed by the builder

        Returns:
            Template: text (with a Template type instead of a simple string
                in order to profit from the formatting advantages of the Template
                type.)
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = None
        if isinstance(text, str):
            self._text = Template(text)

    def reset(self) -> None:
        """reset: resets the text"""
        self._text = None
        self.reduction = None

    def handle_comment(self, reduction):
        self._text = self._text.format(**reduction)

    def compute(self, reduction: dict) -> None:
        self.reset()
        self.reduction = reduction
