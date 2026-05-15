# Real Workflow

This is the sanitized shape of the production workflow. Private names are replaced with ACME and private artifacts are omitted.

## Slack To Native Voice Memo

```mermaid
sequenceDiagram
    participant User
    participant Slack
    participant Hermes as Hermes Slack gateway
    participant Workflows as meeting-intelligence-workflows runner
    participant Native as Hermes-native voice memo bundle
    participant Mac as macOS Voice Memos
    participant Models as Local summary models
    participant Judge
    participant Store as Recording artifacts

    User->>Slack: /voicememo
    Slack->>Hermes: slash command payload
    Hermes->>Workflows: route voicememo through meeting-intelligence-workflows
    Workflows->>Slack: post voice memo controls
    User->>Slack: Start Recording - ACME
    Workflows->>Native: voice-memo-start.sh --collection ACME
    Native->>Mac: launch/focus native Voice Memos and start capture
    User->>Slack: Stop -> Summarize
    Workflows->>Native: voice-memo-pipeline.sh --pipeline dual --channel slack
    Native->>Mac: stop recording and locate .m4a
    Mac-->>Native: native audio file or UI export fallback
    Native->>Native: extract transcript and create pending folder
    Native->>Models: summarize sequential local model branches
    Native->>Models: run optional cloud branch in dual mode
    Models-->>Native: model-specific summary files
    Native->>Store: metadata.json, transcript.txt, summary files
    Native->>Judge: evaluate summaries
    Judge-->>Store: summary-evaluation.json / .md
    Workflows->>Slack: update original message with final folder, summary, transcript
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
