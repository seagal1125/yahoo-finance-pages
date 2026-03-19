# Yahoo Finance Digest Runbook

Repository path: `/Users/minim4/.openclaw/workspace/yahoo-finance-pages`

## Goal
For each scheduled run:

1. Read shared configuration:
   - Sources: `config/digest_sources.yaml`
   - Behavior/format rules: `config/digest_behavior.md`
2. Fetch and summarize all configured sources in **Traditional Chinese**.
3. Produce a complete HTML digest under `digests/`.
4. Update `index.html` so it links to the newest digest first and keeps a history list.
5. Commit and push the changes to `main`.

## Output naming
Use: `digests/YYYY-MM-DD-HHMM.html` (Asia/Taipei time)

## Digest structure
- Title with timestamp
- Short executive summary
- Section for finance.yahoo.com
- Section for tw.stock.yahoo.com
- Cross-market takeaways
- Risk watch / things to monitor
- Source links
- At the bottom of the HTML, record which model was used to generate it.

## HTML layout requirements
- Use the visual direction of `digests/2026-03-19-1350-compare.html` as the default house style for future digest pages.
- Visual style must feel stylish, modern, and clean rather than plain default document styling.
- Prioritize readability: clear information hierarchy, strong section headings, good spacing, easy scanning, and mobile-friendly layout.
- Prefer a polished hero section, compact summary cards near the top, card-based content sections, a visually distinct risk box, and chip-style source links when appropriate.
- Keep the writing easy for readers to understand at a glance; avoid cluttered blocks and confusing visual density.
- Content must remain complete: do not omit important facts, reasoning, market context, risks, or source-backed details just to make the page shorter.
- When simplifying presentation, simplify wording and layout only — never cut essential information.

## Index rules
- Show newest digest as a highlighted card near the top
- History section should list all digest files, newest first

## Git rules
Use a commit message like:
`feat: add yahoo finance digest for YYYY-MM-DD HH:MM CST`
