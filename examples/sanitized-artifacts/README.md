# Sanitized Artifacts

These files preserve the shape of the real workflow while replacing private content with ACME examples.

Included:

- `voice-memo-recording/metadata.json` - production-shaped recording metadata.
- `voice-memo-recording/* summary.md` - model-specific summaries from a dual summary run.
- `voice-memo-recording/summary-evaluation.json` and `.md` - judge output used to compare summaries.
- `autoresearch/*.job.json` - sanitized AutoResearch job shape created from evaluated recordings.
- `autoresearch/*.summary.json` and `.proposal.json` - sanitized result and promotion artifacts.

Not included:

- Audio files.
- Raw private transcripts.
- Secrets.
- Local logs.
