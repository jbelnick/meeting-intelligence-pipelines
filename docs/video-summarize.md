# Video Summarize Pipeline

This page documents the sanitized shape of the real `video-summarize` workflow. The local demo uses a synthetic transcript, but the diagram mirrors the production path: media ingestion, transcription, chunked local summarization, parsed note sheets, and deterministic final rendering.

```mermaid
%%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 48, "rankSpacing": 58}, "themeVariables": {"fontSize": "18px", "fontFamily": "Inter, ui-sans-serif, system-ui"}}}%%
flowchart TB
    subgraph Source["1. Source intake"]
        direction TB
        Request["User provides URL<br/>or transcript file"]
        Download["Download audio/video<br/>yt-dlp"]
        Existing["Existing transcript<br/>skips download"]
    end

    subgraph Transcript["2. Transcript creation"]
        direction TB
        Audio["Extracted audio"]
        Mini["Mini Parakeet<br/>remote Apple Silicon path"]
        Whisper["Whisper MLX<br/>distil-large-v3 path"]
        Text["Transcript artifact<br/>plain text or JSON report"]
    end

    subgraph Summary["3. Local summarization"]
        direction TB
        Chunk["Chunk transcript<br/>context-window aware"]
        Lock["Shared local summary lock<br/>protects model runner"]
        Model["Qwen 3.6 local chat endpoint<br/>OpenAI-compatible API"]
        Notes["Parsed chunk note sheets"]
    end

    subgraph Render["4. Sanitized render"]
        direction TB
        Clean["Sanitize and dedupe notes"]
        Final["Deterministic final summary"]
        Sidecars["Transcript + metadata sidecars"]
    end

    Request --> Download --> Audio
    Request --> Existing --> Text
    Audio --> Mini --> Text
    Audio --> Whisper --> Text
    Text --> Chunk --> Lock --> Model --> Notes
    Notes --> Clean --> Final
    Text --> Sidecars
    Final --> Sidecars

    classDef source fill:#eef6ff,stroke:#2563eb,stroke-width:2px,color:#0f172a
    classDef transcript fill:#ecfdf5,stroke:#059669,stroke-width:2px,color:#0f172a
    classDef model fill:#fff7ed,stroke:#ea580c,stroke-width:2px,color:#111827
    classDef artifact fill:#f8fafc,stroke:#475569,stroke-width:2px,color:#0f172a

    class Request,Download,Existing source
    class Audio,Mini,Whisper,Text transcript
    class Chunk,Lock,Model,Notes model
    class Clean,Final,Sidecars artifact
```

## Demo

```bash
PYTHONPATH=src python3 scripts/run_video_summary_demo.py
```

The demo reads a synthetic transcript and writes a final video summary into `outputs/`.

## Real Workflow Shape

- URL/media sources are downloaded with `yt-dlp`; existing transcript files skip the download and transcription stages.
- Transcription is provider-routed: the fast path uses Mini Parakeet, while the local fallback uses Whisper MLX with `distil-large-v3`.
- The summarizer sends transcript chunks to a local OpenAI-compatible endpoint, with Qwen 3.6 as the represented production model family.
- Chunk sizing is context-window aware so long videos are not silently truncated.
- A shared local summary lock prevents overlapping video, stock-update, and meeting-summary jobs from overloading the same local model runner.
- Each chunk returns a structured note sheet. The final summary is rendered locally from parsed notes instead of relying on a second fragile merge prompt.
- The public demo preserves the artifact lifecycle with synthetic data and never contacts private model services or private source URLs.
