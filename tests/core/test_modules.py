import pytest
from msys.modules import *


@pytest.mark.core
@pytest.mark.parametrize(
    "key, exists",
    [
        ("math", True),
        ("sql", True),
        ("processor", True),
        ("dont exist", False),
    ],
)
def test_find_modules(key, exists):
    modules = get_modules()
    assert (key in modules.keys()) == exists
