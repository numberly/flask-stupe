Easier collection of configuration values
#########################################

Stupeflask makes it easier to collect configuration variables from different
sources.

config.py
=========

If a file named `config.py` is present in the working directory, it will be
imported and used as the configuration file for your application.

$CONFIG
=======

If an environment variable named `CONFIG` exists, its value will be imported as
a Python configuration file.

Environment
===========

Any key present in the documentation at this point will be checked in the
environment. If a corresponding variable is found in the environment, its value
will override the current configuration.

Since all environment variables are strings, the value will be cast in the type
of the value present in the configuration in the first place.

Let's say you have a variable like so in the config.py file:

.. code-block:: python

    DEBUG = True

You can override it by putting that in the environment:

.. code-block:: python

    DEBUG=1

In your code, it will not be treated a string or an integer, but as `True`,
because Stupeflask will have detected that it was a boolean and cast it.
