from bson import ObjectId
from flask import url_for


def test_converter_to_python(app):
    @app.route("/foo/<ObjectId:id>")
    def foo(id):
        assert isinstance(id, ObjectId)
        return str(id)

    client = app.test_client()

    route = "/foo/{}".format(ObjectId())
    client.get(route)


def test_converter_to_url(app):
    @app.route("/foo/<ObjectId:id>")
    def foo(id):
        return str(id)

    with app.test_request_context():
        route = url_for("foo", id=ObjectId())
    assert route
