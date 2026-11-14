# Contributing to Executive Assistant

For a bug report, include your operating system, shell, Python version, and
plugin version. Give the command or skill prompt, the expected result, and
what happened. Use synthetic inputs and redact private paths and account
details before sharing logs or screenshots.

For a workflow proposal, describe the task someone needs to complete, the
inputs they can supply, and the expected output. See the
[workflow guide](docs/CODEX-WORKFLOWS.md) for existing entry points.

## Prepare a pull request

1. Follow the [development guide](DEVELOPING.md) to set up the repo and
   validate your change.
2. Keep the change focused. Update user-facing docs or examples when a
   command or configuration field changes. Start a new packaged skill with
   the [skill template](docs/SKILL-TEMPLATE.md). For any packaged skill change,
   update the [sample prompts](docs/SAMPLE-PROMPTS.md),
   [Codex workflows](docs/CODEX-WORKFLOWS.md), and
   [workflow diagrams](docs/WORKFLOW-DIAGRAMS.md) in the same pull request.
   Follow the [skill documentation guide](.agents/skills/sync-skill-docs/SKILL.md).
   Add or update tests where they protect the behavior you changed.
3. Keep vault notes, email bodies, Outlook identifiers and link stores,
   private profiles, tokens, and credentials out of commits and fixtures.
   Keep calendar, mail, and task inputs local. Prepare drafts on request and
   leave sending to the user. See the [repo guide](AGENTS.md#operating-rules)
   for the full data and workflow boundaries.
4. In the pull request, describe the user-facing change, any configuration
   or upgrade steps, and the checks you ran. Include relevant checks you
   could not run.

The project uses the [MIT License](LICENSE). Preserve applicable third-party
notices when adapting or copying material. See the
[third-party notices](plugins/executive-assistant/THIRD_PARTY_NOTICES.md).
