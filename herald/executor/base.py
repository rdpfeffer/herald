"""Responsible for Task Execution"""

from os import path


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


def segregate_nonexistent_files(filepaths):
    non_existent = frozenset([f for f in filepaths if not path.exists(f)])
    existent = filepaths - non_existent
    return existent, non_existent
