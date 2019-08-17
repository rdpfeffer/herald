#! /usr/bin/env python

import herald.config as config
import herald.git_status as git_status
from herald.executor import subprocess


def entrypoint(lines, config_map, create_executor):
    checkable_lines = git_status.get_checkable_lines(lines)
    filepaths = [l.path for l in checkable_lines]
    task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
    for group in task_groups:
        exec = create_executor(group._executor_name)
        exec.run(group._tasks, group._filepaths)


def main():
    entrypoint(
        git_status.get_raw_git_status_lines(),
        config.load_config(),
        subprocess.create_executor,
    )


if __name__ == "__main__":
    main()
