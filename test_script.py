from script import StatusLine
from script import parse

def test_parse():
    test_pairs = [
        # Statuses without merge conflicts
        (" A a.py", StatusLine(status=" A", orig_path=None, path="a.py")),
        (" M a.py", StatusLine(status=" M", orig_path=None, path="a.py")),
        (" D a.py", StatusLine(status=" D", orig_path=None, path="a.py")),
        ("M  a.py", StatusLine(status="M ", orig_path=None, path="a.py")),
        ("MM a.py", StatusLine(status="MM", orig_path=None, path="a.py")),
        ("MD a.py", StatusLine(status="MD", orig_path=None, path="a.py")),
        ("A  a.py", StatusLine(status="A ", orig_path=None, path="a.py")),
        ("AM a.py", StatusLine(status="AM", orig_path=None, path="a.py")),
        ("AD a.py", StatusLine(status="AD", orig_path=None, path="a.py")),
        ("D  a.py", StatusLine(status="D ", orig_path=None, path="a.py")),
        ("R  a.py -> b.py", StatusLine(status="R ", orig_path="a.py", path="b.py")),
        ("RM a.py -> b.py", StatusLine(status="RM", orig_path="a.py", path="b.py")),
        ("RD a.py -> b.py", StatusLine(status="RD", orig_path="a.py", path="b.py")),
        ("C  a.py", StatusLine(status="C ", orig_path=None, path="a.py")),
        ("CM a.py", StatusLine(status="CM", orig_path=None, path="a.py")),
        ("CD a.py", StatusLine(status="CD", orig_path=None, path="a.py")),
        (" R a.py -> b.py", StatusLine(status=" R", orig_path="a.py", path="b.py")),
        ("DR a.py -> b.py", StatusLine(status="DR", orig_path="a.py", path="b.py")),
        (" C a.py", StatusLine(status=" C", orig_path=None, path="a.py")),
        ("DC a.py", StatusLine(status="DC", orig_path=None, path="a.py")),
        # Statuses with merge conflicts
        ("DD a.py", StatusLine(status="DD", orig_path=None, path="a.py")),
        ("AU a.py", StatusLine(status="AU", orig_path=None, path="a.py")),
        ("UD a.py", StatusLine(status="UD", orig_path=None, path="a.py")),
        ("UA a.py", StatusLine(status="UA", orig_path=None, path="a.py")),
        ("DU a.py", StatusLine(status="DU", orig_path=None, path="a.py")),
        ("AA a.py", StatusLine(status="AA", orig_path=None, path="a.py")),
        ("UU a.py", StatusLine(status="UU", orig_path=None, path="a.py")),
        # Untracked and Ignored Statuses
        ("?? a.py", StatusLine(status="??", orig_path=None, path="a.py")),
        ("!! a.py", StatusLine(status="!!", orig_path=None, path="a.py")),
        # Status lines with quoted and escaped paths
        ('A  "file with a space.txt"', StatusLine(status="A ", orig_path=None, path='"file with a space.txt"')),
        (r'A  "file with a space \/ and slash.txt"', StatusLine(status="A ", orig_path=None, path=r'"file with a space \/ and slash.txt"')),
    ]
    for line, parse_example in test_pairs:
        assert parse(line) == parse_example
