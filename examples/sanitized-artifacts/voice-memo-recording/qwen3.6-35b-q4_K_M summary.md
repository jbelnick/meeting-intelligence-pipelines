# ACME Launch Checklist Review

## Summary
The team reviewed ACME launch readiness and focused on support readiness, billing handoff, and dashboard metrics. The rollout can proceed only after support approves the runbook and the webhook retry metric is added.

## Key Points
- The release is tied to account settings and billing handoff readiness.
- The webhook retry metric is needed before support can triage event delays.
- The launch starts at 10 percent for one business day.

## Decisions
- Hold the launch flag until support approves the runbook.

## Next Steps
| name | action item | date |
| --- | --- | --- |
| Avery | Add webhook retry metric. | Friday |
| Morgan | Send support runbook update. | Thursday |
