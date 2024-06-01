from functools import cached_property
from typing import Tuple

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseModel
from mfire.composite.component import RiskComponentComposite
from mfire.composite.geo import GeoComposite
from mfire.composite.level import LevelComposite
from mfire.localisation.iolu_localisation import get_n_area
from mfire.settings import get_logger
from mfire.utils.exception import LocalisationError, LocalisationWarning

# Logging
LOGGER = get_logger(name="localisation", bind="localisation")


class SpatialLocalisation(BaseModel):
    """
    This module is responsible for the spatial localisation.

    Args:
        component (RiskComponentComposite): The risk_component.
        geo_id (str): The ID of the area to consider.
    """

    component: RiskComponentComposite
    geo_id: str

    domain: xr.DataArray = None
    areas: xr.DataArray = None

    @cached_property
    def risk_level(self) -> int:
        """
        Get the risk level for the risk_component and geographical area.

        The risk level is calculated using the `final_risk_max_level()` method of
        the risk_component.

        Returns:
            int: The risk level.
        """
        return self.component.final_risk_max_level(self.geo_id)

    @cached_property
    def localised_risk_ds(self) -> xr.Dataset:
        """
        Computes the risk for the given level over the localized area for the full
        period.

        Returns:
            xr.Dataset: The Dataset containing the risk_component's risks.
        """
        # Create a new risk_component.
        new_component = self.component.model_copy().reset()

        # Get the list of levels for the given risk level.
        level_list = [
            lvl.model_copy().reset()
            for lvl in self.component.risks_of_level(level=self.risk_level)
        ]

        # For each level, force the calculation of the geographical areas and elements.
        for level in level_list:
            # Set the list of elements to calculate.
            level.compute_list = ["density", "representative"]

            # For each event in the level, set the geos and the list of elements to
            # calculate.
            for event in level.events:
                event.geos = self.areas
                event.compute_list = ["density", "representative"]

        # Set the levels of the new risk_component.
        new_component.levels = level_list

        # Compute the new risk_component.
        return new_component.compute()

    @property
    def areas_with_occurrence(self) -> xr.DataArray:
        """
        Get the areas with occurrence for the localized risk.

        The areas with occurrence are the areas where the risk has a non-zero
        occurrence.

        Returns:
            xr.DataArray: A DataArray containing the areas with occurrence.

        Raises:
            LocalisationWarning: If the spatially localized occurrence is empty.
        """

        # Get the occurrence DataArray.
        occurrence = self.localised_risk_ds["occurrence"].squeeze("risk_level")

        # If the risk density DataArray is present, threshold the occurrence by the
        # risk density.
        if "risk_density" in self.localised_risk_ds:
            density = self.localised_risk_ds["risk_density"].squeeze("risk_level")
            threshold = density.max() / (5 if density.max() > 0.3 else 20)
            occurrence *= density > threshold

        if occurrence.sum().data == 0:
            raise LocalisationWarning("No occurrence for the risk")

        # Return the areas with occurrence.
        return occurrence

    def compute(self):
        """
        Localizes a risk to a specific geographical area.

        Raises:
            LocalisationError: If the `geo_id` is not present in `LevelComposite`.
            LocalisationError: If the risk is upstream.
        """
        if self.risk_level == 0:
            raise LocalisationWarning(
                "RiskLocalisation is only possible for risk level > 0."
            )
        hourly_maxi_risk = self.component.final_risk_da.sel(id=self.geo_id)
        periods = set(
            hourly_maxi_risk.sel(
                valid_time=(hourly_maxi_risk == self.risk_level)
            ).valid_time.data.astype("datetime64[s]")
        )

        # Find the best configuration for the given risk level and period.
        level, periods = self._find_configuration(periods)

        # Check if the risk is downstream. We can only localize downstream risks.
        if level.aggregation_type != "downStream":
            raise LocalisationWarning(
                "RiskLocalisation is only possible for downstream risk."
            )

        # Filter the events in the best level to only include those in the
        # given geographical area.
        level.compute_list = []
        for event in level.events:
            event.compute_list = []
            if isinstance(event.geos, GeoComposite):
                event_masks = event.geos.mask_id
                if isinstance(event_masks, str):
                    event_masks = [event_masks]

                if self.geo_id in event_masks:
                    event.geos.mask_id = [self.geo_id]
                else:
                    raise LocalisationError(
                        f"Mask with id '{self.geo_id}' not available "
                        f"(among {event_masks})."
                    )
            else:
                if self.geo_id in event.geos.id:
                    event.geos = event.geos.sel(id=self.geo_id)
                else:
                    raise LocalisationError(
                        f"Mask with id '{self.geo_id}' not available (among "
                        f"{event.geos.id.values})."
                    )

        # Compute the domain and areas
        self._compute_domain_and_areas(level, periods)

        return self

    def _compute_domain_and_areas(self, level: LevelComposite, periods: list):
        """
        Finds the possible localisation areas.

        Args:
            level (LevelComposite): Level element.
            periods (list): List of periods.

        Returns:
            Tuple[xr.DataArray, xr.DataArray]: The domain and the localisation areas.

        Raises:
            LocalisationWarning: If there are no areas for localisation.
        """
        # Get the spatial information for the best level.
        geos = level.events[0].geos

        # If the spatial information is a `GeoComposite` object, convert it to a
        # `DataArray` object with the specified grid name and `mask_id` set to `None`.
        if isinstance(geos, GeoComposite):
            geos = geos.compute(mask_id=None)

        # Select the domain from the full list.
        self.domain = geos.sel(id=self.geo_id)

        # Get the list of IDs of the localisation areas.
        id_list = [
            id
            for id in geos.id.data
            if id.startswith(self.geo_id) and id != self.geo_id
        ]

        # Select the localisation areas from the full list.
        # We also drop the areas that are not compatible with the `compass_split`
        # and `altitude_split` parameters.
        selected_area, drop_ids = geos.sel(id=id_list), []
        if not level.localisation.compass_split:
            compass_idx = selected_area["areaType"] == "compass"
            drop_ids.extend(selected_area.sel(id=compass_idx).id.values)
        if not level.localisation.altitude_split:
            alt_idx = selected_area["areaType"] == "Altitude"
            drop_ids.extend(selected_area.sel(id=alt_idx).id.values)

        # Add the descriptive geos to the list of IDs.
        id_list.extend(level.localisation.geos_descriptive)
        id_list = list(set(id_list).difference(set(drop_ids)))

        # Raise a warning if there are no areas for localisation.
        if not id_list:
            raise LocalisationWarning("There is no area for localisation process.")

        # Select the localisation areas from the full list.
        localisation_area = geos.sel(id=id_list).dropna("id", how="all").sortby("id")

        # Update the period to the specified period. We do this for all risks
        # except for accumulation risks, which require the entire dataset to be
        # calculated.
        if not level.is_accumulation:
            level.update_selection(new_sel={level.time_dimension: periods})

        level.compute()
        full_risk = level.spatial_risk_da

        # If the risk is an accumulation risk, select the specified period.
        if level.is_accumulation:
            full_risk = full_risk.sel({self.component.time_dimension: periods})

        # Squeeze the `full_risk` DataArray to remove the `id` dimension.
        full_risk = full_risk.squeeze("id").reset_coords("id", drop=True)

        # Get the localized area by selecting the `n` best areas from the `full_risk`
        # DataArray.
        self.areas = get_n_area(full_risk, self.domain, localisation_area)

    def _find_configuration(self, periods: set) -> Tuple[LevelComposite, list]:
        """
        Finds the best configuration for the given periods.

        The best configuration is the one with the most common periods with the
        input period. If there is a tie, the configuration with the earliest first
        period is chosen. If there is still a tie, the configuration with the most
        common periods is chosen.

        Args:
            periods (set): Period we are interested in.

        Returns:
            [LevelComposite]: The best level of the list for localisation.
            [list] The list of period to localise for this risk.

        Raises:
            ValueError: If no configuration with a common period is found.
        """
        best_level, best_periods = None, None

        # Iterate over the levels in the list and find the best match.
        for level in self.component.risks_of_level(level=self.risk_level):
            # Get the period covered by the current level.
            level_period = set(level.cover_period)

            # Find the intersection of the input period and the level period.
            common_periods = sorted(periods.intersection(level_period))

            # If there are no common periods, skip this level
            if len(common_periods) == 0:
                continue

            # Update best_periods and level
            if (
                best_periods is None
                or (
                    common_periods[0] < min(best_periods)
                    and len(common_periods) >= len(best_periods) / 4
                )
                or (
                    common_periods[0] > min(best_periods)
                    and len(common_periods) >= 4 * len(best_periods)
                )
            ):
                best_level = level.model_copy().reset()
                best_periods = set(common_periods)

        # If we haven't found any level with a common period, raise an error.
        if best_level is None:
            raise ValueError("Best conf not found")

        return best_level, list(best_periods)
