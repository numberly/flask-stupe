import functools
import fnmatch

from flask import abort, request


def auth_required(function):
    @functools.wraps(function)
    def __inner(*args, **kwargs):
        if not request.user:
            abort(403)
        return function(*args, **kwargs)
    return __inner


def permission_required(*permissions):
    def __decorator(function):
        @functools.wraps(function)
        def __inner(*args, **kwargs):
            if isinstance(request.user, dict):
                user_permissions = request.user.get("permissions", [])
            else:
                user_permissions = getattr(request.user, "permissions", [])

            for user_group in user_permissions:
                if fnmatch.filter(permissions, user_group):
                    return function(*args, **kwargs)
            abort(403)
        return auth_required(__inner)
    return __decorator


__all__ = ["auth_required", "permission_required"]
