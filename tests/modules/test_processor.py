import pytest
from msys.modules import DefaultProcessor, Math


@pytest.mark.modules
@pytest.mark.parametrize(
    "priority",
    [
        ("static"),
        ("dynamic"),
        ("time"),
    ],
)
def test_processor(priority):
    processor = DefaultProcessor()
    processor.from_dict({"options": [{"id": "prio", "value": [priority]}]})
    # ([8, 12]+ ([10, 9]-[6, 1])=[4, 8])/[3, 4] = [4, 5]
    math0 = Math()
    math0.from_dict({"options": [{"id": "eval", "value": "in0 / in1"}]})

    math0 = Math()
    math0.from_dict({"options": [{"id": "eval", "value": "in0 / in1"}]})

    math1 = Math()
    math1.from_dict({"options": [{"id": "eval", "value": "in0 + in1"}]})

    math2 = Math()
    math2.from_dict({"options": [{"id": "eval", "value": "in0 - in1"}]})

    math2.inputs[0].set_value([10, 9])
    math2.inputs[1].set_value([6, 1])

    math1.inputs[0].set_value([8, 12])
    math1.inputs[1].connect(math2.outputs[0])

    math0.inputs[0].connect(math1.outputs[0])
    math0.inputs[1].set_value([3, 4])

    processor.modules = [math0, math1, math2]

    processor.process()

    assert list(math0.outputs[0].get_value()) == [4, 5]
