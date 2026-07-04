# {CATEGORY.SUBTYPE}: {Human-Readable Name}

## Description

{One to three sentences describing what this behavior IS, mechanically. No judgment, no severity, no "commonly used for malicious purposes." Just: what does this code do?}

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | {Yes/No/Partial} | {What it looks like in source code} |
| Static Binary | {Yes/No/Partial} | {What it looks like in compiled artifacts} |
| Runtime/Dynamic | {Yes/No/Partial} | {What it looks like during execution} |

## Disambiguation

{How to distinguish this atom from similar atoms. Focus on STRUCTURAL differences, what makes this behavior different from adjacent behaviors. Not "this is more suspicious than X", that's a lens judgment.}

- **vs {SIMILAR.ATOM}**: {Structural distinction}

## Structural Relationships

{Observed co-occurrence patterns and structural dependencies. These are FACTUAL observations about how behaviors relate, not interpretive claims about what those relationships mean.}

- **Often co-occurs with**: {atoms that frequently appear alongside this one}
- **May imply**: {atoms that are structurally necessary for this one to function}
- **Commonly part of idioms**: {named idioms this atom participates in}

## Notes

{Any additional context that helps a practitioner recognize and correctly classify this behavior. Keep judgment-free.}
