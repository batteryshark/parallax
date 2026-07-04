# Curiosity Lens

> **Core question:** *What's surprising here? What does this do that you wouldn't expect, given what it claims to be?*

The curiosity lens is the **discovery engine**. It is not asking "is this malicious?" (MCD) or "what's the blast radius?" (capability); it asks "*wait, it does THAT?*" It surfaces behavior that is unexpected, rare, or inconsistent with the project's stated purpose, and ranks by **interestingness, not severity.**

This lens exists because of a hard-won product truth: **finding flaws is not the hard part; getting people to care is.** Nobody reads a wall of alerts. Everybody reads "a tiny string-padding helper that phones home at install time." Surprise is the mechanism that makes people care, and it is the engine of adoption: people point Parallax at software they use, find something weird, and share it. That loop grows the tool, the corpus, and, for a practitioner, the portfolio.

## How it works

1. **Establish the stated purpose.** Read it from manifests (`package.json` / `pyproject.toml` / `mcp.json` description) and the README's first heading. "tiny string padding helper", "thin client for the exchangerate API", "docs-search MCP server".
2. **Infer expected capability categories** from that purpose (a "client/api" implies network; a "padding helper" implies nothing but computation).
3. **Score each observation by interestingness** = atom rarity + an inconsistency bonus when the behavior is *unexpected for the stated purpose*. The same `NETW.HTTP` is boring in an API client and **striking** in a padding helper.
4. **Rank and report**, most surprising first, with confidence and an explicit "what would make this unsurprising."

## Interestingness ≠ severity

A curiosity finding's `severity` is always `informational`. The signal is the **interestingness label** (`mild` / `notable` / `striking`) encoded in the finding title and ordering. A striking finding is not a verdict that something is wrong; it's an invitation to look. The follow-up is explicit: escalate to the MCD lens ("is it malicious?") or the capability lens ("what's the blast radius?").

See [indicators.md](indicators.md) for the rarity table and the purpose-inference keywords.

## Evidence-based, not clickbait

The discipline that separates this from sensationalism: every curiosity finding carries **confidence** and a **disproof criterion** ("the docs justify this as part of the package's real purpose"; "this is standard for this category of software"). The lens surfaces the surprising thing *and* tells you how to make it boring again. That honesty is the difference between a credible discovery and a dunk.

## Output

- Ranked `CUR-UNEXPECTED` / `CUR-NOTABLE` findings (`[striking]` / `[notable]` / `[mild]`).
- A `CUR-PROFILE` roll-up: "*N surprising behaviors for `<stated purpose>`*", the **shareable one-liner**, the seed of a future findings/content pipeline ("look what Parallax found in X").

## Relationship to the other lenses

Curiosity is a *router*, not a judge. It finds the interesting thing; the other lenses decide what it means. A striking curiosity finding on an install-time network call points at MCD (`BP-SUPPLY`) and capability (`CAP-INSTALL`). The curiosity lens is deliberately the front door: low friction, high "huh," with the rigorous lenses one hop away.
