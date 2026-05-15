#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_intelligence import summarize_video_transcript


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the video transcript summary demo.")
    parser.add_argument("--transcript", type=Path, default=ROOT / "examples/transcripts/product_walkthrough.txt")
    parser.add_argument("--title", default="Product Walkthrough")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs/video-summary-demo.md")
    args = parser.parse_args()

    summary = summarize_video_transcript(
        args.transcript.read_text(encoding="utf-8"),
        title=args.title,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(summary.to_markdown(), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
