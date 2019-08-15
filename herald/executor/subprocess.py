from herald.executor import base


class SerialExecutor(base.Executor):

    """A concrete Executor which runs tasks in serial"""

    def __init__(self):
        """Create the class """
        base.Executor.__init__(self)

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me


class ParallelExecutor(base.Executor):

    """A concrete Executor which runs tasks in parallel"""

    def __init__(self):
        """Create the class """
        base.Executor.__init__(self)

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me


def create_executor(executor_name):
    executor_instance = None
    if executor_name == "parallel":
        executor_instance = ParallelExecutor()
    elif executor_name == "serial":
        executor_instance = SerialExecutor()
    else:
        raise base.BadExecutorError()
    return executor_instance
