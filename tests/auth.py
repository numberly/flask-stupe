from flask import request

from flask_stupe.auth import auth_required, permission_required


def test_auth_required(app, client):
    @app.before_request
    def set_user():
        from flask import request
        request.user = request.args.get("user")

    @app.route("/foo")
    @auth_required
    def foo():
        return "bar"

    assert client.get("/foo").status_code == 401
    assert client.get("/foo?user=1").status_code == 200


def get_permissions():
    permissions = request.args.get("permissions", [])
    if permissions:
        return permissions.split(',')
    return []


def test_permission_required(app, client):
    @app.before_request
    def set_user():
        request.user = dict(permissions=get_permissions())

    @app.route("/foo")
    @permission_required("vip", "secret_stuff")
    def foo():
        return "bar"

    assert client.get("/foo").status_code == 403
    assert client.get("/foo?permissions=user").status_code == 403
    assert client.get("/foo?permissions=user,vip").status_code == 200
    assert client.get("/foo?permissions=user,secret_*").status_code == 200
    assert client.get("/foo?permissions=user,*_stuff").status_code == 200


def test_permission_required_with_user_object(app, client):
    class User(object):
        pass

    @app.before_request
    def set_user():
        request.user = User()
        request.user.permissions = get_permissions()

    @app.route("/foo")
    @permission_required("vip", "secret_stuff")
    def foo():
        return "bar"

    assert client.get("/foo").status_code == 403
    assert client.get("/foo?permissions=vip").status_code == 200
