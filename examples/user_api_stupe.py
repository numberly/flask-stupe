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
