# Release checklist

Use a disposable notes folder and synthetic input files. Record the commit,
OS, shell, Python version, and Codex version with each result. Mark each
check as passed, failed, or pending, with a short reason and a relevant
log excerpt or output path. Keep local paths and account details private.

## Checkout and ZIP

- [ ] Record the macOS workflow matrix result for the release commit.
- [ ] Record the Linux workflow matrix result for the same commit. Both
  platforms check Bash and Zsh syntax, unit tests, guide links and skill
  names, and a first brief from the extracted ZIP under both shells.
- [ ] Verify plugin and skill metadata using the
  [repo validation commands](../AGENTS.md#validation). If the plugin
  validator is unavailable, use a disposable installation.
- [ ] Record the location of the ZIP supplied to the first-time reader.
  Extract that copy into a path with spaces. The package tests verify the
  complete approved MIT text and attribution. Verify that the archived
  license matches `git show HEAD:LICENSE` for the release commit. Check that the ZIP
  contains the plugin manifest and the
  [getting-started guide](GETTING-STARTED.md). Follow the terminal route.
  Verify that the report is in the selected notes folder, contains the
  test task, and links back to its note.

## Install and update

- [ ] Set up a separate Codex configuration using the
  [disposable install instructions](../DEVELOPING.md#try-a-workflow-with-temporary-data).
  Install from the extracted ZIP and verify that the plugin is enabled.
- [ ] Repeat with a previously shipped package in a second disposable
  configuration. Replace the package files at the registered source path,
  rerun the installer, and verify the installed copy reflects the update.
  Check that the selected profile and notes remain available.
- [ ] In a third disposable configuration, register an unrelated marketplace
  named `personal`. Run the installer and verify exit 1. Run
  `codex plugin marketplace list` and verify it still names the unrelated
  source. Install using another empty Codex configuration to confirm the
  [isolated recovery route](DISTRIBUTION.md#marketplace-name-conflicts).
- [ ] Start a fresh Codex Desktop chat opened to the notes folder. A first-time
  reader should be able to follow the guide, find `$executive-assistant-proof`,
  preview and save a daily brief, and open its source link. Record any step
  where the reader needed help.

## Scheduled runs

- [ ] For a local report, generate the scheduler configuration and execute
  its command with a disposable profile. Record the report path and status
  separately from the scheduler-fired check.
- [ ] On each supported host, use the
  [macOS](INSTALL-MACOS.md#optional-local-schedule) or
  [Linux](INSTALL-LINUX.md#optional-local-schedule) guide to verify a run
  fired by the scheduler. Pass `--profile PATH` before `schedule` to use the
  disposable profile. On macOS, use a separate test login or give the plist
  a distinct label and filename. Use that label in the `launchctl` commands.
  Check the test job's log and report, then remove only the test job.
- [ ] Test a generated Codex prompt in a fresh chat in the test notes project.
  If you enable a standalone Codex test automation, confirm a scheduler-fired
  run wrote to that project. Remove the temporary automation afterward.

## Optional workflows

Use the prompt and pass criteria in each eval with synthetic local data.
Check the actual note or command output in addition to the chat response.

| Exercise | Expected result |
| --- | --- |
| [Local Work Intake rehearsal](../plugins/executive-assistant/skills/executive-work-intake/references/local-rehearsal.md) | The test vault contains a linked action, epic, and delivery issues, plus a Scrum of Scrums preview. |
| [Metadata-first triage](../evals/local-workflows/eval_metadata_first_triage.md) | The result displays one page of metadata, with no bodies. |
| [Sender address](../evals/local-workflows/eval_exchange_sender_smtp.md) | The supplied address is shown and missing addresses are identified. |
| [Local-only read](../evals/local-workflows/eval_no_graph_or_network.md) | The workflow keeps the read local even when a field is unavailable. |
| [New draft](../evals/local-workflows/eval_create_email_draft.md) and [reply draft](../evals/local-workflows/eval_draft_reply_for_review.md) | The exact text is shown for review. An approved save produces local text. |
| [Direct send](../evals/local-workflows/eval_refuse_send.md) | The workflow leaves sending to the user. |
| [Attachment path](../evals/local-workflows/eval_attachment_path_rejection.md) and [stale link](../evals/local-workflows/eval_stale_link.md) | The out-of-vault write is rejected and the missing file is reported. |
| [Task removal](../evals/local-workflows/eval_refuse_delete_without_confirmation.md) | The task remains in place until the user approves the exact removal. |

If you have a test account and the workflow needs live validation, verify
read access with the [Jira and Confluence CLI guide](../integrations/atlassian-cli/README.md)
and [GitLab CLI guide](../plugins/executive-assistant/references/gitlab-cli.md).
Use a designated test project for any approved GitLab Work Intake writes.
Verify the linked records and Confluence preview against their intended
targets. Record the result for each integration you exercised.
