# SideQuest-Guild/.github

Defaults for every repo in the [SideQuest-Guild](https://github.com/SideQuest-Guild) organization.

- `profile/README.md` is the organization's landing page. Its art lives in `profile/assets/`.
- `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` and `SUPPORT.md` apply to any repo that doesn't have its own copy.
- `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` do the same for issues and pull requests.

## Rebuilding the art

The paintings were made with Codex image generation from the prompts in `art/*.txt`. The SVGs embed WebP crops of them and the website's fonts. To rebuild after a change:

```sh
uv run --with pillow python art/build.py
```

The full-size PNGs aren't committed. Regenerate them from the prompts if you need to recrop.
