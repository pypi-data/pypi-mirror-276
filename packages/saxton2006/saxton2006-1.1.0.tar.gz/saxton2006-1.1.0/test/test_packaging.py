# {# pkglts, glabpkg_dev
import saxton2006


def test_package_exists():
    assert saxton2006.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert saxton2006.pth_clean.exists()
    try:
        assert saxton2006.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
