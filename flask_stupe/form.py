__all__ = []

try:
    from flask import abort
    from flask.ext.wtf import Form as BaseForm

    class Form(BaseForm):

        def validate(self):
            valid = super(Form, self).validate()
            if not valid:
                abort(400, self.errors)
            return valid

    __all__.append("Form")
except ImportError:
    pass
