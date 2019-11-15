"""Helpers for unit test suites."""
import json
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Dict

HERE = Path(__file__).parent
VECTORS_DIR = HERE / ".." / "vectors"


class VectorTypes(Enum):
    def __init__(self, friendly_name: str, directory: Path):
        self.friendly_name = friendly_name
        self.directory = directory

    STATE_MACHINE = ("state machine", VECTORS_DIR / "state-machines")
    STATE = ("state", VECTORS_DIR / "states")
    CHOICE_RULE = ("choice rule", VECTORS_DIR / "choice-rules")


def _get_vector(vector_type: VectorTypes, vector_name: str) -> Dict:
    filepath = vector_type.directory / f"{vector_name}.json"

    if not filepath.is_file():
        raise FileNotFoundError(f"Unable to locate {vector_type.friendly_name} vector {vector_name}.json")

    with filepath.open("r") as vector:
        return json.load(vector)


state_machine_body = partial(_get_vector, VectorTypes.STATE_MACHINE)
state_body = partial(_get_vector, VectorTypes.STATE)
choice_rule_body = partial(_get_vector, VectorTypes.CHOICE_RULE)


def load_and_test_vectors(loader, *, kind, name, value):
    all_expected = loader(kind)
    expected = all_expected[name]

    actual = value.to_dict()

    assert actual == expected
