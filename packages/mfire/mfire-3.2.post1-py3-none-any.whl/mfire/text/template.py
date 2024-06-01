"""
@package text.template

Module retrieving text templates
"""

# Standard packages
from __future__ import annotations

import json
from configparser import ConfigParser
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Hashable, Mapping, Optional, Sequence, Tuple, Union

import numpy as np

# Third parties packages
import pandas as pd
from dtaidistance import dtw

from mfire.settings import get_logger
from mfire.utils import FormatDict

# Logging
LOGGER = get_logger(name="text.template.mod", bind="text.template")


def read_file(
    filename: Path,
    col: Optional[str] = "template",
    weights: Optional[np.ndarray] = None,
    **kwargs,
) -> TemplateRetriever:
    """read_file : reads a templates file and returns the proper corresponding
    TemplateRetriever object.

    Args:
        filename (Path): Name of the file containing the templates.
        col (Optional[str]): templates column name in a csv file.
        weights (Optional[np.ndarray]): weights if centroids.
        **kwargs (Optional[dict]) : keyword arguments of the file reader used :
            - json : json.load()
            - ini  : ConfigParser().read()
            - csv  : pandas.read_csv()

    Returns:
        TemplateRetriever: TemplateRetriever object.
    """
    filename = Path(filename)
    if filename.suffix == ".json":
        return JsonTemplateRetriever.read_file(filename, **kwargs)
    if filename.suffix == ".ini":
        return IniTemplateRetriever.read_file(filename, **kwargs)
    if filename.suffix == ".csv":
        if weights is not None:
            return CentroidTemplateRetriever.read_file(
                filename, col=col, weights=weights, **kwargs
            )
        index_col = kwargs.pop("index_col", 0)
        tpl_rtr = CsvTemplateRetriever.read_file(
            filename, col=col, index_col=index_col, **kwargs
        )
        if "weights" in tpl_rtr.table.index:
            return CentroidTemplateRetriever.read_file(
                filename, col=col, index_col=index_col, **kwargs
            )
        return tpl_rtr

    return TemplateRetriever.read_file(filename, **kwargs)


class Template(str):
    """Template: class extending str type for formating using a custom FormatDict
    (in order to avoid issues when keys are missing).
    >>> s = Template("Ma {b} connait des blagues de {a}, et {c} ?")
    >>> s.format(a="toto", b="tata")
    "Ma tata connait des blagues de toto, et {c} ?"
    >>> s = Template("Bonjour M. {a_prenom} {a_nom}.")
    >>> s.format(a={"nom": "dupont", "prenom": "toto"}, b="tata")
    "Bonjour M. toto dupont."
    """

    def format(self, **kwargs) -> Template:
        try:
            flat_kwargs = pd.json_normalize(kwargs, sep="_").to_dict(orient="records")[
                0
            ]
        except IndexError:
            flat_kwargs = kwargs

        return self.format_map(FormatDict(flat_kwargs))


