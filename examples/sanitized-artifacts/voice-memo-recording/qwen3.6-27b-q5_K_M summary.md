# ACME Account Settings Launch Readiness

## Summary
ACME reviewed account settings launch readiness across the billing handoff, support runbook, and dashboard. The launch flag remains disabled until support approves the runbook. The only blocker is the missing webhook retry metric, which support needs to distinguish delayed events from failed events.

## Key Points
- ACME needs the billing handoff, support runbook, and launch dashboard aligned before rollout.
- The launch flag stays disabled until support approves the runbook.
- The missing webhook retry metric is blocking support readiness.
- The first rollout is capped at 10 percent for one business day before expansion.
- The duplicate-invoice alert remains an open question.

## Decisions
- Keep the launch flag disabled until support approves the runbook.
- Start rollout at 10 percent for one business day before expanding.

## Next Steps
| name | action item | date |
| --- | --- | --- |
| Avery | Add the webhook retry metric to the dashboard. | Friday |
| Morgan | Send the updated support runbook to the launch channel. | Thursday |
