"""Check that packaged skill changes include the public workflow guides."""

import argparse
import os
import subprocess
import sys


SKILL_PREFIX = "plugins/executive-assistant/skills/"
GUIDES = (
    "docs/SAMPLE-PROMPTS.md",
    "docs/CODEX-WORKFLOWS.md",
    "docs/WORKFLOW-DIAGRAMS.md",
)


def resolve_commit(ref: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
        capture_output=True, text=True,
    )
    if result.returncode:
        raise ValueError(f"Cannot resolve Git commit {ref!r}: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="Base branch, tag, or commit")
    parser.add_argument("head", help="Head branch, tag, or commit")
    args = parser.parse_args()
    try:
        base = resolve_commit(args.base)
        head = resolve_commit(args.head)
        result = subprocess.run(
            ["git", "diff", "--name-only", "-z", "--no-renames", f"{base}...{head}", "--"],
            capture_output=True,
        )
        if result.returncode:
            raise ValueError(f"Cannot compare Git commits: {os.fsdecode(result.stderr).strip()}")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    changed = set(os.fsdecode(result.stdout).split("\0"))
    if any(path.startswith(SKILL_PREFIX) for path in changed):
        missing = [guide for guide in GUIDES if guide not in changed]
        if missing:
            print("Packaged skill changes also require updates to these guides:", file=sys.stderr)
            for guide in missing:
                print(f"  {guide}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
