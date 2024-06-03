import json
from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from mfire.settings import SIT_GEN, UNITS_TABLES
from mfire.settings.constants import LOCALE_DIR, TEMPLATES_FILENAME
from mfire.utils.template import read_template


class TestConstants:
    def _parse_json(self, filename: Path):
        try:
            with open(filename) as f:
                return json.load(f)
        except ValueError:
            return None

    def _check(self, val: Any, read_func: Optional[Callable] = None):
        if isinstance(val, Path):
            assert val.is_file(), f"File {val} does not exist"
            if read_func:
                assert read_func(val) is not None, f"File {val} can't be read"
        elif isinstance(val, dict):
            for val in val.values():
                self._check(val, read_func=read_func)

    @pytest.mark.parametrize("language", ["fr", "en", "es"])
    def test_templates_filenames(self, language):
        for template_filename in TEMPLATES_FILENAME.values():
            self._check(
                LOCALE_DIR / language / template_filename, read_func=read_template
            )

    def test_sit_gen(self):
        self._check(SIT_GEN, read_func=self._parse_json)

    def test_units_tables(self):
        self._check(UNITS_TABLES)
