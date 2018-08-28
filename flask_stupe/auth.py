import fnmatch
import functools

from flask import abort, request


def auth_required(function):
    """Decorator checking that the request is made by an authenticated user.

    If you want to use that function, you should set a before_request handler
    that authenticate requests when possible. It must then expose a `user`
    attribute on the :obj:`flask.request` object.

    .. code-block:: python

        @app.before_request
        def get_user():
            token = request.args.get("token")
            if verify_token(token):
                request.user = {"username": "toto"}

    A view decorated with :func:`auth_required` will be aborted with a status
    code 401 if the user making the request is not authenticated.
    """
    @functools.wraps(function)
    def __inner(*args, **kwargs):
        if not request.user:
            abort(401)
        return function(*args, **kwargs)
    return __inner


def permission_required(*permissions):
    """Decorator checking that the request is made by a user with adequate
    privileges.

    This decorator also decorates the function with the :func:`auth_required`
    doecorator, thus the same constraints apply here.

    If the :obj:`flask.request.user` is a dictionnary, it must contains a
    "permissions" key. If it is an object, it must have "permissions"
    attribute.

    These permissions must be a list of strings. They will be checked against
    the strings passed as parameter to this decorator. At least one must match.

    You can apply this decorator multiple times if you need several permissions
    at once to access a view.
    """
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
