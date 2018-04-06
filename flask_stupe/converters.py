from werkzeug.routing import BaseConverter

from flask_stupe import bson

converters = []


if bson:
    class ObjectIdConverter(BaseConverter):
        regex = r'[A-Fa-f0-9]{24}'

        def to_python(self, value):
            return bson.ObjectId(value)

        def to_url(self, value):
            return str(value)

    converters.append(ObjectIdConverter)

__all__ = [converter.__name__ for converter in converters]
