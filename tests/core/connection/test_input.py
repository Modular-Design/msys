import pytest
from msys.core.connection import Input, StandardType


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        StandardType(""),
        StandardType(1),
        StandardType(None),
    ],
)
def test_create(value):
    ins = Input(value)
    assert ins.get_value() == value.get_value()
    assert ins.is_changed()


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
    ins = Input(StandardType(None))
    ins.set_value(value)
    assert ins.get_value() == value

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
    ins = Input(type=StandardType())
    assert (success := ins.set_value(value)) == correct
    if success:
        assert ins.get_value() == value
        assert ins.is_changed()


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "output",
    [
        StandardType("1"),
    ],
)
def test_connection_field(output):
    ins = Input(type=StandardType(None), output=output)
    assert ins.get_value() == output.get_value()
    assert ins.is_changed()