import pytest
from .context import herald
from herald import executor


def test_abstract_executor_throws_exception():
    with pytest.raises(NotImplementedError):
        executor.Executor().run((), {})
