import pytest
from mdd.core import Metadata, Point

@pytest.mark.core
@pytest.mark.parametrize(
    "expected,input",
    [({}, Metadata()),
     ({"name": "test"}, Metadata("test")),
     ({"color": "blue"}, Metadata(color="blue")),
     ({"pos": {"x": 1.0, "y": 42.0}}, Metadata(pos=Point(1.0, 42.0))),
     pytest.param({"name": "test", "color": "blue", "pos": {"x": 1.0, "y": 42.0}}, Metadata(), marks=pytest.mark.xfail)],
)
def test_toDict(input, expected):
    res = input.toDict()
    assert res == expected

@pytest.mark.core
@pytest.mark.parametrize(
    "input, expected",
    [({}, Metadata()),
     ({"name": "test"}, Metadata("test")),
     ({"color": "blue"}, Metadata(color="blue")),
     ({"pos": {"x": 1.0, "y": 42.0}}, Metadata(pos=Point(1.0, 42.0))),
     pytest.param({"name": "test", "color": "blue", "pos": {"x": 1.0, "y": 42.0}}, Metadata(),
                  marks=pytest.mark.xfail)],
)
def test_fromDict(input, expected):
    res = Metadata()
    res.fromDict(input)
    assert res.toDict() == expected.toDict()

