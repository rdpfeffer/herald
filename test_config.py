import pytest

import config
import executor
import task


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


def test_executor_creation_serial():
    config_map = config.ConfigurationMap({})
    serial_exec = config_map._executor_for_name("serial")
    assert isinstance(serial_exec, executor.SerialExecutor)


def test_executor_creation_parallel():
    config_map = config.ConfigurationMap({})
    serial_exec = config_map._executor_for_name("parallel")
    assert isinstance(serial_exec, executor.ParallelExecutor)


def test_executor_creation_internal_error():
    config_map = config.ConfigurationMap({})
    with pytest.raises(config.InternalExecutorError):
        serial_exec = config_map._executor_for_name("bananas")


def test_task_group_for_task_entry():
    config_map = config.ConfigurationMap({})
    task_group = config_map._task_group_for_task_entry(
        "parallel", {"parallel": ["foo"]}, "a/b/c.txt"
    )
    assert isinstance(task_group, task.TaskGroup)


def test_map_filepath_to_config_entries(basic_config):
    entries = basic_config._map_filepath_to_config_entries("src/main/java/foo.java")
    assert entries == [
        (
            "src/main/java/*.java",
            {
                "alternate": "src/test/java/{}.java",
                "type": "source",
                "tasks": {"serial": ["ls -la", "echo something"]},
            },
        )
    ]


def test_map_filepath_to_task_data_entries(basic_config):
    entries = basic_config._map_filepath_to_task_data_entries("src/main/java/foo.java")
    assert entries == [{"serial": ["ls -la", "echo something"]}]


def test_get_all_task_groups_for_filepaths(basic_config):
    task_groups = basic_config.get_all_task_groups_for_filepaths(
        ["src/main/java/foo.java"]
    )
    assert len(task_groups) == 1
    for task_group in task_groups:
        assert task_group._tasks == ("ls -la", "echo something")


def test_alternate_matching(basic_config):
    config_map = config.ConfigurationMap
    cases = [
        (
            "src/main/*.java",
            "src/test/{}.java",
            "src/main/foo.java",
            "src/test/foo.java",
        )
    ]
    for pattern, altenate_format, filepath, alternate in cases:
        assert (
            config_map._compute_alternate(pattern, altenate_format, filepath)
            == alternate
        )


def test_first_special_char():
    config_map = config.ConfigurationMap
    cases = [("a/b/*.txt", 4), ("a/b/?.txt", 4), ("a/b/[xyz].txt", 4)]
    for pattern, index in cases:
        assert config_map._prefix_end(pattern) == index


def test_last_special_char():
    config_map = config.ConfigurationMap
    cases = [("a/b/*/**.txt", 8), ("a/b/?.txt", 5), ("a/b/[xyz].txt", 9)]
    for pattern, index in cases:
        assert config_map._suffix_start(pattern) == index


def test_alternative_test_group_creation():
    assert False


def test_more_complex_case_with_many_files():
    assert False
