# Repository Usability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Help a first-time user install Executive Assistant and open their first linked daily brief, and give maintainers a repeatable way to diagnose and verify the same workflow.

**Architecture:** Keep the local marketplace, shell launcher, and Python runtime. Put first-use instructions in one guide with platform-specific links, fix the runtime behaviors that impede recovery or misstate results, and verify both the checkout and the extracted ZIP.

**Tech Stack:** Bash, Zsh, Python standard library, unittest, Markdown, Codex local marketplace, GitHub Actions.

**Spec:** [Repository usability design and audit](../specs/2026-11-14-repository-usability.md)

## Global Constraints

- Support macOS and Linux with Bash 3.2+ and Python 3.9+. Validate with Bash and Zsh where available.
- Keep the shell runtime on the Python standard library. Obsidian and external integrations are optional for the first brief.
- Keep existing command names, flags, profile fields, and success payloads compatible. Add diagnostics without rewriting unrelated profile settings.
- Keep calendar, mailbox, and task inputs local. Prepare drafts only on request. Never autosend.
- Use temporary profiles, synthetic notes and metadata, and disposable plugin installs for validation.
- Keep the documented install route grounded in a verified local marketplace workflow. State when a step needs the terminal, and describe Desktop and terminal verification separately.

## Review Focus

- Custom profile with an obsolete provider. Return the selected path and allow a vault move while preserving Outlook settings. Task 1.
- New notes folder with no Obsidian settings. Produce a report with zero starter actions, then surface the test task with a working relative link. Task 2.
- Private canceled event alongside a valid private event. Keep only the latter in the feed and report, with its generic title. Task 3.
- Empty schedule preferences and a quoted Boolean. Print zero templates for the empty object and return a named error for the quoted flag. Task 4.
- Extracted ZIP in a path with spaces and an unrelated marketplace already named `personal`. Run the packaged shell workflow and verify that install failure leaves the unrelated marketplace alone. Task 5.

---

## File map

| Area | Files and responsibilities |
| --- | --- |
| Profile recovery | `scripts/unix/ea.py` reports vault status independently of Outlook validation. `references/local-outlook.md`, `references/profile-schema.md`, and the proof skill surface the next step. |
| First use | `README.md` routes readers to `docs/GETTING-STARTED.md` and `DEVELOPING.md`. The platform install guides retain platform details. Starter notes explain where to record work without adding report entries. |
| Metadata | `scripts/unix/local_workflows.py` owns validation and privacy. `scripts/unix/outlook.py` requests canceled-event filtering. `references/local-inputs.md` describes and demonstrates the JSON contract. |
| Scheduling | `scripts/unix/schedules.py` validates preferences. The profile and runtime references, scheduled-tasks skill, and platform guides explain the resulting workflow and logs. |
| Verification | `tests/unix/` owns regression tests. `.github/workflows/unix.yml` exercises the ZIP on both platforms. `docs/RELEASE-CHECKLIST.md` and `DEVELOPING.md` describe host checks. |

Short script, reference, asset, and skill paths in this table are relative to
`plugins/executive-assistant/`. Tasks 1 through 4 each deliver an independently
testable change. Task 5 verifies their combined release.

### Task 1: Restore vault checks and configuration with an outdated source

**Files.** Modify `plugins/executive-assistant/scripts/unix/ea.py`,
`plugins/executive-assistant/references/local-outlook.md`,
`plugins/executive-assistant/references/profile-schema.md`, and
`plugins/executive-assistant/skills/executive-assistant-proof/SKILL.md`.
Test `tests/unix/test_outlook.py`.

**Interfaces.** `show_status(path: Path, vault: Path, profile: dict) -> None`
continues to emit the existing JSON for valid configurations. When
`outlook.sources(profile)` raises `ValueError`, emit the existing status keys
with `outlook_available: false`, `outlook_sources: {}`, and one added field
`outlook_error` containing the existing diagnostic. `ok` reflects the vault
check. A successful `config --vault PATH --apply` writes the selected vault
and reports the same status fields. Reports and direct Outlook reads keep
using strict source validation.

