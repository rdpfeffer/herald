import fnmatch
import json
import re
from itertools import chain, groupby
from operator import itemgetter

import attr

import executor
import schema
import task


def load_config(path=".heraldrc.json"):
    """TODO: Docstring for load_config.

    :path: TODO
    :returns: TODO

    """
    with open(path) as file:
        lines = file.read()
        data = json.loads(lines)
        schema.validate(data)
        return ConfigurationMap(data)


@attr.s(frozen=True)
class MatchPair(object):
    filepath = attr.ib()
    task_data = attr.ib()


class ConfigurationMap(object):

    """Herald Config"""

    def __init__(self, data):
        """Initialize config

        :data: TODO

        """
        self._data = data

    def get_all_task_groups_for_filepaths(self, filepaths):
        task_groups = []
        tasks_and_files = chain(
            *[self.pair_task_entries_with_filepath(filepath) for filepath in filepaths]
        )
        for _, group in groupby(tasks_and_files, self._key_for_task_data_entry):
            group = list(group)
            pair = group[0]
            task_data = pair.task_data
            executor_name, tasks = task_data.copy().popitem()
            file_group = {pair.filepath for pair in group}
            task_groups.append(
                self._task_group_for_task_entry(executor_name, task_data, file_group)
            )
        return task_groups

    def pair_task_entries_with_filepath(self, filepath):
        task_data_entries = self._map_filepath_to_task_data_entries(filepath)
        return [MatchPair(filepath, entry) for entry in task_data_entries]

    @staticmethod
    def _key_for_task_data_entry(entry_pair):
        return str(entry_pair.task_data)

    def _map_filepath_to_task_data_entries(self, filepath):
        return [
            entry["tasks"]
            for _, entry in self._map_filepath_to_config_entries(filepath)
        ]

    def _map_filepath_to_config_entries(self, filepath):
        return [
            (pattern, self._data[pattern])
            for pattern in self._data
            if fnmatch.fnmatch(filepath, pattern)
        ]

    def _task_group_for_task_entry(self, executor_name, task_data, filepaths):
        executor = self._executor_for_name(executor_name)
        tasks = task_data[executor_name]
        return task.TaskGroup(executor, tasks, filepaths)

    def _executor_for_name(self, executor_name):
        if executor_name == "parallel":
            return executor.ParallelExecutor()
        elif executor_name == "serial":
            return executor.SerialExecutor()
        else:
            raise InternalExecutorError()

    def get_test_alternates_for_filepath(self, filepath):
        alternate_paths = [
            self._compute_alternate(pattern, entry["alternate"], filepath)
            for pattern, entry in self._map_filepath_to_config_entries(filepath)
            if "alternate" in entry
        ]

    @staticmethod
    def _compute_alternate(pattern, alternate, filepath):
        """Compute the alternate of a given filepath.

        This takes everything between the first and last special character,
        trimming off either end, and using that as input to the alternate
        format string."""
        beggining = pattern[0 : ConfigurationMap._prefix_end(pattern)]
        end = pattern[ConfigurationMap._suffix_start(pattern) :]
        middle = filepath[len(beggining) : -len(end)]
        return alternate.format(middle)

    @staticmethod
    def _prefix_end(pattern):
        match = ConfigurationMap._get_special_char_match(pattern)
        if match is not None:
            return match.span()[0]
        else:
            return 0

    @staticmethod
    def _suffix_start(pattern):
        reverse = pattern[::-1]
        index = ConfigurationMap._prefix_end(reverse)
        return len(pattern) - index

    @staticmethod
    def _get_special_char_match(pattern):
        reg = re.compile(r"[\*\?\[\]]")
        return reg.search(pattern)


class InternalExecutorError(Exception):

    """Thrown when a bad execution mode is supplied. If this error is ever thrown,
    then then there is some internal error with the program"""
