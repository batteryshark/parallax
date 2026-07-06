# parallax (the SDK)

The **pure** parallax code-understanding SDK. It is the machine-readable face of
the taxonomy in this repo: the atom vocabulary, the lens frames, the
signature-pack schema, and the pure callee-matching logic.

**What it is:** vocabulary + matching.
**What it is not:** tooling. There is **no tree-sitter, no parser, no
subprocess, no heavy dependency** here — by design. Parsing source and
extracting callees is a *skill's* job; that skill emits atoms/signatures
conforming to the schema this SDK defines, and depends on this SDK. The library
never parses code.

- Pure Python standard library. Zero runtime dependencies.
- `requires-python >= 3.11`.

## Install (editable, from the repo root)

```sh
uv venv
uv pip install -e ./parallax
```

## Public API

```python
import parallax

# Atoms — the judgment-free behavior vocabulary (ontology/atoms/**).
atoms = parallax.load_atoms()          # {"EXEC.SHELL": Atom, "NETW.HTTP": Atom, ...}

# Signatures — map an already-extracted callee string to an atom.
pack = parallax.load_signature_pack(parallax.resolve_source_callee_pack())
pack.classify_callee("child_process.exec", "javascript")
# -> ("EXEC.SHELL", 0.85, "shell command execution")

# Lenses — interpretive frames over the same atoms (lenses/<id>/).
parallax.list_lenses()                 # [... "mcd" ...]
lens = parallax.load_lens("mcd")       # Lens(id, title, question, components, ...)

# Validation — check a pack against signatures/schema.json (hand-rolled, no jsonschema).
errors = parallax.validate_signature_pack(pack_data)   # [] means valid

# Data model for a single matched behavior.
parallax.Observation(...)
```

Exports: `Atom`, `SignaturePack`, `SignatureRule`, `ObservationGate`,
`Observation`, `Lens`, `load_signature_pack`, `resolve_source_callee_pack`,
`load_atoms`, `load_lens`, `list_lenses`, `validate_signature_pack`,
`taxonomy_root`.

## Where the data comes from

The SDK ships inside the taxonomy repo and reads its data directly:

| API | Reads |
|---|---|
| `load_atoms()` | `ontology/atoms/**/*.md` |
| `load_signature_pack()` / `resolve_source_callee_pack()` | `signatures/packs/source-callees.json` |
| `validate_signature_pack()` | constraints from `signatures/schema.json` |
| `load_lens()` / `list_lenses()` | `lenses/<id>/` |

`taxonomy_root()` resolves the repo root (marker: `signatures/schema.json`).
Pin it with `PRLX_TAXONOMY_ROOT`; pin an explicit callee pack with
`PRLX_SOURCE_CALLEE_PACK`.
