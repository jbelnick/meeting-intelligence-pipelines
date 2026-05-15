#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_intelligence.replay import replay_case_study


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay the sanitized real-workflow case study.")
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=ROOT / "examples/sanitized-artifacts",
        help="Directory containing production-shaped sanitized artifacts.",
    )
    parser.add_argument("--out", type=Path, default=ROOT / "outputs/real-workflow-replay.md")
    args = parser.parse_args()

    report = replay_case_study(args.artifact_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report.to_markdown(), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
