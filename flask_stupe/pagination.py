import functools

from flask import request

try:
    import pymongo
except ImportError:  # pragma: no cover
    pymongo = False

__all__ = []


if pymongo:
    def _paginate(cursor, skip=None, limit=None, sort=None):
        skip = request.args.get("skip", skip, type=int)
        if skip is not None:
            cursor.skip(skip)
        limit = request.args.get("limit", limit, type=int)
        if limit is not None:
            cursor.limit(limit)

        sort = request.args.get("sort", sort)
        if sort:
            if not isinstance(sort, list):
                sort = sort.split(",")
            for index, item in enumerate(sort):
                if isinstance(item, str):
                    if item.startswith("-"):
                        item = (item[1:], pymongo.DESCENDING)
                        sort[index] = item
                if not isinstance(item, tuple):
                    sort[index] = (item, pymongo.ASCENDING)
            cursor.sort(sort)
        return cursor

    def paginate(function_or_cursor=None, skip=None, limit=None, sort=None):
        """Apply pagination to the given cursor or function"""
        if isinstance(function_or_cursor, pymongo.cursor.Cursor):
            return _paginate(function_or_cursor, skip, limit, sort)

        def __decorator(function):
            @functools.wraps(function)
            def __wrapper(*args, **kwargs):
                return _paginate(function(*args, **kwargs), skip, limit, sort)
            return __wrapper

        if function_or_cursor:
            return __decorator(function_or_cursor)
        return __decorator

    __all__.append("paginate")
