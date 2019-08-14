"""Responsible for Task Execution"""


class Executor:

    """Abstract Executor Class"""

    def run(self, tasks, filepaths):
        """Not Implemented"""
        raise NotImplementedError(
            "Executor is an Abstract class. Please use a concrete "
            "implementation with a properly implemented run() method"
        )


class SerialExecutor(Executor):

    """A concrete Executor which runs tasks in serial"""

    def __init__(self):
        """Create the class """
        Executor.__init__(self)

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me
        pass


class ParallelExecutor(Executor):

    """A concrete Executor which runs tasks in parallel"""

    def __init__(self):
        """Create the class """
        Executor.__init__(self)

    def run(self, tasks, filepaths):
        """Run the tasks"""
        # TODO: Implement Me
        pass


def create_executor(executor_name):
    executor_instance = None
    if executor_name == "parallel":
        executor_instance = ParallelExecutor()
    elif executor_name == "serial":
        executor_instance = SerialExecutor()
    else:
        raise BadExecutorError()
    return executor_instance


class BadExecutorError(Exception):

    """Thrown when a bad execution mode is supplied. If this error is ever thrown,
    then there is likely a misspelled/bad config"""
