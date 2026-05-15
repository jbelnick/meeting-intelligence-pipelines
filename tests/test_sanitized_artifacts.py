from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "examples/sanitized-artifacts"


class SanitizedArtifactTests(unittest.TestCase):
    def test_voice_memo_metadata_matches_real_contract(self) -> None:
        metadata = json.loads((ARTIFACTS / "voice-memo-recording/metadata.json").read_text(encoding="utf-8"))

        self.assertEqual(metadata["channel"], "slack")
        self.assertEqual(metadata["collection"], "ACME")
        self.assertEqual(metadata["source"], "slack-voicememo-controls")
        self.assertEqual(metadata["pipelineType"], "dual")
        self.assertIn("summaryArtifacts", metadata)
        self.assertGreaterEqual(len(metadata["summaryArtifacts"]["localModels"]), 3)

    def test_autoresearch_summary_matches_real_result_contract(self) -> None:
        summary = json.loads(
            (ARTIFACTS / "autoresearch/voice-memo-summary-qwen3.6-27b-q5_K_M.summary.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(summary["status"], "proposal_ready")
        self.assertEqual(summary["variable"], "promptVariant")
        self.assertEqual(summary["promotion"]["validationRegressions"], 0)
        self.assertEqual(summary["bestCandidate"]["value"]["label"], "voice-memo-detail-ownership-guard")


if __name__ == "__main__":
    unittest.main()
