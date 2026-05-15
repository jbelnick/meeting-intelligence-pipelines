# Real Workflow

This is the sanitized shape of the production workflow. Private names are replaced with ACME and private artifacts are omitted.

## Slack To Native Voice Memo

```mermaid
flowchart LR
    subgraph Slack["Slack front door"]
        Command["/voicememo"]
        Panel["Voice memo controls<br/>Start / Stop / Status"]
        Update["Final Slack update<br/>folder + summary + transcript"]
    end

    subgraph Hermes["Hermes runtime"]
        Gateway["Slack gateway"]
        Runner["meeting-intelligence-workflows<br/>Slack runner"]
    end

    subgraph Native["Hermes-native workflow bundle"]
        Start["voice-memo-start.sh<br/>collection = ACME"]
        Record["macOS Voice Memos<br/>native recording"]
        Stop["voice-memo-pipeline.sh<br/>dual + slack source"]
        Audio["Locate .m4a<br/>or UI export fallback"]
        Transcript["Transcript extraction<br/>sidecar, then Apple Speech"]
        Pending["Pending folder<br/>audio + transcript"]
    end

    subgraph Summary["Summary and evaluation"]
        Local["Sequential local models"]
        Cloud["Optional cloud branch"]
        Summaries["Model-specific<br/>summary files"]
        Eval["Judge evaluation<br/>summary-evaluation.json / .md"]
    end

    subgraph Store["Recording artifact lane"]
        Final["Final folder<br/>metadata + transcript + summaries"]
    end

    Command --> Gateway --> Runner --> Panel
    Panel -->|"Start Recording - ACME"| Start --> Record
    Panel -->|"Stop -> Summarize"| Stop
    Record --> Stop --> Audio --> Transcript --> Pending
    Pending --> Local --> Summaries
    Pending --> Cloud --> Summaries
    Summaries --> Eval --> Final --> Update

    classDef slack fill:#eef6ff,stroke:#2563eb,color:#0f172a
    classDef hermes fill:#f3e8ff,stroke:#7e22ce,color:#111827
    classDef native fill:#ecfdf5,stroke:#059669,color:#0f172a
    classDef model fill:#fff7ed,stroke:#ea580c,color:#111827
    classDef artifact fill:#f8fafc,stroke:#475569,color:#0f172a

    class Command,Panel,Update slack
    class Gateway,Runner hermes
    class Start,Record,Stop,Audio,Transcript,Pending native
    class Local,Cloud,Summaries,Eval model
    class Final artifact
```

## Important Runtime Details

- Slack commands are handled by the Hermes gateway and routed through the `meeting-intelligence-workflows` runner.
- Slack `/voicememo` uses a Slack-native runner instead of Telegram bridge semantics.
- The runner posts or updates Slack control messages and calls the migrated Hermes-native workflow bundle.
- Start calls the native voice memo start script with a collection. In this repo the private collection name is sanitized to `ACME`.
- Stop calls `voice-memo-pipeline.sh --pipeline dual --channel slack --source slack-voicememo-controls`.
- The native macOS Voice Memos app writes audio under the Voice Memos group container. If direct detection fails, the production scripts attempt a UI export fallback.
- Transcript extraction first tries the Voice Memos transcript sidecar path and then falls back to the compiled Apple Speech transcriber.
- The pipeline writes a pending folder, extracts `transcript.txt`, then runs the summary branches.
- `dual` mode writes local model outputs and a cloud output when they succeed.
- Local model branches run sequentially so the machine does not load every local model at once.
- `metadata.json` records `channel`, `collection`, `source`, `pipelineType`, delivered `summaryModel`, delivered `summaryFile`, and `summaryArtifacts`.
- The summary evaluator compares model-specific summaries against the transcript and writes `summary-evaluation.json` plus `summary-evaluation.md`.

## Artifact Contract

The final recording folder contains:

- `transcript.txt`
- `metadata.json`
- one or more `[model] summary.md` files
- `summary-evaluation.json`
- `summary-evaluation.md`

The sanitized example in `examples/sanitized-artifacts/voice-memo-recording/` keeps that shape without publishing audio, private transcripts, secrets, or logs.
