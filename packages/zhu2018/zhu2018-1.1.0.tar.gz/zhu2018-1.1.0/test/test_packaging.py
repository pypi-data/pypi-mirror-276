# {# pkglts, glabpkg_dev
import zhu2018


def test_package_exists():
    assert zhu2018.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert zhu2018.pth_clean.exists()
    try:
        assert zhu2018.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
