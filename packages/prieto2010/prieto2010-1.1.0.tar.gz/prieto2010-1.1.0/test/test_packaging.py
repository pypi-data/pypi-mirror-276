# {# pkglts, glabpkg_dev
import prieto2010


def test_package_exists():
    assert prieto2010.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert prieto2010.pth_clean.exists()
    try:
        assert prieto2010.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
