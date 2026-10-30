"""Builds the animated SVGs for the org profile README from the painted art and the site's fonts.

Run from the repo root: `uv run --with pillow python art/build.py`. Inputs live in `art/` (the PNGs are gitignored;
the WebP crops are committed so the build can rerun without regenerating the paintings).
Outputs go to `profile/assets/`.

Everything animated stops under `prefers-reduced-motion: reduce`, and every SVG reads fine as a still frame.
"""

from __future__ import annotations

import base64
import html
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art"
OUT = ROOT / "profile" / "assets"
# The site's fonts, from a website checkout next to this repo (sidequest-guild/{.github,website}).
FONTS = ROOT.parent / "website" / "website" / "src" / "fonts"

GOLD = "#d8ab5c"
GOLD_2 = "#a88449"
GOLD_HI = "#f3dca6"
NIGHT = "#0b111d"
INK = "#f2efe9"


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def font_face(family: str, path: Path, style: str = "normal") -> str:
    return (
        f"@font-face{{font-family:'{family}';font-style:{style};"
        f"src:url({data_uri(path, 'font/woff2')}) format('woff2');}}"
    )


DISPLAY = font_face("SQ Display", FONTS / "LibertinusSerifDisplay.woff2")
SERIF = font_face("SQ Serif", FONTS / "EBGaramond.woff2")
ITALIC = font_face("SQ Serif", FONTS / "EBGaramond-italic.woff2", "italic")

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important;}}"

# Torches, lanterns and braziers in the 1280x720 hero crop: (x, y, radius, flicker seconds).
LIGHTS = [
    (429, 192, 120, 3.1),
    (237, 430, 95, 2.3),
    (607, 462, 95, 2.7),
    (1021, 540, 110, 2.9),
    (1233, 588, 95, 2.5),
    (92, 400, 70, 3.4),
    (150, 570, 70, 2.2),
]


def embers(rng: random.Random) -> str:
    """Small sparks drifting up from the torches; each gets its own path, speed and delay."""
    parts = []
    for x, y, r, _ in LIGHTS:
        for _ in range(4 if r > 90 else 2):
            dx = rng.uniform(-28, 28)
            rise = rng.uniform(110, 210)
            dur = rng.uniform(4.5, 8.5)
            delay = rng.uniform(0, 8)
            size = rng.uniform(1.1, 2.2)
            sx = x + rng.uniform(-10, 10)
            sy = y + rng.uniform(-12, 4)
            parts.append(
                f'<circle class="ember" cx="{sx:.0f}" cy="{sy:.0f}" r="{size:.1f}" '
                f'style="--dx:{dx:.0f}px;--rise:-{rise:.0f}px;animation-duration:{dur:.1f}s;'
                f'animation-delay:-{delay:.1f}s"/>'
            )
    return "".join(parts)


def hero() -> str:
    rng = random.Random(7)
    painting = data_uri(ART / "hero.webp", "image/webp")
    logo = data_uri(ART / "logo.webp", "image/webp")
    glows = "".join(
        f'<circle class="glow" cx="{x}" cy="{y}" r="{r}" fill="url(#torch)" '
        f'style="animation-duration:{d}s;animation-delay:-{i * 0.7:.1f}s;transform-origin:{x}px {y}px"/>'
        for i, (x, y, r, d) in enumerate(LIGHTS)
    )
    title = "SIDEQUEST"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 720" width="1280" height="720" role="img" aria-labelledby="t d">
