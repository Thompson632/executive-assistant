---
name: sync-skill-docs
description: Update the sample prompts and workflow guides whenever an Executive Assistant plugin skill is added, edited, renamed, or removed.
---

# Sync Executive Assistant skill documentation

When a change touches a skill under `plugins/executive-assistant/skills/`,
update all three user guides in the same change. For a new skill, start
with the [skill template](../../../docs/SKILL-TEMPLATE.md).

1. Read the changed skill's `SKILL.md`, its UI metadata in `agents/openai.yaml`,
   and any changed references. Use the actual skill name, accepted inputs,
   prerequisites, outputs, and review steps.
2. Update [Sample Prompts](../../../docs/SAMPLE-PROMPTS.md) with a copyable
   prompt for the changed workflow. Use the exact `$executive-…` invocation
   and say what the reader should supply.
3. Update the command table in [Codex Workflows](../../../docs/CODEX-WORKFLOWS.md)
   with when to use the skill and which command or manual action it uses.
4. Update the skill index in [Workflow Diagrams](../../../docs/WORKFLOW-DIAGRAMS.md)
   and any affected diagrams, links, or handoffs. For a rename or removal,
   update or remove the old invocation in each guide.
5. Run `python3 -m unittest discover -s tests/unix -p test_package_contract.py -v`
   from the repository root. Read the edited examples against the skill to
   check that their behavior matches.

After committing the changes, run `python3 tools/check-skill-docs.py origin/main HEAD`
to check the pull-request diff. Substitute the intended base branch if it
differs. The check lists any guide files that are missing from the change.
