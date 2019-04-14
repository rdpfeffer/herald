import attr

from herald import executor


@attr.s(frozen=True)
class TaskGroup(object):

    """A group of tasks to be run"""

    _executor = attr.ib(validator=attr.validators.instance_of(executor.Executor))
    _tasks = attr.ib(converter=tuple)
    _filepaths = attr.ib(converter=frozenset)

    def copy_with_additional_paths(self, filepaths):
        return TaskGroup(self._executor, self._tasks, self._filepaths.union(filepaths))

    def run(self, filepaths):
        self._executor.run(self._tasks, filepaths)
