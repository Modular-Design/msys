import pytest
from msys.core.connection import Input, StandardType


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        (StandardType(""), ),
        (StandardType(1), ),
        (StandardType(None), ),
    ],
)
def test_create(value):
    ins = Input([value])
    assert ins.get_value() == value.get_value()


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
def test_create(value):
    ins = Input([StandardType(None)])
    ins.set_value(value)
    assert ins.get_value() == value