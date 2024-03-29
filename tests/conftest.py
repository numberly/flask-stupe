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

    def __iter__(self):
        return iter(self.data)

    def __empty(self):
        return len(self.data) == 0

    def skip(self, skip):
        del self.data[:skip]
        return self.data

    def limit(self, limit):
        del self.data[limit:]
        return self.data

    def sort(self, sort):
        self.sort_data = sort
        for sort_key, order in reversed(sort):

            def get_key(d):
                if hasattr(self, "collation_data"):
                    return d.get(sort_key, 0).lower()
                return d.get(sort_key, 0)

            self.data = sorted(self.data, key=get_key)
            if order == -1:
                self.data.reverse()
        return self.data

    def collation(self, collation):
        self.collation_data = collation
        return self.sort(self.sort_data)

    def count(self):
        return len(self.data)

    def clone(self):
        return Cursor(self.data)


def response_to_dict(response):
    data = response.get_data()
    return json.loads(data.decode("utf-8"))
