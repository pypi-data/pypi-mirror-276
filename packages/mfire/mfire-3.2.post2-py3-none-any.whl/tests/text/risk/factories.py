import copy
import json
import numpy as np
from pathlib import Path
from pydantic import BaseModel
from typing import Any, ClassVar, Dict, Optional, Union

from mfire.composite.base import BaseComposite
from mfire.composite.operator import ComparisonOperator
from mfire.localisation.risk_localisation import RiskLocalisation
from mfire.text.risk.builder import RiskBuilder
from mfire.text.risk.reducer import RiskReducer
from mfire.text.risk.rep_value import (
    AccumulationRepValueReducer,
    AltitudeRepValueBuilder,
    AltitudeRepValueReducer,
    FFRafRepValueBuilder,
    FFRafRepValueReducer,
    FFRepValueBuilder,
    FFRepValueReducer,
    PrecipitationRepValueBuilder,
    PrecipitationRepValueReducer,
    RainRepValueBuilder,
    RainRepValueReducer,
    RepValueBuilder,
    RepValueReducer,
    SnowRepValueBuilder,
    SnowRepValueReducer,
    TemperatureRepValueBuilder,
    TemperatureRepValueReducer,
)
from tests.composite.factories import RiskComponentCompositeFactory
from tests.localisation.factories import RiskLocalisationFactory
from tests.text.base.factories import BaseBuilderFactory


class RiskReducerFactory(RiskReducer):
    geo_id: str = "geo_id"
    composite: Optional[BaseComposite] = RiskComponentCompositeFactory()
    localisation: Optional[RiskLocalisation] = RiskLocalisationFactory()

    compute_factory: Optional[dict] = None
    is_multizone_factory: Optional[bool] = None
    operator_dict_factory: Optional[dict] = None
    final_risk_max_factory: Optional[int] = None

    def _compute(self) -> dict:
        if self.compute_factory is None:
            return super()._compute()
        return self.compute_factory

    @property
    def is_multizone(self) -> bool:
        if self.is_multizone_factory is None:
            return super().is_multizone
        return self.is_multizone_factory

    @property
    def operator_dict(self) -> Dict:
        if self.operator_dict_factory is None:
            return super().operator_dict
        return self.operator_dict_factory

    @property
    def final_risk_max(self) -> int:
        if self.final_risk_max_factory is None:
            return super().final_risk_max
        return self.final_risk_max_factory


class RiskBuilderFactory(RiskBuilder, BaseBuilderFactory):
    geo_id: str = "geo_id"
    composite: BaseComposite = RiskComponentCompositeFactory()
    reducer_class: type = RiskReducerFactory

    is_multizone_factory: Optional[bool] = None

    @property
    def is_multizone(self) -> bool:
        if self.is_multizone_factory is None:
            return super().is_multizone
        return self.is_multizone_factory

    @property
    def template_name(self) -> Union[str, np.ndarray]:
        if self.template_name_factory is None:
            return super().template_name
        return self.template_name_factory

    @property
    def template_key(self) -> Union[str, np.ndarray]:
        if self.template_key_factory is None:
            return super().template_key
        return self.template_key_factory


class RepValueReducerFactory(RepValueReducer):
    test_var_name: ClassVar[str] = "TEST__VARNAME"

    @property
    def phenomenon(self) -> str:
        return "phen"

    def __init__(
        self, data: Optional[dict] = None, var_name: Optional[str] = None, **kwargs: Any
    ):
        if data is None:
            data = {}
        if var_name is None and self.test_var_name is not None:
            var_name = self.test_var_name
        if var_name is not None:
            data |= {"var_name": var_name}
        super().__init__(data=data, **kwargs)


class AccumulationRepValueReducerFactory(
    AccumulationRepValueReducer, RepValueReducerFactory
):
    test_var_name: ClassVar[str] = "TEST1__VARNAME"
    bounds: list = []
    last_bound_size: int = 10


class AccumulationRepValueBuilderFactory(RepValueBuilder):
    reducer_class: type = AccumulationRepValueReducerFactory


