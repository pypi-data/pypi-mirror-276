# {# pkglts, glabpkg_dev
import intrieri1998


def test_package_exists():
    assert intrieri1998.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert intrieri1998.pth_clean.exists()
    try:
        assert intrieri1998.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
