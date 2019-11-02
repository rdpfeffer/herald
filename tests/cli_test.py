import herald.cli as cli
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


def _run_tasks(config, path):
    output_tasks = []
    with noop.record(output_tasks) as create_executor:
        cli.entrypoint(
            [
                "1 M. N... 100755 100755 100755 "
                "275239cf6d3a0de3e59e54e12b31113dc4769941 "
                "f765280922e5bb1e084650a552c618d19d6794d0 "
                "src/main/java/foo.java"
            ],
            config,
            create_executor,
            path,
        )
    return output_tasks
