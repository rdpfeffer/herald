#! /usr/bin/env python

import click
import invoke

import herald.config as config
import herald.git_status as git_status
from herald import path
from herald.executor import subprocess
from herald import task


class CliLogger:
    def log(self, message):
        click.echo(message)


def entrypoint(lines, config_map, create_executor, path_module):
    logger = CliLogger()

    logger.log("Reading Git status")
    checkable_lines = git_status.get_checkable_lines(lines)
    filepaths = [l.path for l in checkable_lines]
    logger.log("Found {} checkable files.".format(len(filepaths)))

    task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
    logger.log("Mapped to task groups: {}".format(task_groups))

    results = _run_task_groups(task_groups, logger, create_executor, path_module)
    _summarize_results(results)


def _run_task_groups(task_groups, logger, create_executor, path_module):
    results = []

    for group in task_groups:
        logger.log("Handling Task Group: {}".format(group))
        filepaths, non_existent_filepaths = path_module.segregate_nonexistent_files(
            group.filepaths
        )
        if len(filepaths) == 0:
            # TODO: Add name of entry into the formatted string below
            logger.log("Skipping Task Group: {}, matching alternates do not exist.")
            results.append(task.TaskGroupResult(task.Status.SKIP))
            continue

        logger.log("Redacting alternates not found: {}".format(non_existent_filepaths))
        executor = create_executor(group.executor_name, invoke, logger)
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
