#! /usr/bin/env python

import clikit
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

    io = attr.ib()
    indent_level = attr.ib(default=0)

    def log(self, message):
        indent_str = self._padd_indent()
        self.io.write_line("{}{}".format(indent_str, message))

    def warn(self, message):
        indent_str = self._padd_indent()
        self.io.write_line("{}{}".format(indent_str, message))

    @contextmanager
    def indent(self, increment=1):
        previous_indent = self.indent_level
        self.indent_level += increment
        try:
            yield self
        finally:
            self.indent_level = previous_indent

    def _padd_indent(self):
        return "    " * self.indent_level + "→ " if self.indent_level > 0 else ""


def entrypoint(lines, config_map, create_executor, path_module, logger):
    logger.log("<info>Analyzing Project State</info>")

    with logger.indent() as status_logger:
        status_logger.log("Reading Git status")
        checkable_lines = git_status.get_checkable_lines(lines)
        filepaths = [l.path for l in checkable_lines]
        status_logger.log("Found <info>{}</info> checkable files.".format(len(filepaths)))

        task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
        status_logger.log(
            "Mapped to task groups: <info>{}</info>".format(",".join([g.pattern for g in task_groups]))
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
            logger.log(
                "Skipping Task Group: <c2>{}</>, matching alternates do not exist.".format(
                    group.pattern
                )
            )
            results.append(task.TaskGroupResult(task.Status.SKIP))
            continue

        logger.log("<info>Handling Task Group</>: <info>{}</info>".format(group.pattern))
        with logger.indent() as group_logger:
            if len(non_existent_filepaths) > 0:
                group_logger.log(
                    "Redacting alternates not found: <c2>{}</>".format(
                        ", ".join(non_existent_filepaths)
                    )
                )
            executor = create_executor(group.executor_name, invoke, group_logger)
            result = executor.run(group.tasks, filepaths)
            group_logger.log(result[0])
            results.append(result)
    return results


def _summarize_results(results):
    # TODO: Summarize the results
    pass


def main():

    io = clikit.io.console_io.ConsoleIO()
    logger = CliLogger(io)

    entrypoint(
        git_status.get_raw_git_status_lines(invoke),
        config.load_config(),
        subprocess.create_executor,
        path,
        logger,
    )


if __name__ == "__main__":
    main()
