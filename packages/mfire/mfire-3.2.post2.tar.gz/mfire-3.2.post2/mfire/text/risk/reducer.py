from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from itertools import combinations
from typing import Dict, List, Optional, Union, cast

import numpy as np
from pydantic import model_validator

import mfire.utils.mfxarray as xr
from mfire.composite.component import RiskComponentComposite
from mfire.composite.operator import ComparisonOperator
from mfire.localisation.risk_localisation import RiskLocalisation
from mfire.settings import Settings, get_logger
from mfire.text.base.reducer import BaseReducer
from mfire.text.risk.rep_value import RepValueReducer
from mfire.utils.date import Datetime, Period, PeriodDescriber, Periods
from mfire.utils.exception import LocalisationWarning
from mfire.utils.string import split_var_name
from mfire.utils.template import CentroidTemplateRetriever

# Logging
LOGGER = get_logger(name="text_reducer.mod", bind="text_reducer")


class RiskReducerBase(BaseReducer):
    composite: Optional[RiskComponentComposite] = None
    localisation: Optional[RiskLocalisation] = None
    geo_id: str

    @model_validator(mode="after")
    def init_localisation(self):
        if self.localisation is None:
            try:
                self.localisation = RiskLocalisation(
                    risk_component=cast(RiskComponentComposite, self.composite),
                    geo_id=self.geo_id,
                )
                self.localisation.compute()
            except LocalisationWarning:
                self.localisation = None
        return self

    @property
    def is_multizone(self) -> bool:
        return self.localisation is not None and self.localisation.is_multizone

    @cached_property
    def final_risk_da(self) -> xr.DataArray:
        return self.composite.final_risk_da.sel(id=self.geo_id)

    @cached_property
    def final_risk_max(self) -> int:
        return self.final_risk_da.max().item()

    @cached_property
    def risk_ds(self) -> xr.Dataset:
        return self.composite.risk_ds


