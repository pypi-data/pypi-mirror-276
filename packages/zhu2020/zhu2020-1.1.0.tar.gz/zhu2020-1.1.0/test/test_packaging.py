# {# pkglts, glabpkg_dev
import zhu2020


def test_package_exists():
    assert zhu2020.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert zhu2020.pth_clean.exists()
    try:
        assert zhu2020.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
