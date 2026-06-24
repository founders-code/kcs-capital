#!/usr/bin/env python3
"""Remove data-room links, raise copy, and investor CTAs sitewide."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

REMOVALS = [
    '\n <li><a href="https://data.4ormfinance.com" target="_blank" rel="noopener">4orm Finance data room</a></li>',
    '<li><a href="https://data.4ormfinance.com" target="_blank" rel="noopener">4orm Finance data room</a></li>',
    '<li><a href="/contact">Contact</a></li><li><a href="https://data.4ormfinance.com" target="_blank" rel="noopener">4orm Finance data room</a></li>',
    '\n <li><a href="https://data.4ormfinance.com" target="_blank" rel="noopener">4orm Finance investor relations</a></li>',
    '<li><a href="https://data.4ormfinance.com" target="_blank" rel="noopener">4orm Finance investor relations</a></li>',
    '<li><a href="/contact" class="nav-cta">Contact Us</a></li>',
]

SAMARA_OLD = (
    "Project Samara is directional support that settlement finality works in Canada "
    "(it settled against central-bank money, not 4orm's commercial-bank deposit model)."
)
SAMARA_NEW = (
    "Project Samara is directional support that settlement finality works in Canada."
)

FOURM_PRESEED = [
    "4orm Finance pre-seed &middot; <strong>closing Q2 2026</strong>",
    "4orm Finance pre-seed &middot; closing Q2 2026",
    "4orm Finance pre-seed &middot; architecture &amp; discovery",
    "from the firm's pre-seed phase, with the explicit goal",
]

FOURM_PRESEED_REPLACEMENTS = {
    "from the firm's pre-seed phase, with the explicit goal": "from the firm's early build phase, with the explicit goal",
}


def clean_nav_active_js(text: str) -> str:
    return text.replace(
        "if(s==='investors'&&h==='/data-room')a.classList.add('nav-active');",
        "",
    )


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old in REMOVALS:
        text = text.replace(old, "")
    text = text.replace(SAMARA_OLD, SAMARA_NEW)
    for old, new in FOURM_PRESEED_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = clean_nav_active_js(text)
    if path.name == "team.html":
        text = text.replace("Vice President of Investor Relations at Collective Technologies Inc.", "Vice President of Corporate Development at Collective Technologies Inc.")
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        if path.name in {"data-room.html", "request-access.html", "investors.html"}:
            continue
        if process_file(path):
            changed.append(path.name)
    print(f"Updated {len(changed)} files")


if __name__ == "__main__":
    main()
