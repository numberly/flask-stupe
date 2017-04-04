import pytest

from flask_stupe.config import Config
from werkzeug.routing import BaseConverter


def test_app_config(app):
    assert isinstance(app.config, Config)


class FooConverter(BaseConverter):
    def to_python(self, value):
        return "foo" + value


def test_register_converter(app, client):
    with pytest.raises(LookupError):
        app.route("/<Foo:foo>/<Bar:bar>")(lambda foo, bar: foo + bar)

    app.register_converter(FooConverter)
    app.register_converter(FooConverter, "Bar")
    assert app.route("/<Foo:foo>/<Bar:bar>")(lambda foo, bar: foo + bar)
    assert client.get("/foo/bar").data == b"foofoofoobar"


def test_register_converters(app, client):
    class BarConverter(BaseConverter):
        def to_python(self, value):
            return "bar" + value

    with pytest.raises(LookupError):
        app.route("/<Foo:foo>/<Bar:bar>")(lambda foo, bar: foo + bar)

    app.register_converters([FooConverter, BarConverter])
    assert app.route("/<Foo:foo>/<Bar:bar>")(lambda foo, bar: foo + bar)
    assert client.get("/foo/bar").data == b"foofoobarbar"
