#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_intelligence import summarize_meeting_transcript, summarize_video_transcript
from meeting_intelligence.autoresearch import load_cases, run_prompt_research, write_report


def main() -> int:
    outputs = ROOT / "outputs"
    outputs.mkdir(exist_ok=True)

    meeting_transcript = (ROOT / "examples/transcripts/team_sync.txt").read_text(encoding="utf-8")
    meeting_notes = summarize_meeting_transcript(meeting_transcript)
    voice_path = outputs / "voice-memo-demo.md"
    voice_path.write_text(meeting_notes.to_markdown(), encoding="utf-8")

    video_transcript = (ROOT / "examples/transcripts/product_walkthrough.txt").read_text(encoding="utf-8")
    video_summary = summarize_video_transcript(video_transcript, title="Product Walkthrough")
    video_path = outputs / "video-summary-demo.md"
    video_path.write_text(video_summary.to_markdown(), encoding="utf-8")

    report = run_prompt_research(load_cases(ROOT / "examples/autoresearch/evaluation_cases.json"))
    json_path = outputs / "autoresearch-report.json"
    markdown_path = outputs / "autoresearch-report.md"
    write_report(report, json_path, markdown_path)

    for path in (voice_path, video_path, json_path, markdown_path):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
