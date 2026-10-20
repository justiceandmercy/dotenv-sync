import tempfile
from pathlib import Path

import dotenv_sync


def test_parse_keys_basic():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / ".env"
        p.write_text("FOO=1\n# comment\nBAR=2\nexport BAZ=3\n", encoding="utf-8")
        assert dotenv_sync.parse_keys(p) == {"FOO", "BAR", "BAZ"}


def test_diff_reports_both_directions():
    missing, stale = dotenv_sync.diff({"A", "B"}, {"B", "C"})
    assert missing == ["A"]
    assert stale == ["C"]


def test_find_pairs_includes_local():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / ".env.local").write_text("X=1\n", encoding="utf-8")
        (root / ".env.local.example").write_text("X=\n", encoding="utf-8")
        pairs = dotenv_sync.find_pairs(root)
        assert any(p[0].name == ".env.local" for p in pairs)
