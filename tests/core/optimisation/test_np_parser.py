import pytest
from msys.core.optimisation import NumericStringParser
import numpy as np


@pytest.mark.core
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
    if isinstance(result, np.ndarray):
        for i in range(len(expected)):
            assert result[i] == expected[i]
    else:
        assert result == expected


@pytest.mark.core
@pytest.mark.parametrize(
    "string, expected",
    [
        ("var", np.array([1, 2, 34])),
        ("9*var", np.array([9 * 1, 9 * 2, 9 * 34])),
        ("var*-9", np.array([-9 * 1, -9 * 2, -9 * 34])),
    ],
)
def test_variable_expr(string, expected):
    parser = NumericStringParser()
    parser.vars["var"] = np.array([1, 2, 34])
    result = parser.eval(string)
    if isinstance(result, np.ndarray):
        for i in range(len(expected)):
            assert result[i] == expected[i]
    else:
        assert result == expected
