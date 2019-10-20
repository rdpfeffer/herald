#! /usr/bin/env python

import herald.config as config
import herald.git_status as git_status
from herald.executor import subprocess
import invoke
import click


def entrypoint(lines, config_map, create_executor):
    click.echo("Reading Git status")
    checkable_lines = git_status.get_checkable_lines(lines)
    filepaths = [l.path for l in checkable_lines]
    click.echo("Found {} checkable files.".format(len(filepaths)))
    task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
    click.echo("Mapped to task groups: {}".format(task_groups))
    for group in task_groups:
        executor = create_executor(group.executor_name, invoke)
        executor.run(group.tasks, group.filepaths)


def main():
    entrypoint(
        git_status.get_raw_git_status_lines(invoke),
        config.load_config(),
        subprocess.create_executor,
    )


if __name__ == "__main__":
    main()
