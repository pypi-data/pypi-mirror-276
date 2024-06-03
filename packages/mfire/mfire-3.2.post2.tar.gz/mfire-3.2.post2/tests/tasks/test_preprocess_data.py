import os
import json
import shutil
import tarfile

from pathlib import Path

import pytest

from mfire.settings.settings import Settings
from mfire.tasks.preprocess_data import DataPreprocessor
from mfire.utils.date import Datetime
from mfire.utils.exception import ConfigurationError


class TestPreprocessData:
    inputs_dir: Path = Path(__file__).parent / "inputs" / "preprocess_data"

    @pytest.mark.validation
    @pytest.mark.parametrize("rules", ["psym"])
    def test_preprocess_data(
        self,
        rules,
        tmp_path_cwd,
        assert_equals_file,
    ):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}.json",
            Settings().data_config_filename,
        )
        tarfile.open(self.inputs_dir / f"data_{rules}.tgz").extractall(tmp_path_cwd)

        assert os.system("python -m mfire.tasks.preprocess_data") == 0

        filenames = [
            "DD__HAUTEUR10.0006_0048_0001",
            "DD__HAUTEUR10.0051_0096_0003",
            "EAU1__SOL.0006_0048_0001",
            "EAU3__SOL.0006_0048_0001",
            "EAU6__SOL.0006_0048_0001",
            "EAU24__SOL.0006_0048_0001",
            "EAU__SOL.0006_0048_0001",
            "EAU__SOL.0051_0096_0003",
            "FF__HAUTEUR10.0006_0048_0001",
            "FF__HAUTEUR10.0051_0096_0003",
            "LPN__SOL.0006_0048_0001",
            "LPN__SOL.0051_0096_0003",
            "NEIPOT1__SOL.0006_0048_0001",
            "NEIPOT6__SOL.0006_0048_0001",
            "NEIPOT24__SOL.0006_0048_0001",
            "NEIPOT__SOL.0006_0048_0001",
            "NEIPOT__SOL.0051_0096_0003",
            "PRECIP__SOL.0006_0048_0001",
            "PRECIP__SOL.0051_0096_0003",
            "RAF__HAUTEUR10.0006_0048_0001",
            "RAF__HAUTEUR10.0051_0096_0003",
            "T__HAUTEUR2.0006_0048_0001",
            "T__HAUTEUR2.0051_0096_0003",
            "WWMF__SOL.0006_0048_0001",
            "WWMF__SOL.0051_0096_0003",
        ]

        for filename in filenames:
            path = Path("data/20230401T0000/promethee/FRANXL1S100") / (
                f"{filename}.netcdf"
            )
            assert path.exists(), f"{filename} was not computed"
            assert_equals_file(path)

    @pytest.mark.parametrize("rules", ["psym"])
    def test_preprocess_data_fonction(self, rules, tmp_path_cwd, assert_equals_result):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}.json",
            Settings().data_config_filename,
        )
        with pytest.raises(ValueError) as exc:
            DataPreprocessor(Settings().data_config_filename, None)
        assert isinstance(exc.value, ValueError)

        with pytest.raises(FileNotFoundError) as exc:
            DataPreprocessor("", rules)
        assert isinstance(exc.value, FileNotFoundError)

        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        with pytest.raises(KeyError) as exc:
            preprocessor.get_grib_params("", "")
        assert isinstance(exc.value, KeyError)
        dtype = preprocessor.get_param_dtype("EAU__SOL", "")
        assert dtype == "float32"
        get_grib_default = preprocessor.get_grib_params("EAU__SOL", "")
        assert_equals_result(get_grib_default)

    @pytest.mark.parametrize("rules", ["psym"])
    def test_get_backend_kwargs(self, rules, tmp_path_cwd, assert_equals_result):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}.json",
            Settings().data_config_filename,
        )
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        category = preprocessor.grib_param_dtypes.pop("parameterCategory")
        with pytest.raises(ConfigurationError) as exc:
            preprocessor.get_backend_kwargs("EAU__SOL", "default")
        assert isinstance(exc.value, ConfigurationError)
        preprocessor.grib_param_dtypes["parameterCategory"] = category
        backend = preprocessor.get_backend_kwargs("EAU__SOL", rules)
        assert_equals_result(backend)

    @pytest.mark.parametrize("rules", ["psym"])
    def test_extract_param_file(self, rules, tmp_path_cwd, assert_equals_file):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}.json",
            Settings().data_config_filename,
        )
        with open(self.inputs_dir / f"extract_{rules}.json") as f:
            file_input = json.load(f)
        file_input["grib_filename"] = Path(file_input["grib_filename"])
        file_input["preproc_filename"] = Path(file_input["preproc_filename"])
        file_input["postproc"]["start"] = Datetime(
            file_input["postproc"]["start"],
        )
        file_input["postproc"]["stop"] = Datetime(
            file_input["postproc"]["stop"],
        )
        grib_key = ("EAU__SOL", "sympo", 46)
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        grib_key, data = preprocessor.extract_param_file(grib_key, file_input)
        assert data is None

        tarfile.open(self.inputs_dir / f"data_{rules}_eau.tgz").extractall(tmp_path_cwd)
        dtype = file_input["dtype"]
        file_input["dtype"] = "type_inconnu"
        grib_key, data = preprocessor.extract_param_file(grib_key, file_input)
        assert data is not None
        file_input["dtype"] = dtype

        file_input["grib_attrs"].update({"GRIB_dataType": "fc"})
        grib_key, data = preprocessor.extract_param_file(grib_key, file_input)
        assert data is not None
        file_input["grib_attrs"].pop("GRIB_dataType")

        grib_key, data = preprocessor.extract_param_file(grib_key, file_input)
        assert data is not None
        data.to_netcdf("0046.netcdf")
        assert_equals_file(Path("0046.netcdf"))

    @pytest.mark.parametrize("rules", ["psym"])
    @pytest.mark.parametrize("accum", [None, 1, 3])
    def test_concat_export_dataarrays(
        self, rules, accum, tmp_path_cwd, assert_equals_file
    ):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}_cumul.json",
            Settings().data_config_filename,
        )
        tarfile.open(self.inputs_dir / f"data_{rules}_eau.tgz").extractall(tmp_path_cwd)
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        stack, preproc_stack = preprocessor.build_stack()
        eau = [
            resource
            for resource in preproc_stack.values()
            if resource["postproc"]["accum"] is accum
        ]
        for extract_id, extract_config in stack.items():
            file_id, dataarray = preprocessor.extract_param_file(
                extract_id, extract_config
            )
            if dataarray is None:
                print(f"Extracted grib empty for {file_id}.")
                assert False
            [
                preproc_config["files"][file_id].update({"data": dataarray})
                for preproc_config in preproc_stack.values()
                if file_id in preproc_config["files"]
            ]
        for dataarray_group in eau:
            preprocessor.concat_export_dataarrays(
                dataarray_group["filename"], dataarray_group
            )
        for filename in Path("data/20230401T0000/promethee/FRANXL1S100").iterdir():
            assert_equals_file(filename)

        filename = 0
        print(dataarray_group)
        [
            file_group["preproc"].update({"preproc_grid": "eurw1s100"})
            for file_group in dataarray_group["files"].values()
        ]
        assert not all(preprocessor.concat_export_dataarrays(filename, dataarray_group))
        assert not all(preprocessor.concat_export_dataarrays(filename, {"file": None}))

    @pytest.mark.parametrize("rules", ["psym"])
    def test_build_stack(self, rules, tmp_path_cwd, assert_equals_result):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}.json",
            Settings().data_config_filename,
        )
        tarfile.open(self.inputs_dir / f"data_{rules}_eau.tgz").extractall(tmp_path_cwd)
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        errors = {}
        stack, preproc_stack = preprocessor.build_stack(errors=errors)
        stack = {str(key): value for key, value in stack.items()}
        for resource in preproc_stack.values():
            maj = {"files": {}}
            for file_id, file_value in resource["files"].items():
                maj["files"].update({str(file_id): file_value})
            resource["files"] = maj
        res = [stack, preproc_stack]
        assert_equals_result(res)
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        os.makedirs("data/20230401T0000/MAJ06/FRANXL1S100", exist_ok=True)
        with open("data/20230401T0000/MAJ06/FRANXL1S100/0006.grib", "w") as f:
            f.write("vide")
        preprocessor.build_stack(errors=errors)
        assert errors["count"] == 877
        [
            preprocessor.sources_config[preproc_id][str(preproc_term)].clear()
            for preproc_config in preprocessor.preprocessed_config.values()
            for preproc_id, preproc_source in preproc_config["sources"].items()
            for preproc_term in preproc_source["terms"]
        ]
        preprocessor.build_stack(errors=errors)
        assert errors["count"] == 911
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        [
            preproc_source.update({"terms": ["NaN"]})
            for preproc_config in preprocessor.preprocessed_config.values()
            for preproc_source in preproc_config["sources"].values()
        ]
        preprocessor.build_stack(errors=errors)
        assert errors["count"] == 32
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        # to pass empty control
        with open("data/20230401T0000/MAJ06/FRANXL1S100/0006.grib", "w") as f:
            f.write("vide" * 1000)
        [
            preproc_config["agg"].update({"param": "inconnu"})
            for preproc_config in preprocessor.preprocessed_config.values()
        ]
        preprocessor.build_stack(errors=errors)
        assert errors["count"] == 911

    @pytest.mark.parametrize("rules", ["psym", "alpha"])
    def test_time_integration(self, rules, tmp_path_cwd, assert_equals_file):
        os.makedirs(Settings().config_filename.parent, exist_ok=True)
        shutil.copy(
            self.inputs_dir / f"data_task_config_{rules}_cumul.json",
            Settings().data_config_filename,
        )
        preprocessor = DataPreprocessor(Settings().data_config_filename, rules)
        tarfile.open(self.inputs_dir / f"data_{rules}_eau.tgz").extractall(tmp_path_cwd)
        stack, preproc_stack = preprocessor.build_stack()
        # Extract grib file only once
        eau = {
            key_res: resource
            for key_res, resource in preproc_stack.items()
            if resource["postproc"]["accum"] == 3
        }
        for extract_id, extract_config in stack.items():
            file_id, dataarray = preprocessor.extract_param_file(
                extract_id, extract_config
            )
            if dataarray is None:
                print(f"Extracted grib empty for {file_id}.")
            [
                preproc_config["files"][file_id].update({"data": dataarray})
                for preproc_config in preproc_stack.values()
                if file_id in preproc_config["files"]
            ]

        accum_data = preprocessor.create_accum_config(eau)
        # only one key
        for parameter in accum_data.values():
            assert all(preprocessor.time_integration(parameter))
            for preproc_file in parameter["preprocs"]:
                filename = preproc_file["filename"]
                assert_equals_file(Path(filename))
