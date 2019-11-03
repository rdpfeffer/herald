"""This module is responsible for grouping a set of files against a list of tasks to be run"""
import attr
import enum

from herald import executor


@attr.s(frozen=True)
class TaskGroup:

    """A group of tasks to be run"""

    pattern = attr.ib(type=str)
    executor_name = attr.ib(type=str)
    tasks = attr.ib(converter=tuple)
    filepaths = attr.ib(converter=frozenset)

    def copy_with_additional_paths(self, filepaths):
        """Return a copy of the task group with the union of the provided
        tasks and the tasks that already exist within this TaskGroup"""
        return TaskGroup(
            self.pattern,
            self.executor_name,
            self.tasks,
            self.filepaths.union(filepaths),
        )


class Status(enum.Enum):
    OK = "ok"
    ERROR = "error"
    SKIP = "skip"


@attr.s
class TaskGroupResult:
    status = attr.ib(validator=attr.validators.in_(Status))
    results = attr.ib(default=attr.Factory(list))
