""" preprocess_data.py

Preprocessing data 'binary' file
Preprocesses raw model data files (grib files) according to a given "data" configuration
"""
from datetime import timezone
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Union

from mfire.configuration.rules import Rules
from mfire.settings import RULES_NAMES, get_logger
from mfire.settings.settings import Settings
from mfire.tasks.CLI import CLI
from mfire.utils import Tasks, exception
from mfire.utils import mfxarray as xr
from mfire.utils import xr as xr_utils
from mfire.utils.date import Datetime, Timedelta

# Logging
LOGGER = get_logger(name="tasks.preprocess_data.mod", bind="tasks.preprocess_data")


def run_info(all_grib: dict):
    """
    retrieve subCentre and run info for all param
    in order to be viewed by forecasters
    Args:
        all_grib : all info about data from grib
    """
    # Extract subcentre and run time (dataTime) from dataarray from grib
    run_info = {}
    for gribkey, gribinfo in all_grib.items():
        data = gribinfo["data"]
        param, _, step = gribkey
        subCentre = data.attrs["GRIB_subCentre"]
        dataTime = data.attrs["GRIB_dataTime"]
        # dataTime is numeric as HMM : we needd only H
        run_info.setdefault(param, {})["run"] = dataTime / 100
        run_info[param].setdefault("step_subCentre", {})[step] = subCentre
    # get list of all step over all parametre
    all_step = {}
    for info in run_info.values():
        all_step.update(info["step_subCentre"])
    all_step = dict(sorted(all_step.items(), key=lambda kv: int(kv[0])))
    # format to suitable structure for json_normalize
    params = []
    for param, info in run_info.items():
        single_param = {}
        single_param["param"] = param
        single_param["run"] = info["run"]
        for step in all_step.keys():
            if step in info["step_subCentre"].keys():
                single_param[step] = int(info["step_subCentre"][step])
            else:
                single_param[step] = None
        params.append(single_param)
    df = pd.json_normalize(params)
    # format float becasue when otherwise None covnet to float
    df.to_csv("run_info.csv", float_format="%.0f")


