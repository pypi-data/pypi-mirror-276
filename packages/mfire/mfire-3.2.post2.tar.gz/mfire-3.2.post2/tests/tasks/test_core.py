import os
import shutil
import tarfile
from pathlib import Path

import pytest

from mfire.settings.settings import Settings
from mfire.utils.dict import recursive_format
from mfire.utils.json import JsonFile


class TestCore:
    inputs_dir: Path = Path(__file__).parent / "inputs" / "core"

    @pytest.mark.validation
    @pytest.mark.parametrize("rules", ["psym"])
    def test_core(self, rules, tmp_path_cwd, assert_equals_result):
        os.makedirs(Settings().config_filename.parent)
        shutil.copy(
            self.inputs_dir / f"prod_task_config_{rules}.json",
            Settings().prod_config_filename,
        )
        tarfile.open(self.inputs_dir / f"data_{rules}.tgz").extractall(tmp_path_cwd)

        prod_task_config = JsonFile(Settings().prod_config_filename)
        prod_task_result = recursive_format(
            prod_task_config.load(),
            {"altitudes_dirname": str(Settings().altitudes_dirname)},
        )
        prod_task_config.dump(prod_task_result)

        assert os.system("python -m mfire.tasks.core --disable_random") == 0
        tarfile.open("output.tgz").extractall("output")

        result = {}
        for filename in Path("output").iterdir():
            content = JsonFile(filename).load()
            content.pop("DateProduction")
            result[filename.name[:23]] = content
        assert_equals_result(result)
