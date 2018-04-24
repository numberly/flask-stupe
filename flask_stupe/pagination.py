import functools

from flask import request

from flask_stupe import pymongo

__all__ = []


if pymongo:
    def _paginate(cursor, skip=None, limit=None, sort=None, count=True):
        metadata = getattr(request, "metadata", None)
        if count and isinstance(metadata, dict):
            metadata.update(count=cursor.count())

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

    def paginate(function_or_cursor=None, skip=None, limit=None, sort=None,
                 count=True):
        """Apply pagination to the given MongoDB cursor or function"""
        if isinstance(function_or_cursor, pymongo.cursor.Cursor):
            return _paginate(function_or_cursor, skip, limit, sort, count)

        def __decorator(function):
            @functools.wraps(function)
            def __wrapper(*args, **kwargs):
                cursor = function(*args, **kwargs)
                return _paginate(cursor, skip, limit, sort, count)
            return __wrapper

        if function_or_cursor:
            return __decorator(function_or_cursor)
        return __decorator

    __all__.append("paginate")
