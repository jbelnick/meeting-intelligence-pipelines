from __future__ import annotations

from pathlib import Path
import unittest

from meeting_intelligence.autoresearch import load_cases, run_prompt_research


ROOT = Path(__file__).resolve().parents[1]


class AutoResearchTests(unittest.TestCase):
    def test_detail_guard_beats_baseline_without_regressions(self) -> None:
        cases = load_cases(ROOT / "examples/autoresearch/evaluation_cases.json")
        report = run_prompt_research(cases)

        self.assertEqual(report.winning_variant, "detail-ownership-guard")
        self.assertGreater(report.validation_delta, 0)
        self.assertEqual(report.regressions, 0)


if __name__ == "__main__":
    unittest.main()
