===========
Flask-Stupe
===========

*a.k.a. « Flask on steroids »*

Flask-Stupe provides better defaults for APIs and more features. It is biased
towards marshmallow_ and MongoDB_ users, so more power to them.

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
    * Validate payload through marshmallow_ schemas
    * More marshmallow_ fields

Build the documentation
=======================

To build the documentation and view it in your browser, run these commands:

.. code-block:: bash

    pip install -r requirements.txt
    make -C docs html
    firefox docs/build/html/index.html

.. _marshmallow: https://marshmallow.readthedocs.io/en/latest/
.. _mongodb: https://www.mongodb.com/
