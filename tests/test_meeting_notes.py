from __future__ import annotations

from pathlib import Path
import unittest

from meeting_intelligence import summarize_meeting_transcript


ROOT = Path(__file__).resolve().parents[1]


class MeetingNotesTests(unittest.TestCase):
    def test_voice_memo_demo_preserves_actions_and_risks(self) -> None:
        transcript = (ROOT / "examples/transcripts/team_sync.txt").read_text(encoding="utf-8")
        notes = summarize_meeting_transcript(transcript)
        markdown = notes.to_markdown()

        self.assertIn("webhook retry metric", markdown)
        self.assertIn("Avery", markdown)
        self.assertIn("Friday", markdown)
        self.assertIn("## Risks And Blockers", markdown)
        self.assertIn("## Next Steps", markdown)


if __name__ == "__main__":
    unittest.main()
