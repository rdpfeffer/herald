import attr

from herald.executor import base


@attr.s
class NoopResult:

    ok = attr.ib(type=bool, default=True)
    stdout = attr.ib(type=str, default="")


@attr.s
class NoopExecutor(base.Executor):

    """A concrete Executor which keeps track of which tasks were run,
    but doesn't actually run them."""

    output_tasks = attr.ib(type=list)
    result_fixtures = attr.ib(type=list, default=[])

    def run(self, tasks, filepaths, logger):
        """Run the tasks"""
        results = []
        for task in tasks:
            self.output_tasks.append(base.format_task(task, filepaths))
            results.append(self._get_next_result())
        return results

    def _get_next_result(self):
        result = None
        if len(self.result_fixtures) > 0:
            result = self.result_fixtures.pop(0)
        else:
            result = NoopResult(False, "Stubbed output")
        return result


@attr.s
class record:

    output_tasks = attr.ib(type=list)
    result_fixtures = attr.ib(type=list, default=[])

    def __enter__(self):
        def create_executor(_=None, __=None):
            return NoopExecutor(self.output_tasks, self.result_fixtures)

        return create_executor

    def __exit__(self, exc_type, exc_value, traceback):
        pass
