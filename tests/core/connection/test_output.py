import pytest
from msys.core.connection import Output, StandardType


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        (StandardType("")),
        (StandardType("")),
        (StandardType(None)),
    ],
)
def test_create(value):
    out = Output(value)
    assert out.get_value() == value.get_value()
    assert out.is_changed()
    assert out.disconnect()


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value, correct",
    [
        ("", False),  # "" is default value
        ("Test Output", True),
        (1234, True),
        ({"test": 123}, True),
        ([1, 2, 3], True),
    ]
)
def test_set_value( value, correct):
    out = Output(type=StandardType())
    assert (success := out.set_value(value)) == correct
    if success:
        assert out.get_value() == value
        assert out.is_changed()
        assert out.disconnect()
