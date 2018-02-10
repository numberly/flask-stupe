Showcase
########

A demonstration of the efficiency of Stupeflask in certain use cases with a
side by side comparison.

Stupeflask
==========

.. code-block:: python

    import json

    from flask import request
    from flask_stupe import schema_required
    from flask_stupe.json import Stupeflask
    from marshmallow import Schema
    from marshmallow.fields import String
    from pymongo import MongoClient

    app = Stupeflask(__name__)
    client = MongoClient()
    users = client.test_db.users


    class UserSchema(Schema):
        username = String(required=True)
        password = String()


    @app.route("/user", methods=["POST"])
    @schema_required(UserSchema())
    def post_user():
        result = users.insert_one(request.schema)
        request.schema.update(_id=result.inserted_id)
        return request.schema


    @app.route("/user/<ObjectId:id>")
    def get_user(id):
        return users.find_one({"_id": id})


    if __name__ == '__main__':
        client = app.test_client()
        data = json.dumps({"username": "Trotro", "password": "rigolo"})
        response = client.post("/user", data=data)
        response = json.loads(response.get_data().decode("utf-8"))
        userid = response.get("data", {}).get("_id")
        response2 = client.get("/user/" + userid)
        assert response2.status_code == 200

Flask
=====

.. code-block:: python

    import json

    from bson import ObjectId
    from flask import abort, request
    from flask_stupe import schema_required
    from flask_stupe.json import Stupeflask
    from marshmallow import Schema
    from marshmallow.fields import String
    from pymongo import MongoClient

    app = Stupeflask(__name__)
    client = MongoClient()
    users = client.test_db.users


    class UserSchema(Schema):
        username = String(required=True)
        password = String()


    @app.route("/user", methods=["POST"])
    @schema_required(UserSchema())
    def post_user():
        json = request.get_json(force=True)
        validation_result = UserSchema().load(json)
        if validation_result.errors:
            abort(400, validation_result.errors)
        result = users.insert_one(validation_result.data)
        validation_result.data.update(_id=str(result.inserted_id))
        return validation_result.data


    @app.route("/user/<id>")
    def get_user(id):
        try:
            id = ObjectId(id)
        except ValueError:
            abort(404)
        user = users.find_one({"_id": id})
        user["_id"] = str(user["_id"])
        return user


    if __name__ == '__main__':
        client = app.test_client()
        data = json.dumps({"username": "Trotro", "password": "rigolo"})
        response = client.post("/user", data=data)
        response = json.loads(response.get_data().decode("utf-8"))
        userid = response.get("data", {}).get("_id")
        response2 = client.get("/user/" + userid)
        assert response2.status_code == 200
