.. Stupeflask documentation master file, created by
   sphinx-quickstart on Sat Feb 10 19:11:24 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stupeflask's documentation!
=======================================

*a.k.a. « Flask on steroids »*

An opinionated Flask extension designed by and for web developers who want
better defaults for MongoDB, Marshmallow and/or crafting JSON APIs.


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
    * Marshmallow_ field

Additionnal features
--------------------

    * Add JSON converters
    * Fetch blueprints from a whole module
    * Validate payloads through marshmallow_ schemas
    * More marshmallow_ fields


Summary
=======

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   application
   config
   objectid
   reference
   showcase


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _mongodb: https://www.mongodb.com/
