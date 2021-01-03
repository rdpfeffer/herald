"""
This module is responsible for grouping a set of files against a list of tasks to be run
"""
import enum

import attr


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

    def run(self, path_module, logger, executor):
        """Run the task group
        :returns: TODO

        """
        filepaths, non_existent_filepaths = path_module.segregate_nonexistent_files(
            self.filepaths
        )
        if len(filepaths) == 0:
            return TaskGroupResultSummary(
                self.pattern, Status.SKIP, [], "Target files do not exist."
            )

        logger.log("<c2>Handling Task Group</>: <info>{}</info>".format(self.pattern))
        with logger.indent() as group_logger:
            if len(non_existent_filepaths) > 0:
                group_logger.log(
                    "Redacting alternates not found: <c2>{}</>".format(
                        ", ".join(non_existent_filepaths)
                    )
                )
            task_group_results = executor.run(self.tasks, filepaths, group_logger)
            return TaskGroupResultSummary(
                self.pattern,
                Status.OK if all(r.ok for r in task_group_results) else Status.ERROR,
                task_group_results,
            )


class Status(enum.Enum):
    OK = "ok"
    ERROR = "error"
    SKIP = "skip"


@attr.s
class TaskGroupResultSummary:
    pattern = attr.ib(type=str)
    status = attr.ib(validator=attr.validators.in_(Status))
    results = attr.ib(default=attr.Factory(list))
    message = attr.ib(default="")
