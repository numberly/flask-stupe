import pytest

from flask_stupe.inputs import boolean


def test_boolean():
    assert boolean(True) is True
    assert boolean(False) is False

    with pytest.raises(ValueError):
        boolean(None)

    assert boolean("0") is False
    assert boolean("1") is True

    assert boolean("true") is True
    assert boolean("false") is False

    assert boolean("tRuE") is True
    assert boolean("fAlSE") is False

    with pytest.raises(ValueError):
        boolean("invalid_string")


def test_str_list():
    assert str_list("") == []
    assert str_list("foo") == ["foo"]
    assert str_list("foo,bar") == ["foo", "bar"]
    assert str_list("foo,baz,bar") == ["foo", "baz", "bar"]
