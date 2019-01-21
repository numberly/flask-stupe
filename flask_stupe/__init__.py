# flake8: noqa
try:
    import bson
except ImportError:  # pragma: no cover
    bson = False

try:
    import dateutil
    import dateutil.parser
except ImportError:  # pragma: no cover
    dateutil = False

try:
    import marshmallow
except ImportError:  # pragma: no cover
    marshmallow = False

try:
    import pymongo
except ImportError:  # pragma: no cover
    pymongo = False

try:
    from pymongo.collation import Collation
except ImportError:  # pragma: no cover
    Collation = False

from flask_stupe.app import Stupeflask
from flask_stupe.validation import *
from flask_stupe.pagination import *
from flask_stupe.auth import *
from flask_stupe.inputs import *
