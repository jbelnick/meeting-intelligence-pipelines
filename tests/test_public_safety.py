from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.public_safety_scan import scan


class PublicSafetyTests(unittest.TestCase):
    def test_scan_detects_runtime_banned_term(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.txt").write_text("ForbiddenClient appears here.\n", encoding="utf-8")
            findings = scan(root, ["ForbiddenClient"])
        self.assertEqual(len(findings), 1)

    def test_scan_passes_clean_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.txt").write_text("Only synthetic public data.\n", encoding="utf-8")
            findings = scan(root, ["ForbiddenClient"])
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
