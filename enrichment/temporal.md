# Temporal

Facts about timing: when accounts were active, when versions were published, and
how those times relate to each other and to the code. Sourced from registry and
version-control history and OSINT.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.TIME.DORMANCY` | Activity dormancy | A maintainer or project's activity timeline, including dormant stretches followed by bursts | VCS/registry history, OSINT |
| `ENR.TIME.COORDINATION` | Coordinated publication | Near-simultaneous publication across multiple packages or accounts | registry history, OSINT |
| `ENR.TIME.PRESTAGE` | Pre-staged version | A version published before any code or consumer references it | registry history |

Judgment-free: this records the timeline facts. Whether a dormant-then-burst
pattern or a pre-staged version is part of an attack is a lens call. The MCD
lens's weighting is in
[`../lenses/mcd/signals/temporal-signals.md`](../lenses/mcd/signals/temporal-signals.md).
