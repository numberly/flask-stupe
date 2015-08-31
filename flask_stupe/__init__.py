import os
from pkgutil import iter_modules

from flask import Flask

from flask_stupe.config import Config
from flask_stupe.converters import converters
from flask_stupe.logging import log


class Stupeflask(Flask):

    def __init__(self, *args, **kwargs):
        super(Stupeflask, self).__init__(*args, **kwargs)
        config_path = os.path.join(os.getcwd(), "config.py")
        log.info(" * Loading default config ({})".format(config_path))
        self.config.from_pyfile(config_path, silent=True)
        log.info(" * Loading $CONFIG ({})".format(os.environ.get("CONFIG")))
        self.config.from_envvar("CONFIG", silent=True)
        from_env = self.config.from_env()
        log.info(" * Config from environment: {}".format(from_env))
        self.register_converters(converters)

    # ramnes: TODO: replace this by `Stupeflask.config_class = Config` when
    # Flask 1.0 is out (here we're just rewriting a `Flask` method to use our
    # own Config class)
    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

    def register_converter(self, converter, name=None):
        """Register a new converter that can be used in endpoints URLs.

        A converter is a Werkzeug class that transform a part of an URL to a
        Python object, passed as an argument to the endpoint function.

        Stupeflask currently implement the following converters:
        - /<ObjectId>/ with ::ObjectIdConverter

        See `Werkzeug documentation about custom converters
        <http://werkzeug.pocoo.org/docs/0.10/routing/#custom-converters>`_
        if you want to implement your own converter.
        """
        if not name:
            name = converter.__name__
            if "Converter" in name:
                name = converter.__name__.replace("Converter", "")
        self.url_map.converters[name] = converter

    def register_converters(self, converter_list):
        """Register multiple converters at once.

        See :meth:`register_converter`.
        """
        for converter in converter_list:
            self.register_converter(converter)

    def register_blueprints(self, package):
        """Auto-discover blueprints and register them.

        It will look recursively in every module of the package to find a variable
        that has the same name as its module.

        It means that if a file called `foo.py` has an exportable variable called
        `foo`, it will try to register that variable as a blueprint.
        """
        prefix = package.__name__ + '.'
        for importer, name, is_pkg in iter_modules(package.__path__, prefix):
            module = importer.find_module(name).load_module(name)
            blueprint_name = name.rsplit('.')[-1]
            if is_pkg:
                self.register_blueprints(module)
            elif hasattr(module, blueprint_name):
                log.info(' * Registering blueprint {}'.format(name))
                self.register_blueprint(getattr(module, blueprint_name))