<title id="t">SideQuest</title>
<desc id="d">A painted guild hall at night: adventurers study a quest board by torchlight under blue and gold banners. The title reads SideQuest, an Alliance guild for World of Warcraft: Forever.</desc>
<style>
{DISPLAY}{ITALIC}
.glow{{mix-blend-mode:screen;animation:flicker 3s ease-in-out infinite alternate;}}
@keyframes flicker{{0%{{opacity:.55;transform:scale(.94)}}35%{{opacity:.85;transform:scale(1.03)}}55%{{opacity:.6;transform:scale(.97)}}80%{{opacity:.95;transform:scale(1.05)}}100%{{opacity:.7;transform:scale(1)}}}}
.ember{{fill:{GOLD_HI};opacity:0;animation:rise 6s linear infinite;}}
@keyframes rise{{0%{{opacity:0;transform:translate(0,0)}}12%{{opacity:.9}}70%{{opacity:.5}}100%{{opacity:0;transform:translate(var(--dx),var(--rise))}}}}
.drift{{animation:drift 40s ease-in-out infinite alternate;transform-origin:640px 360px;}}
@keyframes drift{{from{{transform:scale(1)}}to{{transform:scale(1.045) translate(-6px,4px)}}}}
.shine{{animation:shine 7s ease-in-out infinite;}}
@keyframes shine{{0%,55%{{transform:translateX(-520px)}}100%{{transform:translateX(1320px)}}}}
.title{{font-family:'SQ Display',Georgia,serif;font-size:104px;letter-spacing:.24em;}}
.sub{{font-family:'SQ Serif',Georgia,serif;font-style:italic;font-size:30px;fill:{INK};}}
{REDUCED}
</style>
<defs>
<clipPath id="frame"><rect width="1280" height="720" rx="22"/></clipPath>
<radialGradient id="torch"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".55"/><stop offset=".35" stop-color="{GOLD}" stop-opacity=".22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="hush" cx="640" cy="150" r="560" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1 0 0 .42 0 87)"><stop offset="0" stop-color="{NIGHT}" stop-opacity=".88"/><stop offset=".6" stop-color="{NIGHT}" stop-opacity=".55"/><stop offset="1" stop-color="{NIGHT}" stop-opacity="0"/></radialGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset=".72" stop-color="{NIGHT}" stop-opacity="0"/><stop offset="1" stop-color="{NIGHT}" stop-opacity=".75"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD_HI}"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_2}"/></linearGradient>
<linearGradient id="band" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="letters"><text class="title" x="652" y="214" text-anchor="middle">{title}</text></clipPath>
<filter id="lift" x="-10%" y="-40%" width="120%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000" flood-opacity=".8"/></filter>
</defs>
<g clip-path="url(#frame)">
<g class="drift"><image href="{painting}" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/></g>
<g>{glows}</g>
<g>{embers(rng)}</g>
<rect width="1280" height="720" fill="url(#hush)"/>
<rect width="1280" height="720" fill="url(#floor)"/>
<image href="{logo}" x="604" y="26" width="72" height="89"/>
<g filter="url(#lift)">
<text class="title" x="652" y="214" text-anchor="middle" fill="url(#gold)">{title}</text>
</g>
<g clip-path="url(#letters)"><rect class="shine" x="0" y="120" width="260" height="120" fill="url(#band)" transform="skewX(-20)"/></g>
<g stroke="{GOLD}" stroke-width="1.4" fill="none" opacity=".9">
<path d="M330 250H600"/><path d="M680 250H950"/>
<path d="M640 243l7 7-7 7-7-7z" fill="{GOLD}"/>
<path d="M330 250l-5 0" />
</g>
<text class="sub" x="640" y="296" text-anchor="middle" filter="url(#lift)">An Alliance guild for World of Warcraft: Forever</text>
<rect width="1280" height="720" rx="22" fill="none" stroke="{GOLD_2}" stroke-opacity=".7" stroke-width="2"/>
</g>
</svg>"""


# The Courier's Loft, scaled to 1280x698 and shown 1280x600 (shifted up 50px). Lights: (x, y, radius, seconds).
COMPANION_LIGHTS = [
    (92, 395, 110, 2.6),  # the desk lantern
    (458, 361, 46, 3.3),  # the candle by the shelves
]
MOON = (995, 137)
DOVE = (800, 190)
CASTLE = (1034, 252)


def companion() -> str:
    painting = data_uri(ART / "companion.webp", "image/webp")
    glows = "".join(
        f'<circle class="glow" cx="{x}" cy="{y}" r="{r}" fill="url(#torch)" '
        f'style="animation-duration:{d}s;transform-origin:{x}px {y}px"/>'
        for x, y, r, d in COMPANION_LIGHTS
    )
    # The letter's road: from the dove, arcing up and over the valley, down to the lit castle.
    (dx, dy), (cx, cy) = DOVE, CASTLE
    road = f"M{dx} {dy} C{dx + 70} {dy - 46} {cx - 80} {cy - 96} {cx} {cy - 6}"
    title = "SIDEQUEST COMPANION"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 600" width="1280" height="600" role="img" aria-labelledby="t d">
<title id="t">SideQuest Companion</title>
<desc id="d">A painted tower loft at night: a guild courier in a blue cloak releases a white dove carrying a sealed scroll toward a distant lit castle. The title reads SideQuest Companion.</desc>
<style>
{DISPLAY}{ITALIC}
.glow{{mix-blend-mode:screen;animation:flicker 3s ease-in-out infinite alternate;}}
@keyframes flicker{{0%{{opacity:.55;transform:scale(.94)}}35%{{opacity:.85;transform:scale(1.03)}}55%{{opacity:.6;transform:scale(.97)}}80%{{opacity:.95;transform:scale(1.05)}}100%{{opacity:.7;transform:scale(1)}}}}
.moon{{mix-blend-mode:screen;animation:moon 9s ease-in-out infinite alternate;transform-origin:{MOON[0]}px {MOON[1]}px;}}
@keyframes moon{{from{{opacity:.45;transform:scale(.96)}}to{{opacity:.8;transform:scale(1.06)}}}}
.drift{{animation:drift 40s ease-in-out infinite alternate;transform-origin:640px 300px;}}
@keyframes drift{{from{{transform:scale(1)}}to{{transform:scale(1.04) translate(-5px,3px)}}}}
.road{{stroke-dasharray:2 9;animation:march 2.4s linear infinite;}}
@keyframes march{{to{{stroke-dashoffset:-22}}}}
.letter{{offset-path:path('{road}');offset-rotate:0deg;animation:carry 6.5s cubic-bezier(.45,.05,.3,1) infinite;}}
@keyframes carry{{0%{{offset-distance:0%;opacity:0}}10%{{opacity:1}}86%{{opacity:1}}100%{{offset-distance:100%;opacity:0}}}}
.title{{font-family:'SQ Display',Georgia,serif;font-size:58px;letter-spacing:.24em;}}
.sub{{font-family:'SQ Serif',Georgia,serif;font-style:italic;font-size:24px;fill:{INK};}}
{REDUCED}
</style>
<defs>
<clipPath id="frame"><rect width="1280" height="600" rx="22"/></clipPath>
<radialGradient id="torch"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".55"/><stop offset=".35" stop-color="{GOLD}" stop-opacity=".22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="moonlight"><stop offset="0" stop-color="#dfe8ff" stop-opacity=".5"/><stop offset=".4" stop-color="#9fb4e6" stop-opacity=".16"/><stop offset="1" stop-color="#9fb4e6" stop-opacity="0"/></radialGradient>
<radialGradient id="hush" cx="640" cy="74" r="560" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1 0 0 .24 0 56)"><stop offset="0" stop-color="{NIGHT}" stop-opacity=".9"/><stop offset=".55" stop-color="{NIGHT}" stop-opacity=".5"/><stop offset="1" stop-color="{NIGHT}" stop-opacity="0"/></radialGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset=".7" stop-color="{NIGHT}" stop-opacity="0"/><stop offset="1" stop-color="{NIGHT}" stop-opacity=".7"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD_HI}"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_2}"/></linearGradient>
<filter id="lift" x="-10%" y="-40%" width="120%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000" flood-opacity=".8"/></filter>
<filter id="spark" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2"/></filter>
</defs>
<g clip-path="url(#frame)">
<g class="drift"><image href="{painting}" y="-50" width="1280" height="698" preserveAspectRatio="xMidYMid slice"/></g>
<circle class="moon" cx="{MOON[0]}" cy="{MOON[1]}" r="70" fill="url(#moonlight)"/>
<g>{glows}</g>
<path class="road" d="{road}" fill="none" stroke="{GOLD_HI}" stroke-opacity=".9" stroke-width="2.2" stroke-linecap="round"/>
<g class="letter"><path d="M0 -10 10 0 0 10 -10 0z" fill="{GOLD_HI}" filter="url(#spark)"/><path d="M0 -6 6 0 0 6 -6 0z" fill="#fff4d6"/></g>
<rect width="1280" height="600" fill="url(#hush)"/>
<rect width="1280" height="600" fill="url(#floor)"/>
<g filter="url(#lift)">
<text class="title" x="654" y="68" text-anchor="middle" fill="url(#gold)">{title}</text>
</g>
<g stroke="{GOLD}" stroke-width="1.4" fill="none" opacity=".9">
<path d="M400 90H612"/><path d="M668 90H880"/>
<path d="M640 83l7 7-7 7-7-7z" fill="{GOLD}"/>
</g>
<text class="sub" x="640" y="124" text-anchor="middle" filter="url(#lift)">Raid nights to the site. Points back to the game.</text>
<rect width="1280" height="600" rx="22" fill="none" stroke="{GOLD_2}" stroke-opacity=".7" stroke-width="2"/>
</g>
</svg>"""


