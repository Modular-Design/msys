from msys.registration import *
import pytest
from msys.types import FileType

def test_get_registered():
    assert get_registered("dont_exists") is None


# def test_get_modules():
#     assert get_modules() is None

def test_get_types():
    types = get_types()
    assert types != []
    in_package = filter_package("msys", types)
    assert len(in_package) == 1



@pytest.mark.core
@pytest.mark.parametrize(
    "t_class",
    [
        FileType,
    ]
)
def test_get_individual_types(t_class):
    name = t_class.registered_name
    package = t_class.registered_package
    assert filter_name(name, filter_package(package, get_types()))[0]["class"] == t_class

# def test_get_extensions():
#     assert get_extensions() is None
