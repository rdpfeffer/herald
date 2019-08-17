"""This module is responsible for grouping a set of files against a list of tasks to be run"""
import attr

from herald import executor


@attr.s(frozen=True)
class TaskGroup:

    """A group of tasks to be run"""

    executor_name = attr.ib(type=str)
    tasks = attr.ib(converter=tuple)
    filepaths = attr.ib(converter=frozenset)

    def copy_with_additional_paths(self, filepaths):
        """Return a copy of the task group with the union of the provided
        tasks and the tasks that already exist within this TaskGroup"""
        return TaskGroup(
            self.executor_name, self.tasks, self.filepaths.union(filepaths)
        )
