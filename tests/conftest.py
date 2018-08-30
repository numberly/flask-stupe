import json
import os

import pymongo
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


# ramnes: we're just inheriting from pymongo.cursor.Cursor so that paginate can
# understand it's not a function to decorate
class Cursor(pymongo.cursor.Cursor):

    def __init__(self, data):
        self.data = data

    def __del__(self):
        pass

    def skip(self, skip):
        del self.data[:skip]
        return self.data

    def limit(self, limit):
        del self.data[limit:]
        return self.data

    def sort(self, sort):
        for sort_key, order in reversed(sort):
            self.data = sorted(self.data, key=lambda d: d.get(sort_key, 0))
            if order == -1:
                self.data.reverse()
        return self.data

    def count(self):
        return len(self.data)

    def clone(self):
        return Cursor(self.data)


def response_to_dict(response):
    data = response.get_data()
    return json.loads(data.decode("utf-8"))
