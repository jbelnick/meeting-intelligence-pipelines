---
Date Created: 2026-06-16
Date modified: 2026-06-25 9:14 AM
Status: active
Tags:
  - belnick
  - project
  - meeting-intelligence-pipelines
  - agent-policy
---

# AGENTS.md - meeting-intelligence-pipelines

Agent policy for `projects/products/meeting-intelligence-pipelines` — a
public-safe engineering case study (portfolio repo) with its own git remote. It
is not a live workflow root and must stay publishable.

Narrows the root [[AGENTS]] policy; only what differs or tightens here.

## Scope / Folder Roles

| Area | Role / Edit rule |
|---|---|
| `src/`, `tests/`, `scripts/` | Reusable pipeline code, unit tests, and CLI entry points. Keep compact and dependency-free; mirror production schemas, not private content. |
| `examples/sanitized-artifacts/` | Source of all examples. Reference these — never invent estate paths or real client data. |
| `docs/` | Architecture and pipeline notes. Public-safe narrative only. |
| `outputs/` | Git-ignored demo output. Regenerate via the Makefile; never commit. |
| `README.md` | Upstream-facing. Keep badges and links accurate to the public remote. |

## Rules

1. Public-safe only: no estate paths, credentials, personal data, or live
   runtime references in any tracked file. Examples come from
   `examples/sanitized-artifacts/`.
2. Never commit `outputs/`; it is git-ignored demo output, regenerated via the
   Makefile.
3. Keep `README.md` badges and links accurate to the public remote.

## Verification

- `make verify` (runs `test` + `smoke` + `scan`) before calling changes done.
- At minimum `make test` for code-only changes; always run the public-safety
  scanner (`make scan`, or
  `python3 scripts/public_safety_scan.py --term "$BANNED_TERM"`) before
  publishing.

Always report any verification that could not be run and why.
