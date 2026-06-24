#!/usr/bin/env python3
"""Apply audit 5B items 7-9: disclaimer, 4orm estimate labels, dash/AI sweep."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LEGAL_BLOCK = """<div class="foot-reg foot-legal-block">
<p><strong>KCS Capital.</strong> KCS Capital is an independent technology and research firm, not a registered dealer or adviser. Any securities offering referenced is made by 4orm Finance under prospectus exemptions to accredited investors only (NI 45-106). Nothing on this site is an offer or solicitation. 4orm Finance operates as a separate regulated entity with independent governance, structured as HoldCo / OpCo / CustodyCo per the CIRO Digital Asset Custody Framework.</p>
<p><em>Accredited investors only.</em> The securities referenced on this website are being offered only to &ldquo;accredited investors&rdquo; as defined in National Instrument 45-106. This is not an offer to sell or a solicitation of an offer to buy securities in any jurisdiction where such offer is not permitted. No securities regulatory authority has assessed the merits of any securities described on this website.</p>
<p><em>Forward-looking statements.</em> This website contains forward-looking statements within the meaning of applicable Canadian securities laws, including statements about 4orm Finance&rsquo;s planned operations, regulatory pathway, market opportunity, partnership pipeline, and capital raise. Forward-looking statements are based on assumptions current as of the date stated and are subject to material risks and uncertainties, including the receipt of required regulatory approvals. Actual results may differ materially. KCS Capital and 4orm Finance disclaim any obligation to update forward-looking statements except as required by law.</p>
<p><em>No affiliation or endorsement.</em> References to third-party companies, products, and services are for market-context and educational purposes only and do not imply any partnership, endorsement, sponsorship, or affiliation. All third-party names, trademarks, and logos are the property of their respective owners. KCS Capital and 4orm Finance are not affiliated with the Bank of Canada, OSFI, the CSA (or its member regulators including OSC, AMF, BCSC, ASC), CIRO, FINTRAC, or any other regulator. No regulator has reviewed, endorsed, or approved KCS Capital, 4orm Finance, its planned platform, or any securities described on this website. KCS Capital and 4orm Finance are informed by, but not participants in, the Bank of Canada&rsquo;s Project Samara experiment (Staff Analytical Paper 2026-8) and the CSA Project Tokenization initiative.</p>
<p>Market statistics are sourced from McKinsey, BCG, PwC, KPMG, Bank of Canada, rwa.xyz, DefiLlama, and the 4orm Master Pro Forma where noted. Dollar ranges labeled as 4orm estimates are internal projections, not market facts.</p>
</div>"""

LEGAL_BLOCK_REGULATOR = LEGAL_BLOCK.replace(
    "</div>",
    "<p>Regulatory summaries on this page are KCS Capital commentary, not the official position of any regulator. Nothing on this page constitutes legal advice.</p>\n</div>",
    1,
)

OLD_FOOT_REG = (
    '<div class="foot-reg">KCS Capital Inc. is an independent technology and research firm. '
    "4orm Finance operates as a separate regulated entity with independent governance, "
    "structured as HoldCo / OpCo / CustodyCo per the CIRO Digital Asset Custody Framework. "
    "This website does not constitute an offer or solicitation to buy or sell securities. "
    "Market statistics sourced from McKinsey, BCG, PwC, KPMG, Bank of Canada, and the 4orm Master Pro Forma.</div>"
)

OLD_FOOT_REG_REGULATOR = (
    '<div class="foot-reg">KCS Capital Inc. is an independent technology and research firm. '
    "4orm Finance operates as a separate regulated entity with independent governance, "
    "structured as HoldCo / OpCo / CustodyCo per the CIRO Digital Asset Custody Framework. "
    "This website does not constitute an offer or solicitation to buy or sell securities, nor does it constitute legal advice. "
    "Regulatory summaries are KCS Capital commentary, not the official position of any regulator. "
    "Market statistics sourced from McKinsey, BCG, PwC, KPMG, Bank of Canada, and the 4orm Master Pro Forma.</div>"
)

DISCLAIMER_PAGES = {
    "index.html": LEGAL_BLOCK,
    "data-room.html": LEGAL_BLOCK,
    "solutions.html": LEGAL_BLOCK,
    "research.html": LEGAL_BLOCK,
    "briefs.html": LEGAL_BLOCK,
    "regulator.html": LEGAL_BLOCK_REGULATOR,
    "contact.html": LEGAL_BLOCK,
}

ESTIMATE_REPLACEMENTS = [
    (r"\$350M to \$1\.9B(?!\s*\(4orm estimate\))", "$350M to $1.9B (4orm estimate)"),
    (r"\$1\.33B to \$8\.3B(?!\s*\(4orm estimate\))", "$1.33B to $8.3B (4orm estimate)"),
    (r"C\$350M to C\$1\.9B(?!\s*\(4orm estimate\))", "C$350M to C$1.9B (4orm estimate)"),
    (r"<td><strong>C\$1\.33B</strong></td><td><strong>C\$8\.3B</strong></td>",
     "<td><strong>C$1.33B (4orm est.)</strong></td><td><strong>C$8.3B (4orm est.)</strong></td>"),
]

AI_REPLACEMENTS = [
    ("Can AI outgrow the debt trap?", "Can automation outgrow the debt trap?"),
    ("Can AI Outgrow the Debt Trap?", "Can Automation Outgrow the Debt Trap?"),
    ("AI &amp; THE DEBT TRAP", "AUTOMATION &amp; THE DEBT TRAP"),
    ("AI-driven productivity", "compute-driven productivity"),
    ("can AI-driven productivity", "compute-driven productivity"),
    ("Can AI, Compute Economies", "Automation, Compute Economies"),
    ("A hypothesis on whether AI-driven productivity", "A hypothesis on whether compute-driven productivity"),
    ("#2-ai-as-a-new-gdp-engine", "#2-compute-as-a-new-gdp-engine"),
    ("2 · AI as a new GDP engine", "2 · Compute as a new GDP engine"),
    ("#4-programmable-money-as-the-ai-economys-settlement-laye", "#4-programmable-money-as-the-automation-economys-settlement-laye"),
    ("4 · Programmable money as the AI economy", "4 · Programmable money as the automation economy"),
    ("Can AI outgrow the debt trap? <em>", "Can automation outgrow the debt trap? <em>"),
    ("driven by AI, compute-based", "driven by compute-based automation,"),
    ("what AI could change", "what compute-driven automation could change"),
    ("2 &middot; AI as a new GDP engine", "2 &middot; Compute as a new GDP engine"),
    ("AI changes the", "Compute-driven automation changes the"),
    ("AI introduces a new factor", "Automation introduces a new factor"),
    ("generative AI could add", "generative automation could add"),
    ("estimated AI could lift", "estimated automation could lift"),
    ("once AI is paired", "once automation is paired"),
    ("AI is already drafting", "Software is already drafting"),
    ("4 &middot; Programmable money as the AI economy's settlement layer", "4 &middot; Programmable money as the automation economy's settlement layer"),
    ("In an AI-driven economy", "In an automation-driven economy"),
    ("With AI-native risk engines", "With machine-native risk engines"),
    ("<li>AI sharply reduces", "<li>Automation sharply reduces"),
    ("<li>AI-assisted underwriting", "<li>Machine-assisted underwriting"),
    ("<li>AI productivity gains", "<li>Automation productivity gains"),
    ("<li>AI's benefits must", "<li>Automation's benefits must"),
    ("AI introduces a potential fifth path", "Automation introduces a potential fifth path"),
    ("settlement layer of AI economies", "settlement layer of automation economies"),
    ("Generative AI's potential economic contribution", "Generative automation's potential economic contribution"),
    ('"The economic potential of generative AI."', '"The economic potential of generative automation."'),
    ("AI and productivity growth estimates", "Automation and productivity growth estimates"),
    ("Applied AI & Systems Architect", "Applied Machine Intelligence & Systems Architect"),
]


def sweep_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    orig = text

    for pat, repl in ESTIMATE_REPLACEMENTS:
        text = re.sub(pat, repl, text)

    text = text.replace("\u2014", "-").replace("\u2013", "-")

    if path.name in DISCLAIMER_PAGES:
        if path.name == "regulator.html":
            text = text.replace(OLD_FOOT_REG_REGULATOR, DISCLAIMER_PAGES[path.name])
        else:
            text = text.replace(OLD_FOOT_REG, DISCLAIMER_PAGES[path.name])

    if path.suffix == ".html":
        for old, new in AI_REPLACEMENTS:
            text = text.replace(old, new)
        # Remove any remaining standalone AI word (word boundary)
        text = re.sub(r"\bAI\b", "automation", text)
        text = re.sub(r"\bAI's\b", "automation's", text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"updated: {path.relative_to(ROOT)}")


def main() -> None:
    exts = {".html", ".css", ".svg", ".md"}
    for path in ROOT.rglob("*"):
        if path.suffix in exts and "scripts" not in path.parts:
            sweep_file(path)

    # Fix double (4orm estimate) if script ran twice
    for path in ROOT.rglob("*.html"):
        t = path.read_text(encoding="utf-8")
        fixed = t.replace("(4orm estimate) (4orm estimate)", "(4orm estimate)")
        fixed = fixed.replace("(4orm est.) (4orm estimate)", "(4orm est.)")
        if fixed != t:
            path.write_text(fixed, encoding="utf-8")


if __name__ == "__main__":
    main()
