import pytest

from herald import config, task

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


@pytest.fixture
def single_java_status_line_list():
    return [
            "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 src/main/java/foo.java"
        ]


@pytest.fixture
def missing_task_config():
    return config.ConfigurationMap(
        {
            "herald/**.py": {"alternate": "tests/{}_test.py", "type": "source"},
            "tests/**_test.py": {
                "alternate": "herald/{}.py",
                "type": "test",
                "tasks": {"serial": ["pytest {}"]},
            },
        }
    )


@pytest.fixture
def everything_exists_path():
    class Path:
        @staticmethod
        def segregate_nonexistent_files(filepaths):
            return filepaths, frozenset([])

    return Path()


@pytest.fixture
def nothing_exists_path():
    class Path:
        @staticmethod
        def segregate_nonexistent_files(filepaths):
            return frozenset([]), filepaths

    return Path()


@pytest.fixture
def test_doesnt_exist_path():
    class Path:
        @staticmethod
        def segregate_nonexistent_files(filepaths):
            return (
                frozenset([f for f in filepaths if "test" not in f]),
                frozenset([f for f in filepaths if "test" in f]),
            )

    return Path()


@pytest.fixture
def source_doesnt_exist_path():
    class Path:
        @staticmethod
        def segregate_nonexistent_files(filepaths):
            return (
                frozenset([f for f in filepaths if "test" in f]),
                frozenset([f for f in filepaths if "test" not in f]),
            )

    return Path()


@pytest.fixture
def foo_test_doesnt_exist_path():
    class Path:
        @staticmethod
        def segregate_nonexistent_files(filepaths):
            return (
                frozenset([f for f in filepaths if "foo" not in f or "test" not in f]),
                frozenset([f for f in filepaths if "foo" in f and "test" in f])
            )
    return Path()


@pytest.fixture
def basic_task_group():
    return task.TaskGroup(
        "src/main/java/*.java",
        "serial",
        ("ls -la", "echo something"),
        ["src/main/java/foo.java"]
    )
