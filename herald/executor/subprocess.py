import attr

from herald.executor import base


@attr.s
class SerialExecutor(base.Executor):

    """A concrete Executor which runs tasks in serial"""

    invoke = attr.ib()

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me


@attr.s
class ParallelExecutor(base.Executor):

    """A concrete Executor which runs tasks in parallel"""

    invoke = attr.ib()

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me


def create_executor(executor_name, invoke):
    executor_instance = None
    if executor_name == "parallel":
        executor_instance = ParallelExecutor(invoke)
    elif executor_name == "serial":
        executor_instance = SerialExecutor(invoke)
    else:
        raise base.BadExecutorError()
    return executor_instance
