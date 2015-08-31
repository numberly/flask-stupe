import os

from flask.config import Config as FlaskConfig


class Config(FlaskConfig):

    def from_env(self):
        """Try to overload the config with the environment."""
        env_config = {}
        for key, value in self.items():
            if key in os.environ:
                env_config[key] = type(value)(os.environ.get(key))
        self.update(env_config)
        return env_config


__all__ = ["Config"]
