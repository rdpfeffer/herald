import attr

from herald.executor import base


@attr.s
class SerialExecutor(base.Executor):

    """A concrete Executor which runs tasks in serial"""

    invoke = attr.ib()
    logger = attr.ib()

    def run(self, tasks, filepaths):
        """Run the tasks"""
        results = []
        for task in tasks:
            results.append(
                self.invoke.run(base.format_task(task, filepaths), warn=True, hide=True)
            )
        return results


@attr.s
class ParallelExecutor(base.Executor):

    """A concrete Executor which runs tasks in parallel"""

    invoke = attr.ib()
    logger = attr.ib()

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me


def create_executor(executor_name, invoke, logger):
    executor_instance = None
    if executor_name == "parallel":
        executor_instance = ParallelExecutor(invoke, logger)
    elif executor_name == "serial":
        executor_instance = SerialExecutor(invoke, logger)
    else:
        raise base.BadExecutorError()
    return executor_instance
