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

    class Nested(marshmallow.fields.Nested):
        """An overloaded Nested field that can handle more than a single schema

        By giving it a list of schemas, it will iterate through them to find one
        that matches with the input data. It raises an error if the data doesn't
        correspond to any schema.
        """

        def _deserialize(self, value, attr, data):
            try:
                return super(Nested, self)._deserialize(value, attr, data)
            except ValueError:
                if isinstance(self.nested, (list, tuple)):
                    for schema in self.nested:
                        if isinstance(schema, type):
                            schema = schema()
                        data, errors = schema.load(value)
                        if not errors:
                            return data
                    self.fail("validator_failed")
                raise

    __all__.extend(["Color", "Nested"])


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
