import pytest
from msys.core import Option

ldescipt= """
        Long and
        multiline description.
        """

@pytest.mark.core
@pytest.mark.parametrize(
    "id",
    [None, "test_id", 123],
)
@pytest.mark.parametrize(
    "title",
    [None, "test_title"],
)
@pytest.mark.parametrize(
    "description",
    [None, "test_description", ldescipt],
)
def test_header_to_dict(id, title, description):
    opt = Option(id=id, title=title, description=description)
    result = opt.to_dict()

    def _test_key(key: str, expected):
        if expected:
            assert result[key] == expected
        else:
            try:
                result[key]
                assert False
            except KeyError:
                assert True

    _test_key("id", id)
    _test_key("title", title)
    _test_key("description", description)


@pytest.mark.core
@pytest.mark.parametrize(
    "json, expected",
    [
        ({}, Option(id=None)),
        ({"id": 123}, Option(id=123)),
        ({"id": "test"}, Option(id="test")),
        ({"title": "test"}, Option(id=None, title="test")),
        ({"description": ldescipt}, Option(id=None, description=ldescipt)),
    ],
)
def test_from_dict(json, expected):
    res = Option(id=None)
    res.from_dict(json)
    assert res.to_dict() == expected.to_dict()
