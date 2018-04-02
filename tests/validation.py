import json

from flask import request
from flask_stupe.validation import schema_required
from marshmallow import Schema
from marshmallow.fields import Integer


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
