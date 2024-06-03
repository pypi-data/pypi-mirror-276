from __future__ import annotations

from functools import cached_property
from typing import Optional, Union

import numpy as np
from pydantic import model_validator

from mfire.settings import get_logger
from mfire.text.base.builder import BaseBuilder
from mfire.text.risk.reducer import RiskReducer
from mfire.text.risk.rep_value import RepValueBuilder, RepValueReducer
from mfire.utils.string import clean_text

# Logging
LOGGER = get_logger(name="text.risk.builder.mod", bind="risk.builder")


class RiskBuilderBase(BaseBuilder):
    """
    This class enable to manage all text for representative values.
    It chooses which class needs to be used for each case.
    """

    geo_id: str
    reducer_class: type = RiskReducer
    reducer: Optional[RiskReducer] = None

    module_name: str = "risk"

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
    def is_multizone(self):
        return self.reducer.is_multizone

    @cached_property
    def template_name(self) -> str:
        if self.is_multizone:
            return f"multizone_{self.reducer.localisation.template_type}"
        if self.reduction["type"] == "general":
            return "monozone_generic"
        return "monozone_precip_or_snow"

    @property
    def template_key(self) -> Union[str, np.ndarray]:
        """
        Get the template key.

        Returns:
            str: The template key.
        """
        if self.is_multizone:
            return self.reducer.localisation.unique_name
        if self.reduction["type"] != "general":
            return self.reduction["type"]
        return self.reducer.norm_risk

    def append_rep_value(self, text: str) -> None:
        self.text += text if text.startswith("\n") else " " + text


class RiskMonozoneBuilder(RiskBuilderBase):
    """Specific builder for handling "monozone" type components."""

    def process_rep_value_monozone(self):
        """Processes the representative values for the comment.

        For cumulative values, only the highest-level block is considered.

        Args:
            reduction (dict): The block reduction.
        """
        rep_value_table = {}
        for bloc, data in self.reduction.items():
            if isinstance(data, dict):
                data_dict = {
                    k: v
                    for k, v in data.items()
                    if k not in ["start", "stop", "centroid", "period"]
                }

                if not data_dict.get("level"):
                    data_dict["level"] = -1
                if bool(data_dict) and data_dict["level"] != 0:
                    rep_value_table[f"{bloc}_val"] = data_dict

        if self.reduction["type"] in ["SNOW", "PRECIP", "PRECIP_SNOW"]:
            max_val = {}
            for bloc, data in rep_value_table.items():
                if data["level"] == self.reducer.final_risk_max:
                    for key, param in data.items():
                        if key in max_val and RepValueReducer.compare(
                            max_val[key], param
                        ):
                            pass
                        elif key != "level":
                            max_val[key] = param
            if max_val:
                self.append_rep_value(RepValueBuilder.compute_all(max_val))
        else:
            final_rep_value = {
                key: RepValueBuilder.compute_all(
                    {k: v for k, v in value.items() if k != "level"}
                )
                for key, value in rep_value_table.items()
                if len(value) > 1
            }
            self.text = clean_text(self.text.format(**final_rep_value))


class RiskMultizoneBuilder(RiskBuilderBase):
    """RiskMultizoneBuilder comment builder for handling 'multizone' types of
    components.
    """

    def process_rep_value_multizone(self):
        self.append_rep_value(
            RepValueBuilder.compute_all(self.reducer.localisation.critical_values)
        )


class RiskBuilder(RiskMonozoneBuilder, RiskMultizoneBuilder):
    def post_process(self):
        """Make a post-process operation on the text."""
        self.process_rep_value()
        super().post_process()

    def process_rep_value(self, **_kwargs):
        """
        The various representative values are processed.
        """
        if self.is_multizone:
            self.process_rep_value_multizone()
        else:
            self.process_rep_value_monozone()
