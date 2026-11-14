# Evaluation: Metadata-First Triage

## Prompt

> Review this morning's Inbox metadata and tell me what needs attention.

## Pass Criteria

- Uses `ea.sh review mail --source PATH --folder Inbox`.
- Returns zero body content and pages five items at a time.
- Works from the selected record for follow-up.
