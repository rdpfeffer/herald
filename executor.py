class Executor(object):

    """Abstract Executor Class"""

    def run(self, tasks, filepaths):
        raise NotImplemented(
            "Executor is an Abstract class. Please use a concrete "
            "implementation with a properly implemented run() method"
        )


class SerialExecutor(Executor):

    """A concrete Executor which runs tasks in serial"""

    def __init__(self):
        """Create the class """
        Executor.__init__(self)

    def run(self, tasks, filepaths):
        # TODO: Implement Me
        pass


class ParallelExecutor(Executor):

    """A concrete Executor which runs tasks in parallel"""

    def __init__(self):
        """Create the class """
        Executor.__init__(self)

    def run(self, tasks, filepaths):
        # TODO: Implement Me
        pass
