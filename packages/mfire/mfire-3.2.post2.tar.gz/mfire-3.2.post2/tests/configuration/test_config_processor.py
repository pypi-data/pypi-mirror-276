from pathlib import Path
from typing import Optional
from unittest import mock

import numpy as np

from mfire.composite.geo import AltitudeComposite
from mfire.configuration import VersionConfig
from mfire.configuration.config_processor import ConfigProcessor
from mfire.configuration.config_tools import config_metronome
from mfire.configuration.configs import ConfigGlobal
from mfire.utils.date import Datetime

# numpy.random seed
np.random.seed(42)

# Basic tests configuration
DRAFTING_DATETIME = Datetime(2021, 10, 20, 8)


class TestConfigProcessor:
    """New class for testing the config processing step"""

    inputs_dir: Path = Path(__file__).parent / "inputs"
    config_basename: Path = Path("prometheeInit_configprocessor.json")

    def grid_name_mock(
        self,
        grid_name: str,
        alt_min: Optional[int] = None,
        alt_max: Optional[int] = None,
    ):
        return AltitudeComposite(
            filename=f"mfire/settings/geos/altitudes/{grid_name}.nc",
            alt_min=alt_min,
            alt_max=alt_max,
        )

    def single_config_test(self, rules: str):
        config_filename = self.inputs_dir / self.config_basename
        cp = ConfigProcessor(
            config_filename=config_filename,
            rules=rules,
            drafting_datetime=DRAFTING_DATETIME,
            experiment="TEST",
        )
        configs = config_metronome(config_filename)
        config_global = ConfigGlobal(
            cp.experiment,
            "abcdef",
            cp.settings,
            cp.rules,
            cp.get_geo,
            cp.list_components_configs,
        )
        cp.set_confhash(configs)
        cp.set_configuration_datetime(configs)
        assert cp.version_config == VersionConfig(
            version="690db3a7",
            drafting_datetime=Datetime(2021, 10, 20, 8),
            reference_datetime=Datetime(2021, 10, 20, 8),
            production_datetime=Datetime(2021, 10, 20, 8),
            configuration_datetime=Datetime(2021, 10, 19, 20, 45, 12),
        )

        mask_dico, data_dico, prod_dico, _, _ = cp.process_single_prod(
            config_global, configs[0]
        )
        data_dico = {" ".join(key): value for key, value in data_dico.items()}
        data_sort = {key: data_dico[key] for key in sorted(data_dico.keys())}
        prod_dico["components"] = sorted(
            prod_dico["components"], key=lambda k: (k["id"], k["hazard_id"])
        )
        return {"mask": mask_dico, "data": data_sort, "prod": prod_dico}

    def test_single_config_alpha(self, assert_equals_result, root_path_cwd):
        with mock.patch.object(
            AltitudeComposite, "from_grid_name", new=self.grid_name_mock
        ):
            assert_equals_result(self.single_config_test(rules="alpha"))

    def test_single_config_psym(self, assert_equals_result, root_path_cwd):
        with mock.patch.object(
            AltitudeComposite, "from_grid_name", new=self.grid_name_mock
        ):
            assert_equals_result(self.single_config_test(rules="psym"))

    def test_single_config_psym_archive(self, assert_equals_result, root_path_cwd):
        with mock.patch.object(
            AltitudeComposite, "from_grid_name", new=self.grid_name_mock
        ):
            assert_equals_result(self.single_config_test(rules="psym_archive"))
