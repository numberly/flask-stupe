import os

from flask.config import Config as FlaskConfig


class Config(FlaskConfig):

    def from_env(self):
        """Try to overload the config with the environment"""

        # ramnes: we don't want DEBUG=0 to be casted as DEBUG=True
        def __str2bool(v):
            return bool(int(v))

        env_config = {}
        for key, value in self.items():
            if key in os.environ:
                cast = type(value)
                if cast is bool:
                    cast = __str2bool
                env_config[key] = cast(os.environ.get(key))
        self.update(env_config)
        return env_config


__all__ = ["Config"]
