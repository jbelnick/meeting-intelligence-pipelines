#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_intelligence.autoresearch import load_cases, run_prompt_research, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the AutoResearch style prompt-variant demo.")
    parser.add_argument("--cases", type=Path, default=ROOT / "examples/autoresearch/evaluation_cases.json")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs/autoresearch-report.json")
    parser.add_argument("--markdown-out", type=Path, default=ROOT / "outputs/autoresearch-report.md")
    args = parser.parse_args()

    report = run_prompt_research(load_cases(args.cases))
    write_report(report, args.out, args.markdown_out)
    print(args.out)
    print(args.markdown_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