- [ ] In `LocalOutlookTest`, replace
  `test_unsupported_provider_explains_how_to_configure_file_sources` with
  `test_vault_management_survives_an_unsupported_provider`. Reuse
  `self.configure(provider="unsupported")` and the explicit profile used by
  `self.command`. Assert the following for both `check` and `config`.

```python
self.assertEqual(result.returncode, 0)
self.assertEqual(status["profile_path"], str(self.profile))
self.assertEqual(status["vault_path"], str(self.vault))
self.assertTrue(status["ok"])
self.assertFalse(status["outlook_available"])
self.assertEqual(status["outlook_sources"], {})
self.assertEqual(status["outlook_error"],
                 "Set outlook.provider to local and configure outlook.maildir or outlook.calendarFile.")
```

- [ ] In the same test, create `self.root / "Moved Vault"`. Assert that
  `config --vault …` leaves the profile bytes alone and that adding `--apply`
  returns 0, updates `vaultPath`, and preserves the previous `outlook` object.
  Assert that `outlook mail` and `report daily --write` both exit 1 with the
  source error and that the moved vault has no `_briefings` directory.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_outlook.py -v`.
  Expect the new status check to fail with exit 1 before changes.
- [ ] Catch the source error in `show_status` only. Remove the independent
  Outlook validation from the vault apply path. Leave vault path validation
  and strict feed consumers in place.
- [ ] Update the proof skill and both references. Explain that the notes
  folder can be healthy while Outlook needs attention. Direct the reader to
  `profile_path` and show the two recovery options, disabling Outlook for
  vault-only use or configuring file sources.
- [ ] Rerun the Outlook tests and the full suite. Expect exit 0. Run the skill
  validator per `AGENTS.md`. Commit as `Keep vault management available with invalid Outlook settings`.

### Task 2: Give first-time users one path to a useful brief

**Files.** Create `docs/GETTING-STARTED.md`. Modify `README.md`,
`docs/INSTALL-MACOS.md`, `docs/INSTALL-LINUX.md`,
`docs/DISTRIBUTION.md`, `docs/SAMPLE-PROMPTS.md`,
`plugins/executive-assistant/assets/vault-template/Action-Items.md`,
`plugins/executive-assistant/assets/vault-template/HOME.md`,
`plugins/executive-assistant/assets/vault-template/AI-Workflows.md`,
`plugins/executive-assistant/assets/vault-template/One-on-Ones.md`, and
`plugins/executive-assistant/assets/vault-template/templates/Meeting Notes.md`.
Test `tests/unix/test_vault_workflow.py`.

**Interfaces.** Use the existing `setup --vault PATH --copy-template`,
`check`, and `report daily [--write]` entry points. The shared guide owns the
first-run sequence. The installer flags and marketplace identity stay compatible.

- [ ] Add `test_starter_vault_reports_only_real_actions` to
  `VaultWorkflowTest`. Use a copied starter vault, a fixed focus date, and
  run the preview before adding anything. Assert
  `self.assertIn("0 vault attention signals surfaced.", preview)`.
  Append `- [ ] Review the meeting agenda` to `Action-Items.md`, run
  `report daily --date 2026-11-14 --write`, then assert that its
  `output_path` exists, the saved text contains `Review the meeting agenda`,
  and the relative link labeled `Action-Items` resolves to that note.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_vault_workflow.py -v`.
  Expect the zero-signal assertion to fail.
- [ ] Turn the two instructional open checkboxes into prose. Use wording
  such as “Add new actions here” and “List items delegated to others.” Keep
  the Inbox, Waiting On, and Done headings. Rephrase the instructional
  “blocked work,” “follow-ups,” and “due dates” lines in `AI-Workflows.md`,
  the “due dates” prompt in `One-on-Ones.md`, and the “due date” line in
  `templates/Meeting Notes.md` so they do not match report cues. Keep
  the report scanner as it is. Add a short first-brief prompt inside the copied
  vault Home that works without the checkout.
