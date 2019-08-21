import functools

from flask import abort, request

from flask_stupe import marshmallow

__all__ = []


if marshmallow:
    def _load_schema(schema, json):
        try:
            return schema.load(json)
        except marshmallow.exceptions.ValidationError as e:
            abort(400, e.messages)

    def schema_required(schema):
        """Validate body of the request against the schema.

        Abort with a status code 400 if the schema yields errors."""

        if isinstance(schema, type):
            schema = schema()

        def __inner(f):
            @functools.wraps(f)
            def __inner(*args, **kwargs):
                json = request.get_json(force=True)
                request.schema = _load_schema(schema, json)
                return f(*args, **kwargs)
            return __inner
        return __inner

    __all__.extend(["schema_required"])
