#!/usr/bin/env python3
"""Move investor/raise CTAs to 4orm; soften homepage positioning copy."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORM_4ORM = "https://data.4ormfinance.com"

REPLACEMENTS = [
    (
        "Canada's institution-grade RWA exchange and digital settlement network",
        "Canada's institutional settlement layer for tokenized real-world assets",
    ),
    (
        "Pre-Seed Active &middot; <strong>Closing Q2 2026</strong>",
        "4orm Finance pre-seed &middot; <strong>closing Q2 2026</strong>",
    ),
    (
        "Pre-Seed Active &middot; Closing Q2 2026",
        "4orm Finance pre-seed &middot; closing Q2 2026",
    ),
    (
        "Pre-Seed &middot; Closing Q2 2026",
        "4orm Finance pre-seed &middot; closing Q2 2026",
    ),
    (
        "Pre-Seed &middot; Architecture &amp; Discovery",
        "4orm Finance pre-seed &middot; architecture &amp; discovery",
    ),
    (
        "Project Samara proved the model.",
        "Project Samara is directional support that settlement finality works in Canada (it settled against central-bank money, not 4orm's commercial-bank deposit model).",
    ),
    (
        '<a href="/data-room" class="btn-p">Request Access to Data Room <span>&rarr;</span></a>',
        f'<a href="{FORM_4ORM}" class="btn-p" target="_blank" rel="noopener">Access the 4orm Finance data room. <span>&rarr;</span></a>',
    ),
    (
        '<a href="/data-room" class="btn-p">Request Access to Data Room &rarr;</a>',
        f'<a href="{FORM_4ORM}" class="btn-p" target="_blank" rel="noopener">Access the 4orm Finance data room. &rarr;</a>',
    ),
    (
        '<li><a href="/data-room">Investor Relations</a></li>',
        f'<li><a href="{FORM_4ORM}" target="_blank" rel="noopener">4orm Finance investor relations</a></li>',
    ),
    (
        '<li><a href="/data-room">Data Room</a></li>',
        f'<li><a href="{FORM_4ORM}" target="_blank" rel="noopener">4orm Finance data room</a></li>',
    ),
    (
        '<li><a href="/data-room" class="nav-cta">Access Data Room</a></li>',
        f'<li><a href="{FORM_4ORM}" class="nav-cta" target="_blank" rel="noopener">4orm Finance data room</a></li>',
    ),
]

PARTNERS_REPLACEMENTS = [
    (
        "KCS Capital is building Canada's institution-grade real-world asset exchange and digital settlement network through 4orm Finance. We work with a select group of capital partners, banks, family offices, accredited investors, and strategic companies, who want to be early to regulated digital asset infrastructure built for the Canadian market.",
        "KCS Capital develops the technology behind 4orm Finance. 4orm Finance operates the platform as a separately governed regulated entity. Qualified capital partners exploring early exposure to Canadian regulated digital asset infrastructure should review materials through 4orm Finance.",
    ),
    (
        "We are preparing our Seed financing.",
        "4orm Finance is preparing its pre-seed financing.",
    ),
    (
        '<a href="/contact" class="capital-cta">Register Interest &rarr;</a>',
        f'<a href="{FORM_4ORM}" class="capital-cta" target="_blank" rel="noopener">Access the 4orm Finance data room. &rarr;</a>',
    ),
    (
        "We are not raising on the open market. Any participation would be by private placement to qualified investors under the applicable prospectus exemptions, and begins with a confidential conversation, a review of the data room, and proper offering documentation. The Seed round is the entry point.",
        "KCS Capital does not solicit investors for the raise. Qualified parties may review 4orm Finance offering materials through the 4orm Finance data room. Any participation would be by private placement under applicable prospectus exemptions and only by means of definitive offering documentation from 4orm Finance.",
    ),
    (
        "Any securities offering by KCS Capital Inc. would be made solely",
        "Any securities offering by 4orm Finance would be made solely",
    ),
]


def apply_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if path.name == "partners.html":
        for old, new in PARTNERS_REPLACEMENTS:
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        if apply_file(path):
            changed.append(path.name)
    print(f"Updated {len(changed)} files:")
    for name in changed:
        print(f"  {name}")


if __name__ == "__main__":
    main()
