#! /usr/bin/env python

import herald.config as config
import herald.git_status as git_status


def main(lines, config_map):
    checkable_lines = git_status.get_checkable_lines(lines)
    filepaths = [l.path for l in checkable_lines]
    task_groups = config_map.get_all_task_groups_for_filepaths(filepaths)
    for group in task_groups:
        group.run()


if __name__ == "__main__":
    main(git_status.get_raw_git_status_lines(), config.load_config())
