---
Date Created: 2026-06-16
Date modified: 2026-06-16 10:06 PM
Status: active
Tags:
  - belnick
  - project
  - meeting-intelligence-pipelines
  - agent-policy
---

# AGENTS.md - meeting-intelligence-pipelines

Narrows the root [[AGENTS]] policy for
`projects/products/meeting-intelligence-pipelines`.

Public-safe engineering case study (portfolio repo). It is not a live workflow
root and must stay publishable.

## Boundaries

| Rule | Detail |
|---|---|
| Public-safe only | No estate paths, credentials, personal data, or live runtime references. Examples come from `examples/sanitized-artifacts/`. |
| `outputs/` | Git-ignored demo output; regenerate via the Makefile, never commit. |
| Upstream-facing README | Keep badges/links accurate to the public remote. |

## Verification

`make test` (or the repo's documented test target) before calling changes done.
