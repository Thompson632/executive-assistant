# Onboarding and Release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give users clear recovery steps when local setup fails and give contributors checks that catch stale workflow documentation and incomplete release archives.

**Architecture:** Reuse the existing path and regular-file helpers at the launcher boundary. Validate installer capabilities before registration, and add focused checks for pull-request documentation and ZIP contents to the existing workflow.

**Tech Stack:** Bash, Python standard library, unittest, Git, GitHub Actions, Codex local marketplace.

**Spec:** [Onboarding and release hardening design](../specs/2026-11-14-onboarding-release-hardening.md)

## Global Constraints

- Support macOS and Linux with Bash 3.2+ and Python 3.9+. Use the Python standard library for runtime and validation code.
- Preserve valid existing profiles, CLI flags and payloads, marketplace identity, and the optional Obsidian and integration paths.
- Keep vaults and the executing package separate. Reject a notes folder that contains or is contained in the executing package before writing or scanning it.
- Keep calendar, mail, and task inputs local. Use synthetic data for tests and leave live credentials, notes, and schedules out of CI.
- Require changes to all three public guides in the same pull request as any change under the packaged skills directory.
- Keep license validation tied to the repository and ZIP. Record platform and Desktop evidence only after a real check.

## Review Focus

- A named pipe passed as `--profile` returns a regular-file error within the test timeout. Task 1.
- A selected notes folder contains the extracted package. Setup rejects it and an existing profile can be moved to a sibling. Task 2.
- A CLI implements marketplace management and lacks plugin installation. Installation stops before the first registration write. Task 3.
- A packaged skill's instructions or UI metadata change while an unchanged guide still mentions it. The PR check reports the missing guide. Task 4.
- A release ZIP contains an existing but incomplete license or a different license from the selected Git commit. Validation fails. Task 5.

---

## File map

| Files | Responsibility |
| --- | --- |
| `plugins/executive-assistant/scripts/unix/{ea,local_workflows,outlook}.py` | Read profiles safely, report path errors, and validate notes folder placement. |
| `install/unix/install-plugin.sh`, `tests/unix/test_install.py` | Check the chosen CLI before making changes and cover both supported and unsupported executables. |
| `tools/check-skill-docs.py`, `tests/unix/test_skill_docs.py`, `.github/workflows/unix.yml` | Check skill edits and guide changes across the pull request. |
| `tests/unix/test_package_contract.py`, `.github/workflows/unix.yml` | Validate the restored license and the exact archived file. |
| `docs/GETTING-STARTED.md`, platform guides, profile schema, contribution guide and release checklist | Explain user recovery, local reviewer commands, and the evidence required for a release. |

The local setup tasks can ship together or independently of the pull-request
and release checks. Task 2 builds on Task 1's path diagnostics.

### Task 1: Return actionable profile and input path errors

**Files:** Modify `plugins/executive-assistant/scripts/unix/ea.py`,
`plugins/executive-assistant/scripts/unix/local_workflows.py`,
`plugins/executive-assistant/scripts/unix/outlook.py`, and
`plugins/executive-assistant/references/profile-schema.md`.
Test `tests/unix/test_vault_workflow.py`, `tests/unix/test_local_workflows.py`,
and `tests/unix/test_outlook.py`.

**Interfaces:** `read_profile(path: Path) -> dict` reads a regular UTF-8 JSON
file via existing `local_workflows.read_input(path)`, preserving BOM and
symlink-to-regular-file behavior. Missing profiles keep the existing setup
hint. Invalid `~user` expansion from `local_path(value: str) -> Path` becomes
`ValueError("Use an absolute local path or ~ for your home folder.")`.
For a non-regular profile, return `Choose a regular JSON profile file: PATH`.
For configured Outlook inputs, preserve the field-specific
`Set outlook.maildir to an absolute local path.` diagnostic.

- [ ] Add `test_profile_fifo_returns_a_regular_file_error` to
  `VaultWorkflowTest`. Use `os.mkfifo(self.profile)` after creating the
  parent. Run `ea.sh --profile PATH check` with `timeout=3`. Assert
  `returncode == 1`, empty stdout, and `Choose a regular JSON profile file`
  in stderr. Add a case for a symlink to a valid profile and assert
  `json.loads(stdout)["vault_path"] == str(self.vault)`.