class RepValueBuilderFactory(RepValueBuilder):
    reducer_class: type = RepValueReducerFactory

    def __init__(
        self, data: Optional[dict] = None, var_name: Optional[str] = None, **kwargs: Any
    ) -> None:
        if data is None:
            data = {}

        super().__init__(data=data, **kwargs)

        if var_name is None and self.reducer_class.test_var_name is not None:
            var_name = self.reducer_class.test_var_name
        if var_name is not None:
            self.data |= {"var_name": var_name}


class FFRepValueReducerFactory(FFRepValueReducer, RepValueReducerFactory):
    test_var_name: ClassVar[str] = "FF__HAUTEUR"


class FFRepValueBuilderFactory(FFRepValueBuilder, RepValueBuilderFactory):
    reducer_class: type = FFRepValueReducerFactory


class TemperatureRepValueReducerFactory(
    TemperatureRepValueReducer, RepValueReducerFactory
):
    test_var_name: ClassVar[str] = "T__HAUTEUR2"


class TemperatureRepValueBuilderFactory(TemperatureRepValueBuilder):
    reducer_class: type = TemperatureRepValueReducerFactory


class FFRafRepValueReducerFactory(FFRafRepValueReducer, RepValueReducerFactory):
    test_var_name: ClassVar[str] = "RAF__HAUTEUR10"


class FFRafRepValueBuilderFactory(FFRafRepValueBuilder):
    reducer_class: type = FFRafRepValueReducerFactory


class SnowRepValueReducerFactory(SnowRepValueReducer, RepValueReducerFactory):
    test_var_name: ClassVar[str] = "NEIPOT1__SOL"


class SnowRepValueBuilderFactory(SnowRepValueBuilder):
    reducer_class: type = SnowRepValueReducerFactory


class PrecipitationRepValueReducerFactory(
    PrecipitationRepValueReducer, RepValueReducerFactory
):
    test_var_name: ClassVar[str] = "PRECIP3__SOL"


class PrecipitationRepValueBuilderFactory(PrecipitationRepValueBuilder):
    reducer_class: type = PrecipitationRepValueReducerFactory


class RainRepValueReducerFactory(RainRepValueReducer, RepValueReducerFactory):
    test_var_name: ClassVar[str] = "EAU24__SOL"


class RainRepValueBuilderFactory(RainRepValueBuilder):
    reducer_class: type = RainRepValueReducerFactory


class AltitudeRepValueReducerFactory(AltitudeRepValueReducer):
    pass


class AltitudeRepValueBuilderFactory(AltitudeRepValueBuilder):
    reducer_class: type = AltitudeRepValueReducerFactory


class DataFactory(BaseModel):
    units: Optional[str] = "cm"
    operator: Optional[ComparisonOperator] = ComparisonOperator.SUPEGAL
    value: Optional[float] = None
    next_critical: Optional[float] = None
    threshold: Optional[float] = None
    occurrence: Optional[bool] = False


def data_factory(**kwargs) -> dict:
    return DataFactory(**kwargs).dict()