class RiskReducerMonozone(RiskReducerBase):
    def process_value(self, param: str, evts_ds: List, kind: str) -> Optional[Dict]:
        """
        Retrieves all significant values (min, max, rep_value, units, etc.)
        for plain or mountain (kind argument).

        Args:
            param (str): Parameter (e.g. NEIPOT24__SOL).
            evts_ds (List): List of datasets containing events for a parameter.
            kind (str): Plain or mountain.

        Returns:
            Dict: Dictionary containing the information or None if the information is
                not available (e.g., for a qualitative parameter or when kind is
                mountain but no mountain is available).
        """
        occurrence_evt = False
        data_vars = evts_ds[0].data_vars
        threshold, min_v, max_v, rep_value = np.NaN, np.NaN, np.NaN, np.NaN
        if (
            f"min_{kind}" in data_vars
            and f"max_{kind}" in data_vars
            and f"rep_value_{kind}" in data_vars
            and kind in self.operator_dict[param]
        ):
            ev_values = []
            for ev in evts_ds:
                occurrence_evt = occurrence_evt or ev[f"occurrence_{kind}"].item()
                if ev[f"min_{kind}"].values < min_v or np.isnan(min_v):
                    min_v = ev[f"min_{kind}"].values

                if ev[f"max_{kind}"].values > max_v or np.isnan(max_v):
                    max_v = ev[f"max_{kind}"].values

                ev_values.append(ev[f"rep_value_{kind}"].values)

            rep_value = self.operator_dict[param][kind].critical_value(ev_values)
            threshold = evts_ds[0][f"threshold_{kind}"].item()

        values_dict = {
            "min": float(min_v) if not np.isnan(min_v) else None,
            "max": float(max_v) if not np.isnan(max_v) else None,
            "value": float(rep_value) if not np.isnan(rep_value) else None,
            "units": str(evts_ds[0].units.data),
            "operator": self.operator_dict[param].get(kind),
            "threshold": threshold,
            "occurrence": occurrence_evt,
        }

        return values_dict if None not in values_dict.values() else None

    def get_infos(self, data: Union[List[xr.Dataset], List[xr.DataArray]]) -> Dict:
        """
        Retrieves the information for each block Bi.

        Args:
            data (List[xr.Dataset]): List of data arrays for the same level.

        Returns:
            dict: Dictionary summarizing the desired information.
        """
        bloc, time = {"centroid": data[0].centroid.item()}, []

        if isinstance(data[0], xr.DataArray):
            bloc["level"] = 0
            time = [ech.values for ech in data]
        else:
            level = int(data[0].risk_level.values)
            bloc["level"] = level

            event_dict = defaultdict(lambda: [])
            for ech in data:
                time.append(ech.valid_time.values)
                for ev in ech.evt:
                    event = ech.sel(evt=ev)
                    key_event = str(event.weatherVarName.values)
                    # to handle no condition for some event for some level
                    # e.g. lvl1 with evt1 and evt2 but lvl2 with only evt1
                    if key_event != "nan":
                        event_dict[str(event.weatherVarName.data)].append(event)

            for k, v in event_dict.items():
                bloc[k] = {}
                plain = self.process_value(k, v, "plain")
                if plain:
                    bloc[k]["plain"] = {**plain}

                mountain = self.process_value(k, v, "mountain")
                if mountain:
                    bloc[k]["mountain"] = {**mountain}
                if (
                    mountain_altitude := self.composite.risks_of_level(level=level)[0]
                    .events[0]
                    .mountain_altitude
                ) is not None:
                    bloc[k]["mountain_altitude"] = mountain_altitude

        bloc["start"], bloc["stop"] = Datetime(min(time)), Datetime(max(time))
        return bloc

    @property
    def norm_risk(self) -> np.ndarray:
        """
        Returns normalized risk levels in the range 0 to 1.

        Returns:
            np.ndarray: Normalized risk levels.
        """
        norm_risk = self.final_risk_da.values
        if (max_level := self.risk_ds.risk_level.max().item()) > 1:
            # Normalize risk levels
            norm_risk = np.where(
                norm_risk, 1 - (((max_level - norm_risk) * 0.5) / (max_level - 1)), 0
            )
        return norm_risk

    @cached_property
    def operator_dict(self) -> Dict[str, Dict[str, ComparisonOperator]]:
        """Get the comparison operators used for rounding the representative values.

        Returns:
            operator_dict (Dict): Dictionary containing the comparison operators per
                event.
        """
        operator_dict = {}
        for level in self.composite.levels:
            for ev in level.events:
                operator_dict[ev.field.name] = {}
                try:
                    operator_dict[ev.field.name]["plain"] = ev.plain.comparison_op
                except AttributeError:
                    pass
                try:
                    operator_dict[ev.field.name]["mountain"] = ev.mountain.comparison_op
                except AttributeError:
                    pass
        return operator_dict

    def find_template_type(self):
        """
        Determines the template type (general, snow or precip) based on the variables
        included in the reduction block.

        Returns:
            str: The template type.
        """
        template_type = "general"

        if self.final_risk_max > 0:
            # Iterate over the reduction blocks
            for key, bloc in self.reduction.items():
                # Skip blocks that don't start with "B" or don't have the maximum risk
                # level.
                if not key.startswith("B") or bloc["level"] != self.final_risk_max:
                    continue

                # Get the variable names of the reduction block, excluding the keys that
                # are not relevant.
                keys = {
                    split_var_name(var_name)[0]
                    for var_name in bloc.keys()
                    if var_name not in ["level", "start", "stop", "centroid"]
                }

                # Determine the template type based on the variable names.
                if keys.issubset({"PRECIP", "EAU"}):
                    template_type = "PRECIP"
                    break
                if keys == {"NEIPOT"}:
                    template_type = "SNOW"
                    break
                if keys.issubset({"PRECIP", "EAU", "NEIPOT"}):
                    template_type = "PRECIP_SNOW"
                    break

        self.reduction["type"] = template_type

    def find_levels(self):
        """
        Add information about the maximum and intermediate levels to the reduction.

        This function iterates over the blocks in the reduction and adds information
        about the maximum and intermediate levels to the `level_max` and `level_int`
        dictionaries.

        The maximum level is determined by the centroid value. The intermediate levels
        are determined by comparing the representative values of the same parameter for
        the same level.
        """

        # Initialize the maximum and intermediate level dictionaries.
        self.reduction["level_max"] = {}
        self.reduction["level_int"] = {}

        # Iterate over the blocks in the reduction.
        for bloc, data in self.reduction.items():
            # Skip blocks that do not start with "B".
            if not bloc.startswith("B"):
                continue

            # Determine the level key based on the centroid value.
            if data["centroid"] == 1:
                level_key = "level_max"
            elif data["level"] != 0:
                level_key = "level_int"
            else:
                continue

            # Iterate over the keys and parameters in the block data.
            for key, param in data.items():
                # Skip keys that are not relevant to the level comparison
                if key in ["level", "start", "stop", "centroid"]:
                    continue

                # If the key is already present in the level dictionary and the
                # representative values is not better than the stored one, skip the
                # parameter.
                if key in self.reduction[level_key] and RepValueReducer.compare(
                    self.reduction[level_key][key], param
                ):
                    continue

                # Otherwise, add the parameter to the level dictionary.
                self.reduction[level_key][key] = param

    def process_period_monozone(self):
        """Process period-related tags in the comment for monozone case."""
        prod_date = self.composite.production_datetime

        # Process each key-value pair in the reduction dictionary
        for key, val in self.reduction.items():
            # Check if the value is a dictionary with 'start' and 'stop' keys
            if isinstance(val, dict) and "start" in val and "stop" in val:
                # Get the period description, start description, and stop description
                period = PeriodDescriber(prod_date).describe(
                    Period(val["start"], val["stop"])
                )
                start = PeriodDescriber(prod_date).describe(Period(val["start"]))
                stop = PeriodDescriber(prod_date).describe(Period(val["stop"]))

                # Add the period elements to the period table_localisation
                self.reduction[key]["period"] = period
                self.reduction[key]["start"] = start
                self.reduction[key]["stop"] = stop

    def compute_monozone(self) -> dict:
        """
        Reduces the risk into blocks based on the blocks found after using dtw.

        Returns:
            Union[List, dict]: Reduced risk as a list and a dictionary containing
                information for each block.
        """
        final_risk_da = self.final_risk_da

        self.reduction = CentroidTemplateRetriever.read_file(
            Settings().template_path("risk/monozone_generic"),
            index_col=["0", "1", "2", "3", "4"],
        ).get_by_dtw(self.norm_risk)

        final_risk_da["blocks"] = ("valid_time", [v[1] for v in self.reduction["path"]])
        centroid_list = []
        last = final_risk_da["blocks"].values[0]
        for x in final_risk_da["blocks"].values:
            if last == x:
                centroid_list.append(self.reduction["centroid"][last])
            else:
                centroid_list.append(self.reduction["centroid"][last + 1])
            last = x
        final_risk_da["centroid"] = ("valid_time", centroid_list)

        # Construction of B blocks
        same_level_list = []
        for idx, risk in enumerate(final_risk_da):
            if (
                idx > 0
                and risk["centroid"].data != final_risk_da["centroid"].data[idx - 1]
            ):
                previous_block = risk["blocks"].data - 1
                self.reduction[f"B{previous_block}"] = self.get_infos(same_level_list)
                same_level_list.clear()

            if risk["centroid"].values == 0:
                same_level_list.append(risk["valid_time"])
            elif risk.values in self.risk_ds.risk_level.values:
                same_level_list.append(
                    self.risk_ds.sel(
                        id=self.geo_id,
                        valid_time=risk["valid_time"],
                        risk_level=risk.values,
                    )
                )
        last_block = final_risk_da[-1]["blocks"].data
        self.reduction[f"B{last_block}"] = self.get_infos(same_level_list)
        self.find_template_type()
        self.find_levels()

        return self.reduction


