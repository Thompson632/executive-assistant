# Executive Assistant skill template

Create `plugins/executive-assistant/skills/executive-<task>/` with the two
files below. Replace the examples with the new skill's name and workflow.
Use the same name in the directory, frontmatter, and example prompt.

## SKILL.md

```markdown
---
name: executive-example-task
description: Describe what the skill does and when a user would ask for it.
---

# Executive Example Task

State what the user will receive and which notes, files, or project the skill
needs.

## Workflow

1. Identify the input and target from the request or configured profile.
2. Describe the steps in the order they occur. Include the command and its
   working directory when the workflow uses one.
3. Return the result with links to source notes or saved output when available.
```

Add a prerequisite, review step, or failure instruction where it changes how
the workflow runs. For a skill that writes, say what the user reviews before
the write and how the skill verifies the result.

## agents/openai.yaml

```yaml
interface:
  display_name: "Executive Example Task"
  short_description: "Describe the task in 25 to 64 characters"
  default_prompt: "Use $executive-example-task to complete a specific task with the supplied notes."
```

Use a real request in the default prompt. Follow the
[skill documentation maintenance instructions](../.agents/skills/sync-skill-docs/SKILL.md)
to update the sample prompts and workflow guides, then run
[skill validation](../AGENTS.md#validation).
