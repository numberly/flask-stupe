from datetime import date, datetime

from flask import Response as FlaskResponse
from flask import jsonify, request
from flask.json import JSONEncoder as FlaskJSONEncoder
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)

from flask_stupe import bson
from flask_stupe.app import Stupeflask as BaseStupeflask

encoder_rules = [
    ((date, datetime), lambda d: d.isoformat()),
]


if bson:
    encoder_rules.append((bson.ObjectId, lambda o: str(o)))


class EncodeError(Exception):

    def __init__(self, o):
        self.message = "{} is not JSON serializable".format(repr(o))


def encode(o, silent=True):
    """Recursively encode a Python object in a JSON serializable format.

    objects natively supported by json's library are obviously supported, but
    so are datetimes, and ObjectId (if bson is installed).

    If you want to add such encoding for custom types, see
    :meth:`JSONEncoder.add_rule`.
    """
    for rule in encoder_rules:
        if isinstance(o, rule[0]):
            return rule[1](o)
    if not silent:
        raise EncodeError(o)
    return o


class JSONEncoder(FlaskJSONEncoder):
    """Stupeflask extensible JSON encoder

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
        except EncodeError:
            return super(JSONEncoder, self).default(o)

    def add_rule(type_or_tuple, function):
        """Add a new serializing rule

        A rule is defined by one or multiple types, and a function to execute
        in order to serialize this or those types.

        Dumb example:
            >>> app = flask.ext.stupe.json.Stupeflask(__name__)
            >>> app.json_encoder.add_rule(int, lambda i: str(i))
        """
        encoder_rules.append((type_or_tuple, function))


class Response(FlaskResponse):
    default_mimetype = "application/json"


def handle_error(e):
    """Convert any exception into a JSON message, with a proper HTTP code

    The JSON message will have the following form:

    .. code-block:: json

        {
            "code": 403,
            "message": "You don't have the permission to access the requested
                        resource. It is either read-protected or not readable
                        by the server."
        }
    """
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    response = jsonify(code=e.code, message=e.description)
    response.status_code = e.code
    return response


class Stupeflask(BaseStupeflask):
    json_encoder = JSONEncoder
    response_class = Response

    def make_response(self, rv):
        if isinstance(rv, self.response_class):
            return rv

        data = None
        code = 200
        if isinstance(rv, tuple):
            data, code = rv
        elif isinstance(rv, int):
            code = rv
        else:
            data = rv

        rv = {"code": code}
        if data is not None:
            rv.update(data=data)
        if request.metadata:
            rv.update(**request.metadata)

        rv = jsonify(rv)
        rv.status_code = code
        return rv

    def __init__(self, *args, **kwargs):
        super(Stupeflask, self).__init__(*args, **kwargs)

        for code in default_exceptions.keys():
            self.register_error_handler(code, handle_error)


__all__ = ["encoder_rules", "encode", "JSONEncoder", "handle_error",
           "Stupeflask"]
