import pytest

from herald.executor import base, subprocess

from .context import herald


def test_abstract_executor_throws_exception():
    with pytest.raises(NotImplementedError):
        base.Executor().run((), {})


def test_executor_creation_serial():
    serial_exec = subprocess.create_executor("serial")
    assert isinstance(serial_exec, subprocess.SerialExecutor)


def test_executor_creation_parallel():
    parallel_exec = subprocess.create_executor("parallel")
    assert isinstance(parallel_exec, subprocess.ParallelExecutor)


def test_executor_creation_internal_error():
    with pytest.raises(base.BadExecutorError):
        subprocess.create_executor("bananas")
