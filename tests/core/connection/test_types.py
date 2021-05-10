import pytest
from mdd.core.connection import StandardType, TypeInterface
from mdd.types import get_types


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        (None,),
        ([1, 2, 3],),
        (1,),
        ("test",),
    ],
)
def test_create(value):
    t = StandardType(value)
    assert t.get_value() == value


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "obj, correct",
    [
        (StandardType(""), True),
        (TypeInterface(), False),
    ],
)
def test_is_connectable(obj, correct):
    assert StandardType("123").is_connectable(obj) == correct


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value0, value1, same",
    [
        (None, None, True),
        ("", "", True),
        (1, 1, True),
        ([1, 2, 3], [1, 2, 3], True),
        ([1, 2], [1, 2, 3], False),
        (1, [1, 2, 3], False),
    ],
)
def test_create(value0, value1, same):
    t = StandardType(value0)
    assert t.is_same(value1) == same


@pytest.mark.core
@pytest.mark.parametrize(
    "key, exists",
    [
        ("vector", True),
        ("dont exist", False),
    ],
)
def test_find_types(key, exists):
    types = get_types()
    assert (key in types.keys()) == exists