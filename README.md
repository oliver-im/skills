# Skills

Personal agent skills, hooks, and workflow tools, versioned together for use
across projects and machines.

## Skills

| Skill | Purpose |
| --- | --- |
| [write-tests](skills/write-tests/SKILL.md) | Add or strengthen only tests that catch credible failures; audit code for missing protection. |
| [prune-tests](skills/prune-tests/SKILL.md) | Give every existing test a verdict and remove or merge the ones that add no protection. |

## Layout

- `skills/`: self-contained skill directories, each with a `SKILL.md`. Keep any
  skill-specific scripts, references, or assets alongside its instructions.
- `hooks/`: agent lifecycle hooks and their setup instructions, as they are added.
- `scripts/`: installation and other utilities shared by the collection.

Repository-specific contracts and testing commands stay in each project's own
guidance. The shared skills discover and use that context.

## Install

From this checkout, use Python 3 to link all skills globally for Codex:

```sh
python3 scripts/install.py
```

To install for Claude Code as well:

```sh
python3 scripts/install.py --target-dir ~/.claude/skills
```

The default destination is `$CODEX_HOME/skills`, or `~/.codex/skills` when
`CODEX_HOME` is unset. Use `--target-dir` for any other agent's skill directory.
The installer uses only the Python standard library.

Each link points directly into this checkout, so edits and `git pull` update the
linked files immediately. Rerun the installer when adding skills. Keep the
checkout at its installed location; links use absolute paths.

Matching links are left alone. The installer checks every destination before
adding links and refuses to replace existing files, directories, or links to
another source. It installs skill folders only; hooks need their own
agent-specific configuration.

The dotfiles `install.sh` also runs this installer for both Codex and Claude Code.
It defaults to a sibling `skills` checkout; set `SKILLS_REPO_DIR` to use another
location on a particular machine:

```sh
SKILLS_REPO_DIR="$HOME/src/skills" /path/to/dotfiles/install.sh
```

The collection also works with [npx skills](https://github.com/vercel-labs/skills),
whose installs use a separate copy instead of a live link to this checkout.

`write-tests` also applies whenever an agent writes tests. To run a gap audit
or a pruning sweep, ask explicitly, for example:

```text
Use write-tests to find contracts in this repository that the tests do not protect.
Use prune-tests to sweep the tests in this repository and remove the ones that add no protection.
```

## Inspiration

The test audit workflow was informed by
[OpenClaw's test-audit skill](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md)
and practical audits of personal projects.
