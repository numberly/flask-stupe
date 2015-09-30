import re

from flask_stupe.validation import wtforms, marshmallow

__all__ = []

hexcolor_re = re.compile(r"^#[0-9a-f]{6}$")

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

    __all__.append("Color")


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
