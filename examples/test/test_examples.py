"""Test the examples!"""
import json
from importlib import import_module
from pathlib import Path

import pytest


def find_tests():
    test_src = Path(__file__).parent.parent / "src"
    for testfile in test_src.iterdir():
        if testfile.suffix == ".py" and testfile.stem != "__init__":
            module_name = testfile.stem
            module = import_module(f"..src.{module_name}", __spec__.name.rsplit(".", 1)[0])
            yield pytest.param(module, id=module_name)


def load_vector(module):
    vector = Path(module.__file__).parent / module.__file__.replace(".py", ".json")
    with vector.open("r") as raw_vector:
        return json.load(raw_vector)


@pytest.mark.parametrize(
    "module", find_tests(),
)
@pytest.mark.examples
def test_examples(module):

    expected = load_vector(module)

    test = module.build().to_dict()

    assert test == expected

    test_json = json.dumps(test, indent=4, sort_keys=True)
    expected_json = json.dumps(expected, indent=4, sort_keys=True)

    assert test_json == expected_json
