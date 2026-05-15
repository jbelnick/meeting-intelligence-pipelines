# Architecture

This repo is organized around the real workflow boundary: Slack and Hermes trigger the workflow, a migrated Hermes-native bundle owns the macOS and model pipeline, artifacts preserve every branch result, and AutoResearch turns evaluation failures into prompt variants.

## System Map

```mermaid
flowchart LR
    Slack["Slack slash command"] --> Hermes["Hermes gateway"]
    Hermes --> Bundle["Hermes-native workflow bundle"]
    Bundle --> Mac["macOS Voice Memos"]
    Mac --> Transcript["transcript.txt"]
    Transcript --> Summaries["model-specific summaries"]
    Summaries --> Eval["summary-evaluation.json"]
    Eval --> Research["AutoResearch promptVariant job"]
    Research --> Promotion["proposal.json"]
    Promotion --> Safety["public-safety scan"]
    Promotion --> Safety
```

## Design Principles

- Preserve raw source artifacts separately from generated notes.
- Keep transcript chunking explicit so long inputs are not silently truncated.
- Render final summaries from structured notes instead of relying on a fragile final merge.
- Treat evaluation as a first-class pipeline output, not a manual afterthought.
- Keep public artifacts synthetic and scan them before publishing.

## Public Repo Boundary

This repository does not include private recordings, raw transcripts, live configs, secrets, logs, or customer-specific labels. The examples are invented to demonstrate the engineering pattern.
