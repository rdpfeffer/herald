import json

import pytest
from jsonschema.exceptions import ValidationError

import schema


def test_validate_config():
    example_config = {
        "src/main/java*.java": {
            "alternate": "src/test/java/{}.java",
            "type": "source",
            "tasks": {"serial": ["ls -la", "echo something"]},
        },
        "src/test/java/*.java": {
            "alternate": "src/main/java/{}.java",
            "type": "test",
            "tasks": {"parallel": ["ls -la", "echo something"]},
        },
    }
    schema.validate(example_config)


def test_validate_bad_pattern():

    with pytest.raises(ValidationError):
        example_config = {
            "/": {
                "alternate": "src/main/java/{}.java",
                "type": "test",
                "tasks": {"parallel": ["ls -la", "echo something"]},
            }
        }
        schema.validate(example_config)


def test_validate_bad_tasks():

    with pytest.raises(ValidationError):
        example_config = {
            "src/main/java*.java": {
                "alternate": "src/main/java/{}.java",
                "type": "test",
                "tasks": {"XXXXX": ["ls -la", "echo something"]},
            }
        }
        schema.validate(example_config)
