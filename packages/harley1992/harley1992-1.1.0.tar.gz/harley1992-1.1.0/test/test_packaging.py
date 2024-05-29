# {# pkglts, glabpkg_dev
import harley1992


def test_package_exists():
    assert harley1992.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert harley1992.pth_clean.exists()
    try:
        assert harley1992.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
