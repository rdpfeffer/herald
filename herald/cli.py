#! /usr/bin/env python

import click
import invoke
import attr

import herald.config as config
import herald.git_status as git_status
from herald import path
from herald.executor import subprocess
from herald import task
from contextlib import contextmanager


@attr.s()
class CliLogger:

    indent_level = attr.ib(default=0)

    def log(self, message):
        indent_str = self._padd_indent()
        click.echo("{}{}".format(indent_str, message))

    @contextmanager
    def indent(self, increment=1):
        previous_indent = self.indent_level
        self.indent_level += increment
        try:
            yield self
        finally:
            self.indent_level = previous_indent

    def _padd_indent(self):
        return "    " * self.indent_level


def entrypoint(lines, config_map, create_executor, path_module):
    logger = CliLogger()

    logger.log("Reading Git status")
    checkable_lines = git_status.get_checkable_lines(lines)
    filepaths = [l.path for l in checkable_lines]
    logger.log("Found {} checkable files.".format(len(filepaths)))

    task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
    logger.log(
        "Mapped to task groups: {}".format(",".join([g.pattern for g in task_groups]))
    )

    results = _run_task_groups(task_groups, logger, create_executor, path_module)
    _summarize_results(results)


def _run_task_groups(task_groups, logger, create_executor, path_module):
    results = []

    for group in task_groups:
        filepaths, non_existent_filepaths = path_module.segregate_nonexistent_files(
            group.filepaths
        )
        if len(filepaths) == 0:
            # TODO: Add name of entry into the formatted string below
            logger.log(
                "Skipping Task Group: {}, matching alternates do not exist.".format(
                    group.pattern
                )
            )
            results.append(task.TaskGroupResult(task.Status.SKIP))
            continue

        logger.log("Handling Task Group: {}".format(group.pattern))
        with logger.indent() as group_logger:
            if len(non_existent_filepaths) > 0:
                group_logger.log(
                    "Redacting alternates not found: {}".format(
                        ", ".join(non_existent_filepaths)
                    )
                )
            group_logger.log("Proceeding with files: {}".format(", ".join(filepaths)))
            executor = create_executor(group.executor_name, invoke, group_logger)
            results.append(executor.run(group.tasks, filepaths))
    return results


def _summarize_results(results):
    # TODO: Summarize the results
    pass


def main():
    entrypoint(
        git_status.get_raw_git_status_lines(invoke),
        config.load_config(),
        subprocess.create_executor,
        path,
    )


if __name__ == "__main__":
    main()
