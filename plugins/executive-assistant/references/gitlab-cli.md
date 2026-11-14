# GitLab CLI

Use `$executive-gitlab-review` to review open issues, merge requests, and
recent pipelines on a GitLab project. It uses the `glab` executable on PATH
and its existing login. GitLab credentials stay in the CLI's credential
store. The executive-assistant profile needs no GitLab settings.

## Connect and verify

If you already use `glab`, run `glab --version` and check auth for the
project's host. For a new installation, follow [GitLab's CLI install guide](https://docs.gitlab.com/cli/#install-the-cli),
then run `glab auth login --hostname gitlab.com` and follow the prompts.
Substitute your GitLab hostname for a self-managed instance.

Use the project's full URL, without credentials or a trailing issue or
merge request path. The full URL lets you run from the Obsidian vault or
another checkout and selects the correct host.

```sh
glab auth status --hostname gitlab.com
glab issue list --repo https://gitlab.com/group/project --per-page 5
glab mr list --repo https://gitlab.com/group/project --per-page 5
glab ci list --repo https://gitlab.com/group/project --per-page 5
```

After updating the Executive Assistant plugin, start a new Codex chat and
ask “Use `$executive-gitlab-review` to summarize open work and recent
pipeline status for `https://gitlab.com/group/project`.”

[GitLab CLI authentication](https://docs.gitlab.com/cli/authentication/)
