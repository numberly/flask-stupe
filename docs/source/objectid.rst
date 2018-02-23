Native ObjectId support
#######################

The `bson.ObjectId` type is natively supported by Stupeflask.

Path parameter
==============

Stupeflask recognizes ObjectIds in path parameters. You can use it like this:

.. code-block:: python

    @app.route("/user/<ObjectId:id>")

JSON
====

Any ObjectIds a in JSON response will be coerced to string automaticaly.

Marshmallow field
=================

Stupeflask features a field (:class:`~flask_stupe.fields.ObjectId`)
for ObjectIds.

If the `bson` module exists (for example if you're using MongoDB), you can
use it with :func:`~flask_stupe.validation.schema_required`. It allows to
automaticaly cast indicated fields from string to ObjectId.
