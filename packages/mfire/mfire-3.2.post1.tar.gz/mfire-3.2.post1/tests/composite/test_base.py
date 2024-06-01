import pytest

import mfire.utils.mfxarray as xr
from tests.composite.factories import BaseCompositeFactory
from tests.functions_test import assert_identically_close


class TestBaseComposite:
    def test_hash(self, assert_equals_result):
        composite = BaseCompositeFactory()
        assert_equals_result(composite.hash)

    def test_compute(self):
        # Behavior by default: data are not kept
        data = xr.DataArray([1])
        compo = BaseCompositeFactory()
        compo._data = data
        assert_identically_close(compo.compute(), data)
        assert compo.compute() is None

        # When data are kept
        compo._data = data
        compo._keep_data = True
        assert_identically_close(compo.compute(), data)
        assert_identically_close(compo.compute(), data)

        # Test the kwargs _keep_data
        data = xr.DataArray([1])
        compo = BaseCompositeFactory()
        compo._data = data
        assert_identically_close(compo.compute(keep_data=True), data)
        assert_identically_close(compo.compute(), data)
        assert compo.compute() is None

    def test_reset(self, tmp_path_cwd):
        # Test deletion of self._data
        composite = BaseCompositeFactory()
        composite._data = xr.DataArray([1])
        composite.reset()

        assert composite.compute() is None

        # Test of deletion of cache
        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        open(path, mode="w").close()

        assert path.exists()
        composite.reset()
        assert not path.exists()

    def test_is_cached(self, tmp_path_cwd):
        composite = BaseCompositeFactory()
        assert composite.is_cached is False

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        open(path, mode="w").close()
        assert composite.is_cached is True

        composite.cached_attrs_factory = {}
        assert composite.is_cached is False

    def test_load_cache(self, tmp_path_cwd):
        composite = BaseCompositeFactory()
        with pytest.raises(
            FileNotFoundError,
            match="BaseCompositeFactory not cached, you must compute it before.",
        ):
            composite.load_cache()

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        open(path, mode="w").close()

        assert composite.load_cache() is False
        assert composite._data is None

        data = xr.DataArray([1])
        data.to_netcdf(path)
        assert composite.load_cache() is True
        assert_identically_close(composite._data, data)
