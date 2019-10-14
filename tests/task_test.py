import attr
import pytest

from herald import executor, task

from .context import herald


def test_immutable_properties():
    g = task.TaskGroup("", [], [])
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g.tasks = True
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        g.filepaths = True


def test_copy_additional_paths():
    g = task.TaskGroup("", [], ["x/y/bar.txt"])
    g2 = g.copy_with_additional_paths(["a/b/foo.txt"])
    assert id(g2) != id(g)
    assert g2.filepaths == frozenset(["a/b/foo.txt", "x/y/bar.txt"])


def test_hashable_by_value():
    g1 = (task.TaskGroup("", [], ["x/y/bar.txt"]),)
    g2 = (task.TaskGroup("", [], ["x/y/bar.txt"]),)
    s = {g1, g2}
    assert hash(g1) == hash(g2)
    assert len(s) == 1
