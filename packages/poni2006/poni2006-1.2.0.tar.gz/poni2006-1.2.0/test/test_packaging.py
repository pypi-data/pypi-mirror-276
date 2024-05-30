# {# pkglts, glabpkg_dev
import poni2006


def test_package_exists():
    assert poni2006.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert poni2006.pth_clean.exists()
    try:
        assert poni2006.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
