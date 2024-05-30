# {# pkglts, glabpkg_dev
import yin2009


def test_package_exists():
    assert yin2009.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert yin2009.pth_clean.exists()
    try:
        assert yin2009.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
