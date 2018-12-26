from collections import namedtuple

StatusLine = namedtuple("StatusLine", ["status", "orig_path", "path"])


def main():
    lines = [
        "AM script.py",
        "A  script.py",
        " M script.py",
    ]
    parsed_lines = [parse(l) for l in lines]
    checkable_lines = [l for l in parsed_lines if is_checkable(l)]


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


def is_checkable(git_status_line):
    status = {
        "??": True,
        "A ": True,
    }

if __name__ == "__main__":
    main()
