# Voice Memo Pipeline

The `/voicememo` style pipeline starts from a command or recording control and ends with structured meeting notes plus metadata.

```mermaid
flowchart TD
    A["/voicememo command"] --> B["Recording control"]
    B --> C["Audio or transcript artifact"]
    C --> D["Transcript extraction"]
    D --> E["Pending work folder"]
    E --> F["Local and cloud summary branches"]
    F --> G["Model-specific summary files"]
    G --> H["Metadata records winning branch"]
    H --> I["Final recording folder"]
```

## Demo

```bash
PYTHONPATH=src python3 scripts/run_voice_memo_demo.py
```

The demo reads `examples/transcripts/team_sync.txt` and writes `outputs/voice-memo-demo.md`.

## Production Pattern Represented

- Command-triggered workflow.
- Transcript and summaries saved as separate artifacts.
- Summary output uses consistent sections: summary, key points, decisions, risks, next steps, and open questions.
- Owners and dates are preserved when explicitly stated.
- Unclear items remain open questions instead of being converted into false decisions.
