# Meeting Intelligence Pipelines

This repository is a public-safe portfolio showcase for applied AI workflow engineering. It demonstrates how meeting audio, video transcripts, and evaluation-driven prompt improvement can work together without publishing private source data, secrets, or customer-specific material.

Everything in this repo is synthetic or sanitized. The architecture mirrors production patterns I have built: command-triggered capture, transcript generation, chunked summarization, deterministic rendering, evaluation, and prompt-variant promotion.

## What This Shows

- `/voicememo` style workflow: capture or receive a meeting transcript, produce structured notes, save model-specific artifacts, and keep metadata about the chosen result.
- `video-summarize` style workflow: ingest a video or audio transcript, chunk long text, build per-chunk notes, sanitize notes, and render a final summary locally.
- AutoResearch style improvement loop: evaluate meeting-note outputs against concrete criteria, mine failure modes, test prompt variants, and promote the strongest variant.
- Public-safety workflow: scan tracked content and generated artifacts for banned client terms and common secret patterns before publishing.

## Quick Start

```bash
python3 scripts/run_full_demo.py
python3 -m unittest discover -s tests -v
python3 scripts/public_safety_scan.py --term "$BANNED_TERM"
```

The full demo writes generated artifacts to `outputs/`, which is intentionally git-ignored.

## Repository Layout

```text
docs/                  Architecture and pipeline notes
examples/              Synthetic transcripts and eval cases
scripts/               CLI entry points and public-safety scanner
src/meeting_intelligence/  Reusable pipeline code
tests/                 Unit tests for demos and safety checks
```

## Demo Commands

Run the voice memo style pipeline:

```bash
PYTHONPATH=src python3 scripts/run_voice_memo_demo.py \
  --transcript examples/transcripts/team_sync.txt \
  --out outputs/voice-memo-demo.md
```

Run the video summary style pipeline:

```bash
PYTHONPATH=src python3 scripts/run_video_summary_demo.py \
  --transcript examples/transcripts/product_walkthrough.txt \
  --title "Product Walkthrough" \
  --out outputs/video-summary-demo.md
```

Run the AutoResearch style prompt-variant loop:

```bash
PYTHONPATH=src python3 scripts/run_autoresearch_demo.py \
  --cases examples/autoresearch/evaluation_cases.json \
  --out outputs/autoresearch-report.json \
  --markdown-out outputs/autoresearch-report.md
```

Run everything:

```bash
PYTHONPATH=src python3 scripts/run_full_demo.py
```

## What Is Real vs Synthetic

Real architectural ideas represented here:

- A command surface starts the workflow.
- Audio or transcript artifacts are preserved separately from summaries.
- Long transcript input is chunked before summary generation.
- Summary rendering is deterministic once note sheets are parsed.
- Evaluation criteria focus on factuality, owners, dates, decisions, blockers, and action items.
- Prompt variants are promoted only when validation scores improve without regressions.

Synthetic parts:

- Example transcripts are invented.
- Model calls are represented by deterministic local functions so reviewers can run the repo without API keys.
- Evaluation cases are small fixtures designed to show the mechanics of the loop.

## Public-Safety Checks

Run the scanner before publishing:

```bash
python3 scripts/public_safety_scan.py --term "$BANNED_TERM"
```

The scanner checks project files for banned terms supplied at runtime and common secret-like patterns. It avoids hard-coding private client names into the repository itself.

## Engineering Notes

The code is intentionally compact and dependency-free. In production, the same interfaces can be backed by real transcription providers, local OpenAI-compatible model servers, queue runners, and dashboard APIs. For this public repo, the focus is the pipeline architecture and verification discipline.
