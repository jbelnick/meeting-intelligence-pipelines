from __future__ import annotations

from pathlib import Path
import unittest

from meeting_intelligence.replay import replay_case_study


ROOT = Path(__file__).resolve().parents[1]


class ReplayTests(unittest.TestCase):
    def test_replay_reads_production_shaped_artifacts(self) -> None:
        report = replay_case_study(ROOT / "examples/sanitized-artifacts")
        markdown = report.to_markdown()

        self.assertEqual(report.channel, "slack")
        self.assertEqual(report.source, "slack-voicememo-controls")
        self.assertEqual(report.pipeline_type, "dual")
        self.assertEqual(report.autoresearch_status, "proposal_ready")
        self.assertEqual(report.promoted_variant, "voice-memo-detail-ownership-guard")
        self.assertIn("qwen3.6:27b-q5_K_M", markdown)


if __name__ == "__main__":
    unittest.main()
