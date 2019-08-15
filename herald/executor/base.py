"""Responsible for Task Execution"""


class Executor:

    """Abstract Executor Class"""

    def run(self, tasks, filepaths):
        """Not Implemented"""
        raise NotImplementedError(
            "Executor is an Abstract class. Please use a concrete "
            "implementation with a properly implemented run() method"
        )


class BadExecutorError(Exception):

    """Thrown when a bad execution mode is supplied. If this error is ever thrown,
    then there is likely a misspelled/bad config"""


def format_task(task, filepaths):
    return task.format(" ".join(filepaths))
