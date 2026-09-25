# Skills

Personal agent skills, hooks, and workflow tools, versioned together for use
across projects and machines.

## Skills

| Skill | Purpose |
| --- | --- |
| [test-quality-audit](skills/test-quality-audit/SKILL.md) | Review tests for weak assertions, missing protection, and costly redundancy. |

## Layout

- `skills/`: self-contained skill directories, each with a `SKILL.md`. Keep any
  skill-specific scripts, references, or assets alongside its instructions.
- `hooks/`: agent lifecycle hooks and their setup instructions, as they are added.
- `scripts/`: installation and other utilities shared by the collection.

Repository-specific contracts and testing commands stay in each project's own
guidance. The shared skills discover and use that context.

## Install

Run from this checkout with Python 3:

```sh
python3 scripts/install.py
```

This links each skill into `$CODEX_HOME/skills`, or `~/.codex/skills` when
`CODEX_HOME` is unset. Edits in this checkout are reflected through the links.
Keep the checkout at its installed location, or relink after moving it.

To choose another skill directory:

```sh
python3 scripts/install.py --target-dir ~/.claude/skills
```

The installer leaves matching links alone and refuses to replace existing files,
directories, or links to a different source. It installs skill folders only;
hooks need their own agent-specific configuration.

Use the audit skill by asking, for example:

```text
Use test-quality-audit to review the tests in this repository and recommend improvements.
```

## Inspiration

The test audit workflow was informed by
[OpenClaw's test-audit skill](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md)
and practical audits of personal projects.
