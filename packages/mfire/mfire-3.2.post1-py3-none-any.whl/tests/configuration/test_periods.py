from typing import Iterable

import pytest
from pydantic import ValidationError

from mfire.composite.period import Period, PeriodCollection
from mfire.configuration.periods import (
    PeriodCollectionConfig,
    PeriodElementConfig,
    PeriodMultipleElementConfig,
    PeriodSingleElementConfig,
)
from mfire.utils.date import Datetime


class TestPeriodElementConfig:
    starts = [
        {"Start": 6},
        {"start": 6},
        {"deltaStart": 1},
        {"absoluStart": "20210101T000000"},
    ]
    stops = [
        {"stop": 12},
        {"deltaStop": 24},
        {"absoluStop": "2021-01-02T00:00:00"},
        {"Stop": 12},
    ]

    @pytest.mark.parametrize("start", starts)
    @pytest.mark.parametrize("stop", stops)
    def test_init(self, start, stop):
        assert PeriodElementConfig(**start, **stop)
        dico = {"productionTime_until": 9}
        dico.update(**start, **stop)
        assert PeriodElementConfig(**dico)

    def test_init_fail(self):
        dico = {"productionTime_until": 9}
        with pytest.raises(ValidationError):
            PeriodElementConfig(**dico)

        dico.update(**self.starts[0], **self.stops[0])
        with pytest.raises(ValidationError):
            PeriodElementConfig(**dico, **self.starts[1])
        with pytest.raises(ValidationError):
            PeriodElementConfig(**dico, **self.stops[1])

    def test_get_bound_datetime(self):
        element = PeriodElementConfig(deltaStart=1, stop=20, productionTime_until=16)

        prod_df = Datetime(2021, 1, 1, 15)
        # Si production_time est avant pT_until,
        # on devrait produire pour la même journée
        assert element.get_bound_datetime(prod_df, "start") == Datetime(2021, 1, 1, 16)
        assert element.get_bound_datetime(prod_df, "stop") == Datetime(2021, 1, 1, 20)

        prod_dt = Datetime(2021, 1, 1, 16)
        # Si production_time == pT_until, on devrait produit pour le lendemain
        assert element.get_bound_datetime(prod_dt, "start") == Datetime(2021, 1, 1, 17)
        assert element.get_bound_datetime(prod_dt, "stop") == Datetime(2021, 1, 2, 20)

        # Si le production_time  > pT_until, on devrait produire jusqu'au lendemain
        prod_dt = Datetime(2021, 1, 1, 17)
        assert element.get_bound_datetime(prod_dt, "start") == Datetime(2021, 1, 1, 18)
        assert element.get_bound_datetime(prod_dt, "stop") == Datetime(2021, 1, 2, 20)

        element = PeriodElementConfig(
            start=6, absoluStop=Datetime(2021, 1, 3, 12), productionTime_until=16
        )
        assert element.get_bound_datetime(prod_dt, "start") == Datetime(2021, 1, 2, 6)
        assert element.get_bound_datetime(prod_dt, "stop") == Datetime(2021, 1, 3, 12)


class TestPeriodSingleElementConfig:
    base = {"id": "my_id", "name": "my_name"}
    dico = {"deltaStart": 1, "stop": 32, "productionTime_until": 16}

    def test_get_processed_period(self):
        period = PeriodSingleElementConfig(**self.base, **self.dico)

        prod_dt1 = Datetime(2021, 1, 1, 15)
        processed_period1 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 16),
            stop=Datetime(2021, 1, 2, 8),
        )
        assert period.get_processed_period(prod_dt1) == processed_period1

        prod_dt2 = Datetime(2021, 1, 1, 16)
        processed_period1 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 17),
            stop=Datetime(2021, 1, 3, 8),
        )
        assert period.get_processed_period(prod_dt2) == processed_period1

        prod_dt3 = Datetime(2021, 1, 1, 17)
        processed_period2 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 18),
            stop=Datetime(2021, 1, 3, 8),
        )
        assert period.get_processed_period(prod_dt3) == processed_period2


