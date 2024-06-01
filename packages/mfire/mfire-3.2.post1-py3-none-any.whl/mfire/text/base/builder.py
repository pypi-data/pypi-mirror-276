from __future__ import annotations

from abc import abstractmethod
from functools import cached_property
from pathlib import Path
from typing import Optional, Union, cast

import numpy as np
from pydantic import model_validator

from mfire.composite.base import BaseComposite, BaseModel
from mfire.settings import Settings, get_logger
from mfire.text.base.reducer import BaseReducer
from mfire.utils.string import clean_text
from mfire.utils.template import (
    CentroidTemplateRetriever,
    Template,
    TemplateRetriever,
    read_template,
)

# Logging
LOGGER = get_logger(name="base_builder.mod", bind="base_builder")


class BaseBuilder(BaseModel):
    """
    BaseBuilder class that must build texts (summary text or detailed comment)
    """

    module_name: str

    text: str = ""
    data: dict = {}

    geo_id: Optional[str] = None
    composite: Optional[BaseComposite] = None
    reducer: Optional[BaseReducer] = None
    reducer_class: type = BaseReducer

    @model_validator(mode="after")
    def init_reducer(self):
        if self.reducer is None:
            self.reducer = self.reducer_class(
                geo_id=self.geo_id,
                data=self.data,
                composite=self.composite,
            )
        return self

    @property
    def reduction(self) -> Optional[dict]:
        return self.reducer.reduction

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

    @property
    def template_path(self) -> Path:
        return Settings().template_path(f"{self.module_name}/{self.template_name}")

    @cached_property
    def template_retriever(self) -> TemplateRetriever:
        """
        Get the template retriever.

        Returns:
            TemplateRetriever: The template retriever.
        """
        kwargs = {}
        if self.template_path.suffix == ".csv":
            kwargs["index_col"] = ["0", "1", "2", "3", "4"]
        return read_template(self.template_path, force_centroid=True, **kwargs)

    @cached_property
    def template(self) -> Optional[str]:
        """
        Retrieve the template from the file system.

        Returns:
            str: The template or None if the template name is not set or the template
                was not found.
        """
        template_key = self.template_key
        if template_key is None or (
            isinstance(template_key, str) and template_key == ""
        ):
            return template_key

        if self.template_path.suffix == ".csv":
            centroid_tpl_retriever = cast(
                CentroidTemplateRetriever, self.template_retriever
            )
            return centroid_tpl_retriever.get_by_dtw(template_key)["template"]
        return self.template_retriever.get(
            template_key, default=f"Unknown key {template_key}"
        )

    def clean_text(self):
        """Make a clean of the text."""
        self.text = clean_text(self.text)

    def pre_process(self):
        """Make a pre-process operation on the text."""

    def post_process(self):
        """Make a post-process operation on the text."""
        self.clean_text()

    def compute(self) -> str:
        """
        Generate the text according to the weather composite

        Returns:
            str: The built text.
        """
        if self.reduction is None:
            self.reducer.compute()

        self.text = self.template
        if self.text is None:
            self.text = (
                "Ce commentaire n'a pas pu être produit à cause d'un incident "
                "technique."
            )
            LOGGER.error(
                "Failed to retrieve template",
                template_key=self.template_key,
                template_path=self.template_path,
                template_name=self.template_name,
                module_name=self.module_name,
            )
        else:
            self.pre_process()
            self.text = Template(self.text).format(**self.reduction)
            self.post_process()

        return self.text
