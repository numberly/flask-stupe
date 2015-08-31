import functools

from datetime import date, datetime

from flask import jsonify, request
from flask import Response as FlaskResponse
from flask.json import JSONEncoder as FlaskJSONEncoder
from werkzeug.exceptions import (default_exceptions, HTTPException,
                                 InternalServerError)

from flask_stupe import Stupeflask as BaseStupeflask

encoder_rules = [
    ((date, datetime), lambda d: d.isoformat()),
]

try:
    from bson import ObjectId

    encoder_rules.append((ObjectId, lambda o: str(o)))
except ImportError:
    pass


def unencodable(o):
    return TypeError(repr(o) + " is not JSON serializable")


def encode(o, silent=True):
    for rule in encoder_rules:
        if isinstance(o, rule[0]):
            return rule[1](o)
    if not silent:
        raise unencodable(o)
    return o


class JSONEncoder(FlaskJSONEncoder):
    """Stupeflask extensible JSON encoder.

    The JSONEncoder is used by :func:`flask.jsonify` to convert a Python
    dictionary into a real JSON string. If the JSONEncoder receive a dict
    containing unknown type, a `TypeError` exception will be raised.

    Default supported types are Python built-in types (`int`, `list`, etc.),
    `datetime.date` and `datetime.date`, as well as `bson.ObjectId` if `bson`
    module is present.

    To make the JSONEncoder support more types, see :meth:`add_rule`.
    """

    def default(self, o):
        try:
            return encode(o, silent=False)
        except TypeError as e:
            if e != unencodable(o):
                raise
            return super(JSONEncoder, self).default(o)

    def add_rule(type_or_tuple, function):
        """Add a new serializing rule.

        A rule is defined by one or multiple types, and a function to execute in
        order to serialize this or those types.

        Dumb example:
            >>> app = flask.ext.stupe.json.Stupeflask(__name__)
            >>> app.json_encoder.add_rule(int, lambda i: str(i))
        """
        global encoder_rules
        encoder_rules.append((type_or_tuple, function))


class Response(FlaskResponse):
    default_mimetype = "application/json"

    @classmethod
    def force_type(cls, response, *args, **kwargs):
        response = jsonify(response)
        return super(Response, cls).force_type(response, *args, **kwargs)


def handle_error(e):
    """Convert any exception into a JSON message, with a proper HTTP code.

    The JSON message will have the following form:
    {
        "code": 403,
        "message": "You don't have the permission to access the requested
                    resource. It is either read-protected or not readable by the
                    server."
    }
    """
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    response = jsonify(code=e.code, message=e.description)
    response.status_code = e.code
    return response


class Stupeflask(BaseStupeflask):

    def __init__(self, *args, **kwargs):
        super(Stupeflask, self).__init__(*args, **kwargs)

        self.json_encoder = JSONEncoder

        try:
            import wtforms_json

            wtforms_json.init()
        except ImportError:
            pass

        for code in default_exceptions.keys():
            self.register_error_handler(code, handle_error)


def form_required(form_cls):
    def __inner(f):
        @functools.wraps(f)
        def __inner(*args, **kwargs):
            json = request.get_json(force=True)
            form = form_cls.from_json(json)
            form.validate()
            request.form = form
            return f(*args, **kwargs)
        return __inner
    return __inner


__all__ = ["encoder_rules", "encode", "JSONEncoder", "handle_error",
           "Stupeflask", "form_required"]
