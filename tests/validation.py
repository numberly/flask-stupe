import json

from flask import request
from flask_stupe.validation import Schema, schema_required
from marshmallow.fields import Integer, List, Nested


def test_unrequire():
    class TestSchema(Schema):
        foo = Integer(required=True)

    schema = TestSchema()
    assert schema.validate({}) == {'foo': ['Missing data for required field.']}

    schema = TestSchema(unrequire=True)
    assert schema.validate({}) == {}


def test_unrequire_list():
    class TestSchema(Schema):
        foo = List(Integer, required=True)

    schema = TestSchema()
    assert schema.validate({}) == {'foo': ['Missing data for required field.']}

    schema = TestSchema(unrequire=True)
    assert schema.validate({}) == {}


def test_unrequire_nested():
    class NestedSchema(Schema):
        foo = Integer(required=True)

    class TestSchema(Schema):
        foo = Nested(NestedSchema(), required=True)

    schema = TestSchema()
    assert schema.validate({}) == {'foo': {'foo': ['Missing data for required field.']}}

    schema = TestSchema(unrequire=True)
    assert schema.validate({}) == {}
    assert schema.validate({"foo": {}}) == {}


def test_schema_required(app):
    class TestSchema(Schema):
        id = Integer(required=True)

    @app.route("/foo", methods=["POST"])
    @schema_required(TestSchema())
    def foo():
        return str(request.schema.get("id"))

    client = app.test_client()

    data = json.dumps({"id": 42})
    response = client.post("/foo", data=data)
    assert response.status_code == 200

    data = json.dumps({})
    response = client.post("/foo", data=data)
    assert response.status_code == 400
