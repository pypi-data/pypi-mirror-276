# {# pkglts, glabpkg_dev
import medlyn2002


def test_package_exists():
    assert medlyn2002.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert medlyn2002.pth_clean.exists()
    try:
        assert medlyn2002.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
