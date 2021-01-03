import attr
import pytest

from herald import logging, task
from herald.executor import noop

from .context import herald


def test_immutable_properties():
    g = task.TaskGroup("", "", [], [])
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g.tasks = True
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g.filepaths = True


def test_copy_additional_paths():
    g = task.TaskGroup("", "", [], ["x/y/bar.txt"])
    g2 = g.copy_with_additional_paths(["a/b/foo.txt"])
    assert id(g2) != id(g)
    assert g2.filepaths == frozenset(["a/b/foo.txt", "x/y/bar.txt"])


def test_hashable_by_value():
    g1 = (task.TaskGroup("", "", [], ["x/y/bar.txt"]),)
    g2 = (task.TaskGroup("", "", [], ["x/y/bar.txt"]),)
    s = {g1, g2}
    assert hash(g1) == hash(g2)
    assert len(s) == 1


def test_task_group_summary_error_when_at_least_one_task_fails(
    basic_config, everything_exists_path, single_java_status_line_list, basic_task_group
):
    task_results = [
        noop.NoopResult(True, "1st one is ok"),
        noop.NoopResult(False, "2nd one fails"),
    ]

    result_summary, _ = _run_task_group(
        basic_task_group, everything_exists_path, task_results
    )

    assert result_summary.status == task.Status.ERROR


def test_task_group_summary_error_when_all_tasks_fail(
    basic_config, everything_exists_path, single_java_status_line_list, basic_task_group
):
    task_results = [
        noop.NoopResult(False, "1st one fails"),
        noop.NoopResult(False, "2nd one fails"),
    ]

    result_summary, _ = _run_task_group(
        basic_task_group, everything_exists_path, task_results
    )

    assert result_summary.status == task.Status.ERROR


def test_task_group_summary_ok_when_all_tasks_succeed(
    basic_config, everything_exists_path, single_java_status_line_list, basic_task_group
):
    task_results = [
        noop.NoopResult(True, "1st one ok"),
        noop.NoopResult(True, "2nd one ok"),
    ]

    result_summary, _ = _run_task_group(
        basic_task_group, everything_exists_path, task_results
    )

    assert result_summary.status == task.Status.OK


def _run_task_group(group, path, result_fixtures):
    output_tasks = []
    with noop.record(output_tasks, result_fixtures) as create_executor:
        executor = create_executor()
        logger = logging.buffered_logger()
        result_summary = group.run(path, logger, executor)
    return result_summary, logger.io.fetch_output()
