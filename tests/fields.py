import bson
import pytest
from marshmallow import Schema, ValidationError
from marshmallow.fields import Integer, String

from flask_stupe.fields import IP, Color, Cron, Currency, IPv4, IPv6, ObjectId, OneOf


def test_ip():
    class TestSchema(Schema):
        IP = IP(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "127.0.0.1"})
    assert result["IP"] == "127.0.0.1"

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "127.0.0"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 or IPv6 address."]

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "256.256.256.256"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 or IPv6 address."]

    result = schema.load({"IP": "2001:0db8:0000:0000:0000:ff00:0042:8329"})
    assert result["IP"] == "2001:0db8:0000:0000:0000:ff00:0042:8329"

    result = schema.load({"IP": "2001:db8:0:0:0:ff00:42:8329"})
    assert result["IP"] == "2001:db8:0:0:0:ff00:42:8329"

    result = schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert result["IP"] == "2001:db8::ff00:42:8329"

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "2001:gb8::ff00:42:8329"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 or IPv6 address."]


def test_ipv4():
    class TestSchema(Schema):
        IP = IPv4(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "127.0.0.1"})
    result["IP"] == "127.0.0.1"

    with pytest.raises(ValidationError) as error:
        result = schema.load({"IP": "127.0.0"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 address."]

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "256.256.256.256"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 address."]

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert error.value.messages["IP"] == ["Not a valid IPv4 address."]


def test_ipv6():
    class TestSchema(Schema):
        IP = IPv6(required=True)

    schema = TestSchema()
    result = schema.load({"IP": "2001:0db8:0000:0000:0000:ff00:0042:8329"})
    assert result["IP"] == "2001:0db8:0000:0000:0000:ff00:0042:8329"

    result = schema.load({"IP": "2001:db8:0:0:0:ff00:42:8329"})
    assert result["IP"] == "2001:db8:0:0:0:ff00:42:8329"

    result = schema.load({"IP": "2001:db8::ff00:42:8329"})
    assert result["IP"] == "2001:db8::ff00:42:8329"

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "2001:gb8::ff00:42:8329"})
    assert error.value.messages["IP"] == ["Not a valid IPv6 address."]

    with pytest.raises(ValidationError) as error:
        schema.load({"IP": "255.255.255.255"})
    assert error.value.messages["IP"] == ["Not a valid IPv6 address."]


def test_color():
    class TestSchema(Schema):
        color = Color(required=True)

    schema = TestSchema()
    result = schema.load({"color": "#ec068d"})
    assert result["color"] == "#ec068d"

    with pytest.raises(ValidationError) as error:
        schema.load({"color": "test"})
    assert error.value.messages["color"] == ["Not a valid color."]

    with pytest.raises(ValidationError) as error:
        schema.load({"color": ["test", "test"]})
    assert error.value.messages["color"] == ["Invalid type."]


def test_cron(app):
    class TestSchema(Schema):
        schedule = Cron(required=True)

    schema = TestSchema()
    result = schema.load({"schedule": "* * 4 * *"})
    assert result["schedule"] == "* * 4 * *"

    with pytest.raises(ValidationError) as error:
        schema.load({"schedule": "* * 1 * * *"})
    assert error.value.messages["schedule"] == ["Not a valid cron expression."]

    with pytest.raises(ValidationError) as error:
        schema.load({"schedule": "60 * * * *"})
    assert error.value.messages["schedule"] == ["The minutes field is "
                                                "invalid."]

    with pytest.raises(ValidationError) as error:
        schema.load({"schedule": "a * * * *"})
    assert error.value.messages["schedule"] == ["Not a valid cron expression."]


def test_currency():
    class TestSchema(Schema):
        currency = Currency(required=True)

    schema = TestSchema()
    result = schema.load({"currency": "EUR"})
    assert result["currency"] == "EUR"

    with pytest.raises(ValidationError) as error:
        schema.load({"currency": "1MD"})
    assert error.value.messages["currency"] == ["Not a valid currency."]

    with pytest.raises(ValidationError) as error:
        schema.load({"currency": ["ILS", "EUR"]})
    assert error.value.messages["currency"] == ["Invalid type."]


def test_oneof(app):
    class TestSchema(Schema):
        value_type = OneOf([Integer, String])

    schema = TestSchema()
    result = schema.load({"value_type": 42})
    assert result["value_type"] == 42

    result = schema.load({"value_type": "test"})
    assert result["value_type"] == "test"

    with pytest.raises(ValidationError) as error:
        schema.load({"value_type": ["42", 42]})
    assert error.value.messages["value_type"] == [("Object type doesn't match "
                                                   "any valid type")]

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
    assert result["value_type"] == 42


def test_object_id():
    class TestSchema(Schema):
        id = ObjectId()

    test_id = bson.ObjectId()

    schema = TestSchema()
    result = schema.load({"id": test_id})
    assert result["id"] == test_id

    with pytest.raises(ValidationError) as error:
        schema.load({"id": "fail"})
    assert error.value.messages["id"] == ["Not a valid ObjectId."]

    with pytest.raises(ValidationError) as error:
        schema.load({"id": 42})
    assert error.value.messages["id"] == ["Invalid type."]
