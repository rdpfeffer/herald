import pytest

from herald import executor

from .context import herald


def test_abstract_executor_throws_exception():
    with pytest.raises(NotImplementedError):
        executor.Executor().run((), {})


def test_executor_creation_serial():
    serial_exec = executor.create_executor("serial")
    assert isinstance(serial_exec, executor.SerialExecutor)


def test_executor_creation_parallel():
    parallel_exec = executor.create_executor("parallel")
    assert isinstance(parallel_exec, executor.ParallelExecutor)


def test_executor_creation_internal_error():
    with pytest.raises(executor.BadExecutorError):
        serial_exec = executor.create_executor("bananas")
