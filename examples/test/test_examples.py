"""Test the examples!"""
import json
from pathlib import Path

import pytest

from ..src import (
    accretion_builder,
    accretion_listener,
    hello_world,
    simple_choice,
    simple_map,
    simple_parallel,
    three_tasks,
)


def load_vector(module):
    vector = Path(module.__file__).parent / module.__file__.replace(".py", ".json")
    with vector.open("r") as raw_vector:
        return json.load(raw_vector)


@pytest.mark.parametrize(
    "module",
    (accretion_builder, accretion_listener, three_tasks, simple_choice, simple_map, simple_parallel, hello_world),
)
@pytest.mark.examples
def test_examples(module):
    expected = load_vector(module)

    test = module.build().to_dict()

    assert test == expected

    test_json = json.dumps(test, indent=4, sort_keys=True)
    expected_json = json.dumps(expected, indent=4, sort_keys=True)

    assert test_json == expected_json
