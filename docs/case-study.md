---
Date Created: 2026-06-16
Date modified: 2026-06-16 10:06 PM
Status: active
Tags:
  - belnick
  - project
  - meeting-intelligence-pipelines
---

# Case Study: Meeting Intelligence Pipelines

## Problem

Meeting and video workflows become brittle when the capture surface, transcript extraction, summarization, evaluation, and prompt-improvement loop are treated as separate scripts. A useful workflow needs to preserve raw source artifacts, produce reviewable summaries, evaluate quality, and turn failures into prompt-improvement jobs without exposing private recordings or transcripts.

The production pattern behind this repo solved three linked problems:

- Voice memo capture needed a reliable command surface that could start, stop, summarize, and report status back to the requester.
- Video and recording summaries needed deterministic artifact contracts so downstream publishing and review were not dependent on ad hoc prose.
- Weak summaries needed to feed a repeatable prompt-variant evaluation loop instead of becoming one-off manual feedback.

## Architecture

This public repo models the workflow as three connected lanes:

- **Voice memo lane:** command-style entry, native capture, transcript extraction, summary rendering, metadata, and evaluation artifacts.
- **Video summary lane:** transcript chunking, structured note extraction, and deterministic final-note rendering.
- **AutoResearch lane:** evaluated artifacts become prompt-variant cases, candidates are scored on train and validation examples, and promotion requires improvement without regressions.

The reusable code lives under `src/meeting_intelligence/`, while `scripts/` provides reviewer-friendly entry points. The committed files in `examples/sanitized-artifacts/` preserve schema and lifecycle shape without publishing private source data.

## Tradeoffs

The repo uses synthetic transcripts and deterministic local functions. That keeps the case study cloneable and safe to run in GitHub Actions, but it means the demo is not claiming to perform live transcription, Slack delivery, native macOS automation, or live model inference.

The artifact contracts are intentionally more important than model cleverness. A reviewer can inspect exactly what the pipeline writes, how a replay works, and how an AutoResearch proposal is accepted or rejected. The tradeoff is that the public implementation is compact rather than infrastructure-complete.

The safety scan is runtime-configurable. Sensitive terms are supplied through `--term`, `BANNED_TERM`, or `PUBLIC_SAFETY_TERMS` so private client names do not need to be committed to prove they are absent.

## Verification

The single proof command is:

```bash
make verify
```

That command runs:

- Unit tests for meeting-note extraction, video summary rendering, replay, AutoResearch scoring, sanitized artifacts, and public-safety scanning.
- Smoke generation for the full demo and the sanitized replay.
- A public-safety scan over tracked files.

GitHub Actions runs the same `make verify` command on every push and pull request to `main`. The hosted proof path is intentionally the same as the local proof path.

## Sanitized Boundary

This repository keeps the production workflow shape while replacing private surfaces:

| Real system concept | Public repo representation |
| --- | --- |
| Slack-triggered voice memo controls | Command-shaped synthetic demo inputs |
| Native macOS recording and transcript extraction | Invented transcript files under `examples/transcripts/` |
| Model-specific summary branches | Deterministic local renderers with model-shaped metadata |
| Judge evaluation artifacts | Synthetic `summary-evaluation` style outputs |
| AutoResearch prompt-variant jobs | Sanitized evaluation cases and proposal-ready demo output |
| Private recordings, logs, and client data | Omitted or replaced with ACME examples |

The result is a faithful engineering case study: the architecture, file contracts, replay surface, and verification discipline are visible, while private operational data stays out of the public repo.

## Result

The project gives hiring reviewers a concrete applied-AI systems sample: not just "summarize meetings," but capture orchestration, structured artifacts, summary quality evaluation, prompt improvement, reproducible demos, and release safety checks.

