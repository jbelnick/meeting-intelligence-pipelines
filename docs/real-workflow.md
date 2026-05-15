# Real Workflow

This is the sanitized shape of the production workflow. Private names are replaced with ACME and private artifacts are omitted.

## Slack To Native Voice Memo

```mermaid
sequenceDiagram
    participant User
    participant Slack
    participant Hermes as Hermes Slack gateway
    participant Cipher as cipher-workflows Slack runner
    participant Claw as Claw voice-memo controls
    participant Mac as macOS Voice Memos
    participant Models as Local summary models
    participant Judge as Cipher judge
    participant Store as Recording artifacts

    User->>Slack: /voicememo
    Slack->>Hermes: slash command payload
    Hermes->>Cipher: route voicememo through cipher-workflows
    Cipher->>Slack: post voice memo controls
    User->>Slack: Start Recording - ACME
    Cipher->>Claw: voice-memo-start.sh --collection ACME
    Claw->>Mac: launch/focus native Voice Memos and start capture
    User->>Slack: Stop -> Summarize
    Cipher->>Claw: voice-memo-pipeline.sh --pipeline dual --channel slack
    Claw->>Mac: stop recording and locate .m4a
    Mac-->>Claw: native audio file or UI export fallback
    Claw->>Claw: extract transcript and create pending folder
    Claw->>Models: summarize sequential local model branches
    Claw->>Models: run optional cloud branch in dual mode
    Models-->>Claw: model-specific summary files
    Claw->>Store: metadata.json, transcript.txt, summary files
    Claw->>Judge: evaluate summaries
    Judge-->>Store: summary-evaluation.json / .md
    Cipher->>Slack: update original message with final folder, summary, transcript
```

## Important Runtime Details

- Slack commands are handled by the Hermes gateway and routed through the `cipher-workflows` plugin.
- Slack `/voicememo` uses a Slack-native runner instead of Telegram bridge semantics.
- The runner posts or updates Slack control messages and calls the Claw voice memo scripts.
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
