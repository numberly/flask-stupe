import functools

from flask import abort, request

__all__ = []

try:
    import marshmallow
except ImportError:  # pragma: no cover
    marshmallow = False


if marshmallow:
    def unrequire(schema_or_field):
        if isinstance(schema_or_field, marshmallow.fields.List):
            unrequire(schema_or_field.container)
        elif isinstance(schema_or_field, marshmallow.fields.Nested):
            unrequire(schema_or_field.schema)
        elif isinstance(schema_or_field, marshmallow.Schema):
            for field in schema_or_field.fields.values():
                unrequire(field)
        if isinstance(schema_or_field, marshmallow.fields.Field):
            schema_or_field.required = False

    class Schema(marshmallow.Schema):

        def __init__(self, *args, **kwargs):
            _unrequire = kwargs.pop("unrequire", False)
            super(Schema, self).__init__(*args, **kwargs)

            if _unrequire:
                unrequire(self)

    def schema_required(schema):
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

    __all__.extend(["unrequire", "Schema", "schema_required"])
