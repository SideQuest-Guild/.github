# SideQuest-Guild/.github

The GitHub org's shared files: the profile page at https://github.com/SideQuest-Guild and the community files every
repo in the org gets unless it has its own copy (`SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
`SUPPORT.md`, issue forms and the pull request template). `README.md` explains the repo to people.

## Layout
- `profile/README.md`: the org profile page. `profile/assets/` holds its images.
- `art/`: the painting prompts (`*.txt`), WebP crops and `build.py`, which builds the SVGs in `profile/assets/`.
  The large source PNGs are gitignored.
- `.github/`: the issue forms and pull request template.

## Working
- Rebuild the images with `uv run --with pillow python art/build.py`. It reads the site's fonts from a website checkout
  next to this one (`../website`).
- Preview the profile in dark and light before you push: GitHub shows it to everyone.
- Commits are SSH-signed via 1Password. If signing fails, ask the user to unlock it; never turn signing off.
- Conventional Commit subjects written as plain sentences. This repo has no releases.

## Rules that bite
- Write in plain words: Orwell's six rules, no jargon, no em dashes.
- Security reports go through GitHub private vulnerability reporting. Never add a contact email.
- A repo's own copy of a community file replaces the one here (the addon has its own `SECURITY.md`).
- Never name the guild's leaders.
- `AGENTS.md` is in the global gitignore; add it with `git add -f AGENTS.md`.