- [ ] Add `test_unknown_home_in_profile_or_vault_has_a_path_error` to the
  same class and `test_unknown_home_in_metadata_source_has_a_path_error`
  to `LocalWorkflowTest`. Use `~ea-no-such-user-8731/Notes` as the source,
  explicit profile path, setup or config folder, or profile's `vaultPath`.
  Assert `returncode == 1`, `Use an absolute local path or ~ for your home
  folder.` in stderr, and no `Traceback`. Keep the existing Outlook test.
- [ ] Run `python3 -m unittest discover -s tests/unix -k 'profile_fifo' -v`
  and again with `-k 'unknown_home'`. Expect a timeout and tracebacks from
  the new tests.
- [ ] Normalize the expansion error inside the existing `local_path`
  helper and route profile and vault arguments and saved paths through it.
  Resolve the profile path inside `main`'s existing exception handler.
  Use the existing nonblocking reader for profile JSON, with profile-specific
  diagnostics for a missing or non-regular file. In `outlook.sources`,
  translate invalid local paths to the existing field-specific error.
- [ ] Document the accepted profile file and path types. Rerun both
  targeted commands and the full suite. Expect exit 0. Commit as
  `Explain invalid local profile and input paths`.

### Task 2: Block a notes folder that surrounds the executing package

**Files:** Modify `plugins/executive-assistant/scripts/unix/ea.py` and
`docs/GETTING-STARTED.md`. Test `tests/unix/test_vault_workflow.py`.

**Interfaces:** Extend existing `get_vault(profile: dict, create: bool = False) -> Path`.
After resolving the selected folder, reject ancestors of `PLUGIN_ROOT`
with `Choose a notes folder separate from the Executive Assistant package.`
Keep the existing protection for the repository and its descendants.
The `config --vault PATH` preview and `--apply` still validate the new folder
without requiring access to the old one.

- [ ] Add `test_vault_cannot_contain_the_executing_package`. Copy the plugin
  to `self.root / "Containing Folder" / "executive-assistant"` and invoke
  its launcher with the explicit fixture profile. For `setup --copy-template`
  using `Containing Folder` as vault, assert exit 1, the exact new diagnostic,
  and that neither the profile nor `Action-Items.md` was created.
- [ ] In the same regression, write a synthetic existing profile pointing to
  `Containing Folder`. Assert that `check` and `report daily --write` exit 1
  with the diagnostic and that `_briefings` does not exist. Create
  `self.root / "Sibling Notes"`; assert a preview preserves the profile and
  applying the move returns the sibling as `vault_path`. Check that a
  following `report daily` succeeds.
- [ ] Run `python3 -m unittest discover -s tests/unix -k vault_cannot_contain -v`.
  Expect setup to succeed on the old implementation and fail the assertion.
- [ ] Add the ancestry guard to `get_vault` before creating the folder.
  Add a troubleshooting row explaining how to choose a separate folder
  and run the existing configuration preview if needed.
- [ ] Rerun the vault workflow tests. Expect exit 0. Commit as
  `Reject notes folders that contain the running package`.

### Task 3: Check installer capabilities before changing marketplace state

**Files:** Modify `install/unix/install-plugin.sh`, `docs/INSTALL-MACOS.md`,
`docs/INSTALL-LINUX.md`, and `docs/GETTING-STARTED.md`. Create
`tests/unix/test_install.py`.

**Interfaces:** `install-plugin.sh [--codex /absolute/path/to/codex]` keeps
its current syntax and plugin identity. A supplied executable must support
both `plugin marketplace --help` and `plugin add --help`. A missing or
unsupported implicit CLI can fall back to the bundled executable on macOS.
Failure after selection but before registration returns 1 and includes
`Update Codex or pass --codex /absolute/path/to/codex.`

