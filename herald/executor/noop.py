import attr

from herald.executor import base


@attr.s
class NoopExecutor(base.Executor):

    """A concrete Executor which keeps track of which tasks were run,
    but doesn't actually run them."""

    output_tasks = attr.ib(type=list)
    invoke = attr.ib()
    logger = attr.ib()

    def run(self, tasks, filepaths):
        """Run the tasks"""
        for task in tasks:
            self.output_tasks.append(base.format_task(task, filepaths))


@attr.s
class record:

    output_tasks = attr.ib(type=list)

    def __enter__(self):
        def create_executor(executor_name, invoke, logger):
            executor_instance = None
            if executor_name in ("parallel", "serial"):
                executor_instance = NoopExecutor(self.output_tasks, invoke, logger)
            else:
                raise base.BadExecutorError()
            return executor_instance

        return create_executor

    def __exit__(self, exc_type, exc_value, traceback):
        pass
