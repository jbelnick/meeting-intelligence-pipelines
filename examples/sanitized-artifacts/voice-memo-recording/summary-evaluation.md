# Summary Evaluation

Judge: Meeting Quality Judge (`openai-codex/gpt-5.5`, High, speed enabled)
Evaluated: 2026-05-14T18:24:09.000Z

Winner: [qwen3.6:27b-q5_K_M](<qwen3.6-27b-q5_K_M summary.md>) - 94/100
Why: Best balance of transcript fidelity, specific owners, dates, decisions, and blocker preservation.

## Rankings

| Rank | Model | Score | Duration | Rationale |
|---:|---|---:|---:|---|
| 1 | [qwen3.6:27b-q5_K_M](<qwen3.6-27b-q5_K_M summary.md>) | 94 | 41.2s | Preserved ACME, the support runbook gate, the webhook retry blocker, owners, dates, and rollout percentage. |
| 2 | [qwen3.6:35b-a3b-q4_K_M](<qwen3.6-35b-q4_K_M summary.md>) | 87 | 56.6s | Usable but less specific about the launch dashboard and duplicate-invoice open question. |
| 3 | [mlx-community/Qwen3.6-27B-OptiQ-4bit](<mlx-qwen3.6-27b-optiq-4bit summary.md>) | 82 | 48.8s | Accurate but compresses too much operational detail. |
| 4 | [glm-5.1](<glm-5.1 summary.md>) | 79 | 33.8s | Strong detail retention but includes meta commentary about summary quality. |

## Model Removal Signals

- glm-5.1: watch - Useful but should avoid meta commentary in final customer-facing notes.

## Prompt Improvement Ideas

- Preserve blockers, owners, dates, rollout percentages, and open questions exactly.
- Do not add meta commentary about summary quality.
- Use Owner unclear when a task lacks an explicit owner.
