import attr

from herald.executor import base


@attr.s
class SerialExecutor(base.Executor):

    """A concrete Executor which runs tasks in serial"""

    invoke = attr.ib()

    def run(self, tasks, filepaths, logger):
        """Run the tasks"""
        results = []
        for task in tasks:
            command = base.format_task(task, filepaths)
            logger.log("Running: <info>{}</>".format(command))
            results.append(self.invoke.run(command, warn=True, hide=True, pty=True))
        return results


@attr.s
class ParallelExecutor(base.Executor):

    """A concrete Executor which runs tasks in parallel"""

    invoke = attr.ib()

    def run(self, tasks, filepaths, logger):
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