- [ ] Add a disposable fake executable that logs each argument list and
  returns 0 for marketplace help and 2 for plugin-add help.
  In `test_installer_rejects_partial_cli_before_registration`, invoke the
  real Bash installer with that path, then assert `returncode == 1`, the
  remedy in stderr, and neither `plugin marketplace add` nor
  `plugin add executive-assistant@personal` in the log. In
  `test_installer_registers_then_installs_with_supported_cli`, switch the
  fake to support both probes and assert exit 0, registration with the
  checkout path, and that registration precedes plugin installation.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_install.py -v`.
  Expect the unsupported test to fail against the current installer.
- [ ] Add an installer-local Bash function to check both help commands.
  Apply it to the selected executable and to the existing macOS fallback
  before any marketplace registration. Keep explicit CLI selection
  authoritative and preserve the distinct missing-executable error.
- [ ] Explain the compatibility message and recovery in the platform and
  getting-started guides. Run `bash -n install/unix/install-plugin.sh`,
  the installer tests, and a disposable plugin installation using the
  actual CLI. Expect exit 0. Commit as `Check Codex installer support before registration`.

### Task 4: Verify that skill changes include all three guide updates

**Files:** Create `tools/check-skill-docs.py` and
`tests/unix/test_skill_docs.py`. Modify `.github/workflows/unix.yml`,
`CONTRIBUTING.md`, and `.agents/skills/sync-skill-docs/SKILL.md`.

**Interfaces:** `python3 tools/check-skill-docs.py BASE HEAD`, run from the
checkout, compares the merge base to HEAD using Git. If any changed file is
under `plugins/executive-assistant/skills/`, exit 1 and list the missing
paths in guide order. Guide order is `docs/SAMPLE-PROMPTS.md`,
`docs/CODEX-WORKFLOWS.md`, `docs/WORKFLOW-DIAGRAMS.md`. A complete change
or a change outside the packaged skill directory exits 0. Missing Git refs
exit 1 with a diagnostic. The check requires changed guide files, and review
continues to verify prompt behavior.

- [ ] Add `test_existing_skill_update_requires_all_guides`,
  `test_added_or_removed_skill_file_requires_guides`, and
  `test_repo_local_skill_does_not_trigger_packaged_guide_check`. Build
  synthetic commits in temporary Git repositories using local test author
  settings. For a change to a packaged `agents/openai.yaml` with only the
  sample and diagrams changed, assert exit 1 and
  `docs/CODEX-WORKFLOWS.md` in stderr. Change the remaining guide in a
  subsequent commit and assert exit 0 for the original base and new tip.
  Exercise addition and removal, a change to a repo-local skill, and an
  unknown base. Assert the exit behavior from the interface above.
- [ ] Run `python3 -m unittest discover -s tests/unix -p test_skill_docs.py -v`.
  Expect failures because the script is absent.
- [ ] Implement the CLI with standard library argument parsing and
  `git diff --name-only -z --no-renames BASE...HEAD --`. Resolve BASE and
  HEAD to commits before the diff and report Git failures to stderr. Add
  a single `pull_request`-only job to the workflow with `fetch-depth: 0`.
  Pass the PR base SHA through an environment variable and use the
  checked-out HEAD as the comparison tip.
- [ ] Document the local check command for contributors and in
  `sync-skill-docs`. Rerun the targeted and full suites. Expect exit 0.
  Commit as `Check skill documentation changes in pull requests`.

### Task 5: Verify the license shipped in the release ZIP

**Files:** Modify `tests/unix/test_package_contract.py`,
`.github/workflows/unix.yml`, and `docs/RELEASE-CHECKLIST.md`.

**Interfaces:** The package contract requires the MIT title, the approved
copyright line, and recognizable grant, notice, and warranty paragraphs.
The ZIP smoke workflow compares the extracted license byte-for-byte to the
file at HEAD before running the existing first-brief check.

- [ ] Add `test_release_license_contains_the_approved_mit_notice` to
  `PackageContractTest`. Normalize whitespace before checking for
  `MIT License`, `Copyright (c) 2026 Robert Thompson`,
  `Permission is hereby granted`,
  `The above copyright notice and this permission notice shall be included`,
  and the warranty paragraph ending with
  `OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.`. Run the new test in a
  disposable copy with a `TBD` license and again with its warranty paragraph
  removed. Expect both fixtures to fail and the restored license to pass.
- [ ] In the existing extracted-ZIP job, replace the license existence check
  with `git show HEAD:LICENSE | cmp - "$package/LICENSE"` under Bash
  pipefail. In a disposable extracted archive, exercise the comparison with
  an edited license and expect exit 1. Rerun on a clean archive and expect 0.
- [ ] Update the release checklist to include this validation and the
  location of the ZIP actually supplied to a new user. Keep terminal, Desktop,
  Linux CI, and scheduler-fired evidence in separate checklist entries.
- [ ] Run the full suite, the workflow's syntax and ZIP commands, and the
  disposable plugin install locally. Expect exit 0. After the implementation
  is pushed, check the hosted matrix for that commit if visible. Record
  unavailable checks as pending. Commit as `Verify license text in releases`.
