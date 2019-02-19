from jsonschema import validate as _validate


def validate(instance):
    """Validate that the config is valid

    """
    schema = {
        "$id": "https://example.com/.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Projectionist",
        "description": "A configuration for projections.",
        "type": "object",
        "patternProperties": {
            "(\\\\?([^\\/]*[\\/])*)([^\\/]+)$": {
                "type": "object",
                "properties": {
                    "alternate": {"type": "string"},
                    "type": {"type": "string"},
                    "tasks": {
                        "oneOf": [
                            {
                                "type": "object",
                                "properties": {"parallel": {"type": "array"}},
                                "additionalProperties": False,
                            },
                            {
                                "type": "object",
                                "properties": {"serial": {"type": "array"}},
                                "additionalProperties": False,
                            },
                        ]
                    },
                },
                "required": ["type"],
            }
        },
        "additionalProperties": False,
    }
    _validate(instance=instance, schema=schema)
