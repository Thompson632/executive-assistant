# Atlassian CLI Integration

Install and authenticate the CLI your organization uses before invoking the
corresponding skill.

- Use `$executive-jira-triage` with `jira-cli` to review active issues, identify stale work, and propose issue changes.
- Use `$executive-confluence-refresh` with `confluence-cli` to draft updates from reviewed notes for a specified space and page.

The local [example profile](../../config/executive-assistant.example.json)
shows optional command names and target settings under `atlassian`. The
shell launcher does not configure or run these tools. Give the skill the
project or space when the profile does not specify it. Store tokens with your
CLI or credential manager.

Review the exact issue changes or page draft before approving any write.

