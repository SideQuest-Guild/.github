# Security policy

SideQuest is a player-run guild. Our code runs [sidequest-guild.com](https://sidequest-guild.com), the guild's Discord bot, the SideQuest addon, the SideQuest Companion desktop app and the handbook at docs.sidequest-guild.com. If you find a security problem in any of it, tell us privately so we can fix it before anyone abuses it.

## How to report

Use GitHub's private reporting. Open the repo, go to the **Security** tab and choose **Report a vulnerability**. Only the maintainers see your report.

- [Report a problem in the website or API](https://github.com/SideQuest-Guild/website/security/advisories/new)
- [Report a problem in the bot](https://github.com/SideQuest-Guild/bot/security/advisories/new)
- [Report a problem in the addon or the uploader](https://github.com/SideQuest-Guild/addon/security/advisories/new)
- [Report a problem in the companion app](https://github.com/SideQuest-Guild/companion/security/advisories/new)
- [Report a problem in the handbook site](https://github.com/SideQuest-Guild/docs/security/advisories/new)

Please don't open a public issue, post about it in the guild Discord, or test it against other members' accounts.

## What to send

- What you found and where: a URL, a file, or a command.
- The steps to reproduce it.
- What an attacker could do with it.

## What happens next

We read every report and reply to confirm we have it. We keep you posted while we work on a fix. Once the fix is live we publish an advisory and credit you, unless you would rather stay anonymous.

## What we cover

- sidequest-guild.com and its API
- the SideQuest Discord bot
- the SideQuest addon and the `sidequest-sync` uploader
- the SideQuest Companion desktop app
- the handbook at docs.sidequest-guild.com

## What we don't cover

- World of Warcraft, Battle.net, Discord and GitHub themselves. Report those to the company that runs them.
- Denial of service, spam, and tricking guild members into giving up their accounts.
- Scanner output with no working proof.

## Versions

We fix whatever runs on sidequest-guild.com today and the latest release of the addon and the companion app. Older versions don't get fixes, so please update.
