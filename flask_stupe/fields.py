import re

from flask_stupe.validation import wtforms, marshmallow

__all__ = []

try:
    import bson
except ImportError:
    bson = False


if bson and wtforms:
    class ObjectIdField(wtforms.Field):
        widget = wtforms.widgets.TextInput()

        def process_formdata(self, values):
            try:
                self.data = bson.ObjectId(values[0])
            except bson.errors.InvalidId:
                raise wtforms.validators.ValidationError("Not a valid ObjectId.")

    __all__.append("ObjectIdField")


if marshmallow:
    hexcolor_re = re.compile(r"^#[0-9a-f]{6}$")

    class Color(marshmallow.fields.Field):
        default_error_messages = {
            "invalid": "Not a valid color."
        }

        def _deserialize(self, value, attr, data):
            try:
                value = value.lower()
            except AttributeError:
                self.fail("type")
            if not hexcolor_re.match(value):
                self.fail("invalid")
            return value

    class OneOf(marshmallow.fields.Field):
        default_error_messages = {
            "invalid": "Object type doesn't match any valid type"
        }

        def __init__(self, fields, *args, **kwargs):
            super(OneOf, self).__init__(*args, **kwargs)

            if not isinstance(fields, (list, tuple)):
                raise ValueError("Fields must be contained in a list or tuple")

            self.fields = []
            for field in fields:
                if isinstance(field, type):
                    if not issubclass(field, marshmallow.base.FieldABC):
                        raise ValueError("Fields types must subclass FieldABC")
                    self.fields.append(field())
                else:
                    if not isinstance(field, marshmallow.base.FieldABC):
                        raise ValueError("Fields must be FieldABC instances")
                    self.fields.append(field)

        def _deserialize(self, value, *args, **kwargs):
            for field in self.fields:
                try:
                    return field._deserialize(value, *args, **kwargs)
                except marshmallow.exceptions.ValidationError:
                    pass
            self.fail("invalid")

    __all__.extend(["Color", "OneOf"])


if bson and marshmallow:
    class ObjectId(marshmallow.fields.String):
        default_error_messages = {
            "invalid": "Not a valid ObjectId."
        }

        def _deserialize(self, value, attr, data):
            try:
                return bson.ObjectId(value)
            except TypeError:
                self.fail("type")
            except bson.errors.InvalidId:
                self.fail("invalid")

    __all__.append("ObjectId")
