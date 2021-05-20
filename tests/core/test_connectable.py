import pytest
from msys.core import Connectable, Type


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        Type(""),
        Type(1),
        Type(None),
    ],
)
def test_create(value):
    con = Connectable(value)
    assert con.get_value() == value.get_value()
    assert con.is_changed()


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        (None, ),
        ("", ),
        (1, ),
        ([1, 2, 3], ),
    ],
)
def test_set_value(value):
    con = Connectable(Type(None))
    con.set_value(value)
    assert con.get_value() == value

@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value, correct",
    [
        (1, True),
        ("", False),  # correct=False, b/c "" is 'default_value' of StandardType
        (None, True),
        ([1, 2, 3], True),
    ],
)
def test_set_value(value, correct):
    con = Connectable(type=Type())
    success = con.set_value(value)
    assert success == correct
    if success:
        assert con.get_value() == value
        assert con.is_changed()
