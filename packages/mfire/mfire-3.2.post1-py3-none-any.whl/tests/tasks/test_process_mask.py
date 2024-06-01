import os
import shutil
from pathlib import Path

import pytest

from mfire.settings.settings import Settings


class TestProcessMask:
    inputs_dir: Path = Path(__file__).parent / "inputs" / "process_mask"

    @pytest.mark.validation
    def test_process_mask(self, tmp_path_cwd, assert_equals_file):
        os.makedirs(Settings().config_filename.parent)
        shutil.copy(
            self.inputs_dir / "mask_task_config.json", Settings().mask_config_filename
        )
        assert os.system("python -m mfire.tasks.process_mask") == 0

        assert_equals_file(
            tmp_path_cwd / "mask" / "c717afb6-154d-4c9d-9755-bdf5bb326e5c.nc"
        )
