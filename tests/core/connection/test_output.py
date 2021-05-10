import pytest
from mdd.core.connection import Output, StandardType


@pytest.mark.core
@pytest.mark.connection
@pytest.mark.parametrize(
    "value",
    [
        (StandardType("")),
        (StandardType(1)),
        (StandardType(None)),
    ],
)
def test_create(value):
    output = Output(value)
    assert output.get_value() == value.get_value()
