from msys.registration import *


def test_get_registered():
    assert get_registered("dont_exists") is None


def test_get_modules():
    assert get_modules() is None


def test_get_types():
    assert get_types() is None


def test_get_extensions():
    assert get_extensions() is None