class RiskReducerMultizone(RiskReducerBase):
    def process_period_multizone(self):
        """Process period-related tags in the comment for multizone case."""
        request_time = self.composite.production_datetime
        periods = []
        for period_name in self.localisation.periods_name:
            time_list = period_name.split("_to_")
            periods += [Period(time_list[0], time_list[-1])]

        elements = range(len(periods))

        for i in elements:
            for combin in combinations(elements, i + 1):
                keys, values = [], Periods()
                for j in combin:
                    keys += [str(j + 1)]
                    values += [periods[j]]
                key = "periode" + "_".join(keys)
                self.reduction[key] = PeriodDescriber(request_time).describe(values)

    def compute_multizone(self) -> dict:
        self.reduction = self.localisation.table_localisation.table
        return self.reduction


class RiskReducer(RiskReducerMonozone, RiskReducerMultizone):
    """RiskReducer: Object managing all functionalities of the risk_component
    necessary to create an appropriate comment.
    """

    def process_period(self):
        """Process period-related tags in the comment."""
        if self.is_multizone:
            self.process_period_multizone()
        else:
            self.process_period_monozone()

    def post_process(self):
        """Make a post-process operation in the reduction."""
        super().post_process()
        self.process_period()

    def _compute(self) -> dict:
        """Decides which comment generation module to use."""
        reduction = (
            self.compute_multizone() if self.is_multizone else self.compute_monozone()
        )
        reduction["alt_area_name"] = self.composite.alt_area_name(self.geo_id)
        return reduction
