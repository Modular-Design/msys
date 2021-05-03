import pytest
from mdd.core.optimisation import NumericStringParser
import numpy as np

@pytest.mark.parametrize(
    "string, expected",
    [
        ("9", 9),
        ("-9", -9),
        ("--9", 9),
        ("array(1, 2,34)", np.array([1, 2, 34])),
    ],
)
def test_simple_expr(string, expected):
    parser = NumericStringParser()
    result = parser.eval(string)
    if isinstance(, np.array()):
        for i in range(len(expected)):
            assert result[i] == expected[i]
    else:
        assert result == expected
