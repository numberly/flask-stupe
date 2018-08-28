import logging

import pytest
from werkzeug.routing import BaseConverter

from flask_stupe.app import Stupeflask
from flask_stupe.config import Config


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


def test_register_blueprints(test_apps, caplog, app):
    import blueprintapp

    caplog.set_level(logging.INFO)
    app.register_blueprints(blueprintapp)
    messages = [record.message for record in caplog.records]
    assert " * Registering blueprint blueprintapp.apps.admin" in messages
    assert " * Registering blueprint blueprintapp.apps.frontend" in messages
    assert len(app.blueprints) == 2


@pytest.fixture
def app():
    return Stupeflask(__name__)
