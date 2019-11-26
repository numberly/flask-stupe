import functools
from collections import OrderedDict

from flask import request

from flask_stupe import pymongo

__all__ = []


if pymongo:

    def _get_pagination_links(skip, limit, total_count=None):
        template = "{}?limit={}&skip={{skip}}".format(request.base_url, limit)
        links = OrderedDict([
            ("self", template.format(skip=skip)),
            ("first", template.format(skip=0))
        ])
        prev_skip = skip - limit
        if prev_skip >= 0:
            links.update(prev=template.format(skip=prev_skip))
        next_skip = skip + limit
        if next_skip < total_count:
            links.update(next=template.format(skip=next_skip))
        if total_count:
            links.update(last=template.format(skip=total_count - limit))
        return links

    def _paginate(cursor, skip=None, limit=None, sort=None, count=True):
        total_count = None
        if count:
            total_count = cursor.count()
        links = None
        if limit:
            links = _get_pagination_links(skip or 0, limit, total_count)

        headers = getattr(request, "response_headers", None)
        if isinstance(headers, dict):
            if total_count:
                headers["X-Total-Count"] = total_count
            if links:
                header_links = []
                for name, link in links.items():
                    header_links.append('<{}>; rel="{}"'.format(link, name))
                headers["Link"] = ", ".join(header_links)

        metadata = getattr(request, "metadata", None)
        if isinstance(metadata, dict):
            if total_count:
                metadata.update(count=total_count)
            if links:
                metadata.update(links=links)

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
