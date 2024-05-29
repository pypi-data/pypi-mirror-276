# {# pkglts, glabpkg_dev
import greer2018


def test_package_exists():
    assert greer2018.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert greer2018.pth_clean.exists()
    try:
        assert greer2018.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
