import clikit

from herald import cli, logging
from herald.executor import noop


def test_entrypoint_when_all_files_exist(basic_config, everything_exists_path):
    output_tasks = _run_tasks(basic_config, everything_exists_path)
    assert output_tasks == ["ls -la", "echo something", "wc -l", "echo test"]


def test_entrypoint_when_no_files_exist(basic_config, nothing_exists_path):
    output_tasks = _run_tasks(basic_config, nothing_exists_path)
    assert output_tasks == []


def test_entrypoint_when_source_files_missing(basic_config, source_doesnt_exist_path):
    output_tasks = _run_tasks(basic_config, source_doesnt_exist_path)
    assert output_tasks == ["wc -l", "echo test"]


def test_entrypoint_when_test_files_missing(basic_config, test_doesnt_exist_path):
    output_tasks = _run_tasks(basic_config, test_doesnt_exist_path)
    assert output_tasks == ["ls -la", "echo something"]


def test_alternate_redaction_when_some_alternates_dont_exist(
    basic_config, foo_test_doesnt_exist_path
):
    output_tasks, output_buffer = _run_tasks_with_custom_state(
        basic_config,
        foo_test_doesnt_exist_path,
        [
            "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 src/main/java/foo.java",
            "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 src/main/java/bar.java",
            "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 src/test/java/bar.java",
        ],
        [],
    )
    assert "Redacting alternates not found: src/test/java/foo.java" in output_buffer


def _run_tasks(config, path):
    output_tasks, _ = _run_tasks_with_custom_state(
        config,
        path,
        [
            "1 M. N... 100755 100755 100755 275239cf6d3a0de3e59e54e12b31113dc4769941 f765280922e5bb1e084650a552c618d19d6794d0 src/main/java/foo.java"
        ],
        [],
    )
    return output_tasks


def _run_tasks_with_custom_state(config, path, status_lines, result_fixtures):
    output_tasks = []
    with noop.record(output_tasks, result_fixtures) as create_executor:
        logger = logging.buffered_logger()
        cli.entrypoint(status_lines, config, create_executor, path, logger)
    return output_tasks, logger.io.fetch_output()