class RepValueTestFactory:
    """Create test data of representative values."""

    DATA_NO_VALUE: dict = data_factory()
    DATA_REP_PLAIN_ONLY_10: dict = data_factory(value=10.0)
    DATA_REP_PLAIN_ONLY_15: dict = data_factory(value=15.0)
    DATA_ACC_REP_LOCAL_ONLY_2: dict = data_factory(
        value=1e-7, threshold=2.0, occurrence=True
    )
    DATA_ACC_REP_LOCAL_ONLY_10: dict = data_factory(
        value=1e-7, threshold=10.0, occurrence=True
    )
    # rep plain < rep local
    DATA_REP_PLAIN_AND_LOCAL_10_15: dict = data_factory(
        value=10.0, threshold=15.0, occurrence=True
    )
    DATA_REP_PLAIN_AND_LOCAL_15_20: dict = data_factory(
        value=15.0, threshold=20.0, occurrence=True
    )
    # rep plain > rep local
    DATA_REP_PLAIN_AND_LOCAL_20_10: dict = data_factory(
        value=20.0,
        threshold=10.0,
        occurrence=True,
        operator=ComparisonOperator.INFEGAL,
    )
    DATA_REP_PLAIN_AND_LOCAL_40_30: dict = data_factory(
        value=40.0,
        threshold=30.0,
        occurrence=True,
        operator=ComparisonOperator.SUPEGAL,
    )
    # rep plain = rep local
    DATA_REP_PLAIN_AND_LOCAL_12_12: dict = data_factory(
        value=12.0, threshold=12.0, occurrence=True
    )
    DATA_REP_PLAIN_AND_LOCAL_20_20: dict = data_factory(
        value=20.0, threshold=20.0, occurrence=True
    )

    def __init__(self):
        self.data: list[dict] = []

    def _add_case_data(self, case_data: dict):
        self.data.append(case_data)

    def _create_mixed_case(self, plain_data: dict, mountain_data: dict):
        self._add_case_data(
            {
                "plain": plain_data,
                "mountain": mountain_data,
            }
        )

    def _create_simple_cases(self, data_name) -> None:
        for data in [
            self.DATA_NO_VALUE,
            self.DATA_REP_PLAIN_ONLY_10,
            self.DATA_ACC_REP_LOCAL_ONLY_2,
            self.DATA_REP_PLAIN_AND_LOCAL_10_15,
            self.DATA_REP_PLAIN_AND_LOCAL_20_10,
            self.DATA_REP_PLAIN_AND_LOCAL_12_12,
        ]:
            self._add_case_data({data_name: data})

    def _create_mixed_cases(self):
        data_1: list[dict] = [
            self.DATA_NO_VALUE,
            self.DATA_REP_PLAIN_ONLY_10,
            self.DATA_ACC_REP_LOCAL_ONLY_2,
            self.DATA_REP_PLAIN_AND_LOCAL_10_15,
        ]

        data_2: list[dict] = [
            self.DATA_NO_VALUE,
            self.DATA_REP_PLAIN_ONLY_15,
            self.DATA_ACC_REP_LOCAL_ONLY_10,
            self.DATA_REP_PLAIN_AND_LOCAL_15_20,
        ]

        for plain_data in data_1:
            for mountain_data in data_2:
                self._create_mixed_case(plain_data, mountain_data)

        # rep plain > rep mountain
        self._create_mixed_case(
            self.DATA_REP_PLAIN_ONLY_15, self.DATA_REP_PLAIN_ONLY_10
        )

        # rep plain = rep mountain, no rep local
        self._create_mixed_case(
            self.DATA_REP_PLAIN_ONLY_10, self.DATA_REP_PLAIN_ONLY_10
        )

        # no rep plain, local plain = local mountain (only for accumulated variable)
        self._create_mixed_case(
            self.DATA_ACC_REP_LOCAL_ONLY_10, self.DATA_ACC_REP_LOCAL_ONLY_10
        )

        # rep plain (without local rep) = rep mountain < rep local mountain
        self._create_mixed_case(
            self.DATA_REP_PLAIN_ONLY_10, self.DATA_REP_PLAIN_AND_LOCAL_10_15
        )

    def run(self, file_path: Optional[Path | str] = None) -> list[dict]:
        # Generate empty case
        self._add_case_data({})

        # Generate plain cases
        self._create_simple_cases("plain")

        # Generate mountain cases
        self._create_simple_cases("mountain")

        # Generate plain/mountain mixed-cases
        self._create_mixed_cases()

        if file_path is not None:
            with open(Path(file_path), "w") as f:
                json.dump(self.data, f, indent=4)

        return self.data


def create_rep_value_test_data_altitude(
    test_data: list, file_path: Optional[Path | str] = None
) -> list[dict]:
    """Create test data of representative values with altitude."""
    test_data_altitude: list = copy.deepcopy(test_data)

    for i, data in enumerate(test_data_altitude):
        test_data_altitude[i]["mountain_altitude"] = 1500

    if file_path is not None:
        with open("data_altitude.json", "w") as f:
            json.dump(test_data_altitude, f, indent=4)

    return test_data_altitude
