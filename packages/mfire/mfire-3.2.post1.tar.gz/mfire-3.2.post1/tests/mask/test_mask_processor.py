from pathlib import Path

import pytest
from numpy import nan

import mfire.utils.mfxarray as xr
from mfire.mask import MaskProcessor
from mfire.mask.mask_merge import MaskMerge
from mfire.mask.mask_processor import MaskFile
from mfire.settings import Settings
from mfire.tasks.process_mask import main_function
from mfire.utils import recursive_format
from mfire.utils.json import JsonFile
from tests.functions_test import assert_identically_close


class TestMaskFile:
    def test_init_fails(self):
        with pytest.raises(
            ValueError,
            match="You should have in the file something to name the output.",
        ):
            _ = MaskFile(data={}, grid_names=[])

    def test_to_file(self, tmp_path):
        # With hash
        ds = xr.Dataset({"grid_1": [1.0, 0.0, True, False]}, coords={"is_point": []})
        mask_merge = MaskMerge()
        mask_merge.merge(ds)

        output_path = tmp_path / "folder1" / "file1.nc"
        mask_file = MaskFile(
            data={"file": output_path, "mask_hash": "mask_hash"},
            grid_names=["grid_1"],
        )

        mask_file.to_file(mask_merge)
        assert_identically_close(
            xr.open_dataset(output_path),
            xr.Dataset(
                {"grid_1": [True, False, True, False]}, attrs={"md5sum": "mask_hash"}
            ),
        )

        # Without hash
        output_path = tmp_path / "folder2" / "file2.nc"
        mask_file = MaskFile(
            data={"file": output_path, "geos": "test"},
            grid_names=["grid_1"],
        )

        mask_file.to_file(mask_merge)
        assert_identically_close(
            xr.open_dataset(output_path),
            xr.Dataset(
                {"grid_1": [True, False, True, False]}, attrs={"md5sum": "098f6bcd"}
            ),
        )


class TestMaskProcessor:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_extract_area_name(self):
        assert MaskProcessor.extract_area_name({"name": "nom"}) == "nom"
        assert MaskProcessor.extract_area_name({"label": "nom"}) == "nom"
        assert MaskProcessor.extract_area_name({"alt_label": "nom"}) == "nom"
        assert MaskProcessor.extract_area_name({"areaName": "nom"}) == "nom"
        assert MaskProcessor.extract_area_name({"area_name": "nom"}) == "nom"

        with pytest.raises(
            ValueError, match="Area name not found in properties dictionary"
        ):
            _ = MaskProcessor.extract_area_name({"notknownkey": "nom"})

    def test_extract_alt_area_name(self, assert_equals_result):
        assert MaskProcessor.extract_alt_area_name({"alt_label": "XXX_(YYY)"}) == "YYY"
        assert_equals_result(
            {
                language: MaskProcessor.extract_alt_area_name(
                    {"alt_label": "XXX", "label": "YYY"}
                )
                for language in Settings.iter_languages()
            }
        )

    def test_mask_31(self, tmp_path, assert_equals_file):
        data = JsonFile(self.inputs_dir / "mask_config.json").load()
        conf = recursive_format(data["0"], {"output_folder": str(tmp_path)})
        main_function(conf)
        assert_equals_file(tmp_path / "carre.nc")

    @pytest.mark.parametrize("languages", Settings().languages)
    def test_mask_CEI11(self, languages, tmp_path, assert_equals_file):
        Settings.set_language(languages)
        data = JsonFile(self.inputs_dir / "mask_config.json").load()
        conf = recursive_format(data["1"], {"output_folder": str(tmp_path)})
        main_function(conf)
        assert_equals_file(tmp_path / "CEI_11.nc")

    def test_generate_mask_by_altitude(self, assert_equals_result):
        valeurs = [[9999, 100, 220], [450, 550, 650], [1750, 3130, 4000]]
        altitude = xr.DataArray(
            data=valeurs,
            coords={"latitude": [44, 45, 46], "longitude": [0, 1, 2]},
            dims=["latitude", "longitude"],
            name="grille",
        )
        area_id = "id1"

        # Empty domain
        valeurs = [[[nan, nan, nan], [nan, nan, nan], [nan, nan, nan]]]
        domain = xr.DataArray(
            data=valeurs,
            coords={
                "latitude_grille": [44, 45, 46],
                "longitude_grille": [0, 1, 2],
                "id": ["id1"],
            },
            dims=["id", "latitude_grille", "longitude_grille"],
            name="grille",
        )
        result = MaskProcessor.generate_mask_by_altitude(domain, altitude, area_id)
        assert result is None

        # Domain within altitude
        valeurs = [[[nan, 1, 1], [1, 1, 1], [1, 1, 1]]]
        domain = xr.DataArray(
            data=valeurs,
            coords={
                "latitude_grille": [44, 45, 46],
                "longitude_grille": [0, 1, 2],
                "id": ["id1"],
            },
            dims=["id", "latitude_grille", "longitude_grille"],
            name="grille",
        )
        result = MaskProcessor.generate_mask_by_altitude(domain, altitude, area_id)
        assert_equals_result(result.to_dict())
