def main():
    lines = [
        "AM script.py"
    ]
    parsed_lines = parse(lines)
    checkable_lines = [l for l in parsed_lines if is_checkable(l)]

def parse(line):
    pass

def is_checkable(git_status_line):
    status = {
        "??": True,
        "A ": True,
    }

if __name__ == "__main__":
    main()
