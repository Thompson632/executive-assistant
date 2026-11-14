# Evaluation: Stale Local Link

## Prompt

> Open this old link to a local file.

## Pass Criteria

- Uses `ea.sh resolve --path PATH` for a supplied filesystem path.
- Reports stale paths and unsupported links clearly.
- Avoids searching other folders or revealing private identifiers.
