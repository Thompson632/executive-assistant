# Codex plugin repository blueprint

Give the model this file, a completed project brief, and a writable checkout.
The checkout can start empty. The example uses a local marketplace and one
plugin, and the same layout supports several plugins.

## Handoff prompt

> Build the plugin repository in the current checkout using this blueprint
> and the completed project brief. Start with the first workflow and its
> synthetic input. Implement it and verify its expected output, then add
> the remaining required workflows, setup documentation, and validation.
> Report the files you created, the first prompt to try, and the checks
> you ran. List host or integration checks that are still pending.

## Project brief

```yaml
repository_name: ""
marketplace_id: ""
marketplace_display_name: ""
plugins:
  - id: ""
    display_name: ""
    purpose: ""
    target_users: ""
    first_workflow: ""
    sample_input: ""
    expected_output: ""
    other_workflows: []
    required_integrations: []
    optional_integrations: []
    allowed_writes: ""
supported_hosts: []
runtime_dependencies: []
maintainer: ""
license: ""
```

Describe the first workflow as a task a new user can finish with synthetic
data. Include what they provide, what they see, and where any output is saved.
For each required integration, name its service and the read or write
operations the workflow needs. Use synthetic inputs for the first run
where possible. If the plugin's purpose, required external access, or
license is unclear, ask the maintainer to decide.
Treat the plugin IDs as stable kebab-case names. Use a project-specific
marketplace ID so it can coexist with someone else's marketplace.

## 1. Build a small, installable package

Use this layout. Add the runtime and release pieces where they support a
workflow the project actually ships.

```text
.agents/plugins/marketplace.json
.agents/skills/sync-skill-docs/SKILL.md
.github/workflows/validation.yml
.gitattributes
.gitignore
AGENTS.md
README.md
DEVELOPING.md
CONTRIBUTING.md
LICENSE
docs/
  GETTING-STARTED.md
  SAMPLE-PROMPTS.md
  CODEX-WORKFLOWS.md
  WORKFLOW-DIAGRAMS.md
  SKILL-TEMPLATE.md
  RELEASE-CHECKLIST.md
plugins/
  <plugin-id>/
    .codex-plugin/plugin.json
    skills/
      <skill-id>/
        SKILL.md
        agents/openai.yaml
    references/                 # Shared workflow details, when needed
    assets/                     # Synthetic inputs or starter files
    scripts/                    # Deterministic local operations, when needed
config/                         # Example settings, when needed
install/                        # Installer for supported hosts
tests/
tools/                          # ZIP builder and repository checks
```

Register one marketplace entry per plugin. Use the same plugin ID in the
marketplace, manifest, directory, and installation command. In these
examples, replace `field-notes` and `field-notes-local` with the project
brief's IDs. Add the license text once the maintainer supplies the license
and attribution.

**Example marketplace**

```json
{
  "name": "field-notes-local",
  "interface": { "displayName": "Field Notes" },
  "plugins": [
    {
      "name": "field-notes",
      "source": { "source": "local", "path": "./plugins/field-notes" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

**Example plugin manifest**

```json
{
  "name": "field-notes",
  "version": "0.1.0",
  "description": "Turn supplied field notes into a short digest.",
  "skills": "./skills/",
  "interface": {
    "displayName": "Field Notes",
    "shortDescription": "Summarize a folder of field notes.",
    "category": "Productivity",
    "defaultPrompt": ["Use $field-notes-digest to preview a digest of my sample notes."]
  }
}
```

Finish this step when each marketplace entry resolves to its plugin
directory and each manifest identifies the skills directory.

## 2. Implement one complete user journey

Start with the first workflow in the brief. Define its accepted input, the
result the user gets, and how success or failure is visible. Ship synthetic
starter data that lets someone try it without connecting a live account.

Use skills for interpretation and chat guidance. Use a command for repeatable
configuration, parsing, file operations, and report generation when those
operations are part of the workflow. If the plugin has a runtime, give it an
entry point with `--help` and actionable errors. For a local-file runtime, a
reasonable starting pattern is setup, a read-only check, a preview, and an
explicit save. Pick the runtime and host matrix from the project brief.

For each published skill, keep its directory, frontmatter `name`, and
`$skill-name` references identical. Write the description around what the
user wants to do. The body covers inputs, ordered actions, output, and
recovery from likely failures. Add `agents/openai.yaml` with a readable
display name, a short description, and a copyable default prompt. Start with
a single working skill, then repeat the same pattern for the others.

For the example, save these instructions as
`plugins/field-notes/skills/field-notes-digest/SKILL.md`.

```markdown
---
name: field-notes-digest
description: Summarize supplied field notes into observations and next steps.
---

