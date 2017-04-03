import pytest

from flask_stupe.app import Stupeflask


@pytest.fixture
def app():
    return Stupeflask(__name__)
