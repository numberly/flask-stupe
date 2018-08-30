.. image:: https://raw.githubusercontent.com/numberly/flask-stupe/master/artwork/stupeflask.png
   :target: https://youtu.be/PdaAHMztNVE

|

.. image:: https://img.shields.io/pypi/v/flask-stupe.svg
   :target: https://pypi.python.org/pypi/Flask-Stupe
.. image:: https://img.shields.io/github/license/numberly/flask-stupe.svg
   :target: https://github.com/numberly/flask-stupe/blob/master/LICENSE
.. image:: https://img.shields.io/travis/numberly/flask-stupe.svg
   :target: https://travis-ci.org/numberly/flask-stupe
.. image:: https://img.shields.io/coveralls/numberly/flask-stupe.svg
   :target: https://coveralls.io/github/numberly/flask-stupe
.. image:: https://readthedocs.org/projects/flask-stupe/badge
   :target: http://flask-stupe.readthedocs.io

|

*a.k.a. « Flask on steroids »*

An opinionated Flask extension designed by and for web developers to reduce
boilerplate code when working with Marshmallow, MongoDB and/or JSON.

Documentation: https://flask-stupe.readthedocs.io


Features
========

* Return any object type in views, and it will be coerced to a
  :code:`flask.Response`
* Validate payloads through marshmallow_ schemas
* Easily add JSON converters for any custom type
* Fetch all the blueprints from a whole module in one line
* Native ObjectId support
* Powerful configuration management
* Decorators to handle authentication, permissions, and pagination
* 100% coverage and no dependency


Comparison
==========

Here is a comparison of a bare Flask application and its equivalent Stupeflask
version. They both rely on MongoDB, handle input and output in JSON, and allow
to create a user and retrieve one or more.

+--------------------------------------------------------+-----------------------------------------------------+
| **Bare Flask**                                         | **With Stupeflask**                                 |
+--------------------------------------------------------+-----------------------------------------------------+
|.. code-block:: python                                  |.. code-block:: python                               |
|                                                        |                                                     |
|  from bson import ObjectId                             |  from flask import request                          |
|  from flask import abort, Flask, jsonify, request      |  from flask_stupe import paginate, schema_required  |
|  from marshmallow import Schema                        |  from flask_stupe.json import Stupeflask            |
|  from marshmallow.fields import String                 |  from marshmallow import Schema                     |
|  from pymongo import MongoClient                       |  from marshmallow.fields import String              |
|                                                        |  from pymongo import MongoClient                    |
|  app = Flask(__name__)                                 |                                                     |
|  users = MongoClient().database.users                  |  app = Stupeflask(__name__)                         |
|                                                        |  users = MongoClient().database.users               |
|                                                        |                                                     |
|  class UserSchema(Schema):                             |                                                     |
|      username = String(required=True)                  |  class UserSchema(Schema):                          |
|      password = String()                               |      username = String(required=True)               |
|                                                        |      password = String()                            |
|                                                        |                                                     |
|  @app.route("/user", methods=["POST"])                 |                                                     |
|  def post_user():                                      |  @app.route("/user", methods=["POST"])              |
|      json = request.get_json(force=True)               |  @schema_required(UserSchema())                     |
|      validation_result = UserSchema().load(json)       |  def post_user():                                   |
|      if validation_result.errors:                      |      result = users.insert_one(request.schema)      |
|          abort(400, validation_result.errors)          |      request.schema.update(_id=result.inserted_id)  |
|      result = users.insert_one(validation_result.data) |      return request.schema                          |
|      inserted_id = str(result.inserted_id)             |                                                     |
|      validation_result.data.update(_id=inserted_id)    |                                                     |
|      return jsonify(validation_result.data)            |  @app.route("/user/<ObjectId:id>")                  |
|                                                        |  def get_user(id):                                  |
|                                                        |      return users.find_one({"_id": id})             |
|  @app.route("/user/<id>")                              |                                                     |
|  def get_user(id):                                     |                                                     |
|      try:                                              |  @app.route("/users")                               |
|          id = ObjectId(id)                             |  @paginate(limit=100)                               |
|      except ValueError:                                |  def get_users():                                   |
|          abort(404)                                    |      return users.find()                            |
|      user = users.find_one({"_id": id})                |                                                     |
|      user["_id"] = str(user["_id"])                    |                                                     |
|      return jsonify(user)                              |                                                     |
|                                                        |                                                     |
|                                                        |                                                     |
|  @app.route("/users")                                  |                                                     |
|  def get_users():                                      |                                                     |
|      limit = request.args.get("limit", 100, type=int)  |                                                     |
|      skip = request.args.get("skip", 0, type=int)      |                                                     |
|      cursor = users.find().limit(limit).skip(skip)     |                                                     |
|      return jsonify(list(cursor))                      |                                                     |
+--------------------------------------------------------+-----------------------------------------------------+


.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _MongoDB: https://www.mongodb.com/