# The quest notices: one per repo. Lines are pre-wrapped to fit the parchment at 25px EB Garamond.
NOTICES = {
    "website": (
        "THE GUILD HALL",
        ["sidequest-guild.com and", "its API: events, sign-ups,", "raid charts, the Hall of", "Heroes and the SQL ledger."],
        "Python · Litestar · Astro",
    ),
    "bot": (
        "THE HERALD",
        ["The Game Master bot in", "our Discord: roles, event", "posts, sign-up buttons,", "badges, the weekly board."],
        "Python · discord.py",
    ),
    "addon": (
        "THE WORKSHOP",
        ["The in-game addon. It", "records raid nights, runs", "SQL loot bids and shows", "the standings, plus the", "sync uploader."],
        "Lua · WoW: Forever · Python",
    ),
    "companion": (
        "THE COURIER",
        ["A desktop app for your", "tray. It carries raid nights", "to the site, brings points", "home and keeps the addon", "up to date."],
        "Rust · GPUI · Win · Mac · Linux",
    ),
}
INK_DARK = "#2b1d0e"
INK_SOFT = "#5a4126"


def notice(name: str) -> str:
    eyebrow, lines, tech = NOTICES[name]
    paper = data_uri(ART / "notice.webp", "image/webp")
    body = "".join(
        f'<tspan x="256" dy="{0 if i == 0 else 37}">{html.escape(line)}</tspan>' for i, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 768" width="512" height="768" role="img" aria-labelledby="t d">
<title id="t">{name}</title>
<desc id="d">A quest notice pinned to an oak board. {html.escape(eyebrow.title())}: {html.escape(" ".join(lines))} Built with {html.escape(tech)}.</desc>
<style>
{DISPLAY}{SERIF}
.eyebrow{{font-family:'SQ Serif',Georgia,serif;font-size:21px;letter-spacing:.26em;fill:{INK_SOFT};}}
.name{{font-family:'SQ Display',Georgia,serif;font-size:64px;letter-spacing:.06em;fill:{INK_DARK};}}
.body{{font-family:'SQ Serif',Georgia,serif;font-size:29px;fill:{INK_DARK};}}
.tech{{font-family:'SQ Serif',Georgia,serif;font-size:19px;letter-spacing:.14em;fill:{INK_SOFT};}}
.candle{{mix-blend-mode:soft-light;animation:candle 4.2s ease-in-out infinite alternate;}}
@keyframes candle{{0%{{opacity:.35}}30%{{opacity:.6}}60%{{opacity:.4}}100%{{opacity:.7}}}}
{REDUCED}
</style>
<defs>
<radialGradient id="warm" cx="60" cy="40" r="620" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffd38a"/><stop offset="1" stop-color="#ffd38a" stop-opacity="0"/></radialGradient>
</defs>
<image href="{paper}" width="512" height="768"/>
<rect class="candle" width="512" height="768" fill="url(#warm)"/>
<text class="eyebrow" x="256" y="150" text-anchor="middle">{eyebrow}</text>
<path d="M196 172H316" stroke="{INK_SOFT}" stroke-width="1.2" opacity=".7"/>
<text class="name" x="256" y="252" text-anchor="middle">{name}</text>
<text class="body" x="256" y="314" text-anchor="middle">{body}</text>
<text class="tech" x="256" y="532" text-anchor="middle">{html.escape(tech.upper())}</text>
<text class="eyebrow" x="256" y="572" text-anchor="middle" style="font-size:18px">TAKE THIS QUEST</text>
</svg>"""


def button(label: str, glyph: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 64" width="320" height="64" role="img" aria-label="{html.escape(label.title())}">
<style>{DISPLAY}
.l{{font-family:'SQ Display',Georgia,serif;font-size:19px;letter-spacing:.18em;fill:{INK};}}
.g{{fill:{GOLD};}}
</style>
<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f4c86"/><stop offset=".6" stop-color="#284274"/><stop offset="1" stop-color="#1a2c5a"/></linearGradient></defs>
<path d="M14 2H306L318 32 306 62H14L2 32Z" fill="url(#b)" stroke="{GOLD_2}" stroke-width="1.6"/>
<path d="M20 8H300L309 32 300 56H20L11 32Z" fill="none" stroke="{GOLD}" stroke-opacity=".35"/>
{glyph}
<text class="l" x="192" y="39" text-anchor="middle">{html.escape(label)}</text>
</svg>"""


# 24px glyphs, drawn at x 38..62: a speech bubble for Discord, a tower for the site.
DISCORD_GLYPH = (
    '<path class="g" transform="translate(40 20)" d="M2 2h20v14H9l-5 5v-5H2z" fill-opacity=".95"/>'
    '<g fill="#1a2c5a" transform="translate(40 20)"><circle cx="8" cy="9" r="1.6"/><circle cx="12" cy="9" r="1.6"/><circle cx="16" cy="9" r="1.6"/></g>'
)
SITE_GLYPH = '<path class="g" transform="translate(40 18)" d="M3 26V10l3-2V4h3v2l3-3 3 3V4h3v4l3 2v16h-7v-7a2 2 0 0 0-4 0v7z"/>'
# A sealed scroll with a down arrow over it, for downloading the companion.
DOWNLOAD_GLYPH = (
    '<g transform="translate(38 18)"><path class="g" d="M12 1v13M6 9l6 6 6-6" fill="none" stroke="#d8ab5c" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path class="g" d="M2 19h20v5H2z"/><path d="M10 21.5h4" stroke="#1a2c5a" stroke-width="1.6"/></g>'
)


def divider() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 24" width="800" height="24" role="img" aria-label="">
<defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>
<path d="M40 12H372M428 12H760" stroke="url(#r)" stroke-width="1.4"/>
<path d="M400 4l8 8-8 8-8-8z" fill="none" stroke="{GOLD}" stroke-width="1.4"/><path d="M400 8.5l3.5 3.5-3.5 3.5-3.5-3.5z" fill="{GOLD}"/>
<circle cx="382" cy="12" r="1.8" fill="{GOLD}"/><circle cx="418" cy="12" r="1.8" fill="{GOLD}"/>
</svg>"""


def main() -> None:
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    paper = Image.open(ART / "notice.png").convert("RGB").resize((512, 768), Image.LANCZOS)
    paper.save(ART / "notice.webp", "WEBP", quality=80, method=6)
    loft = ART / "companion.png"
    if loft.exists():  # the full-size painting isn't committed; the WebP crop is
        Image.open(loft).convert("RGB").resize((1280, 698), Image.LANCZOS).save(
            ART / "companion.webp", "WEBP", quality=82, method=6
        )
    (OUT / "hero.svg").write_text(hero())
    (OUT / "companion.svg").write_text(companion())
    for name in NOTICES:
        (OUT / f"quest-{name}.svg").write_text(notice(name))
    (OUT / "button-discord.svg").write_text(button("JOIN THE DISCORD", DISCORD_GLYPH))
    (OUT / "button-site.svg").write_text(button("VISIT THE SITE", SITE_GLYPH))
    (OUT / "button-download.svg").write_text(button("GET THE APP", DOWNLOAD_GLYPH))
    (OUT / "divider.svg").write_text(divider())
    for path in sorted(OUT.glob("*.svg")):
        print(f"{path.relative_to(ROOT)} {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
