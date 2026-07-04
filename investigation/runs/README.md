# Investigation Runs

This directory defines the layout for recorded investigation runs. Scanner runners (for example the parallax reference runner) write this same structure in their own repositories; runs checked in here are shared evidence or worked examples.

Suggested layout:

```text
investigation/runs/<scan-id>/<job-id>/
  prompt.md
  result.json
  finding.md
  notes.md
  artifacts/
```

Runner outputs are evidence. They should preserve what was inspected, what was inferred, what changed in the risk map, and what would change the assessment again.

Do not put large generated decompiler output in the main repo unless it is intentionally part of a fixture or public demo. For normal work, keep bulky artifacts local or ignored.

Checked-in worked examples live under [`examples/`](examples/). Keep them small
and curated: source fixture, prompt, compact result, and a written finding.
