.. image:: artwork/stupeflask.png
    :target: https://youtu.be/PdaAHMztNVE

*a.k.a. « Flask on steroids »*

An opinionated Flask extension designed by and for web developers who want
better defaults and tools for MongoDB_, marshmallow_ and/or crafting JSON APIs.

Features
========

Better defaults
---------------

* Easier to override configuration with environment
* Return any object type

ObjectId support
----------------

* Automatic JSON serialization
* Route converter (eg. */user/<ObjectId:id>*)
* marshmallow_ field

Additionnal features
--------------------

* Add JSON converters for custom types
* Fetch blueprints from a whole module
* Validate payloads through marshmallow_ schemas
* More marshmallow_ fields

.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _MongoDB: https://www.mongodb.com/
