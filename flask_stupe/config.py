import ast
import os

from flask.config import Config as FlaskConfig


# ramnes: we don't want DEBUG=0 to be casted as DEBUG=True
def _str2bool(v):
    return bool(ast.literal_eval(v))


def _str2list(v):
    return v.split(",")


class Config(FlaskConfig):

    def from_env(self):
        """Try to overload the config with the environment"""
        env_config = {}
        for key, value in self.items():
            if key in os.environ:
                cast = type(value)
                if cast is bool:
                    cast = _str2bool
                elif cast is list:
                    cast = _str2list
                env_config[key] = cast(os.environ.get(key))
        self.update(env_config)
        return env_config


__all__ = ["Config"]
