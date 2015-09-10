__all__ = []

try:
    from bson import ObjectId
    from wtforms import Field
    from wtforms.validators import ValidationError
    from wtforms.widgets import TextInput

    class ObjectIdField(Field):
        widget = TextInput()

        def process_formdata(self, values):
            try:
                self.data = ObjectId(values[0])
            except:
                raise ValidationError("Not a valid ObjectId.")

    __all__.append("ObjectIdField")
except ImportError:
    pass
