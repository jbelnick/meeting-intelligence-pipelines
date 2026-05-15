#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_intelligence import summarize_meeting_transcript


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the voice memo style meeting-notes demo.")
    parser.add_argument("--transcript", type=Path, default=ROOT / "examples/transcripts/team_sync.txt")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs/voice-memo-demo.md")
    args = parser.parse_args()

    notes = summarize_meeting_transcript(args.transcript.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(notes.to_markdown(), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
