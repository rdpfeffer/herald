from collections import namedtuple

from script import StatusLine
from script import parse

Case = namedtuple("Case", ["line", "parsed_line", "deleted", "unmerged"])
TEST_CASES = [
    # Statuses without merge conflicts
    Case(" A a.py", StatusLine(status=" A", orig_path=None, path="a.py"), False, False),
    Case(" M a.py", StatusLine(status=" M", orig_path=None, path="a.py"), False, False),
    Case(" D a.py", StatusLine(status=" D", orig_path=None, path="a.py"), True, False),
    Case("M  a.py", StatusLine(status="M ", orig_path=None, path="a.py"), False, False),
    Case("MM a.py", StatusLine(status="MM", orig_path=None, path="a.py"), False, False),
    Case("MD a.py", StatusLine(status="MD", orig_path=None, path="a.py"), True, False),
    Case("A  a.py", StatusLine(status="A ", orig_path=None, path="a.py"), False, False),
    Case("AM a.py", StatusLine(status="AM", orig_path=None, path="a.py"), False, False),
    Case("AD a.py", StatusLine(status="AD", orig_path=None, path="a.py"), True, False),
    Case("D  a.py", StatusLine(status="D ", orig_path=None, path="a.py"), True, False),
    Case("R  a.py -> b.py", StatusLine(status="R ", orig_path="a.py", path="b.py"), False, False),
    Case("RM a.py -> b.py", StatusLine(status="RM", orig_path="a.py", path="b.py"), False, False),
    Case("RD a.py -> b.py", StatusLine(status="RD", orig_path="a.py", path="b.py"), True, False),
    Case("C  a.py", StatusLine(status="C ", orig_path=None, path="a.py"), False, False),
    Case("CM a.py", StatusLine(status="CM", orig_path=None, path="a.py"), False, False),
    Case("CD a.py", StatusLine(status="CD", orig_path=None, path="a.py"), True, False),
    Case(" R a.py -> b.py", StatusLine(status=" R", orig_path="a.py", path="b.py"), False, False),
    Case("DR a.py -> b.py", StatusLine(status="DR", orig_path="a.py", path="b.py"), False, False),
    Case(" C a.py", StatusLine(status=" C", orig_path=None, path="a.py"), False, False),
    Case("DC a.py", StatusLine(status="DC", orig_path=None, path="a.py"), False, False),
    # Statuses with merge conflicts
    Case("DD a.py", StatusLine(status="DD", orig_path=None, path="a.py"), True, True),
    Case("AU a.py", StatusLine(status="AU", orig_path=None, path="a.py"), False, True),
    Case("UD a.py", StatusLine(status="UD", orig_path=None, path="a.py"), True, True),
    Case("UA a.py", StatusLine(status="UA", orig_path=None, path="a.py"), False, True),
    Case("DU a.py", StatusLine(status="DU", orig_path=None, path="a.py"), True, True),
    Case("AA a.py", StatusLine(status="AA", orig_path=None, path="a.py"), False, True),
    Case("UU a.py", StatusLine(status="UU", orig_path=None, path="a.py"), False, True),
    # Untracked and Ignored Statuses
    Case("?? a.py", StatusLine(status="??", orig_path=None, path="a.py"), False, False),
    Case("!! a.py", StatusLine(status="!!", orig_path=None, path="a.py"), False, False),
    # Status lines with quoted and escaped paths
    Case('A  "file with a space.txt"', StatusLine(status="A ", orig_path=None, path='"file with a space.txt"'), False, False),
    Case(r'A  "file with a space \/ and slash.txt"', StatusLine(status="A ", orig_path=None, path=r'"file with a space \/ and slash.txt"'), False, False),
]

def test_parse():
    for line, status_entry, _, _ in TEST_CASES:
        assert parse(line) == status_entry


def test_is_deleted():
    for _, status_entry, deleted, _ in TEST_CASES:
        assert status_entry.is_deleted() == deleted


def test_is_unmerged():
    for _, status_entry, _, unmerged in TEST_CASES:
        assert status_entry.is_unmerged() == unmerged
