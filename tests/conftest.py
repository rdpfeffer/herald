import pytest

from herald import config

from .context import herald


@pytest.fixture
def basic_config():
    return config.ConfigurationMap(
        {
            "src/main/java/*.java": {
                "alternate": "src/test/java/{}.java",
                "type": "source",
                "tasks": {"serial": ["ls -la", "echo something"]},
            },
            "src/test/java/*.java": {
                "alternate": "src/main/java/{}.java",
                "type": "test",
                "tasks": {"parallel": ["wc -l", "echo test"]},
            },
        }
    )


@pytest.fixture
def basic_status_lines():
    return [
        "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 herald/cli.py"
    ]
