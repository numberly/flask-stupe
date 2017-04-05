import json
import os
import pytest

from flask_stupe.app import Stupeflask


@pytest.fixture
def app():
    return Stupeflask(__name__)


@pytest.fixture
def client(app):
    return app.test_client()


# ramnes: shamelessly stolen from Flask
# https://github.com/pallets/flask/blob/0.12.1/tests/conftest.py#L18-L23
@pytest.fixture
def test_apps(monkeypatch):
    monkeypatch.syspath_prepend(
        os.path.abspath(os.path.join(
            os.path.dirname(__file__), "test_apps")
        )
    )


def response_to_dict(response):
    data = response.get_data()
    return json.loads(data.decode("utf-8"))
