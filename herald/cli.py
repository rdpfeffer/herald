#! /usr/bin/env python

from contextlib import contextmanager

import clikit
import invoke

import herald.config as config
import herald.git_status as git_status
from herald import logging, path, task
from herald.executor import subprocess


def entrypoint(lines, config_map, create_executor, path_module, logger):
    logger.log("<c2>Analyzing Project State</c2>")

    with logger.indent() as status_logger:
        status_logger.log("<fg=blue>Reading Git status</>")
        checkable_lines = git_status.get_checkable_lines(lines)
        filepaths = [l.path for l in checkable_lines]
        status_logger.log(
            "<fg=blue>Found <info>{}</info> checkable files.</>".format(len(filepaths))
        )

        task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
        status_logger.log(
            "<fg=blue>Mapped to task groups: <info>{}</info></>".format(
                ",".join([g.pattern for g in task_groups])
            )
        )

    result_summaries = _run_task_groups(
        task_groups, logger, create_executor, path_module
    )
    _summarize_results(result_summaries, logger)


def _run_task_groups(task_groups, logger, create_executor, path_module):
    result_summaries = []

    for group in task_groups:
        executor = create_executor(group.executor_name, invoke)
        result_summaries.append(group.run(path_module, logger, executor))

    return result_summaries


def _summarize_results(result_summaries, logger):
    logger.log("<c2>Result Summary:</>")
    with logger.indent() as summary_logger:
        for summary in result_summaries:
            if summary.status == task.Status.OK:
                summary_logger.log("<info>OK</>: {}".format(summary.pattern))
            elif summary.status == task.Status.ERROR:
                summary_logger.log("<error>ERROR</>: {}".format(summary.pattern))
                for result in summary.results:
                    summary_logger.log(result.stdout)


def main():

    logger = logging.console_logger()

    entrypoint(
        git_status.get_raw_git_status_lines(invoke),
        config.load_config(),
        subprocess.create_executor,
        path,
        logger,
    )


if __name__ == "__main__":
    main()