class TestPeriodMultipleElementConfig:
    base = {"id": "my_id", "name": "my_name"}
    dico = {
        "periodElements": [
            {
                "start": 6,
                "stop": 18,
                "productionTime_until": 6,
            },
            {
                "deltaStart": 1,
                "deltaStop": 12,
                "productionTime_until": 12,
            },
            {
                "absoluStart": "2021-01-01T18:00:00",
                "absoluStop": "20210102T060000",
                "productionTime_until": 18,
            },
        ]
    }

    def test_get_processed_period(self):
        period = PeriodMultipleElementConfig(**self.base, **self.dico)

        # production is before productionTime_until (6),
        # the period should use the first periodElement and be on the same day
        prod_dt0 = Datetime(2021, 1, 1, 5)
        processed_period0 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 6),
            stop=Datetime(2021, 1, 1, 18),
        )
        assert period.get_processed_period(prod_dt0) == processed_period0

        # production == productionTime_until (6),
        # the period should use the second periodElement
        prod_dt1 = Datetime(2021, 1, 1, 6)
        processed_period1 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 7),
            stop=Datetime(2021, 1, 1, 18),
        )
        assert period.get_processed_period(prod_dt1) == processed_period1

        # production is after productionTime_until (6) but before (12),
        # the period should use the second periodElement
        prod_dt2 = Datetime(2021, 1, 1, 7)
        processed_period2 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 8),
            stop=Datetime(2021, 1, 1, 19),
        )
        assert period.get_processed_period(prod_dt2) == processed_period2

        # production == productionTime_until (12), the Period should switch from the
        # second to the third periodElement
        prod_dt3 = Datetime(2021, 1, 1, 12)
        processed_period3 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 18),
            stop=Datetime(2021, 1, 2, 6),
        )
        assert period.get_processed_period(prod_dt3) == processed_period3

        # production is after productionTime_until(13), the Period should use the third
        # periodElement
        prod_dt4 = Datetime(2021, 1, 1, 13)
        processed_period4 = Period(
            **self.base,
            start=Datetime(2021, 1, 1, 18),
            stop=Datetime(2021, 1, 2, 6),
        )
        assert period.get_processed_period(prod_dt4) == processed_period4

        # production == productionTime_until, we've gone full circle and use the first
        # periodElement again but with values for the next day
        prod_dt5 = Datetime(2021, 1, 1, 18)
        processed_period5 = Period(
            **self.base,
            start=Datetime(2021, 1, 2, 6),
            stop=Datetime(2021, 1, 2, 18),
        )
        assert period.get_processed_period(prod_dt5) == processed_period5

        # production is still after productionTime_until(18) and before (6),
        # we still use the first periodElement
        prod_df6 = Datetime(2021, 1, 1, 19)
        assert period.get_processed_period(prod_df6) == processed_period5


class TestPeriodCollectionConfig:
    dico_single = {"deltaStart": 1, "stop": 32, "productionTime_until": 16}
    dico_multiple = {
        "periodElements": [
            {
                "start": 6,
                "stop": 18,
                "productionTime_until": 6,
            },
            {
                "deltaStart": 1,
                "deltaStop": 12,
                "productionTime_until": 12,
            },
            {
                "absoluStart": "2021-01-01T18:00:00",
                "absoluStop": "20210102T060000",
                "productionTime_until": 18,
            },
        ]
    }

    def test_get_processed_periods(self):
        dico_single_full = dict(id="dico1", **self.dico_single)
        dico_multiple_full = dict(id="dico2", **self.dico_multiple)
        perco = PeriodCollectionConfig(periods=[dico_single_full, dico_multiple_full])
        assert isinstance(perco.periods[0], PeriodSingleElementConfig)
        assert isinstance(perco.periods[1], PeriodMultipleElementConfig)
        assert len(perco) == len(perco.periods) == 2
        assert isinstance(list(iter(perco)), Iterable)

        assert perco["dico1"] == perco.get("dico1") == perco.periods[0]
        assert perco["dico2"] == perco.get("dico2") == perco.periods[1]
        assert perco.get("toto") is None
        assert perco.get("toto", "tata") == "tata"

        with pytest.raises(KeyError):
            _ = perco["toto"]

        processed_periods = perco.get_processed_periods(Datetime(2021, 1, 1, 6))
        assert isinstance(processed_periods, PeriodCollection)
