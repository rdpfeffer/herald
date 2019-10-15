import pytest

from herald import config, task


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
    assert len(task_groups) == 2
    _verify_task_group_equivalent(
        task_groups[0],
        "serial",
        ("ls -la", "echo something"),
        {"src/main/java/foo.java"},
    )
    _verify_task_group_equivalent(
        task_groups[1], "parallel", ("wc -l", "echo test"), {"src/test/java/foo.java"}
    )


def test_test_file_does_not_gather_src_files(basic_config):
    task_groups = basic_config.get_all_task_groups_for_filepaths(
        ["src/test/java/foo.java"]
    )
    assert len(task_groups) == 1
    _verify_task_group_equivalent(
        task_groups[0], "parallel", ("wc -l", "echo test"), {"src/test/java/foo.java"}
    )


def test_absence_of_tasks_in_config(missing_task_config):
    task_groups = missing_task_config.get_all_task_groups_for_filepaths(
        [
            "herald/cli.py",
            "poetry.lock",
            "pyproject.toml",
            "tests/config_test.py",
            "tests/conftest.py",
        ]
    )
    assert len(task_groups) == 1
    _verify_task_group_equivalent(
        task_groups[0],
        "serial",
        ("pytest {}",),
        {"tests/config_test.py", "tests/cli_test.py"},
    )
    pass


def _verify_task_group_equivalent(task_group, executor_name, tasks, path_set):
    assert task_group.executor_name == executor_name
    assert task_group.tasks == tasks
    assert task_group.filepaths == path_set


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
