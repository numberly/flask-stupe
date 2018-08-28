import bson
import pytest
from marshmallow import Schema
from marshmallow.fields import Integer, String

from flask_stupe.fields import (IP, Color, Cron, Currency, IPv4, IPv6,
                                ObjectId, OneOf)


def test_ip():
    class TestSchema(Schema):
        IP = IP(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "127.0.0.1"})
    assert result.data["IP"] == "127.0.0.1"

    result = schema.load({"IP": "127.0.0"})
    assert result.errors["IP"] == ["Not a valid IPv4 or IPv6 address."]

    result = schema.load({"IP": "256.256.256.256"})
    assert result.errors["IP"] == ["Not a valid IPv4 or IPv6 address."]

    result = schema.load({"IP": "2001:0db8:0000:0000:0000:ff00:0042:8329"})
    assert result.data["IP"] == "2001:0db8:0000:0000:0000:ff00:0042:8329"

    result = schema.load({"IP": "2001:db8:0:0:0:ff00:42:8329"})
    assert result.data["IP"] == "2001:db8:0:0:0:ff00:42:8329"

    result = schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert result.data["IP"] == "2001:db8::ff00:42:8329"

    result = schema.load({"IP": "2001:gb8::ff00:42:8329"})
    assert result.errors["IP"] == ["Not a valid IPv4 or IPv6 address."]


def test_ipv4():
    class TestSchema(Schema):
        IP = IPv4(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "127.0.0.1"})
    assert result.data["IP"] == "127.0.0.1"

    result = schema.load({"IP": "127.0.0"})
    assert result.errors["IP"] == ["Not a valid IPv4 address."]

    result = schema.load({"IP": "256.256.256.256"})
    assert result.errors["IP"] == ["Not a valid IPv4 address."]

    result = schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert result.errors["IP"] == ["Not a valid IPv4 address."]


def test_ipv6():
    class TestSchema(Schema):
        IP = IPv6(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "2001:0db8:0000:0000:0000:ff00:0042:8329"})
    assert result.data["IP"] == "2001:0db8:0000:0000:0000:ff00:0042:8329"

    result = schema.load({"IP": "2001:db8:0:0:0:ff00:42:8329"})
    assert result.data["IP"] == "2001:db8:0:0:0:ff00:42:8329"

    result = schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert result.data["IP"] == "2001:db8::ff00:42:8329"

    result = schema.load({"IP": "2001:gb8::ff00:42:8329"})
    assert result.errors["IP"] == ["Not a valid IPv6 address."]

    result = schema.load({"IP": "255.255.255.255"})
    assert result.errors["IP"] == ["Not a valid IPv6 address."]


def test_color():
    class TestSchema(Schema):
        color = Color(required=True)

    schema = TestSchema()
    result = schema.load({"color": "#ec068d"})
    assert result.data["color"] == "#ec068d"

    result = schema.load({"color": "test"})
    assert result.errors["color"] == ["Not a valid color."]

    result = schema.load({"color": ["test", "test"]})
    assert result.errors["color"] == ["Invalid input type."]


def test_cron(app):
    class TestSchema(Schema):
        schedule = Cron(required=True)

    schema = TestSchema()
    result = schema.load({"schedule": "* * 4 * *"})
    assert result.data["schedule"] is "* * 4 * *"

    result = schema.load({"schedule": "* * 1 * * *"})
    assert result.errors["schedule"] == ["Not a valid cron expression."]

    result = schema.load({"schedule": "60 * * * *"})
    assert result.errors["schedule"] == ["The minutes field is invalid."]

    result = schema.load({"schedule": "a * * * *"})
    assert result.errors["schedule"] == ["Not a valid cron expression."]


def test_currency():
    class TestSchema(Schema):
        currency = Currency(required=True)

    schema = TestSchema()
    result = schema.load({"currency": "EUR"})
    assert result.data["currency"] == "EUR"

    result = schema.load({"currency": "1MD"})
    assert result.errors["currency"] == ["Not a valid currency."]

    result = schema.load({"currency": ["ILS", "EUR"]})
    assert result.errors["currency"] == ["Invalid input type."]


def test_oneof(app):
    class TestSchema(Schema):
        value_type = OneOf([Integer, String])

    schema = TestSchema()
    result = schema.load({"value_type": 42})
    assert result.data["value_type"] == 42

    result = schema.load({"value_type": "test"})
    assert result.data["value_type"] == "test"

    result = schema.load({"value_type": ["42", 42]})
    assert result.errors["value_type"] == [("Object type doesn't match any "
                                            "valid type")]

    with pytest.raises(ValueError) as error:
        class TestSchema2(Schema):
            value_type = OneOf([int])
    assert str(error.value) == "Fields types must subclass FieldABC"

    with pytest.raises(ValueError) as error:
        class TestSchema3(Schema):
            value_type = OneOf(int)
    assert str(error.value) == "Fields must be contained in a list or tuple"

    with pytest.raises(ValueError) as error:
        class TestSchema5(Schema):
            value_type = OneOf([app])
    assert str(error.value) == "Fields must be FieldABC instances"

    with pytest.raises(ValueError) as error:
        class TestSchema4(Schema):
            value_type = OneOf([int])
    assert str(error.value) == "Fields types must subclass FieldABC"

    class TestSchema6(Schema):
        value_type = OneOf([Integer()])

    schema = TestSchema6()
    result = schema.load({"value_type": 42})
    assert result.data["value_type"] == 42


def test_object_id():
    class TestSchema(Schema):
        id = ObjectId()

    test_id = bson.ObjectId()

    schema = TestSchema()
    result = schema.load({"id": test_id})
    assert result.data["id"] == test_id

    result = schema.load({"id": "fail"})
    assert result.errors["id"] == ["Not a valid ObjectId."]

    result = schema.load({"id": 42})
    assert result.errors["id"] == ["Invalid input type."]
