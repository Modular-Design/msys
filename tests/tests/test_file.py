import pytest
from msys.core import TypeInterface, StandardType
from msys.types import *

from .conftest import *


# connectivity with types
@pytest.mark.types
@pytest.mark.parametrize(
    "obj, correct",
    [
        (FileType(), True),
        (StandardType(), False),
        (TypeInterface(), False),
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