class DataPreprocessor:
    """DataPreprocessor
    Class handling the following data preprocessing according to a given config
    file :
        * parameter extraction from multigrib files
        * concatenation of term by parameter
        * FUTURE : accumulations and combinations of files
        * export to netcdf
    """

    grib_param_dtypes: dict = {
        "discipline": int,
        "parameterCategory": int,
        "productDefinitionTemplateNumber": int,
        "parameterNumber": int,
        "typeOfFirstFixedSurface": str,
        "level": int,
        "typeOfStatisticalProcessing": int,
        "derivedForecast": int,
        "percentileValue": int,
        "scaledValueOfLowerLimit": int,
        "scaledValueOfUpperLimit": int,
        "lengthOfTimeRange": int,
        "units": str,
    }
    mandatory_grib_param: list = [
        "subCentre",
        "dataTime",
        "name",
        "units",
        "startStep",
        "endStep",
        "stepRange",
    ]
    optional_grib_param: list = ["dtype"]

    def __init__(self, data_config_filename: Path, rules: str):
        """__init__

        Args:
            data_config_filename (Path): Name of the data config file
            rules (str): Name of the rules convention used for files selection. This
                argument must be an element of the RULES_NAMES tuple.
        """
        # Opening the data config file
        LOGGER.info(f"Opening config '{data_config_filename}'", func="__init__")
        with open(data_config_filename, "r") as data_config_file:
            data_config = json.load(data_config_file)
        self.sources_config = data_config["sources"]
        self.preprocessed_config = data_config["preprocessed"]
        self.missing_gribs = []

        # Checking rules convention
        LOGGER.info("Checking rules convention", func="__init__")
        if rules not in RULES_NAMES:
            raise ValueError(
                f"Given rules '{rules}' not among the available rules : {RULES_NAMES}"
            )

        # Opening rules file (for the grib_param_df)
        self.rules = Rules(name=rules)

    def get_grib_params(self, param: str, model: str) -> Dict[str, str]:
        """Method which extract grib's params information from the
        self.grib_param_df, for extraction purposes.

        Args:
            param (str): Param's name frollowing the Promethee standard (defined
                in the RULES csv configuration file)
            model (str): Model name following the Promethee standard (defined in
                the RULES csv standard)

        Returns:
            Dict[str, str]: dict of paired keys/values corresponding to the given
                (param, model)
        """
        try:
            return self.rules.grib_param_df.loc[(param, model)].dropna().to_dict()
        except KeyError:
            LOGGER.warning(
                f"Using 'default' model to retrieve '{param}' backend_kwargs.",
                param=param,
                model=model,
                func="get_backend_kwargs",
            )
            return self.rules.grib_param_df.loc[(param, "default")].dropna().to_dict()

    def get_backend_kwargs(
        self, param: str, model: str, indexpath: str = ""
    ) -> Dict[str, Union[List[str], Dict[str, str], str]]:
        """get_backend_kwargs : Method which extract the exact backend_kwargs
        dictionary for the cfgrib engine corresponding to the given param and
        model

        Args:
            param (str): Param name following the Promethee standard (defined
                in the RULES csv configuration file)
            model (str): Model name following the Promethee standard (defined
                in the RULES csv configuration file)
            indexpath (str, optional): Path to the directory where to store the
                .idx temporary files created by cfgrib. Defaults to ''.

        Returns:
            dict : Backend_kwargs dictionary for the cfgrib engine :
                * read_keys : list of keys to read
                * filter_by_keys : dict of paired keys/value corresponding
                    to the given (param, model)
                * indexpath : path where to store the .idx files created by
                    cfgrib. Default to ''.
        """
        raw_dico = self.get_grib_params(param=param, model=model)

        param_keys = {}
        for key, value in raw_dico.items():
            if key in self.optional_grib_param:
                continue
            if key not in self.grib_param_dtypes:
                raise exception.ConfigurationError(
                    f"Grib param key '{key}' not referenced in the grib_param_dtypes"
                )
            value_type = self.grib_param_dtypes[key]
            param_keys[key] = value_type(value)

        return {
            "read_keys": list(param_keys.keys()) + self.mandatory_grib_param,
            "filter_by_keys": param_keys,
            "indexpath": indexpath,
        }

    def get_param_dtype(self, param: str, model: str) -> str:
        """Gives the supposed dtype of a given param in the given model

        Args:
            param (str): Param's name frollowing the Promethee standard (defined
                in the RULES csv configuration file)
            model (str): Model name following the Promethee standard (defined in
                the RULES csv standard)

        Returns:
            str: Expected dtype of the variable
        """
        return self.get_grib_params(param=param, model=model).get("dtype", "float32")

    @staticmethod
    def extract_param_file(
        file_id,
        file_conf: dict,
    ) -> Tuple[dict, xr.DataArray]:
        """extract_param_file : Extracts a single parameter/step/grid from a single
        gribkey file

        Args:
            file_conf (dict): Dictionary configuring the file to open and the
                param to extract. It contains the following keys :
                * grib_filename : Name of the raw gribkey file
                * backend_kwargs : backend cfgrib kwargs used to extract the
                    correct parameter
                * preproc_filename : Name of the output netcdf file
                * grib_attrs : Attributes corrections
        Returns:
            gribkey: unique reference to the param info
            datarray : data itself
        """
        dataarray = None
        log_kwargs = {
            "file_id": file_id,
            "grib_filename": file_conf["grib_filename"],
            "backend_kwargs": file_conf["backend_kwargs"].get("filter_by_keys"),
            "func": "extract_param_file",
        }
        try:
            with xr.open_dataarray(
                file_conf["grib_filename"],
                engine="cfgrib",
                backend_kwargs=file_conf["backend_kwargs"],
            ) as tmp_da:
                dataarray = xr_utils.rounding(tmp_da.load())
        except Exception:
            LOGGER.error("Failed to extract parameter from file.", **log_kwargs)
            return (
                file_id,
                dataarray,
            )

        # Casting dtypes
        try:
            if file_conf["dtype"] == "int8":
                dataarray = dataarray.fillna(0)
            dataarray = dataarray.astype(file_conf["dtype"])
        except TypeError:
            LOGGER.warning(
                f"Failed to cast dtype {file_conf['dtype']} "
                "to the extracted dataarray.",
                **log_kwargs,
            )

        # Attributes corrections
        for attr_key, attr_value in file_conf["grib_attrs"].items():
            if attr_key not in dataarray.attrs:
                dataarray.attrs[attr_key] = attr_value
                continue

            if attr_value == dataarray.attrs.get(attr_key):
                continue

            if (
                attr_key == "units"
                and dataarray.attrs[attr_key] != attr_value
                and attr_value is not None
            ):
                LOGGER.debug(
                    f"Found 'units' = { dataarray.attrs[attr_key]} "
                    f"while '{attr_value}' expected. "
                    f"Changing 'units' to '{attr_value}'.",
                    **log_kwargs,
                )
                dataarray.attrs[attr_key] = attr_value
        # add valid_time dimension with specific attributes
        dataarray = dataarray.expand_dims(dim={"valid_time": 1}, axis=0)
        dataarray["valid_time"] = dataarray.valid_time.assign_attrs(
            {"standard_name": "time", "long_name": "time"}
        )
        # clean some info
        var_to_delete = {"heightAboveGround", "time", "step", "surface"}
        drop_var = set(dataarray.coords).intersection(var_to_delete)
        dataarray = dataarray.drop_vars(list(drop_var))

        return (
            file_id,
            dataarray,
        )

    @staticmethod
    def concat_dataarrays(dict_das: dict) -> xr.DataArray:
        """concat_dataarrays : concatenate a group of dataarrays into a single
            for non-cumulative data

        Args:
            dict_das (dict): Dictionary with all the dataarrays

        Returns:
            xr.DataArray: Concatenated and preprocessed dataarray
        """
        # Avant cela on va mettre les fichiers sur la grille désirée
        das = []
        source_steps = []
        grid_changes = 0
        preproc_grid = dict_das["postproc"]["grid"]
        for elt in sorted(
            dict_das["files"].values(),
            key=lambda file: file["data"].valid_time.values,
        ):
            source_grid = elt["preproc"].get("source_grid")
            source_steps.append(int(elt["preproc"].get("source_step", 1)))
            # On etend du nombre de step present dans le fichier en entree.
            # On vire certaine variables
            if source_grid != preproc_grid:
                grid_changes += 1
                LOGGER.info(f"Change grid : {source_grid} -> {preproc_grid}")
                da = xr_utils.interpolate_to_new_grid(elt["data"], preproc_grid)
                das.append(da)
            else:
                das.append(elt["data"])

        # Maintenant on concatene les differentes steps.
        concat_da = xr.concat(das, dim="valid_time")

        # on trie
        concat_da = concat_da.sortby("valid_time")

        # Enforcing variable name
        variable_name = dict_das["postproc"].get("param")
        concat_da.name = variable_name

        da_out = concat_da

        if (np.array(source_steps) != dict_das["postproc"]["step"]).any():
            LOGGER.info(
                "source_step != target_step, passage par xr_utils.fill_da",
                source_steps=source_steps,
                target_step=dict_das["postproc"]["step"],
                dim="valid_time",
            )
            da_out = xr_utils.fill_da(
                da=concat_da,
                source_steps=source_steps,
                target_step=dict_das["postproc"]["step"],
                freq_base="h",
            )

        return xr_utils.slice_da(
            da=da_out,
            start=dict_das["postproc"]["start"],
            stop=dict_das["postproc"]["stop"],
            coord_name="valid_time",
        )

    def concat_export_dataarrays(self, preproc_filename: str, dict_das: dict) -> bool:
        """concat_export_dataarrays : Concatenate and export to netcdf a
        group of xarray DataArrays

        Args:
            dataarray_group (tuple) : This tuple has two components :
                * ouput_filename (Path) : name of the netcdf file to be exported
                * dict_das (dictionnaire) :

        Returns:
            bool : True if the export went correctly
        """
        global LOGGER
        LOGGER = LOGGER.bind(
            preproc_filename=preproc_filename,
        )

        try:
            concat_da = self.concat_dataarrays(dict_das=dict_das)
        except Exception:
            LOGGER.error(
                "Failed to concat",
                func="concat_export_dataarrays",
                exc_info=True,
            )
            return [False]
        try:
            if concat_da.latitude[0] < concat_da.latitude[-1]:
                concat_da = concat_da.reindex(latitude=concat_da.latitude[::-1])
            concat_da.to_netcdf(preproc_filename)
        except Exception:
            LOGGER.error(
                "Failed to export",
                func="concat_export_dataarrays",
                exc_info=True,
            )
            return [False]
        LOGGER = LOGGER.try_unbind("preproc_filename")
        return [preproc_filename.is_file()]

    def build_stack(self, errors: dict = dict()) -> List[dict]:
        """build_stack : Builds a kind of "task processing stack"

        Returns:
            list : List of dictionaries. Each dictionary is the
                preprocessing config for a speficific file to extract.
        """
        stack = {}
        preproc_stack = {}
        proceed = 0
        # Loop on all the preprocessed files configurations to create
        # a 'raw stack', i.ea list of all the preprocessing config dicts
        for preproc_id, preproc_config in self.preprocessed_config.items():
            preproc_stack[preproc_id] = {}
            preproc_stack[preproc_id]["sources"] = {}
            preproc_rh = preproc_config["resource_handler"][0]
            preproc_rundate = Datetime(preproc_rh["date"])
            postproc = {
                "step": preproc_rh["step"],
                "start": preproc_rundate + Timedelta(hours=preproc_rh["begintime"]),
                "stop": preproc_rundate + Timedelta(hours=preproc_rh["endtime"]),
                "grid": preproc_rh["geometry"],
            }
            postproc.update(preproc_config["agg"])
            preproc_stack[preproc_id]["postproc"] = postproc
            preproc_filename = Path(preproc_rh["local"])
            preproc_stack[preproc_id]["filename"] = preproc_filename
            preproc_filename.parent.mkdir(parents=True, exist_ok=True)
            root_param = preproc_config["agg"]["param"]
            # Retrieving all useful post-proc information
            preproc_stack[preproc_id]["files"] = {}

            for source_id, source_info in preproc_config["sources"].items():
                preproc_stack[preproc_id]["sources"][source_id] = source_info["terms"]
                for term in source_info["terms"]:
                    proceed += 1
                    if str(term) not in self.sources_config[source_id]:
                        LOGGER.error(
                            "Inconsistency between term given by preprocessed file "
                            "and available source terms",
                            preproc_id=preproc_id,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        continue
                    if len(self.sources_config[source_id][str(term)]) == 0:
                        LOGGER.error(
                            "Source file configuration empty.",
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        continue

                    source_conf = self.sources_config[source_id][str(term)][0]
                    # checking if the source_conf["local"] grib is missing or empty
                    grib_filename = Path(source_conf["local"])
                    if grib_filename in self.missing_gribs:
                        # if grib is already labeled as missing
                        continue

                    if not grib_filename.is_file():
                        # if grib is missing and not already labeled as missing
                        LOGGER.error(
                            "Missing source grib file.",
                            grib_filename=grib_filename,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        self.missing_gribs.append(grib_filename)
                        continue

                    if grib_filename.stat().st_size < 300:
                        LOGGER.error(
                            "Source grib file empty (size = "
                            f"{grib_filename.stat().st_size} octets).",
                            grib_filename=grib_filename,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        self.missing_gribs.append(grib_filename)
                        continue
                    block = source_conf["block"]

                    try:
                        backend_kwargs = self.get_backend_kwargs(
                            root_param, source_conf["model"]
                        )
                        dtype = self.get_param_dtype(root_param, source_conf["model"])
                    except Exception:
                        LOGGER.error(
                            "Failed to retrieve backend_kwargs for (param, model)"
                            f" = ({root_param}, {source_conf['model']}).",
                            grib_filename=grib_filename,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                            exc_info=True,
                        )
                        continue

                    # Case of a accum param with lengthOfTimeRange
                    if "lengthOfTimeRange" in backend_kwargs["filter_by_keys"]:
                        backend_kwargs["filter_by_keys"]["lengthOfTimeRange"] = int(
                            source_info["step"]
                        )

                    units = backend_kwargs["filter_by_keys"].pop("units", None)
                    preproc_attrs = {
                        "source_grid": source_conf["geometry"],
                        "source_step": int(source_info["step"]),
                    }
                    file_id = (
                        root_param,
                        block,
                        term,
                    )
                    file_conf = {
                        file_id: {
                            "model": source_conf["model"],
                            "source": source_id,
                            "grib_filename": Path(source_conf["local"]),
                            "backend_kwargs": backend_kwargs,
                            "dtype": dtype,
                            "grib_attrs": {
                                "PROMETHEE_z_ref": preproc_rh["geometry"],
                                "units": units,
                            },
                            "preproc_attrs": preproc_attrs,
                        },
                    }
                    # store reference to grib in preproc file definition
                    preproc_stack[preproc_id]["files"].update(
                        {file_id: {"preproc": preproc_attrs}}
                    )

                    # file_conf_list += [file_conf]
                    stack.update(file_conf)
        errors["count"] = proceed - len(stack)
        return stack, preproc_stack

    @staticmethod
    def create_accum_config(preproc_config) -> dict:
        """
        summarize all info needed to compute accum
        that are : for the trio param/step/grid, start and stop time needed
        Args:
            preproc_config: all preproc files and sources needed
        Returns
            (dcit): all needed info for compute accum
        """
        accum_data = {}
        for file_id, dataarray_group in preproc_config.items():
            # accum param
            if (
                "accum" in dataarray_group["postproc"].keys()
                and dataarray_group["postproc"]["accum"] is not None
            ):
                # create the key from param/step/grid
                data_config = dataarray_group["postproc"]
                grid = data_config["grid"]
                step = data_config["step"]
                key = data_config["param"] + str(step) + grid
                end = data_config["stop"] + Timedelta(hours=data_config["accum"])
                preproc = {
                    "file_id": file_id,
                    "postproc": dataarray_group["postproc"],
                    "filename": dataarray_group["filename"],
                }
                if key in accum_data.keys():
                    # update start/stop key value
                    accum_data[key]["beginTime"] = min(
                        data_config["start"],
                        accum_data[key]["beginTime"],
                    )
                    accum_data[key]["endTime"] = max(
                        end,
                        accum_data[key]["endTime"],
                    )
                    accum_data[key]["files"].update(dataarray_group["files"])
                    accum_data[key]["preprocs"].append(preproc)
                else:
                    # create start/stop key value
                    accum_data[key] = {
                        "param": data_config["param"],
                        "grid": grid,
                        "beginTime": data_config["start"],
                        "endTime": end,
                        "step": step,
                        "files": dataarray_group["files"],
                        "preprocs": [preproc],
                    }

        return accum_data

    def preprocess(self, nproc: int):
        """preprocess : Preprocess all the data config dict in self.data_config

        Args:
            nproc (int): Number of CPUs to be used in parallel
        """

        def append_file(res: Tuple[dict, xr.DataArray]):
            """Tasks Local function to progressively append grib-extracted results
            to the all_grib dictionary.
            """
            file_id, dataarray = res
            if dataarray is None:
                LOGGER.error(f"Extracted grib empty for {file_id}.")
                return None
            [
                preproc_config["files"][file_id].update({"data": dataarray})
                for preproc_config in preproc_stack.values()
                if file_id in preproc_config["files"]
            ]
            stack[file_id]["data"] = dataarray

        def append_accum(res: Tuple[str, xr.DataArray]):
            """Tasks Local function to progressively append cumulative results to the
            accum_data dictionary.
            """
            key, grib_da = res
            accum_data[key]["data"] = grib_da

        def append_grouped(res: List):
            """Tasks Local function to progressively sum results to the
            success_resource dictionary.
            """
            success_resource["ok"] = sum(res) + success_resource["ok"]

        success_resource = {"ok": 0}
        # Building the preprocessing stack
        stack, preproc_stack = self.build_stack()

        # Extract grib file only once
        parallel = Tasks(processes=nproc)
        for extract_id, extract_config in stack.items():
            parallel.apply(
                self.extract_param_file,
                task_name=str(extract_id),
                args=(extract_id, extract_config),
                callback=append_file,
            )
        parallel.run(timeout=Settings().timeout)
        run_info(stack)
        parallel.clean()
        # self.assign_data(stack, preproc_stack)
        # accum info
        accum_data = self.create_accum_config(preproc_stack)
        # generate all time-integrated data of all param
        for name, parameter in accum_data.items():
            parallel.apply(
                self.time_integration,
                task_name=name,
                args=(parameter,),
                callback=append_grouped,
            )
        # Concat and export
        for file_id, dataarray_group in preproc_stack.items():
            if (
                "accum" not in dataarray_group["postproc"].keys()
                or dataarray_group["postproc"]["accum"] is None
            ):
                parallel.apply(
                    self.concat_export_dataarrays,
                    task_name=file_id,
                    args=(
                        dataarray_group["filename"],
                        dataarray_group,
                    ),
                    callback=append_grouped,
                )

        parallel.run((Settings().timeout))
        if success_resource["ok"] == len(preproc_stack):
            LOGGER.info(f"{success_resource['ok']} resources")
        else:
            LOGGER.error(f"{success_resource['ok']}/{len(preproc_stack)} resources")

    def time_sum(self, gridded_data: dict, step):
        """
        time-Normalize series data and cumulative sum
        Args
            gridded_data : list of data info
            step : expected step between 2 successives data
        Returns
            datarray of cumulative data along time step
        """
        # order and add intermedate time as needed
        gridded_data = sorted(gridded_data, key=lambda data: data.valid_time)
        da_step = xr_utils.compute_grib_step_size(gridded_data)
        gridded_data = xr.concat(gridded_data, dim="valid_time")
        gridded_data = xr_utils.stepping_data(gridded_data, da_step, step)
        # add first 0 data
        initial_date = gridded_data.valid_time.min() - np.timedelta64(step, "h")
        initial_data = gridded_data.sel({"valid_time": gridded_data.valid_time.min()})
        initial_data.data = np.zeros(initial_data.shape)
        initial_data = initial_data.assign_coords(valid_time=initial_date)
        initial_data = initial_data.expand_dims(dim={"valid_time": 1}, axis=0)
        initial_data["valid_time"] = initial_data.valid_time.assign_attrs(
            {"standard_name": "time", "long_name": "time"}
        )
        gridded_data = xr.concat(
            [initial_data, gridded_data], dim="valid_time", combine_attrs="no_conflicts"
        )
        # cumulative sum
        return gridded_data.cumsum(dim=["valid_time"])

    def time_integration(self, datas: dict) -> Tuple[str, xr.DataArray]:
        """
        parallel action to create time-integrated data of a "parameter"
            (param/grid/accum)

        Args:
        parameter : reference of the trio param/grid/accum
        needed_info : definition of which data are needed (grid and period)
        datas : list of all data to time-integrate (datarray:valid_time,lat,lon)

        Return:
        parameter : to be available in callback function
        gridded_data : dataarray(valid_time,lat,lon) of the time integrated data
        """
        # prepare and format data
        gridded_data = []
        for instant_data in datas["files"].values():
            # filter by time
            original_step = int(instant_data["data"].attrs["GRIB_lengthOfTimeRange"])
            limit_time = datas["endTime"].as_np_dt64 + np.timedelta64(
                original_step, "h"
            )
            timelimit_data = instant_data["data"].where(
                (instant_data["data"].valid_time <= limit_time),
                drop=True,
            )

            # No more data available
            if timelimit_data.count() == 0:
                continue
            if instant_data["preproc"]["source_grid"] != datas["grid"]:
                # adjust to same grid
                timelimit_data = xr_utils.interpolate_to_new_grid(
                    timelimit_data, datas["grid"]
                )
            timelimit_data = xr.where(
                timelimit_data is not None,
                timelimit_data,
                0,
                keep_attrs=True,
            )
            gridded_data.append(timelimit_data)
        gridded_data = self.time_sum(gridded_data, datas["step"])
        return [
            self.single_cumul(
                param_period["filename"],
                param_period["postproc"],
                gridded_data,
            )
            for param_period in datas["preprocs"]
        ]

    def single_cumul(
        self, filename: str, data_config: dict, time_integrated_data
    ) -> bool:
        """
        retrieve the cumul of a single param for all step given time-integrated data
        and an accum
        Args:
            filename: final filename for param data
            data_config: store accum,param,step,start,stop
            time_integrated_data: dataarray(time,lat,lon) with time integrated data
        Return
            whether backup succeed
        """

        def get_cumul(
            time_integrated_data: xr.DataArray,
            actual_date: np.datetime64,
            step: int,
            period: int,
        ) -> xr.DataArray:
            """
            From a time-integrated datarray, give the cumul
            from start time with period by step
            concept : compute integrate[start+period] - integrate[start]
            Args:
                time_integrated_data: dataarray(time,lat,lon) with time integrated data
                actual_date: start time for computation
                step: step of cumul
                period: duration of cumul
            Return:
                data_cumul: dataarray(time,lat,lon)
                    duration cumul for one time (at actual_date)
            """
            # redefine start as period begin
            # with the info of instant_data of actual_date
            # and therefore, the real start is before the actual_date
            start = actual_date + np.timedelta64(-step, "h")
            stop = start + np.timedelta64(period, "h")
            # filter the period
            data_period = time_integrated_data.sel(valid_time=slice(start, stop))
            # get available start and stop date
            start = data_period.valid_time.data.min()
            stop = data_period.valid_time.data.max()
            if start == stop:
                # only one data available :search for step next time
                # and divide by step as doing in earlier version
                data_period = (
                    time_integrated_data.sel(
                        valid_time=slice(start, stop + np.timedelta64(step, "h"))
                    )
                    / step
                )
                # get available start and stop date
                start = data_period.valid_time.data.min()
                stop = data_period.valid_time.data.max()
            data_cumul = data_period.sel(valid_time=stop) - data_period.sel(
                valid_time=start
            )
            # add valid_time dimension and attributes
            data_cumul = data_cumul.assign_coords(valid_time=actual_date)
            data_cumul = data_cumul.expand_dims(dim={"valid_time": 1}, axis=0)
            data_cumul["valid_time"] = data_cumul.valid_time.assign_attrs(
                {"standard_name": "time", "long_name": "time"}
            )
            dout = data_cumul
            if "GRIB_startStep" in dout.attrs:
                dout.attrs["GRIB_endStep"] = dout.attrs["GRIB_startStep"] + period
                dout.attrs["GRIB_stepRange"] = "{}-{}".format(
                    dout.attrs["GRIB_startStep"], dout.attrs["GRIB_endStep"]
                )
            data_cumul = dout

            return data_cumul

        accum = data_config["accum"]
        # find param filename
        param = data_config["param"]
        meteo, _, niveau = param.split("_")
        nomvariable = "__".join(["".join([meteo, str(accum)]), niveau])
        begin = data_config["start"]
        str_utc = begin.replace(tzinfo=timezone.utc).isoformat().split("+")[0]
        end = data_config["stop"]
        all_cumul = xr.concat(
            [
                get_cumul(
                    time_integrated_data,
                    np.datetime64(str_utc)
                    + np.timedelta64(hour, "h")
                    + np.timedelta64(0, "ns"),
                    data_config["step"],
                    accum,
                )
                for hour in range(
                    0,
                    (end - begin).total_hours + data_config["step"],
                    data_config["step"],
                )
            ],
            dim="valid_time",
            combine_attrs="no_conflicts",
        )
        # format attributes
        all_cumul = all_cumul.rename(nomvariable)
        all_cumul = all_cumul.assign_attrs({"accum_hour": accum})
        if accum == data_config["step"]:
            if "stepUnits" in all_cumul.attrs:
                del all_cumul.attrs["stepUnits"]
            if "history" in all_cumul.attrs:
                del all_cumul.attrs["history"]
        all_cumul.to_netcdf(filename)
        return Path(filename).is_file()


if __name__ == "__main__":
    # Arguments parsing
    args = CLI().parse_args()
    print(args)

    # Preprocessing
    preprocessor = DataPreprocessor(Settings().data_config_filename, args.rules)
    preprocessor.preprocess(nproc=args.nproc)
