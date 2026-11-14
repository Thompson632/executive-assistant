# Local rehearsal

Run the full workflow in the selected Obsidian vault without connecting to
GitLab or Confluence. Label the simulated records **Local rehearsal**.

- Add the approved action under Inbox in `Action-Items.md` or the existing
  task list. Link it to the local epic.
- Save the epic as `GitLab/<Request>/Epic.md`. Save each approved issue in
  `GitLab/<Request>/Issues/<Issue>.md`. Use safe vault-relative names,
  link each issue to its parent, and list the child links in the epic.
- When the user confirms the initial meeting happened, add the exact status
  line under **Comments** in `Epic.md`. While pending, leave that section
  without the comment. Repeating the confirmation should keep just one copy.
- Save the draft to `Confluence/Scrum of Scrums/<Request>.md` and label it
  **Preview**. Use Obsidian links to the local epic and issues.

Start by looking for the request's existing folder and matching issue notes.
Reuse them when rerunning or moving from pending meeting to confirmed.
Keep unrelated notes intact and use one Inbox checkbox per request.
