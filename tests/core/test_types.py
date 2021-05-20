import pytest
from msys.core import Type, TypeInterface
from msys.registration import get_types


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
@pytest.mark.parametrize(
    "name",
    [
        ("",),
        (None,),
        ("standard",),
        ("None",),
    ],
)
def test_create(name, value):
    t = Type(value, name)
    assert t.get_value() == value
    assert t.type_name == name


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "obj, correct",
    [
        (Type(""), True),
        (object(), False),
    ],
)
def test_is_connectable(obj, correct):
    assert Type("123").is_connectable(obj) == correct


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
    t = Type(value0)
    assert t.is_same(value1) == same