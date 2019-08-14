"""This module is responsible for grouping a set of files against a list of tasks to be run"""
import attr

from herald import executor


@attr.s(frozen=True)
class TaskGroup:

    """A group of tasks to be run"""

    _executor_name = attr.ib(type=str)
    _tasks = attr.ib(converter=tuple)
    _filepaths = attr.ib(converter=frozenset)

    def copy_with_additional_paths(self, filepaths):
        """Return a copy of the task group with the union of the provided
        tasks and the tasks that already exist within this TaskGroup"""
        return TaskGroup(
            self._executor_name, self._tasks, self._filepaths.union(filepaths)
        )
