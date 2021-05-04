import pytest
from mdd.modules import Math


@pytest.mark.modules
@pytest.mark.parametrize(
    "json, vals, expected",
    [
        ({}, [], [0.0]),
        ({}, [1.0, 2.0], [3.0]),
        ({"options": [{"id": "eval", "value": "in0 - in1"}]}, [1.0, 2.0], [-1.0]),
        ({"options": [{"id": "eval", "value": "in0 - in1"}]}, [2.0, 1.0], [1.0]),
        ({"options": [{"id": "eval", "value": "in0 * in1"}]}, [[2.0], 3.0], [6.0]),
        ({"options": [{"id": "eval", "value": "in0 * in1"}]}, [[4.0, 3.0], 3.0], [12.0, 9.0]),
        ({"options": [{"id": "eval", "value": "in0 - in1"}]}, [[3.0, 2.0], [1.0, 2.0]], [2.0, 0.0]),
    ],
)
def test_update_from_dict(json, vals, expected):
    math = Math()
    math.from_dict(json)
    for i in range(len(vals)):
        math.inputs[i].set_value(vals[i])
    math.update()
    res = math.outputs[0].get_value()
    assert res == expected
