import json
from datetime import date, datetime
from uuid import uuid4

import flask
import pytest
from bson import ObjectId
from pkg_resources import parse_version
from werkzeug.exceptions import Forbidden, NotFound

from flask_stupe.json import (JSONEncoder, Response, Stupeflask, encode,
                              encoder_rules, handle_error)
from flask_stupe.pagination import paginate
from tests.conftest import Cursor, response_to_dict

original_rules = encoder_rules[:]


@pytest.fixture
def json_app():
    return Stupeflask(__name__)


@pytest.fixture
def client(json_app):
    return json_app.test_client()


@pytest.fixture(autouse=True)
def clean_encoder_rules():
    del encoder_rules[:]
    encoder_rules.extend(original_rules)


class Foo:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


rule = (Foo, str)


def test_encode():
    assert isinstance(encode(datetime.utcnow()), str)
    assert isinstance(encode(date.today()), str)

    assert isinstance(encode(Foo("bar")), Foo)
    with pytest.raises(Exception) as e:
        encode(Foo("bar"), silent=False)
    assert e.typename == "EncodeError"
    assert "not JSON serializable" in e.value.message

    encoder_rules.append(rule)
    assert encode(Foo("bar")) == "bar"


def test_encoder():
    with pytest.raises(TypeError):
        json.dumps(Foo("bar"), cls=JSONEncoder)
    JSONEncoder.add_rule(*rule)
    assert json.dumps(Foo("bar"), cls=JSONEncoder) == '"bar"'


def test_encoder_fallback():
    uuid = uuid4()
    assert json.dumps(uuid, cls=JSONEncoder) == '"{}"'.format(uuid)


def test_bad_encoder_rule():
    del encoder_rules[:]
    JSONEncoder.add_rule(ObjectId, lambda o: int(o))

    with pytest.raises(TypeError):
        json.dumps(ObjectId(), cls=JSONEncoder)


def test_handle_error(json_app):
    with json_app.test_request_context():
        assert handle_error(Exception()).status_code == 500
        assert handle_error(NotFound()).status_code == 404
        assert handle_error(Forbidden()).status_code == 403

        response = handle_error(Forbidden())
        if parse_version(flask.__version__) >= parse_version("1.0"):
            data = response.json
        else:
            data = json.loads(response.response[0])

    assert data.pop("message") == Forbidden.description
    assert data.pop("code") == 403
    assert not data


def test_stupeflask_response_content_type(json_app, client):
    json_app.route("/")(lambda: None)
    response = client.get("/")
    assert response.content_type == "application/json"


def test_stupeflask_empty_response(json_app, client):
    json_app.route("/")(lambda: None)
    response = client.get("/")
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert "data" not in response_dict
    assert response_dict["code"] == 200


def test_stupeflask_response_with_data(json_app, client):
    json_app.route("/")(lambda: "foo")
    response = client.get("/")
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert response_dict["data"] == "foo"
    assert response_dict["code"] == 200


def test_stupeflask_response_with_code(json_app, client):
    json_app.route("/")(lambda: 201)
    response = client.get("/")
    assert response.status_code == 201

    response_dict = response_to_dict(response)
    assert "data" not in response_dict
    assert response_dict["code"] == 201


def test_stupeflask_response_with_data_and_code(json_app, client):
    json_app.route("/")(lambda: ("foo", 201))
    response = client.get("/")
    assert response.status_code == 201

    response_dict = response_to_dict(response)
    assert response_dict["data"] == "foo"
    assert response_dict["code"] == 201


def test_stupeflask_response_with_empty_list(json_app, client):
    json_app.route("/")(lambda: [])
    response = client.get("/")
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert response_dict.get("data") == []
    assert response_dict["code"] == 200


def test_stupeflask_response_with_metadata(json_app, client):
    @json_app.route("/")
    def foo():
        from flask import request
        request.metadata.update(bar="baz")

    response = client.get("/")
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert "data" not in response_dict
    assert response_dict["code"] == 200
    assert response_dict["bar"] == "baz"


def test_stupeflask_response_with_paginate(json_app, client):
    encoder_rules.append((Cursor, lambda c: c.data))

    @json_app.route("/")
    @paginate(limit=2)
    def foo():
        return Cursor([1, 2, 3])

    response = client.get("/")
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert len(response_dict["data"]) == 2
    assert response_dict["code"] == 200
    assert response_dict["count"] == 3


def test_stupeflask_converters(json_app, client):
    @json_app.route("/<ObjectId:foo_id>")
    def foo_id(foo_id):
        return foo_id

    object_id = ObjectId()
    response = client.get("/{}".format(object_id))
    assert response.status_code == 200

    response_dict = response_to_dict(response)
    assert response_dict["data"] == str(object_id)


def test_stupeflask_direct_response(json_app, client):
    json_app.route("/")(lambda: Response("foo"))
    response = client.get("/")
    assert response.status_code == 200

    data = response.get_data().decode("utf-8")
    assert "data" not in data
    assert data == "foo"