- [ ] Write the shared guide in this order. Get and extract the ZIP or open
  an existing checkout. Put it somewhere stable. Follow the platform install
  section with one installer command and its success message. Choose a
  separate notes folder and open it in Codex. Paste a setup prompt, add the
  test action, run a proof check, and save the brief. Show the actual
  `_briefings` destination and where to click to reach the source. Include a
  labeled terminal alternative using the same inputs and a short
  troubleshooting table for missing Python, missing Codex, existing profile,
  missing plugin, and marketplace conflict. Link optional integrations and
  scheduling from the end. Verify Desktop discovery before documenting a
  terminal-free installation route.
- [ ] Link the shared guide from the README and distribution flow. Give
  technical readers a visible `DEVELOPING.md` route. Use the platform pages
  for prerequisites, CLI fallback, update, and scheduler details. Point
  sample-prompt readers back to the common first-run sequence.
- [ ] Rerun the vault tests and the full suite. Walk the guide from a
  disposable ZIP through a report with a test action. Expect all tests to pass
  and the file link to resolve. Commit as `Document and verify the first daily brief`.

### Task 3: Fix private calendar filtering and provide input examples

**Files.** Modify `plugins/executive-assistant/scripts/unix/local_workflows.py`,
`plugins/executive-assistant/scripts/unix/outlook.py`, and
`plugins/executive-assistant/references/local-inputs.md`.
Test `tests/unix/test_outlook.py` and `tests/unix/test_local_workflows.py`.

**Interfaces.** Extend
`read_records(source: str, kind: str, *, exclude_canceled: bool = False) -> list[dict]`
and `validate_records(payload: object, kind: str, *, exclude_canceled: bool = False) -> list[dict]`.
The configured Outlook calendar opts in. The supplied snapshot workflow
retains its current semantics, including redaction. Skip status spellings
`canceled` and `cancelled` case-insensitively after validation and before redaction.

- [ ] Add `test_configured_calendar_excludes_canceled_private_events` to
  `LocalOutlookTest`. Give one private event `status="Canceled"`, a
  visible event `status="CANCELLED"`, and a second private event no status.
  Give the three distinct starts inside the fixture's one-day window. Assert
  `self.assertEqual(records, [{"title": "Private event", "start": kept["start"], "end": kept["end"]}])`.
  In the report assert `self.assertEqual(report.count("· Private event"), 1)`
  and that the original private titles remain absent.
- [ ] Extend `test_calendar_batches_and_rejects_bad_dates` to assert that a
  private record with status `Canceled` in an explicitly supplied snapshot
  still appears as `Private event` with start and end only.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_outlook.py -v`.
  Expect one extra private event in the new test.
- [ ] Implement the opt-in filter and remove the later status check from the
  configured feed path. Add one copyable JSON array each for mail, calendar,
  and tasks to the input reference, with the command to review it. Use
  `example.invalid` for any address. State that the command reads metadata
  JSON and explain the distinction between a snapshot and a configured feed.
- [ ] Run the Outlook and local workflow test files through unittest
  discovery. Copy each JSON block to a temporary file and run its documented
  review command. Expect exit 0 for each. Commit as `Filter canceled private events and document local inputs`.

### Task 4: Validate schedule preferences and explain how to verify runs

**Files.** Modify `plugins/executive-assistant/scripts/unix/schedules.py`,
`plugins/executive-assistant/references/profile-schema.md`,
`plugins/executive-assistant/references/unix-runtime.md`,
`plugins/executive-assistant/skills/executive-scheduled-tasks/SKILL.md`,
`docs/INSTALL-MACOS.md`, and `docs/INSTALL-LINUX.md`.
Test `tests/unix/test_schedules.py`.

**Interfaces.** `schedule_prompts(profile: dict, path: Path) -> None`
continues to print Markdown. An absent `scheduledTasks` key prints all four
optional templates. An explicit object prints only entries with
`enabled: true`. A group with `enabled: false` prints no entries. Require
actual Boolean flags where supplied, validate time and weekly day for enabled
entries, and report a dotted field name on malformed settings before printing
any output. `schedule` continues to generate local configuration independently.

- [ ] Add `test_explicitly_empty_or_disabled_schedule_preferences` to
  `SchedulesTest`. For `{}` and `{"enabled": False, "dailyBrief": {"enabled": True}}`,
  assert `self.assertNotIn(b"## ", result.stdout)` with exit 0. Retain the
  existing absent-preferences and valid weekly checks.
- [ ] Add `test_invalid_schedule_preferences_name_the_field`. For each
  malformed value assert exit 1, empty stdout, and the named diagnostic in
  stderr. Test `scheduledTasks: null`, group `enabled: "false"`,
  `dailyBrief.enabled: "false"`, enabled daily `time: "24:00"`, and
  enabled weekly `day: "Funday"` without a time. Assert the corresponding
  field names `scheduledTasks`, `scheduledTasks.enabled`,
  `scheduledTasks.dailyBrief.enabled`, `scheduledTasks.dailyBrief.time`,
  and `scheduledTasks.weeklyReview.day`.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_schedules.py -v`.
  Expect failures for explicit empty preferences and malformed values.
