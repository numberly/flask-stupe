.. image:: artwork/stupeflask.png
    :target: https://youtu.be/PdaAHMztNVE

*a.k.a. « Flask on steroids »*

An opinionated Flask extension designed by and for web developers to reduce
boilerplate code when working with Marshmallow, MongoDB and/or JSON.

Features
========

* Powerful configuration management
* Return any object type in views; It will be coerced to `flask.Response`
* Add JSON converters for custom types
* Validate payloads through marshmallow_ schemas
* ObjectId native support
* Fetch blueprints from a whole module
* Decorators to handle authentifications and permissions

Comparison
==========

Here is a comparison between the efficiency of a Stupeflask and a simple Flask
applications. Both have the same behaviour. They rely on MongoDB, hangles input
and output in JSON and allow to create an user, as well as retrieving a user,
by its *id*.

+-------------------------------------------------+-------------------------------------------------+
| **Stupeflask**                                  | **Bare Flask**                                  |
+-------------------------------------------------+-------------------------------------------------+
| .. literalinclude:: examples/user_api_stupe.py  | .. literalinclude:: examples/user_api_flask.py  |
+-------------------------------------------------+-------------------------------------------------+

.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _MongoDB: https://www.mongodb.com/
