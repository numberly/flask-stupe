from datetime import datetime as dt

import pytest
from bson import ObjectId

from flask_stupe.inputs import (boolean, date, datetime, int_list,
                                objectid_list, str_list)


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


def test_int_list():
    assert int_list("") == []
    assert int_list("42") == [42]
    assert int_list("13,37") == [13, 37]
    assert int_list("4,2,0") == [4, 2, 0]


def test_objectid_list():
    objectids = [ObjectId() for i in range(5)]
    assert objectid_list("") == []
    assert objectid_list(str(objectids[0])) == [objectids[0]]

    objectids_string = ','.join(str(o) for o in objectids)
    assert objectid_list(objectids_string) == objectids


def test_datetime():
    now = dt.now()
    assert datetime(str(now)) == now


def test_date():
    now = dt.now().date()
    assert date(str(now)) == now
