.. image:: artwork/stupeflask.png
    :target: https://youtu.be/PdaAHMztNVE

*a.k.a. « Flask on steroids »*

An opinionated Flask extension designed by and for web developers who want
better defaults for MongoDB_, marshmallow_ and/or crafting JSON APIs.

Features
========

Better defaults
---------------

* Easier to set configuration
* Wrap objects returned by views in a Response

ObjectId support
----------------

* Optional JSON output
* Route converter (eg. */user/<ObjectId>*)
* marshmallow_ field

Additionnal features
--------------------

* Add JSON converters
* Fetch blueprints from a whole module
* Validate payloads through marshmallow_ schemas
* More marshmallow_ fields

.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _MongoDB: https://www.mongodb.com/
