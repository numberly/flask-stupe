from flask import request

try:
    import pymongo
except ImportError:
    pymongo = False

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = False

__all__ = []


if pymongo or sqlalchemy:
    def paginate(cursor, skip=None, limit=None):
        """Apply pagination to the given cursor"""
        skip = request.args.get("skip", skip)
        if skip is not None:
            cursor = cursor.skip(int(skip))
        limit = request.args.get("limit", limit)
        if limit is not None:
            cursor = cursor.limit(int(limit))
        return cursor

    __all__.append("paginate")
