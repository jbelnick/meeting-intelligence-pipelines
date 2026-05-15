# Voice Memo Pipeline

This page documents the sanitized shape of the real Slack-triggered voice memo workflow. The local demo stays transcript-only, but the production-shaped diagram shows the actual command route, native macOS capture path, transcript extraction, summary branches, Judge output, and artifact contract.

```mermaid
%%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 48, "rankSpacing": 58}, "themeVariables": {"fontSize": "18px", "fontFamily": "Inter, ui-sans-serif, system-ui"}}}%%
flowchart TB
    subgraph Slack["1. Slack command surface"]
        direction TB
        Command["/voicememo"]
        Controls["Slack controls<br/>Start / Stop / Status"]
        Status["Thread updates<br/>recording, summarizing, delivered"]
    end

    subgraph Hermes["2. Hermes routing"]
        direction TB
        Gateway["Hermes Slack gateway"]
        Runner["meeting-intelligence-workflows<br/>Slack runner"]
        StartCall["Start call<br/>collection = ACME"]
        StopCall["Stop call<br/>pipeline = dual<br/>channel = slack"]
    end

    subgraph Native["3. Native capture bundle"]
        direction TB
        Start["voice-memo-start.sh"]
        App["macOS Voice Memos<br/>native recording"]
        Stop["voice-memo-pipeline.sh"]
        Audio["Locate .m4a<br/>or UI export fallback"]
        Transcript["Transcript sidecar<br/>then Apple Speech fallback"]
    end

    subgraph Artifacts["4. Recording artifact lane"]
        direction TB
        Pending["Pending folder<br/>audio + transcript"]
        Summaries["Model summary files<br/>one markdown per model"]
        Eval["Judge files<br/>summary-evaluation.json / .md"]
        Metadata["metadata.json<br/>channel, source, pipelineType, summaryArtifacts"]
        Final["Final recording folder"]
    end

    Command --> Controls --> Gateway --> Runner
    Controls --> Status
    Runner --> StartCall --> Start --> App
    Runner --> StopCall --> Stop
    App --> Audio
    Stop --> Audio --> Transcript --> Pending
    Pending --> Summaries --> Eval
    Pending --> Metadata
    Eval --> Final
    Metadata --> Final
    Final --> Status

    classDef slack fill:#eef6ff,stroke:#2563eb,stroke-width:2px,color:#0f172a
    classDef hermes fill:#f3e8ff,stroke:#7e22ce,stroke-width:2px,color:#111827
    classDef native fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#0f172a
    classDef artifact fill:#fff7ed,stroke:#ea580c,stroke-width:2px,color:#111827

    class Command,Controls,Status slack
    class Gateway,Runner,StartCall,StopCall hermes
    class Start,App,Stop,Audio,Transcript native
    class Pending,Summaries,Eval,Metadata,Final artifact
```

## Demo

```bash
PYTHONPATH=src python3 scripts/run_voice_memo_demo.py
```

The demo reads `examples/transcripts/team_sync.txt` and writes `outputs/voice-memo-demo.md`.

## Real Workflow Shape

- Slack `/voicememo` is the front door. The Hermes Slack gateway routes the command to `meeting-intelligence-workflows`.
- Start and stop are separate native calls so the Slack control surface can manage a live recording session.
- The capture layer uses the native macOS Voice Memos app instead of a web recorder.
- The stop path runs the dual pipeline, extracts the audio artifact, finds or builds `transcript.txt`, and stages a pending recording folder.
- Summary branches write one model-specific markdown file each. The Judge compares those files against the transcript and emits `summary-evaluation.json` plus `summary-evaluation.md`.
- `metadata.json` records the production-shaped routing fields: `channel`, `collection`, `source`, `pipelineType`, delivered `summaryModel`, delivered `summaryFile`, and `summaryArtifacts`.
- The public demo preserves note structure and artifact naming with synthetic transcript content; it does not call Slack, macOS Voice Memos, private model endpoints, or private logs.
