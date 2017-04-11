import pymongo

from flask_stupe import paginate


class Cursor(pymongo.cursor.Cursor):
    def __init__(self, data):
        self.data = data
        self._Cursor__id = "42"
        self._Cursor__killed = "42"

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


def test_paginate_skip(app):
    with app.test_request_context():
        @paginate(skip=2)
        def foo():
            return Cursor([1, 2, 3])
        assert foo().data == [3]


def test_paginate_limit(app):
    with app.test_request_context():
        @paginate(limit=2)
        def foo():
            return Cursor([1, 2, 3])
        assert foo().data == [1, 2]


def test_paginate_sort(app):
    with app.test_request_context():
        @paginate(sort=["foo"])
        def foo():
            return Cursor([{"foo": 1}, {"foo": 3}, {"foo": 2}])
        assert foo().data == [{'foo': 1}, {'foo': 2}, {'foo': 3}]

        @paginate(sort=["-bar"])
        def bar():
            return Cursor([{"bar": 1}, {"bar": 3}, {"bar": 2}])
        assert bar().data == [{'bar': 3}, {'bar': 2}, {'bar': 1}]

        @paginate(sort="foo,-bar")
        def foobar():
            return Cursor([{"bar": 1}, {"bar": 3}, {"bar": 2},
                           {"foo": 1}, {"foo": 3}, {"foo": 2}])
        assert foobar().data == [{'bar': 3}, {'bar': 2}, {'bar': 1},
                                 {'foo': 1}, {'foo': 2}, {'foo': 3}]


def test_paginate_cursor(app):
    with app.test_request_context():
        assert paginate(Cursor([1, 2, 3]), skip=2).data == [3]


def test_paginate_function(app):
    with app.test_request_context():
        def foo_instance():
            return Cursor([1, 2, 3])
        assert paginate(foo_instance, skip=2)().data == [3]
