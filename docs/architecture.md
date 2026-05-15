# Architecture

This repo is organized around the real workflow boundary: Slack and Hermes trigger the workflow, a migrated Hermes-native bundle owns the macOS and model pipeline, artifacts preserve every branch result, and AutoResearch turns evaluation failures into prompt variants.

## System Map

```mermaid
%%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 52, "rankSpacing": 62}, "themeVariables": {"fontSize": "18px", "fontFamily": "Inter, ui-sans-serif, system-ui"}}}%%
flowchart TB
    subgraph Entry["1. Command entry"]
        direction TB
        Slack["Slack slash command"]
        Hermes["Hermes gateway"]
    end

    subgraph Capture["2. Native capture"]
        direction TB
        Bundle["Hermes-native<br/>workflow bundle"]
        Mac["macOS Voice Memos"]
        Transcript["transcript.txt"]
    end

    subgraph Notes["3. Notes and artifacts"]
        direction TB
        Summaries["Model-specific<br/>summary files"]
        Eval["summary-evaluation.json"]
    end

    subgraph Research["4. Self-improvement"]
        direction TB
        Job["AutoResearch<br/>promptVariant job"]
        Proposal["proposal.json"]
    end

    subgraph Safety["5. Public release gate"]
        direction TB
        Scan["public-safety scan"]
    end

    Slack --> Hermes --> Bundle --> Mac --> Transcript
    Transcript --> Summaries --> Eval
    Eval --> Job --> Proposal --> Scan

    classDef entry fill:#eef6ff,stroke:#2563eb,stroke-width:2px,color:#0f172a
    classDef capture fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#0f172a
    classDef notes fill:#fff7ed,stroke:#ea580c,stroke-width:2px,color:#111827
    classDef research fill:#f3e8ff,stroke:#7e22ce,stroke-width:2px,color:#111827
    classDef safety fill:#f8fafc,stroke:#475569,stroke-width:2px,color:#0f172a

    class Slack,Hermes entry
    class Bundle,Mac,Transcript capture
    class Summaries,Eval notes
    class Job,Proposal research
    class Scan safety
```

## Design Principles

- Preserve raw source artifacts separately from generated notes.
- Keep transcript chunking explicit so long inputs are not silently truncated.
- Render final summaries from structured notes instead of relying on a fragile final merge.
- Treat evaluation as a first-class pipeline output, not a manual afterthought.
- Keep public artifacts synthetic and scan them before publishing.

## Public Repo Boundary

This repository does not include private recordings, raw transcripts, live configs, secrets, logs, or customer-specific labels. The examples are invented to demonstrate the engineering pattern.
