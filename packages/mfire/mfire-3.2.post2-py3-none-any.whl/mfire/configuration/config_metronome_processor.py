from mfire.composite.component import TypeComponent
from mfire.configuration.config_processor import ConfigProcessor
from mfire.configuration.config_tools import (
    reshape_risk_component,
    reshape_synthesis_component,
)
from mfire.configuration.geos import FeatureCollectionConfig
from mfire.settings import get_logger
from mfire.utils.exception import ConfigurationError

# Logging
LOGGER = get_logger(
    name="config_metronome_processor.mod", bind="config_metronome_processor"
)


class ConfigMetronomeProcessor(ConfigProcessor):
    """ConfigMetronomeProcessor : Class which parses a configuration
    issued from Metronome, reshape it like an original Promethee config and
    produces three configurations out of it (like the ConfigProcessor) :
        * a mask configuration (self.mask_config)
        * a data configuration (self.data_config)
        * a production configuration (self.prod_config)
    """

    @staticmethod
    def get_geo(config: list) -> FeatureCollectionConfig:
        """surcharge get_geo
        Enable to transform METRONOME area config dictionary such that
        it is compatible with GeoJSON format.

        Args:
            config (list): The input config
        Returns:
            FeatureCollection: [The config in GeoJSON format]
        """
        try:
            return FeatureCollectionConfig(features=config)
        except Exception as v:
            raise ConfigurationError(str(v)) from v

    @staticmethod
    def list_components_configs(single_config):
        """surcharge list_components_config : list all the components configurations
        contained in a prod_idx configuration.

        Args:
            prod_idx (int): Production index in the self.config
        """
        global LOGGER
        components_list = []
        for compo_config in single_config["components"]:
            # On va rajouter les clés de production si elles sont présentes
            # Pour l'instant on ne sait pas si elles sont au niveau du composant ou au
            # dessus.
            compo_config.setdefault(
                "production_id",
                single_config.get("production_id", "UnknownProductionID"),
            )
            compo_config.setdefault(
                "production_name",
                single_config.get("production_name", "UnknownProductionName"),
            )
            try:
                LOGGER = LOGGER.bind(compo_id=compo_config.get("id"))
                compo_type = compo_config["data"]["type"]
                if compo_type == TypeComponent.RISK:
                    components_list += reshape_risk_component(compo_config)
                else:
                    components_list += reshape_synthesis_component(compo_config)
            except ConfigurationError:
                LOGGER.error(
                    "Configuration Error caught.",
                    func="list_components_configs",
                    exc_info=True,
                )
            except BaseException:
                LOGGER.error(
                    "Exception caught.",
                    func="list_components_configs",
                    exc_info=True,
                )

        LOGGER = LOGGER.try_unbind("compo_id")
        return components_list
