---
Date Created: 2026-06-16
Date modified: 2026-07-27 9:29 AM
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

## Estate instruction loading

When operated as part of the BELNICK estate, every agent, harness, and
automation runtime must first manually read
`/Users/admin/BELNICK-AI-AGENTS/00-work-here/docs/reference/AGENT-CONDUCT.md`.
Codex on this host automatically loads `/Users/admin/.codex/AGENTS.md` before
this repository root policy. Non-Codex agents must manually read the BELNICK
contract and stop if it is missing or unreadable. Because this is an
independent Git root, it does not inherit the outer
`/Users/admin/BELNICK-AI-AGENTS/AGENTS.md` instruction chain.

Provenance: NESTED-SENTINEL-meeting-intelligence-pipelines-semantic-fix-20260727

## Mandatory specialist routing

These triggers apply estate-wide, including independent Git roots and non-Codex
agents. Read and apply the canonical owners at these absolute paths:

- **Wiki-first:** When work concerns AI, agents, local models, or the estate's
  own tooling and workflows, consult
  `/Users/admin/BELNICK-AI-AGENTS/llm-wiki/index.md` and apply
  `/Users/admin/BELNICK-AI-AGENTS/llm-wiki/AGENTS.md` before any external search
  and before creating any new document. Search the wiki first; use or extend the existing entry;
  follow `## Related` backlinks to the smallest relevant page set; escalate to
  external research only when the wiki does not cover it, and
  record findings back into the wiki under its ownership, placement, and naming
  rules.
- **GOAL-PROGRESS:** Any goal, task, project, migration, investigation, or
  debugging effort with two or more meaningful stages requires goal-progress
  state to be created and maintained under
  `/Users/admin/BELNICK-AI-AGENTS/00-work-here/docs/runbooks/GOAL-PROGRESS.md`.
  Exclude Direct Answers, Light Checks, single-step surgical changes, and work expected to finish in one short step.
- **DOC-GOVERNANCE:** Any creation, placement, naming, or lifecycle decision for
  maintained documentation or artifacts requires
  `/Users/admin/BELNICK-AI-AGENTS/00-work-here/docs/reference/DOC-GOVERNANCE.md`.
  Exemptions include disposable run-scoped evidence, vendored, generated, demo,
  archived, and named runtime-output content; defer exact detail to that owner.
- **CONCURRENT-WORKTREES:** Any substantial, concurrent, or multi-writer Git
  work requires `/Users/admin/BELNICK-AI-AGENTS/00-work-here/docs/runbooks/CONCURRENT-WORKTREES.md`.
- **Sync/Obsidian:** Any change to the vault, sync behaviour, topology,
  user-visible delivery, or associated tooling requires
  `/Users/admin/BELNICK-AI-AGENTS/00-work-here/docs/runbooks/OBSIDIAN-SYNC-RUNBOOK.md`,
  with MacBook acceptance evidence unless explicitly Studio-scoped.

This file contains the project-specific rules for this repository.

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
