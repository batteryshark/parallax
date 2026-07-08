# Signature Packs

Signature packs are the machine-readable part of the taxonomy that maps stable
code surfaces to ontology atoms. They let scanner implementations share durable
detection knowledge without moving parser mechanics, tree-sitter traversal,
dataflow, or performance glue into this repository.

The format is described by [`schema.json`](schema.json). Packs may be stored as
YAML or JSON; YAML is preferred for review because the content is mostly tables.

## Ownership Boundary

Taxonomy owns:

- stable mappings from observed code surfaces to ontology atoms
- language selectors and match intent
- confidence baselines for direct observation
- concise evidence summaries
- context gates that describe when a broad signature is ambiguous
- per-signature caps that prevent noisy content signatures from flooding a file
- pack-level observation gates for stable post-match ambiguity rules

Engines own:

- parser selection and AST traversal
- callee extraction and normalization
- import/module discovery
- regex fallback strategy
- byte, line, and snippet location handling
- dataflow, reachability, and deduplication
- binary string/import extraction
- generated matcher performance

A signature says "this surface should emit this atom when observed." It does not
say how to walk a grammar or how to optimize a scanner.

## Pack Shape

```yaml
schema_version: parallax-signature-pack/v1
id: parallax.core-surfaces
name: Core source and content surfaces
version: 0.1.0
status: draft
signatures:
  - id: sig.exec.shell.universal.system
    atom: EXEC.SHELL
    surface: callee
    method: static-source
    languages: ["c", "cpp", "php", "ruby", "shell", "r"]
    match:
      mode: base
      values: ["system", "popen", "shell_exec", "passthru"]
    confidence: 0.78
    summary: shell command execution
```

## Surfaces

### `callee`

Use `surface: callee` when an engine has extracted a call target from source.
The engine decides how to extract the callee. The taxonomy only describes how a
normalized callee string should map to an atom.

Supported match modes:

| Mode | Meaning |
|---|---|
| `exact` | Full normalized callee must equal one value. |
| `base` | Final path/member segment must equal one value. |
| `suffix` | Full normalized callee must end with one value. |
| `exact_or_suffix` | Full normalized callee must equal a value or end with `.` plus a value. |
| `substring` | Full normalized callee must contain one value. |
| `regex` | Full normalized callee is matched with regex values. |

### `content`

Use `surface: content` when the signature matches raw file text or extracted
strings. Content signatures use `regex` and should usually set `cap_per_file`.
They are broad by nature, so their summaries should name the artifact plainly
and avoid lens language such as "malicious" or "suspicious."

## Language Selectors

`languages` is a list of engine language identifiers, with `"*"` meaning all
languages or language-unknown content. Engines may map their local names into
these identifiers, but packs should use stable public names such as
`javascript`, `typescript`, `python`, `go`, `rust`, `java`, `c`, `cpp`, `shell`,
or `powershell`.

## Context Gates

Some signatures are intentionally broad but ambiguous without nearby evidence.
Use `requires_context` for those cases.

```yaml
requires_context:
  scope: file
  any_text: ["child_process"]
  on_missing: drop
```

`on_missing` is an instruction to the engine when the gate is not satisfied:

| Action | Meaning |
|---|---|
| `drop` | Do not emit the observation. |
| `downweight` | Emit with `confidence * downweight_multiplier`. |
| `tag` | Emit at the original confidence but add a context-missing note. |

Context gates describe stable ambiguity, not parser mechanics. For example,
"`exec` in JavaScript means shell execution only with child-process evidence" is
taxonomy knowledge; "how to parse an ES module import" is engine knowledge.

Gates can live on a single signature with `requires_context`, or at pack level
with `observation_gates` when the ambiguity applies to every observation with a
given atom and language.

## Consumption Order

When multiple callee signatures match, engines should prefer higher
`priority` values, then pack order. Language-specific signatures should normally
use a higher priority than broad universal signatures. Engines may still add
local deduplication and confidence adjustment, but should not reinterpret the
atom mapping itself.

## Worked Examples

See [`examples/core-surfaces.yaml`](examples/core-surfaces.yaml) for:

- a plain callee signature
- a gated callee signature
- a content regex signature

## Engine Post-Filters

Three engine-level post-filters suppress common false-positive shapes that the
signature packs alone cannot distinguish. These are not signature changes (the
atoms are correct — the evidence is just ambiguous), so they are documented here
as engine contract:

1. **JS `.exec` gate (EXEC.SHELL).** The bare callee `exec` / `execSync` in
   JavaScript/TypeScript is ambiguous between `child_process.exec` (shell
   execution) and `RegExp.prototype.exec` (regex matching — the most common
   method call in any JS codebase). The pack-level context gate
   (`gate.exec.shell.javascript.child-process`, `requires_context: any_text:
   ["child_process"], on_missing: drop`) instructs the engine to drop the
   ambiguous callee when the file has no `child_process` import. The unmask
   engine enforces this in `scanner/observe/callee.py`. Explicitly-qualified
   callees (`child_process.exec`, `cp.exec`) are never gated.

2. **CRED blocklist suppression (CRED.\*).** Credential filenames (`id_rsa`,
   `.npmrc`) that appear inside a `new Set(["id_rsa", ...])` exclusion-set
   literal are a **protection pattern** (the app excludes sensitive files from
   indexing), not a credential read. Matching them as CRED is a semantic
   inversion. The unmask engine suppresses CRED matches inside `Set([...])` /
   assignment-array contexts in `scanner/observe/content.py`.

3. **Language-grammar file skip.** TextMate/VS Code language grammar definition
   files (`bat-*.js`, `shell-syntax.js`) contain command names (`ipconfig`,
   `nslookup`, `runas`, `net localgroup`) as syntax-highlighting data, not
   executable code. These files are detected by filename pattern + content
   density of grammar keys (`match:`, `begin:`, `end:`, `captures:`,
   `patterns:`) and skipped entirely by the content observer.

## Packs

See [`packs/source-callees.yaml`](packs/source-callees.yaml) for the first
extracted callee pack from the Parallax reference engine.