class TemplateRetriever:
    """TemplateRetriever : Abstract class for defining a TemplateRetriever.
    It is done to retrieve a string template identified by a key from a file.
    """

    def __init__(self, table: Mapping[Hashable, Union[str, Sequence[str]]]):
        """__init__: Initialization method

        Args:
            table (Mapping[Hashable, Union[str, Sequence[str]]]): Correspondance table
                between Hashable keys and strings (or list of strings).
        """
        self.table = table

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.table == other.table

    def __repr__(self) -> str:
        return f"{self.__class__}\n{self.table}"

    @classmethod
    def read_file(cls, filename: Path, **kwargs) -> TemplateRetriever:
        """read_file : class method for instantiating an TemplateRetriever
        out of a file.

        Args:
            filename (Path): File's name

        Returns:
            TemplateRetriever: New cls object
        """
        table = {"filename": Path(filename)}
        table.update(kwargs)
        return cls(table)

    def get(
        self, key: Union[Hashable, Sequence[Hashable]], default: Optional[str] = None
    ) -> str:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[Hashable, Sequence[Hashable]]): Key for retrieving our
                template. If the key is a sequence (list, tuple) of keys, then
                we find the template by searching in subdirectories.
            default (str, optional): Default value to return if the given
                key is not in self.table. Defaults to None.

        Returns:
            str: The wanted template
        """
        if key in self.table:
            tpl = self.table[key]
            if isinstance(tpl, str):
                return Template(tpl)
            return tpl
        try:
            tmp_tpl = self.table
            for element in key:
                if element in tmp_tpl:
                    tmp_tpl = tmp_tpl[element]
                else:
                    return Template(default)
            if isinstance(tmp_tpl, str):
                return Template(tmp_tpl)
            return tmp_tpl
        except Exception:
            LOGGER.error(
                f"Failed to get template from {self})",
                key=key,
                default=default,
                exc_info=True,
            )
            return Template("Echec dans la récupération du template (error TPL-001).")


class JsonTemplateRetriever(TemplateRetriever):
    """JsonTemplateRetriever : TemplateRetriever from json files.

    Currently used by:
        - mfire.text.comment.comment_builder
    """

    @classmethod
    def read_file(cls, filename: Path, **kwargs) -> JsonTemplateRetriever:
        """read_file : class method for instantiating an JsonTemplateRetriever
        out of a file.

        Args:
            filename (Path): File's name
            **kwargs (Optional[dict]) : keyword arguments of the file reader used
                (json.load)

        Returns:
            JsonTemplateRetriever: New cls object
        """
        try:
            with open(filename, "r") as json_file:
                return cls(json.load(json_file, **kwargs))
        except Exception:
            LOGGER.error(f"Failed to read json template file {filename}", exc_info=True)
        return cls({"filename": Path(filename)})

    def get(
        self,
        key: Union[str, Sequence[str]],
        default: Optional[str] = None,
        pop_method: Optional[Union[str, Callable[Sequence, str]]] = "first",
    ) -> str:
        """get : method used to retrieve a template identified by a key.
        If the element retrieved from the table is not a str, we must pop
        a str out of this element according to the given 'pop_method'.

        Args:
            key (Union[str, Sequence[str]]): Key for retrieving our template.
                If the key is a sequence (list, tuple) of keys, then
                we find the template by searching in subdirectories.
            default (str, optional): Default value to return if the given key is not
                in self.table. Defaults to None.
            pop_method (Union[str, Callable[Sequence, str]], optional): Method to use
                if the element retrieved with the key is not a string. It can be a
                string among {"first", "last", "random"}, or it can be a function
                which take the element as input and outputs a str.
                Defaults to "random".

        Returns:
            str: The wanted template
        """
        template = super().get(key, default=default)
        if isinstance(template, str):
            return Template(template)

        pop_methods = {
            "first": lambda x: x[0],
            "last": lambda x: x[-1],
            "random": np.random.choice,
        }
        try:
            return Template(pop_methods.get(pop_method, pop_method)(template))
        except Exception:
            LOGGER.error(
                f"Failed to pop template using {pop_method} ({self.__class__})",
                template=template,
                key=key,
                default=default,
                pop_method=pop_method,
                exc_info=True,
            )
            if default is None:
                return Template(
                    "Echec dans la récupération du template (error TPL-002)."
                )
            return Template(default)


class IniTemplateRetriever(TemplateRetriever):
    """JsonTemplateRetriever : TemplateRetriever from ini files.

    Currently unused.
    """

    @classmethod
    def read_file(cls, filename: Path, **kwargs) -> IniTemplateRetriever:
        """read_file : class method for instantiating an IniTemplateRetriever
        out of a file.

        Args:
            filename (Path): File's name
            **kwargs (Optional[dict]) : keyword arguments of the file reader used
                (ConfigParser().read())

        Returns:
            IniTemplateRetriever: New cls object
        """
        try:
            config = ConfigParser()
            config.read(filename, **kwargs)
            return cls(config)
        except Exception:
            LOGGER.error(
                f"Failed to read ini template file {filename}",
                filename=filename,
                exc_info=True,
            )
            return cls({"filename": Path(filename)})

    def get(
        self,
        key: Union[str, Tuple[str, str]],
        default: Optional[str] = None,
    ) -> str:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[str, tuple[str, str]]): Key for retrieving our
                template. If the key is a string, we search directly in
                the DEFAULT section. Else if it is a tuple of strings, then we
                find the tuple using the usual configparser.get()
            default (str, optional): Default value to return if the given
                key is not in self.table. Defaults to None.

        Returns:
            str: The wanted template
        """
        correct_key = deepcopy(key)
        if isinstance(key, str):
            correct_key = ("DEFAULT", key)
        try:
            return Template(self.table.get(*correct_key))
        except Exception:
            LOGGER.error(
                f"Failed to get template from {self}. "
                "Invalid key given. Default taken.",
                key=key,
                default=default,
                exc_info=True,
            )
            return Template(default)


