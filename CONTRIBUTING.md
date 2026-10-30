# Contributing to SideQuest

Thanks for taking a quest. This guide covers every SideQuest repo. A repo's own README has the details for that repo.

## The repos

| Repo | What it is | Language |
|---|---|---|
| [website](https://github.com/SideQuest-Guild/website) | sidequest-guild.com, its API and the database | Python 3.15 (Litestar), Astro |
| [bot](https://github.com/SideQuest-Guild/bot) | The Discord bot. It reaches the database only through the API | Python 3.15 (discord.py) |
| [addon](https://github.com/SideQuest-Guild/addon) | The in-game addon and the `sidequest-sync` uploader | Lua, Python |
| [companion](https://github.com/SideQuest-Guild/companion) | The desktop tray app that syncs the addon with the site | Rust (GPUI) |
| [docs](https://github.com/SideQuest-Guild/docs) | The handbook at docs.sidequest-guild.com: guides, references and changelogs | Markdown (Sphinx) |

## Before you start

- For anything bigger than a typo, open an issue first so we can agree on the approach.
- Check the [guild rules](https://sidequest-guild.com/rules/). They apply here too.
- Found a security problem? Don't open an issue. Follow the [security policy](SECURITY.md).

## Making a change

1. Fork the repo and make a branch.
2. Follow the repo's README to set it up. Each repo has a `Makefile`; `make ci` runs every check that CI runs.
3. Keep the change small and about one thing.
4. Add or update tests for what you change. A test should fail before your change and pass after it.
5. Run `make ci` and fix what it reports.
6. Open a pull request.

## Pull requests

- Title the pull request as a [Conventional Commit](https://www.conventionalcommits.org): `type: what changed`, written as a plain sentence a guild member could read. For example, `fix: the raid chart keeps its groups after a reload`.
- Common types: `feat`, `fix`, `docs`, `test`, `ci`, `chore`, `perf`.
- Say what you changed and why, and how you checked it. Screenshots help for anything on the site.
- Update the docs when behavior changes.

## Writing

Copy on the site, in the bot and in docs follows a few plain rules:

- Use short, common words.
- Cut every word you can.
- Prefer the active voice.
- Skip jargon and stock phrases.
- Don't use em dashes.

## Code of conduct

Everyone who takes part agrees to the [code of conduct](CODE_OF_CONDUCT.md).
