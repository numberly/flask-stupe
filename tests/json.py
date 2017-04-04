import json
import pytest
from datetime import date, datetime

from flask_stupe.json import encode, encoder_rules, JSONEncoder

original_rules = encoder_rules[:]


@pytest.fixture(autouse=True)
def clean_encoder_rules():
    del encoder_rules[:]
    encoder_rules.extend(original_rules)


class Foo:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

rule = (Foo, str)


def test_encode(monkeypatch):
    assert isinstance(encode(datetime.utcnow()), str)
    assert isinstance(encode(date.today()), str)

    assert isinstance(encode(Foo("bar")), Foo)
    with pytest.raises(TypeError):
        encode(Foo("bar"), silent=False)

    encoder_rules.append(rule)
    assert encode(Foo("bar")) == "bar"


def test_encoder():
    with pytest.raises(TypeError):
        json.dumps(Foo("bar"), cls=JSONEncoder)
    JSONEncoder.add_rule(*rule)
    assert json.dumps(Foo("bar"), cls=JSONEncoder) == '"bar"'
