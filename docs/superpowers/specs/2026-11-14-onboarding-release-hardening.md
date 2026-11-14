# Onboarding and release hardening design

This follow-up reviews `cb9fd71`, after the first-brief and skill-documentation
work. It prioritizes the mistakes a person can make while choosing a notes
folder, using an existing installation, or maintaining the package.

## Requirements

- Support macOS and Linux with Bash 3.2+ and Python 3.9+. Use the Python standard library for runtime and validation code.
- Preserve valid existing profiles, CLI flags and payloads, marketplace identity, and the optional Obsidian and integration paths.
- Keep vaults and the executing package separate. Reject a notes folder that contains or is contained in the executing package before writing or scanning it.
- Keep calendar, mail, and task inputs local. Use synthetic data for tests and leave live credentials, notes, and schedules out of CI.
- Require changes to all three public guides in the same pull request as any change under the packaged skills directory.
- Keep license validation tied to the repository and ZIP. Record platform and Desktop evidence only after a real check.

## Audit findings

| Priority | Finding | Evidence |
| --- | --- | --- |
| High | A notes folder that contains the running checkout can turn package content into private-vault report input. | With an extracted copy inside a temporary notes directory, `setup` succeeded and the generated brief surfaced a synthetic unchecked note inside the copy. The check currently covers the package and its descendants. [Vault runtime](../../../plugins/executive-assistant/scripts/unix/ea.py) |
| High | A bad profile can hang or produce a Python traceback. | `check` against a named pipe exceeded a one-second timeout. An unknown home-directory shorthand in `vaultPath` or the source of `review tasks` produced a traceback. Existing metadata reads already have a nonblocking regular-file helper. [Path and file helpers](../../../plugins/executive-assistant/scripts/unix/local_workflows.py) |
| High | A release validation step accepted a license placeholder. | The tracked `LICENSE` was three bytes, `TBD`, although the contribution guide identified MIT. The actual archive smoke passed because it checks that the file exists. This audit restores the previously selected MIT text and attribution. The content check is still pending. [License](../../../LICENSE), [SPDX MIT entry](https://spdx.org/licenses/MIT.html), [CI workflow](../../../.github/workflows/unix.yml) |
| Medium | Installation can fail with an error that gives a first-time reader no next step. | A disposable executable simulating an older CLI returned only `unknown subcommand: plugin` when supplied with `--codex`. Default selection only probes marketplace help, so it can attempt registration before finding out the install subcommand is missing. [Installer](../../../install/unix/install-plugin.sh) |
| Medium | Changes to an existing skill can evade the documentation requirement. | The current test suite remained green after a synthetic change to a skill's instructions with all three guides untouched. Inventory comparison checks names. A PR-level diff can enforce the requirement to edit the guides before review. [Repo rule](../../../AGENTS.md), [Package tests](../../../tests/unix/test_package_contract.py) |
| Medium | Several first-run instructions assume prior familiarity with the terminal, Obsidian or Codex profiles. | The opening steps did not show how to change directory, setup examples referred to Obsidian by default, and a separate CLI configuration was easy to mistake for an install in the current Desktop session. The immediate documentation pass fixes those points and clarifies that Outlook source access is checked by reading the feed. [First brief](../../GETTING-STARTED.md), [Sample prompts](../../SAMPLE-PROMPTS.md), [Distribution](../../DISTRIBUTION.md), [Local Outlook](../../../plugins/executive-assistant/references/local-outlook.md) |

## Acceptance criteria

1. A FIFO profile dies promptly with a message to select a regular profile
   file. Malformed home shorthand in arguments, profile fields, and supplied
   metadata produces a useful path error and no traceback. Existing
   absolute and ordinary home-relative paths keep working.
2. Selecting the parent of an extracted checkout fails before a profile,
   starter note, or report is written. With an existing profile pointing to
   that parent, `check` and `report` explain how to pick a separate notes
   folder. The user can preview and apply a move to a valid sibling folder.
3. The installer checks both required subcommands before registering a
   marketplace. An unsupported explicit executable prints a remedy. The
   supported path continues to install `executive-assistant@personal`.
4. A pull request touching a packaged skill file must also change
   `docs/SAMPLE-PROMPTS.md`, `docs/CODEX-WORKFLOWS.md`, and
   `docs/WORKFLOW-DIAGRAMS.md`. A change outside the packaged skills folder
   does not trigger the gate. The existing inventory checks remain useful
   for additions, removals, and renames. Reviewers check the content.
5. Verification fails for a placeholder or truncated license. It compares
   the archive's license to the release commit and exercises the first brief
   from the archive under Bash and Zsh. The release checklist distinguishes
   the packaged CLI test from Desktop skill discovery and scheduler-fired runs.

## Baseline and validation limits

At `cb9fd71` the local suite passed 35 tests. The existing Actions syntax
and ZIP smoke commands ran successfully on macOS with Python 3.9.6, Bash,
and Zsh. The extracted ZIP installed in a disposable Codex configuration.
The checks reproduced the defects above with synthetic files and executables.

GitHub's Actions result was unavailable to this session and the local Linux
container daemon was down. The hosted matrix, Desktop skill discovery in a
fresh chat, an actual scheduler-fired run, and authenticated integrations
remain open. These are environment checks in the
[release checklist](../../RELEASE-CHECKLIST.md). This follow-up does not
change the platform or integration support policy.
