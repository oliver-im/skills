# Skills

Personal agent skills, hooks, and workflow tools, versioned together for use across projects and machines.

## Skills

| Skill | Purpose |
| --- | --- |
| [write-tests](skills/write-tests/SKILL.md) | Add or strengthen only tests that catch credible failures; audit code for missing protection. |
| [prune-tests](skills/prune-tests/SKILL.md) | Give every existing test a verdict and remove or merge the ones that add no protection. |

## Layout

- `skills/`: self-contained skill directories, each with a `SKILL.md`. Keep any skill-specific scripts, references, or assets alongside its instructions.
- `hooks/`: agent lifecycle hooks and their setup instructions, as they are added.
- `scripts/`: installation and other utilities shared by the collection.

Repository-specific contracts and testing commands stay in each project's own guidance. The shared skills discover and use that context.

## Install

Install with [npx skills](https://github.com/vercel-labs/skills), which supports Claude Code, Codex, and other agents:

```sh
npx skills add oliver-im/skills
```

Add `-g` to install for your user instead of the current project, `-a claude-code` or `-a codex` to choose agents, or `--skill prune-tests` to install one skill.

### From a checkout

To edit the skills, link them from a clone instead. Use Python 3 to link all skills globally for Codex:

```sh
python3 scripts/install.py
```

To install for Claude Code as well:

```sh
python3 scripts/install.py --target-dir ~/.claude/skills
```

The default destination is `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. Use `--target-dir` for any other agent's skill directory. The installer uses only the Python standard library.

Each link points directly into this checkout, so edits and `git pull` update the linked files immediately. Rerun the installer when adding skills. Keep the checkout at its installed location; links use absolute paths.

Matching links are left alone. The installer checks every destination before adding links and refuses to replace existing files, directories, or links to another source. It installs skill folders only; hooks need their own agent-specific configuration.

## Usage

`write-tests` also applies whenever an agent writes tests. To run a gap audit or a pruning sweep, ask explicitly, for example:

```text
Use write-tests to find contracts in this repository that the tests do not protect.
Use prune-tests to sweep the tests in this repository and remove the ones that add no protection.
```

## Inspiration

The test audit workflow was informed by [OpenClaw's test-audit skill](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md) and practical audits of personal projects.
