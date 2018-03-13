import pytest
from bson import ObjectId

from flask_stupe.inputs import boolean, objectid_list, str_list


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


def test_objectid_list():
    assert (objectid_list("") == [])
    assert (objectid_list("5a60ad5343e72318bc2fcb55") ==
            [ObjectId("5a60ad5343e72318bc2fcb55")])
    s = "5a60ad5343e72318bc2fcb55,5a815d07f950777affc7b4e2"
    assert (objectid_list(s) == [ObjectId("5a60ad5343e72318bc2fcb55"),
                                 ObjectId("5a815d07f950777affc7b4e2")])
