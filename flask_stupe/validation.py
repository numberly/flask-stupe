import functools

from flask import abort, request

from flask_stupe import marshmallow

__all__ = []


if marshmallow:
    def schema_required(schema):
        """Validate body of the request against the schema.

        Abort with a status code 400 if the schema yields errors."""
        def __inner(f):
            @functools.wraps(f)
            def __inner(*args, **kwargs):
                json = request.get_json(force=True)
                results = schema.load(json)
                if results.errors:
                    abort(400, results.errors)
                request.schema = results.data
                return f(*args, **kwargs)
            return __inner
        return __inner

    __all__.extend(["schema_required"])
