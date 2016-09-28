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

    class Color(marshmallow.fields.String):
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

    currencies = ("ADF", "ADP", "AED", "AFA", "AFN", "ALL", "AMD", "ANG", "AOA",
                  "AOK", "AON", "AOR", "ARP", "ARS", "ATS", "AUD", "AWG", "AZM",
                  "AZN", "BAM", "BBD", "BDT", "BEF", "BGL", "BGN", "BHD", "BIF",
                  "BMD", "BND", "BOB", "BOP", "BOV", "BRL", "BRR", "BSD", "BTN",
                  "BWP", "BYB", "BYN", "BYR", "BZD", "CAD", "CDF", "CHE", "CHF",
                  "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CSD", "CSK",
                  "CUC", "CUP", "CVE", "CYP", "CZK", "DEM", "DJF", "DKK", "DOP",
                  "DZD", "ECS", "ECV", "EEK", "EGP", "ERN", "ESP", "ETB", "EUR",
                  "FIM", "FJD", "FKP", "FRF", "GBP", "GEL", "GHS", "GIP", "GMD",
                  "GNF", "GRD", "GTQ", "GWP", "GYD", "HKD", "HNL", "HRK", "HTG",
                  "HUF", "IDR", "IEP", "ILS", "INR", "IQD", "IRR", "ISK", "ITL",
                  "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW",
                  "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTL",
                  "LUF", "LVL", "LVR", "LYD", "MAD", "MDL", "MGA", "MGF", "MKD",
                  "MMK", "MNT", "MOP", "MRO", "MTL", "MUR", "MVR", "MWK", "MXN",
                  "MXV", "MYR", "MZE", "MZM", "MZN", "NAD", "NGN", "NHF", "NIC",
                  "NIO", "NLG", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PES",
                  "PGK", "PHP", "PKR", "PLN", "PLZ", "PTE", "PYG", "QAR", "ROL",
                  "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDD", "SDG",
                  "SDP", "SEK", "SGD", "SHP", "SIT", "SKK", "SLL", "SML", "SOS",
                  "SRD", "SSP", "STD", "SUB", "SUR", "SVC", "SYP", "SZL", "THB",
                  "TJS", "TMM", "TMT", "TND", "TOP", "TPE", "TRL", "TRY", "TTD",
                  "TWD", "TZS", "UAH", "UGX", "USD", "USN", "USS", "UYU", "UZS",
                  "VAL", "VEB", "VEF", "VND", "VUV", "WST", "XAF", "XAG", "XAU",
                  "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XEU", "XFO", "XFU",
                  "XOF", "XPD", "XPF", "XPT", "YER", "YUD", "YUM", "ZAR", "ZMK",
                  "ZWD", "ZWL", "ZWR")

    class Currency(marshmallow.fields.String):
        default_error_messages = {
            "invalid": "Not a valid currency."
        }

        def _deserialize(self, value, attr, data):
            try:
                value = value.upper()
            except AttributeError:
                self.fail("type")
            if value not in currencies:
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

    __all__.extend(["Color", "Currency", "OneOf"])


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