# Field Notes Digest

1. Read the notes the user supplied.
2. Summarize the observations and list any explicit next steps. Link to each
   source note when the path is available.
3. Preview the digest in chat. Ask the user to name the source if none was supplied.
```

Save the interface metadata in `agents/openai.yaml` under the skill directory.

```yaml
interface:
  display_name: "Field Notes Digest"
  short_description: "Summarize notes and extract next steps"
  default_prompt: "Use $field-notes-digest to preview a digest of my sample notes."
```

Keep user settings, credentials, working files, and generated outputs
outside tracked source. Use disposable paths in tests. For a workflow that
writes, preview the target and change, respect the user's approval boundary,
and verify the saved result. For local files, preserve existing content on
reruns by default and make replacement an explicit operation. Use the
platform's supported auth flow for optional live integrations.

Finish this step when the package installs and its first skill produces the
expected output from a synthetic input through its normal entry point.

## 3. Write the setup guide and keep it current

- **README.** Explain the outcome, who the plugin is for, and where to
  start. Link the getting-started guide and developer guide near the top.
- **Getting started.** Walk from checkout or ZIP to the first result.
  Show where to run each command, what the installer prints, which folder
  to open in Codex, a prompt to paste, and how to find the output. Give
  returning users a route to verify or update their existing setup. Put
  optional integrations and scheduling after the first successful result.
- **Workflow guides.** Give every skill a prompt in `SAMPLE-PROMPTS.md`,
  an entry with its command or manual action in `CODEX-WORKFLOWS.md`, and
  a place in the index or relevant diagram in `WORKFLOW-DIAGRAMS.md`.
  Keep these documents aligned when skills are added, edited, renamed,
  or removed. Put that rule in `AGENTS.md` and the repo-local maintenance
  skill. Give contributors a short skill template.
- **Developer and release guides.** Document the test command, a disposable
  installation, how to handle a marketplace name conflict, and how to
  build or upgrade from a committed revision. Keep a release checklist
  with distinct entries for automated tests and observed host behavior.

Ignore `docs/superpowers/plans/` and `docs/superpowers/specs/` in Git and
mark both directories `export-ignore` in `.gitattributes`. Keep working plans
and specs there. Put lasting decisions in tracked documentation that can
stand alone in a fresh checkout.

Finish this step when a reader can follow the guide without needing the
maintainer's local paths, accounts, or working plans.

## 4. Verify what ships

Use the same validation commands in the developer guide and CI.

| Check | Passing result |
| --- | --- |
| Package | Manifest loads, each skill has valid metadata, and the source paths resolve to the intended plugin folders. |
| Docs | Local links resolve. Every published skill appears in the sample prompts and both workflow guides. A PR that changes a published skill also updates those files. |
| Data boundaries | Fixtures use synthetic data. Private configuration and working plans stay outside tracked files and release archives. |
| Runtime | The first workflow works with temporary settings. An invalid input produces an actionable message. Where the workflow previews and saves, preview is read-only and rerun behavior matches the guide. |
| ZIP or other release artifact | Build from a known commit, extract to a path with spaces, and run the documented workflow from the extracted files. Verify that required guides, metadata, and the chosen license ship. |
| Installed plugin | In a disposable Codex configuration, register the repo marketplace, install the plugin, and verify the installed copy. Test an upgrade with an existing synthetic profile if the repo ships local configuration. |
| Desktop and live hosts | In a fresh Desktop chat, invoke the installed skill and verify the output. Verify scheduled jobs and authenticated integrations separately when the project ships them. |

For the example, run these disposable CLI checks from the repo root.

```sh
plugin_test_settings=$(mktemp -d)
CODEX_HOME="$plugin_test_settings" codex plugin marketplace add "$PWD"
CODEX_HOME="$plugin_test_settings" codex plugin add field-notes@field-notes-local
CODEX_HOME="$plugin_test_settings" codex plugin list
```

Use a CLI that supports `codex plugin marketplace` and `codex plugin add`.
For projects with an installer, probe that support before registering the
marketplace. Scope tool configuration to the disposable directory during
validation. Record the exact commit, hosts, commands, and results. Mark
Desktop, scheduler-fired, and authenticated integration checks pending if
they still need to run.

Finish when the installable repo, first workflow, user guide, and validation
are usable together. Hand back the files, the first prompt to try, and the
checks that passed or are still pending.
