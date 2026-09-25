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
- `scripts/`: utilities shared by the collection, as they are added.

Repository-specific contracts and testing commands stay in each project's own
guidance. The shared skills discover and use that context.

## Install

Use the [Skills CLI](https://github.com/vercel-labs/skills) with Node.js and npm.
From this checkout, install all skills globally for Codex:

```sh
npx skills add . --global --agent codex --skill '*'
```

To include Claude Code, use `--agent codex claude-code`. To select only the audit
skill, use `--skill test-quality-audit`. Preview available skills with:

```sh
npx skills add . --list
```

The CLI installs a copy and links agent directories to that installed copy.
After editing this checkout or pulling changes, rerun the install command to
refresh it. Hooks need their own agent-specific configuration.

For live development, a direct symlink from an agent's skill directory to a skill
in this checkout makes edits immediately available. Keep the checkout at a stable
path when using that approach.

Use the audit skill by asking, for example:

```text
Use test-quality-audit to review the tests in this repository and recommend improvements.
```

## Inspiration

The test audit workflow was informed by
[OpenClaw's test-audit skill](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md)
and practical audits of personal projects.