class CsvTemplateRetriever(TemplateRetriever):
    """CsvTemplateRetriever : TemplateRetriever for csv files.

    Currently unused.
    """

    def __init__(
        self,
        table: Mapping[Hashable, Union[str, Sequence[str]]],
        col: Optional[str] = "template",
    ):
        """__init__: Initialization method

        Args:
            table (Mapping[Hashable, Union[str, Sequence[str]]]): Correspondance table
                between Hashable keys and strings (or list of strings).
            col (Optional[str]): Name of the column containing template.
        """
        super().__init__(table=table)
        self.col = col
        if col not in self.table.columns:
            self.col = self.table.columns[0]
            if len(self.table.columns) != 1:
                LOGGER.warning(
                    "Wrong column name given for template retrieving, "
                    "default column taken",
                    given_col=col,
                    selected_col=self.col,
                )
        self.table = self.table[self.col]

    @classmethod
    def read_file(cls, filename: Path, **kwargs) -> CsvTemplateRetriever:
        """read_file : class method for instantiating an CsvTemplateRetriever
        out of a file.

        Args:
            filename (Path): File's name
            **kwargs (Optional[dict]) : keyword arguments of the file reader used
                (pandas.read_csv)

        Returns:
            CsvTemplateRetriever: New cls object
        """
        try:
            col = kwargs.pop("col", "template")
            return cls(pd.read_csv(filename, **kwargs), col=col)
        except Exception:
            LOGGER.error(
                f"Failed to read csv template file {filename}",
                filename=filename,
                exc_info=True,
            )
            return cls({"filename": Path(filename)})

    def get(
        self,
        key: Union[Hashable, Tuple],
        default: Optional[str] = None,
    ) -> str:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[Hashable, Tuple]): Key for retrieving our
                template. If the key is a string, we search directly in
                the DEFAULT section. Else if it is a tuple of strings, then we
                find the tuple using the usual configparser.get()
            default (str, optional): Default value to return if the given
                key is not in self.table. Defaults to None.

        Returns:
            str: The wanted template
        """
        try:
            result = self.table.loc[key]
            if isinstance(result, (pd.Series, pd.DataFrame)):
                raise KeyError(key)
            return Template(result)
        except KeyError:
            return Template(default)
        except Exception:
            LOGGER.error(
                f"Failed to get template from {self}. "
                "Invalid key given. Default taken.",
                key=key,
                default=default,
                exc_info=True,
            )
            return Template(default)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.table.equals(other.table)


class CentroidTemplateRetriever(CsvTemplateRetriever):
    """CentroidTemplateRetriever : TemplateRetriever for csv-centroids files.

    Currently used by:
        - mfire.utils.date : for describinng short periods
    """

    def __init__(
        self,
        table: Mapping[Hashable, Union[str, Sequence[str]]],
        col: Optional[str] = "template",
        weights: Optional[np.ndarray] = None,
    ):
        """__init__: Initialization method

        Args:
            table (Mapping[Hashable, Union[str, Sequence[str]]]): Correspondance table
                between Hashable keys and strings (or list of strings).
            col (Optional[str]): Name of the column containing template
            weights (Optional[list]): Weights to apply. Defaults to None. If None,
                all columns will be given a weight of 1.
        """
        super().__init__(table=table, col=col)
        self.weights = np.array(weights)
        if weights is None:
            self.weights = np.ones(len(self.table.index.names))

    @classmethod
    def read_file(cls, filename: Path, **kwargs) -> CentroidTemplateRetriever:
        """read_file : class method for instantiating an CentroidTemplateRetriever
        out of a file.

        Args:
            filename (Path): File's name

        Returns:
            CentroidTemplateRetriever: New cls object
            **kwargs (Optional[dict]) : keyword arguments of the file reader used
                (pandas.read_csv)
        """
        try:
            weights = kwargs.pop("weights", None)
            col = kwargs.pop("col", "template")
            index_col = kwargs.pop("index_col", 0)
            df = pd.read_csv(filename, index_col=index_col, **kwargs)
            if "weights" in df.index:
                weights = df.loc["weights"].dropna().values
                df = df.drop("weights").set_index(list(df.columns)[: len(weights)])
            return cls(df, col=col, weights=weights)
        except Exception:
            LOGGER.error(
                f"Failed to read csv template file {filename}",
                filename=filename,
                exc_info=True,
            )
            return cls({"filename": Path(filename)})

    def get(self, key: np.ndarray) -> str:
        """get: method used to retrieve a specific template identified by a key.
        It returns the template associated to the nearest centroid of the given key.

        Args:
            key (np.ndarray): Key for retrieving our template.

        Returns:
            str: The wanted template
        """
        centroids = self.table.index.to_frame().values
        templates = self.table.values
        dist = np.sum(np.square(self.weights * (centroids - np.array(key))), axis=1)
        return Template(templates[dist.argmin()])

    def get_by_dtw(
        self,
        key: np.ndarray,
        pop_method: Optional[Union[str, Callable[Sequence, str]]] = "first",
    ) -> str:
        """get: method used to retrieve a specific template identified by a key.
        It returns the template associated to the nearest centroid
        of the given key with dtw method.

        Args:
            key (np.ndarray): Key for retrieving our template.
            pop_method (Union[str, Callable[Sequence, str]], optional): Method to use
                if the element retrieved with the key is not a string. It can be a
                string among {"first", "last", "random"}, or it can be a function
                which take the element as input and outputs a str.
                Defaults to "first".

        Returns:
            dict: dict containing the min distance, the path, the template, the centroid
        """
        # il faut gérer le cas ou on a plusieurs distances mini egales

        pop_methods = {
            "first": lambda x: x[0],
            "last": lambda x: x[-1],
            "random": np.random.choice,
        }
        centroids = self.table.index.to_frame().values
        datas = list()
        for centroid in centroids:
            data = [x for x in centroid if not pd.isnull(x)]
            datas.append(data)
        templates = self.table.values

        distance_dict = dict()
        for index, centroid in enumerate(datas):
            distance_dict[tuple(centroid)] = {
                "distance": dtw.distance_fast(
                    np.array(key, dtype=np.double), np.array(centroid, dtype=np.double)
                ),
                "path": dtw.warping_path_fast(
                    np.array(key, dtype=np.double), np.array(centroid, dtype=np.double)
                ),
                "template": Template(
                    pop_methods.get(pop_method, pop_method)(templates[index].split("|"))
                ),
            }

        d_min = {"distance": 9999, "path": None, "template": ""}

        for centroid, result in distance_dict.items():
            if result["distance"] > d_min["distance"]:
                pass
            else:
                d_min = result
                d_min["centroid"] = centroid
                d_min["type"] = "general"

        return d_min

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and np.all(self.weights == other.weights)

    def __repr__(self) -> str:
        return (
            f"{self.__class__}\n{self.table[self.col]}\nweights = {list(self.weights)}"
        )
