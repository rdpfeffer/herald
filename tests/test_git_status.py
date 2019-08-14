from collections import namedtuple

from herald.git_status import StatusEntry, parse

from .context import herald

Case = namedtuple("Case", ["line", "status_entry", "deleted", "unmerged", "submodule"])
TEST_CASES = [
    # Statuses without merge conflicts
    Case(
        "1 .A N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status=".A", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 .M N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status=".M", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 .D N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status=".D", orig_path=None, path="a.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "1 M. N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="M.", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 MM N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="MM", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 MD N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="MD", orig_path=None, path="a.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "1 A. N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="A.", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 AM N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="AM", orig_path=None, path="a.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "1 AD N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="AD", orig_path=None, path="a.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "1 D. N... 100644 100644 100644 b42d4eff b42d4eff a.py",
        StatusEntry(status="D.", orig_path=None, path="a.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "2 R. N... 100644 100644 100644 b42d4eff b42d4eff R100 b.py\ta.py",
        StatusEntry(status="R.", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 RM N... 100644 100644 100644 b42d4eff b42d4eff R100 b.py\ta.py",
        StatusEntry(status="RM", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 RD N... 100644 100644 100644 b42d4eff b42d4eff R100 b.py\ta.py",
        StatusEntry(status="RD", orig_path="a.py", path="b.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "2 C. N... 100644 100644 100644 b42d4eff b42d4eff C100 b.py\ta.py",
        StatusEntry(status="C.", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 CM N... 100644 100644 100644 b42d4eff b42d4eff C100 b.py\ta.py",
        StatusEntry(status="CM", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 CD N... 100644 100644 100644 b42d4eff b42d4eff C100 b.py\ta.py",
        StatusEntry(status="CD", orig_path="a.py", path="b.py", submodule="N..."),
        True,
        False,
        False,
    ),
    Case(
        "2 .R N... 100644 100644 100644 b42d4eff b42d4eff R100 b.py\ta.py",
        StatusEntry(status=".R", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 DR N... 100644 100644 100644 b42d4eff b42d4eff R100 b.py\ta.py",
        StatusEntry(status="DR", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 .C N... 100644 100644 100644 b42d4eff b42d4eff C100 b.py\ta.py",
        StatusEntry(status=".C", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    Case(
        "2 DC N... 100644 100644 100644 b42d4eff b42d4eff C100 b.py\ta.py",
        StatusEntry(status="DC", orig_path="a.py", path="b.py", submodule="N..."),
        False,
        False,
        False,
    ),
    # Statuses with merge conflicts
    Case(
        "u DD N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="DD", orig_path=None, path="a.py", submodule="N..."),
        True,
        True,
        False,
    ),
    Case(
        "u AU N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="AU", orig_path=None, path="a.py", submodule="N..."),
        False,
        True,
        False,
    ),
    Case(
        "u UD N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="UD", orig_path=None, path="a.py", submodule="N..."),
        True,
        True,
        False,
    ),
    Case(
        "u UA N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="UA", orig_path=None, path="a.py", submodule="N..."),
        False,
        True,
        False,
    ),
    Case(
        "u DU N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="DU", orig_path=None, path="a.py", submodule="N..."),
        True,
        True,
        False,
    ),
    Case(
        "u AA N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="AA", orig_path=None, path="a.py", submodule="N..."),
        False,
        True,
        False,
    ),
    Case(
        "u UU N... 100644 100644 100644 100644 b42d4eff b42d4eff b42d4eff a.py",
        StatusEntry(status="UU", orig_path=None, path="a.py", submodule="N..."),
        False,
        True,
        False,
    ),
    # # Untracked and Ignored Statuses
    Case(
        "? a.py",
        StatusEntry(status="??", orig_path=None, path="a.py", submodule=None),
        False,
        False,
        False,
    ),
    Case(
        "! a.py",
        StatusEntry(status="!!", orig_path=None, path="a.py", submodule=None),
        False,
        False,
        False,
    ),
    # # Status lines with quoted and escaped paths
    Case(
        '1 A. N... 100644 100644 100644 b42d4eff b42d4eff "file with a space.txt"',
        StatusEntry(
            status="A.",
            orig_path=None,
            path='"file with a space.txt"',
            submodule="N...",
        ),
        False,
        False,
        False,
    ),
    Case(
        r'1 A. N... 100644 100644 100644 b42d4eff b42d4eff "file with a space \/ and slash.txt"',
        StatusEntry(
            status="A.",
            orig_path=None,
            path=r'"file with a space \/ and slash.txt"',
            submodule="N...",
        ),
        False,
        False,
        False,
    ),
    Case(
        "1 .M SC.. 100644 100644 100644 b42d4eff b42d4eff a",
        StatusEntry(status=".M", orig_path=None, path="a", submodule="SC.."),
        False,
        False,
        True,
    ),
]


def test_parse():
    for line, status_entry, _, _, _ in TEST_CASES:
        assert parse(line) == status_entry


def test_is_deleted():
    for line, _, deleted, _, _ in TEST_CASES:
        assert parse(line).is_deleted() == deleted


def test_is_unmerged():
    for line, _, _, unmerged, _ in TEST_CASES:
        assert parse(line).is_unmerged() == unmerged


def test_is_submodule():
    for line, _, _, _, submodule in TEST_CASES:
        assert parse(line).is_submodule() == submodule
