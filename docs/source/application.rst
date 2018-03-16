Better application defaults
###########################

Stupeflask makes it easy to use JSON to build APIs. A perfect example is the
:class:`flask_stupe.json.Stupeflask` application.

Better support for JSON based APIs
==================================

Automatic conversion to JSON
----------------------------

By using the JSON version of Stupeflask, every Python object your views returns
that is not a :class:`Response` object will be JSON serialized. With that in
mind, you can do that kind of things:

.. code-block:: python

    @app.route("/foo")
    def foo():
        return {"foo": "bar"}


This will be rendered as the equivalent JSON and sent to the client.

Add JSON encoding for objects
-----------------------------

If you want to add serialization methods for other custom types, you can!
You'll need to call :meth:`JSONEncoder.add_rule()
<flask_stupe.json.JSONEncoder.add_rule>`.

.. code-block:: python

    import uuid
    app.json_encoder.add_rule(uuid.UUID, lambda uuid: str(uuid))


This snippet shows how to add a serializer for UUIDs.

Import all blueprints from a package
====================================

You can easily add a bunch of blueprints by passing a package to the
:meth:`Stupeflask.register_blueprints()
<flask_stupe.app.Stupeflask.register_blueprints>`. It will search through all
the package's modules and import a variable named like the module. If this is a
blueprint, it will be registered into the application.

For example, this snippet:

.. code-block:: python

    from application.views.user import user
    from application.views.pets import pets
    from application.views.family import family
    app.register_blueprint(user)
    app.register_blueprint(pets)
    app.register_blueprint(family)

Becomes:

.. code-block:: python

    from application import views
    app.register_blueprints(views)

Add path converters
===================

With Stupeflask, you can add path converters with
:meth:`Stupeflask.register_converter()
<flask_stupe.app.Stupeflask.register_converter>`.

Please head towards werkzeug's `documentation about converters`_ if you want to
learn more.

.. _`documentation about converters`: http://werkzeug.pocoo.org/docs/0.14/routing/#custom-converters
