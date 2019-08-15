import herald.cli as cli
import herald.config as config
from herald.executor import noop

from .fixtures import basic_config


def test_main(basic_config):
    output_tasks = []
    with noop.record(output_tasks) as create_executor:
        cli.main(
            [
                "1 M. N... 100755 100755 100755 "
                "275239cf6d3a0de3e59e54e12b31113dc4769941 "
                "f765280922e5bb1e084650a552c618d19d6794d0 "
                "src/main/java/foo.java"
            ],
            basic_config,
            create_executor,
        )
    assert output_tasks == ["ls -la", "echo something", "wc -l", "echo test"]