- [ ] Distinguish an absent group from an explicit object. Validate flags
  before using them and validate the enabled week's day independently of
  whether it has a time. Preserve the existing output for valid preferences.
- [ ] Update the references, skill, and guides to show how to generate a
  template, install a schedule in the chosen host, and check the first
  scheduled result. Put the human-readable recovery steps ahead of
  internal provider error details. Document the separate launchd
  error log, the combined cron log, and whether a rerun reused a saved report.
- [ ] Rerun the schedule tests and skill validator. Generate both scheduler
  formats with a disposable profile and verify the parsed command produces
  the expected file. Commit as `Validate scheduled workflow preferences`.

### Task 5: Make release verification repeatable

**Files.** Create `docs/RELEASE-CHECKLIST.md`. Modify
`tests/unix/test_package_contract.py`, `.github/workflows/unix.yml`,
`DEVELOPING.md`, `docs/DISTRIBUTION.md`, and `docs/ROADMAP.md`.

**Interfaces.** Extend the package contract and the existing macOS/Linux
matrix. The packaged smoke test uses `setup`, `check`, and
`report daily --date 2026-11-14 --write`. Normal CI requires Bash, Zsh, Python,
Git, and unzip. Actual Desktop, Codex scheduling, and authenticated integration
checks use a maintainer's disposable environment and record what ran.

- [ ] Extend the package contract tests to verify Markdown heading fragments
  in README, getting-started, platform, workflow, and sample-prompt docs,
  alongside existing file links. Validate the GitHub-style heading checker
  with cases for curly apostrophes and duplicate headings. For the sample
  prompt guide and workflow diagrams, assert that the set of
  `$executive-…` references equals the set read from packaged skill
  frontmatter. Keep planning artifacts outside these public-doc assertions.
- [ ] Check the assertions by temporarily adding a misspelled skill name and
  a broken heading fragment to a disposable copy. Run
  `python3 -m unittest discover -s tests/unix -p test_package_contract.py -v`.
  Expect both to be detected. Discard the injected typos and expect exit 0.
- [ ] In CI, run `zsh -n` alongside `bash -n`. After ZIP validation, extract
  into `"$RUNNER_TEMP/Executive Assistant Smoke"`, assert that `LICENSE`,
  `docs/GETTING-STARTED.md`, and the plugin manifest exist, and invoke the
  extracted launcher from both shells. Give each shell its own profile,
  vault, and synthetic task. Parse the report JSON and assert the file exists
  under the selected vault and contains `Review the meeting agenda`.
- [ ] Write the release checklist and link it from the developer and
  distribution guides. Record commit, OS, Python and Codex versions, and
  outcome per check. Cover fresh and in-place plugin installation, a collision
  with an unrelated `personal` marketplace, and skill invocation in a
  new Desktop chat opened to the notes folder. In the collision test assert
  exit 1 and that `plugin marketplace list` still points at the unrelated
  source, then verify installation using a disposable Codex home. Record a
  scheduler-fired run separately from a manually executed generated command.
  List the local Work Intake rehearsal and the existing eval prompts with
  expected outputs and any optional authenticated checks. Link the checklist
  from the roadmap and retire each roadmap validation item once its result
  exists.
- [ ] Run the full Unix suite, shell syntax checks, skill validation, and the
  ZIP smoke locally. Verify the macOS/Linux matrix for the implementation
  commit. Record unavailable live checks explicitly. Commit as
  `Verify the packaged first-run workflow on macOS and Linux`.
