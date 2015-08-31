from werkzeug.routing import BaseConverter

converters = []

try:
    from bson import ObjectId

    class ObjectIdConverter(BaseConverter):
        regex = r'[A-Fa-f0-9]{24}'

        def to_python(self, value):
            return ObjectId(value)

        def to_url(self, value):
            return str(value)

    converters.append(ObjectIdConverter)
except ImportError:
    pass

__all__ = [converter.__name__ for converter in converters]
