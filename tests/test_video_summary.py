from __future__ import annotations

from pathlib import Path
import unittest

from meeting_intelligence import summarize_video_transcript


ROOT = Path(__file__).resolve().parents[1]


class VideoSummaryTests(unittest.TestCase):
    def test_video_summary_chunks_and_renders_metadata(self) -> None:
        transcript = (ROOT / "examples/transcripts/product_walkthrough.txt").read_text(encoding="utf-8")
        summary = summarize_video_transcript(transcript, title="Product Walkthrough", max_chars=450)
        markdown = summary.to_markdown()

        self.assertGreaterEqual(summary.chunk_count, 2)
        self.assertIn("Transcript chunks processed", markdown)
        self.assertIn("synthetic data", markdown)


if __name__ == "__main__":
    unittest.main()
