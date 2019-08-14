"""Main Entrypoint for Herald"""
import os
import shlex
import subprocess
from collections import namedtuple

DELETED_STATUSES = set("D.|.D|MD|AD|RD|CD|DD|UD|DU".split("|"))
UNMERGED_STATUSES = set("DD|AA|UU|AU|UD|UA|DU".split("|"))
_StatusEntry = namedtuple("StatusEntry", ["status", "submodule", "orig_path", "path"])


class StatusEntry(_StatusEntry):

    """Represents one line of status when running 'git status'"""

    def is_deleted(self):
        return self.status in DELETED_STATUSES

    def is_unmerged(self):
        return self.status in UNMERGED_STATUSES

    def is_submodule(self):
        """Return True if the status entry is a submdule"""
        check = False
        if self.submodule is None:
            check = False
        else:
            check = self.submodule.startswith("S")
        return check


def get_raw_git_status_lines():
    return subprocess.run(
        "git status --porcelain=v2".split(" "),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.split(os.linesep)


def get_checkable_lines(lines):
    clean_lines = strip_headers(strip_empty_lines(lines))
    status_entries = parse_lines(clean_lines)
    deleted_entries = [l for l in status_entries if l.is_deleted()]
    unmerged_lines = [l for l in status_entries if l.is_unmerged()]
    submodule_lines = [l for l in status_entries if l.is_submodule()]
    return list(
        set(status_entries)
        - set(deleted_entries)
        - set(unmerged_lines)
        - set(submodule_lines)
    )


def strip_empty_lines(lines):
    return [l for l in lines if len(l) > 0]


def strip_headers(lines):
    return [l for l in lines if not l.startswith("#")]


def parse_lines(lines):
    return [parse(l) for l in lines]


def parse(line):
    tokens = tokenize(line)
    if tokens[0] in ("!", "?"):
        return parse_untracked_ignored_entry(tokens)
    if tokens[0] == "1":
        return parse_ordinary_change_entry(tokens)
    if tokens[0] == "2":
        return parse_renamed_or_copied_entry(tokens)
    if tokens[0] == "u":
        return parse_unmerged_entry(tokens)
    raise ValueError(
        "Line given does not match one of the recognized Git "
        "Porcelain V2 formats. {}".format(line)
    )


def tokenize(line):
    lex = shlex.shlex(line)
    lex.whitespace_split = True
    lex.whitespace = " "
    return list(lex)


def parse_untracked_ignored_entry(tokens):
    # Handle untracked and ignored files, Porcelain V2 gives single letter
    # status for these. We double them to allow for consistency in string
    # parsing elsewhere.
    status, path = tokens
    return StatusEntry(status * 2, None, None, path)


def parse_ordinary_change_entry(tokens):
    _, status, submodule, _, _, _, _, _, path = tokens
    return StatusEntry(status, submodule, None, path)


def parse_renamed_or_copied_entry(tokens):
    _, status, submodule, _, _, _, _, _, _, paths = tokens
    path, orig_path = paths.split("\t")
    return StatusEntry(status, submodule, orig_path, path)


def parse_unmerged_entry(tokens):
    _, status, submodule, _, _, _, _, _, _, _, path = tokens
    return StatusEntry(status, submodule, None, path)
