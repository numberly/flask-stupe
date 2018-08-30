import pytest
from flask import Flask, request

from flask_stupe import Stupeflask, paginate
from tests.conftest import Cursor


@pytest.mark.parametrize("app", [
    Stupeflask(__name__),
    Flask(__name__)
])
def test_paginate_skip(app):
    with app.test_request_context():
        @paginate(skip=2)
        def foo():
            return Cursor([1, 2, 3])
        assert foo().data == [3]
        if isinstance(app, Stupeflask):
            assert request.metadata["count"] == 3


@pytest.mark.parametrize("app", [
    Stupeflask(__name__),
    Flask(__name__)
])
def test_paginate_limit(app):
    with app.test_request_context():
        @paginate(limit=2)
        def foo():
            return Cursor([1, 2, 3])
        assert foo().data == [1, 2]
        if isinstance(app, Stupeflask):
            assert request.metadata["count"] == 3


@pytest.mark.parametrize("app", [
    Stupeflask(__name__),
    Flask(__name__)
])
def test_paginate_sort(app):
    with app.test_request_context():
        @paginate(sort=["foo"])
        def foo():
            return Cursor([{"foo": 1}, {"foo": 3}, {"foo": 2}])
        assert foo().data == [{"foo": 1}, {"foo": 2}, {"foo": 3}]

        @paginate(sort=["-bar"])
        def bar():
            return Cursor([{"bar": 1}, {"bar": 3}, {"bar": 2}])
        assert bar().data == [{"bar": 3}, {"bar": 2}, {"bar": 1}]

        @paginate(sort="foo,-bar")
        def foobar():
            return Cursor([{"bar": 1}, {"bar": 3}, {"bar": 2},
                           {"foo": 1}, {"foo": 3}, {"foo": 2}])
        assert foobar().data == [{"bar": 3}, {"bar": 2}, {"bar": 1},
                                 {"foo": 1}, {"foo": 2}, {"foo": 3}]


@pytest.mark.parametrize("app", [
    Stupeflask(__name__),
    Flask(__name__)
])
def test_paginate_cursor(app):
    with app.test_request_context():
        assert paginate(Cursor([1, 2, 3]), skip=2).data == [3]


@pytest.mark.parametrize("app", [
    Stupeflask(__name__),
    Flask(__name__)
])
def test_paginate_function(app):
    with app.test_request_context():
        def foo_instance():
            return Cursor([1, 2, 3])
        assert paginate(foo_instance, skip=2)().data == [3]


def test_paginate_header_total_count(app):
    with app.test_request_context():
        paginate(Cursor([1, 2, 3]))
        assert request.response_headers["X-Total-Count"] == 3
        assert "Link" not in request.response_headers


def test_paginate_header_link(app):
    with app.test_request_context():
        paginate(Cursor([1, 2, 3]), limit=1, skip=1)
        links = request.response_headers["Link"].split(",")
        assert links[0].split("?")[1] == 'limit=1&skip=1>; rel="self"'
        assert links[1].split("?")[1] == 'limit=1&skip=0>; rel="first"'
        assert links[2].split("?")[1] == 'limit=1&skip=0>; rel="prev"'
        assert links[3].split("?")[1] == 'limit=1&skip=2>; rel="next"'
        assert links[4].split("?")[1] == 'limit=1&skip=2>; rel="last"'


def test_paginate_metadata_links(app):
    with app.test_request_context():
        paginate(Cursor([1, 2, 3]), limit=1, skip=1)
        links = request.metadata["links"]
        assert links["self"].split("?")[1] == "limit=1&skip=1"
        assert links["first"].split("?")[1] == "limit=1&skip=0"
        assert links["prev"].split("?")[1] == "limit=1&skip=0"
        assert links["next"].split("?")[1] == "limit=1&skip=2"
        assert links["last"].split("?")[1] == "limit=1&skip=2"
