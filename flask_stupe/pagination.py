from flask import request

try:
    import pymongo
except ImportError:
    pymongo = False

__all__ = []


if pymongo:
    def paginate(cursor, skip=None, limit=None, sort=None):
        """Apply pagination to the given cursor"""
        skip = request.args.get("skip", skip, type=int)
        if skip is not None:
            cursor = cursor.skip(skip)
        limit = request.args.get("limit", limit, type=int)
        if limit is not None:
            cursor = cursor.limit(limit)

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

    __all__.append("paginate")
