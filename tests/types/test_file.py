import pytest
from msys.core import TypeInterface, Type
from msys.types import *

from .conftest import *


# connectivity with types
@pytest.mark.types
@pytest.mark.parametrize(
    "obj, correct",
    [
        (FileType(), True),
        (Type(), False),
    ],
)
def test_is_connectable(obj, correct):
    assert FileType().is_connectable(obj) == correct


@pytest.mark.types
@pytest.mark.parametrize(
    "obj",
    [
        create_string_file,
        create_byte_file
    ],
)
def test_from_path(obj):
    path, value = obj()
    assert FileType.from_path(path).value == value


@pytest.mark.types
def test_from_path_exception():
    try:
        FileType.from_path("does not exist")
        assert False
    except FileNotFoundError:
        assert True

@pytest.mark.types
@pytest.mark.parametrize(
    "json",
    [
        {"value": 0},
    ],
)
def test_serialisation(json):
    type = FileType()
    assert type.from_dict(json)
    assert type
    tdict = type.to_dict()
    del tdict["mro"]
    assert tdict == json
