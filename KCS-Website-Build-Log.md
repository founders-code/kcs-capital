# KCS Capital Website - Build Log

A complete record of what was designed and built into the KCS Capital website, kept as a reference and recovery document.

_Last updated: May 15, 2026_

---

## 1. Site overview

A custom, hand-built static website for KCS Capital - no website-builder, no CMS. Pure HTML + one shared CSS file, designed to deploy on GitHub + Vercel.

**Tech / structure**
- Static HTML pages with a single shared stylesheet (`styles.css`).
- `vercel.json` configured with clean URLs (no `.html` in addresses) and redirects (e.g. old `/investors` → `/data-room`).
- Brand system: Cormorant Garamond (serif headlines), Syne (UI/labels), DM Sans (body). Gold (#C9882A) on near-black, with surface greys.
- Fully responsive, including a pure-CSS mobile hamburger menu (no JavaScript dependency).
- Subtle, performance-light animations (scroll reveals, hero word-reveal, video backgrounds).

**Pages built**
Home, About, Solutions, Team, Research, KCS Briefs (index + 14 article pages), Partners, Regulator, Contact, Data Room, Request Access (form), Careers, Privacy, Terms - plus an `/investors` redirect stub.

---

## 2. Home page

- **Hero section** with a Calgary skyline video background (slowed 10% for a calmer feel), a staged word-reveal headline - _"Where the future / of finance is built."_ - eyebrow label, supporting paragraph, and two call-to-action buttons.
- Hero copy reveal timing tuned repeatedly to the desired pace; each stage (eyebrow → headline lines → divider → sub-copy → buttons → logo) cascades in sequence.
- Large KCS logo fades into the open space beside the headline (sized down ~15% from its first version; hidden on smaller screens).
- HUD-style corner accents, coordinates, and floating market-reference labels for an "operations" feel.
- Animated gold-particle canvas overlay was added, then removed at your direction - the hero now relies on the video + lighting only.
- **Stats bar** - four headline market figures (tokenized RWA market, on-chain RWA value, Canadian TAM, Project Samara).
- **Who We Serve** - banks, custodians, credit unions, asset managers.
- **Team section** - six core people as cards, each with a "Read more" link to that person on the Team page.
- **Now Hiring section** - three senior technical roles (Applied Machine Intelligence & Systems Architect; CTO - blockchain exchange / tokenization; Lead Full-Stack Developer).
- **"A rising tide raises all ships"** quote band.
- **KCS Capital Research** - three featured research cards.
- **KCS Briefs** - three featured brief cards (added as a mirror of the Research section).
- **Closing CTA** section and full footer (firm info, sitemap, 4orm Finance links, three office addresses).

---

## 3. KCS Briefs - full archive migration

All **14 blog posts** from the old Wix site were migrated into "KCS Briefs."

- Each became a standalone, styled article page, plus a Briefs index page.
- Every post was **rewritten** to current KCS positioning - off-brand framing (e.g. a named consumer "stablecoin," a "DAO," personal investment advice) was reframed into compliant thought-leadership about regulated, verifiable infrastructure, while keeping the original imagination and thesis.
- Each brief was **expanded, not shortened**, and backed with supporting data, statistics, and linked sources (IIF, McKinsey, Goldman Sachs, StatCan, Bank of Canada, OSFI, FINTRAC, CSA, OECD, CFIB, etc.).
- Compliance disclaimers added throughout (not investment/legal/tax advice; KCS / 4orm entity separation).
- Briefs index laid out as wide, horizontal editorial cards (image + text), styled to feel like a real publication.

**The 14 briefs:** Unlocking Alberta's Wealth Through Tokenization · Separating Leverage From Livelihood (two-tier finance) · Governments Fail Because Their Financial Infrastructure Is Outdated · Can Automation Outgrow the Debt Trap? · The Market Opportunity: Where RWAs Actually Live · When IOUs Break · When "Trust Us" Fails · Emergency Money, Without the Wait (Fort McMurray) · Canada's New Budget Signals a Safer Path to Stable Finance · The Shift Has Begun · Plug Into the Future: Blockchain & Global Solar · When "Local" Means Keeping Profits at Home (Amazon vs Shopify) · Too Taxed to Grow · Equity, Debt & Bitcoin Reserves.

- Thumbnails: 13 supplied images matched by title, web-optimized, and placed. (Fort McMurray thumbnail still outstanding.)

---

## 4. Team page

- Nine team members as cards: Chad R. Johnston, Sam Mraiheen, Kevin Wong, Don H, Bruce Fair, Michael Stephens, Zahiruddin Sandeela (Zed), Angelo Aquino, Dean Hesse.
- Circular headshots with a gold border treatment; per-photo framing adjustments so heads read at a consistent size (with custom enlargements for Chad, Sam, and Kevin).
- "Read Full Bio" opens a full-screen modal with the extended biography; closes on outside click.
- LinkedIn profile links added for everyone except Dean.
- Card actions ("Read Full Bio" + LinkedIn) pinned to the bottom of each card so they align across a row.
- Anchor links (`/team#name`) so the homepage "Read more" links scroll to the right person.
- Kevin Wong's title updated from "Partner" to "Co-Founder" across the homepage, the team card, and his bio modal.
- Team page also has its own video hero (city buildings footage, converted from supplied stock).

---

## 5. Forms & data room flow

- **Request Access page** (`/request-access`) - an investor-qualification form with four multiple-choice questions (investor type, allocation range, decision timeline, area of interest) plus contact fields.
- Every "Access Data Room" button across the site routes to this form first.
- On submit, the visitor is taken to the **Data Room** page, which shows a confirmation banner: _"Request received. Someone from the KCS Capital team will be in touch shortly to give you access."_
- **Data Room page** - renamed from the old "Investors" page; themed gateway panel, a "What's Inside" document index, and a Google Drive folder link. (A note is left in the form file explaining how to connect a real form backend for automatic submission capture.)

---

## 6. Other pages

- **About** - hero copy corrected to current positioning (4orm Finance as Canada's institution-grade Real World Asset Exchange and digital settlement network); governance and "human-centered finance" lines kept; founder quote band.
- **Partners** - added a compliant "Capital Partners" section ($10M Seed round opening Oct 1; written to be securities-compliant). Partners page also has a video hero (city/bridge footage, slowed 20%).
- **Regulator page** - built from scratch: a regulatory-news section (CIRO, Stablecoin Act, CSA) and a resources/frameworks library (CIRO custody framework, CSA notices, NI 21-101/23-101, NI 31-103, PCMLTFA, RPAA, etc.). Placed after Partners in the navigation.
- **Contact** - four routed email addresses: compliance@ (regulatory), legal@, founders@ (partnerships), admin@ (general).
- **Careers** - the hiring page; nav button relabeled from "Investor Kit" to "Access Data Room."

---

## 7. Navigation & site-wide details

- Active-page indicator: a faint gold underline stays under the current page's menu item, site-wide.
- Mobile hamburger menu added (pure CSS).
- All "Access Data Room" / "Request Access" calls-to-action route through the questionnaire flow.
- Footer standardized across every page (firm description, entity-separation language, sitemap, 4orm Finance links, offices, legal/regulatory disclaimer).

---

## 8. Media & assets

- **Calgary hero video** - converted and compressed for web; playback slowed 10%.
- **Team page hero video** - supplied stock `.mov` converted to web-optimized MP4.
- **Partners page hero video** - supplied stock `.mov` converted to web-optimized MP4; playback slowed 20%.
- Poster (first-frame) images generated for each video for fast first paint.
- 13 KCS Briefs thumbnails matched to their articles, converted to optimized JPGs, and placed.
- 9 team headshots placed and framed.

---

## 9. Recovery notes

- The entire site is contained in this folder - every page is plain HTML, plus `styles.css`, `vercel.json`, the videos, the images, and this log.
- To restore or move the site, the whole folder can be re-uploaded to GitHub and redeployed on Vercel as-is.
- Numbered `KCS-Website` sub-folders in the working directory are historical save points from earlier in the build and are not part of the live site.
- Outstanding / optional items: Fort McMurray brief thumbnail; a curated Regulator-updates section; case-study pages.

---

_KCS Capital Inc. - independent technology and research firm. 4orm Finance operates as a separate regulated entity._
