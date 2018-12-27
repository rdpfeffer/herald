from collections import namedtuple
import re

StatusLine = namedtuple("StatusLine", ["status", "orig_path", "path"])

UNCHANGED_STATUS_DEMARCATION = " "
DELETED_STATUSES = set([
    "D{0}".format(UNCHANGED_STATUS_DEMARCATION),
    "{0}D".format(UNCHANGED_STATUS_DEMARCATION),
    "MD",
    "AD",
    "RD",
    "CD",
    "DD",
    "UD",
    "DU",
])
UNMERGED_STATUSES = set("DD|AA|UU|AU|UD|UA|DU".split("|"))

def main():
    lines = [
        "AM script.py",
        "A  script.py",
        " M script.py",
    ]
    lines = [l for l in lines if not is_header(l)]
    parsed_lines = [parse(l) for l in lines]
    deleted_lines = [l for l in parsed_lines if is_deleted(l.status)]
    unmerged_lines = [l for l in parsed_lines if is_unmerged(l.status)]
    checkable_lines = list(
        set(parsed_lines) - set(deleted_lines) - set(unmerged_lines)
    )


def is_header(line):
    return line.startswith("#")

def parse(line):
    status = line[0:2]
    remainder = line[3:]
    path_parts = remainder.split(" ")
    orig_path = None
    path = None
    try:
        arrow_separator_idx = path_parts.index("->")
    except ValueError as e:
        # The file's path was not changed, so we take all of the remainder
        path = remainder
    else:
        orig_path = " ".join(path_parts[0:arrow_separator_idx])
        path = " ".join(path_parts[arrow_separator_idx+1:])
    return StatusLine(status, orig_path, path)


def is_deleted(status):
    return status in DELETED_STATUSES


def is_unmerged(status):
    return status in UNMERGED_STATUSES


if __name__ == "__main__":
    main()
