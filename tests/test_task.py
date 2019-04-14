import attr
import pytest

from .context import herald
from herald import executor
from herald import task


def test_immutable_properties():
    g = task.TaskGroup(executor.ParallelExecutor(), [], [])
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g._executor = True
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g._tasks = True
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g._filepaths = True


def test_copy_additional_paths():
    g = task.TaskGroup(executor.ParallelExecutor(), [], ["x/y/bar.txt"])
    g2 = g.copy_with_additional_paths(["a/b/foo.txt"])
    assert id(g2) != id(g)
    assert g2._filepaths  ==  frozenset(["a/b/foo.txt", "x/y/bar.txt"])


def test_run():
    g = task.TaskGroup(executor.ParallelExecutor(), [], ["x/y/bar.txt"])
    g.run("bar.txt")


def test_hashable_by_value():
    p = executor.ParallelExecutor()
    g1 = task.TaskGroup(p, [], ["x/y/bar.txt"]),
    g2 = task.TaskGroup(p, [], ["x/y/bar.txt"]),
    s = {g1, g2}
    assert hash(g1) == hash(g2)
    assert len(s) == 1
