from bson import ObjectId
from flask import abort, Flask, jsonify, request
from marshmallow import Schema
from marshmallow.fields import String
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
users = client.test_db.users


class UserSchema(Schema):
    username = String(required=True)
    password = String()


@app.route("/user", methods=["POST"])
def post_user():
    json = request.get_json(force=True)
    validation_result = UserSchema().load(json)
    if validation_result.errors:
        abort(400, validation_result.errors)
    result = users.insert_one(validation_result.data)
    inserted_id = str(result.inserted_id)
    validation_result.data.update(_id=inserted_id)
    return jsonify(validation_result.data)


@app.route("/user/<id>")
def get_user(id):
    try:
        id = ObjectId(id)
    except ValueError:
        abort(404)
    user = users.find_one({"_id": id})
    user["_id"] = str(user["_id"])
    return jsonify(user)
