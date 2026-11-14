# Repository usability design

The first useful result is a daily brief that a reader can open and trace back
to one of their notes. A person starting with a ZIP should be able to get that
result with their notes folder and Codex. A person working from the terminal
should be able to reproduce it using isolated test files and understand what a
failed command needs from them.

## Requirements

- Support macOS and Linux with Bash 3.2+ and Python 3.9+. Validate with Bash and Zsh where available.
- Keep the shell runtime on the Python standard library. Obsidian and external integrations are optional for the first brief.
- Keep existing command names, flags, profile fields, and success payloads compatible. Add diagnostics without rewriting unrelated profile settings.
- Keep calendar, mailbox, and task inputs local. Prepare drafts only on request. Never autosend.
- Use temporary profiles, synthetic notes and metadata, and disposable plugin installs for validation.
- Keep the documented install route grounded in a verified local marketplace workflow. State when a step needs the terminal, and describe Desktop and terminal verification separately.

## Repository review

Reviewed commit `7ace5ed` across the installer, marketplace, runtime, tests,
CI, vault template, 21 skills, examples, evals, and integration guides. Checked
the current guides against the command interfaces. All 21 skill names appeared
in the prompt guide, workflows reference, and workflow diagrams. A local
path and heading scan found no broken Markdown links in those docs.

| Priority | Finding | Evidence and disposition |
| --- | --- | --- |
| High | First-time instructions start at different points and assume different things about Obsidian. | The README starts at installation, while the platform guides start at vault setup. The Mac guide asked for `.obsidian` despite the runtime accepting a plain Markdown folder. A ZIP reader still needs a single path from extraction to an actual note linked in the report. [README](../../../README.md#quick-start), [macOS setup](../../INSTALL-MACOS.md), [Linux setup](../../INSTALL-LINUX.md) |
| High | A retired Outlook source blocks unrelated vault operations. | A disposable custom profile with the former desktop provider made `config`, `check`, and `config --vault … --apply` fail before reporting the active profile path. A new report failed too. Keep the latter strict and restore vault inspection and updates. [Runtime](../../../plugins/executive-assistant/scripts/unix/ea.py), [Source validation](../../../plugins/executive-assistant/scripts/unix/outlook.py) |
| High | A marketplace name conflict stops installation. | Registering an unrelated local marketplace called `personal` caused the actual installer to exit 1. The registration was preserved. The docs now give recovery steps. Keep the current plugin identity and verify the existing and isolated routes. [Distribution guide](../../DISTRIBUTION.md#marketplace-name-conflicts) |
| Medium | Starter instructions appear as real work. | The first preview from a copied template surfaced seven attention signals from placeholder checkboxes and words such as “due” in instructions. Adjust the starter copy and ask the reader to add one real or clearly marked test task. [Starter actions](../../../plugins/executive-assistant/assets/vault-template/Action-Items.md) |
| Medium | A canceled private event appears on the configured calendar and in its report. | Reproduced from a local JSON record with `private: true` and `status: "Canceled"`. Redaction removes status before the Outlook flow filters cancellations. Preserve the private output shape and filter on the validated original record before redaction. [Metadata reader](../../../plugins/executive-assistant/scripts/unix/local_workflows.py), [Outlook reader](../../../plugins/executive-assistant/scripts/unix/outlook.py) |
| Medium | Users can inadvertently enable schedule prompts with a false-looking value. | A syntax-valid JSON flag of `"false"` enabled the daily prompt. An explicit empty schedule object printed all four prompts. Existing tests cover absent preferences and one selected template. [Schedule implementation](../../../plugins/executive-assistant/scripts/unix/schedules.py), [Schedule tests](../../../tests/unix/test_schedules.py) |
| Medium | The developer checks leave onboarding and integration behavior partly manual. | CI tests both OS families and opens the ZIP. Its shell syntax step only uses Bash, and it neither runs the runner from the extracted ZIP nor checks skill names and heading fragments against the guides. Existing eval prompts have no run instructions. [CI](../../../.github/workflows/unix.yml), [Package tests](../../../tests/unix/test_package_contract.py), [Development guide](../../../DEVELOPING.md) |

The audit also found misleading generic “calendar export” wording, obsolete
example profile fields, and a draft eval that required optional email fields.
The accompanying documentation pass corrects those items, explains the
marketplace collision, and surfaces reader and contributor routes in the
README. Runtime changes are part of the implementation plan.

## Outcomes

1. **Recover an existing setup.** A valid vault can be checked and changed even
   when Outlook configuration is invalid. The response identifies the profile
   and includes an actionable Outlook diagnostic. Direct Outlook reads and new
   report generation still fail clearly when an enabled source is invalid.
2. **Get a first brief.** A shared guide leads from an extracted ZIP or checkout
   through the platform installer, choosing a notes folder, and opening the
   result. A fresh vault has zero fake work items. The guide shows how to add a
   test action, run a preview, save a report, and follow its source link.
3. **Try optional inputs.** The three metadata schemas have small runnable
   examples. A calendar marked private stays redacted, and a canceled private
   event is absent from configured-calendar results and reports.
4. **Configure recurring work deliberately.** With no schedule settings the
   command prints four optional templates. An empty or disabled settings object
   prints zero. An enabled object emits only explicitly enabled templates.
   Malformed Booleans and enabled time or weekday preferences identify the
   offending field. The docs distinguish templates, installed jobs, and logs.
5. **Verify what ships.** On both platforms, CI tests the runtime, verifies
   local guide links and public skill names, and runs the extracted ZIP with a
   synthetic vault. A maintainer can run a fresh and upgrade plugin install,
   a Desktop first-brief exercise, and optional schedule or external-service
   rehearsals using the release checklist.

## Validation baseline and open evidence

On macOS arm64, Python 3.14.3, Bash 3.2, and Zsh 5.9, the baseline had 27
passing unit tests and four passing shell syntax checks under both shells.
The ZIP included the license, installed in a disposable Codex configuration,
and produced a daily report from the cached plugin under each shell. The
official host documentation confirms that Linux Desktop is a preview and
documents repo-local marketplaces. Keep the tested CLI route available and
record actual Desktop discovery across project roots during implementation.
[Linux Desktop](https://learn.chatgpt.com/docs/linux/linux-app) ·
[Local plugin installation](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)

Linux execution, fresh Desktop skill invocation, actual scheduler firing, and
authenticated Jira, Confluence, and GitLab behavior were not verified in this
audit. Keep live integrations in the optional validation checklist. The first
brief can ship and be tested with synthetic local data.
