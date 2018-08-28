import os

from flask_stupe.config import Config, _str2bool, _str2list


def test_str2bool():
    assert _str2bool("0") is False
    assert _str2bool("1") is True
    assert _str2bool("2") is True
    assert _str2bool("False") is False
    assert _str2bool("True") is True


def test_str2list():
    assert _str2list("foo,bar:baz") == ["foo", "bar:baz"]


def test_config_from_env():
    root_path = os.path.dirname(__file__)
    config = Config(root_path, {"TEST_BOOL": False, "TEST_LIST": []})
    assert not config.get("TEST_BOOL")
    assert not config.get("TEST_LIST")

    os.environ["TEST_BOOL"] = "1"
    config.from_env()
    assert config.from_env() == {"TEST_BOOL": True}
    assert config.get("TEST_BOOL") is True

    os.environ["TEST_LIST"] = "foo,bar:baz"
    config.from_env()
    assert config.get("TEST_LIST") == ["foo", "bar:baz"]

    assert "PATH" not in config
