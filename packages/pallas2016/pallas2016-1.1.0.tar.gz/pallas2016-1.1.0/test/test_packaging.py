# {# pkglts, glabpkg_dev
import pallas2016


def test_package_exists():
    assert pallas2016.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert pallas2016.pth_clean.exists()
    try:
        assert pallas2016.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
