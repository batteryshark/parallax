# Signature Packs

This directory contains reviewable signature-pack data for scanner engines.

## `source-callees.yaml`

The first pack extracts the durable callee classification tables from the
Parallax reference engine:

- `_UNIVERSAL_RULES`
- `_LANG_RULES`
- `_IMPORT_GATES`

It intentionally does not include AST traversal, call-node selection,
tree-sitter grammar names, regex fallback behavior, or location handling. Those
remain engine responsibilities.

`source-callees.json` is the same pack serialized as JSON for dependency-light
runtime loaders. Edit/review the YAML form first, then regenerate the JSON
mirror:

```sh
scripts/build-signature-json
```

## Engine Consumption

An engine that consumes a callee pack should:

1. Extract a normalized callee string from source using its own parser or
   fallback strategy.
2. Select signatures whose `surface`, `method`, and `languages` match the
   candidate observation.
3. Apply `match.mode` to the normalized callee.
4. Prefer higher `priority` values, then pack order, when multiple signatures
   match the same callee.
5. Emit the signature's `atom`, `confidence`, and `summary`.
6. Apply `observation_gates` for the emitted atom and language. `drop` removes
   the observation; `downweight` multiplies confidence; `tag` preserves the
   observation and adds a context note.
7. Deduplicate observations and attach file/line/snippet provenance locally.

Engines may add local coverage notes such as "regex fallback" or "AST parser
unavailable", but those notes should not alter the taxonomy-owned mapping.
