# Parallax

<img src="assets/mark.png" alt="Parallax logo" width="84">

Parallax is a tool-independent vocabulary and Python SDK for reasoning about what code can do. It separates mechanical observations, such as invoking a shell, from interpretations about maliciousness, trust decisions or operational risk. Multiple lenses can interpret the same facts while keeping severity separate from confidence and stating what would disprove a finding.

## Requirements

The taxonomy is Markdown and JSON/TOML data, readable without installing anything. The optional SDK requires Python 3.11+ and has no runtime dependencies. It matches already-extracted observations; it does not parse or scan source code itself.

## Install

```sh
git clone https://github.com/batteryshark/parallax.git
cd parallax
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ./parallax
```

Keep the taxonomy checkout available: the SDK reads its vocabulary and signature packs from it.

## Quick start

```python
import parallax

atoms = parallax.load_atoms()
pack = parallax.load_signature_pack(parallax.resolve_source_callee_pack())
print(pack.classify_callee("child_process.exec", "javascript"))
print(parallax.list_lenses())
```

An atom records behavior, not intent. Apply a lens only after recording the observation and its limitations. Capability is not accusation, and no findings does not mean a system is safe.

## Configuration and key operations

- `PRLX_TAXONOMY_ROOT` selects the taxonomy root containing `signatures/schema.json`.
- `PRLX_SOURCE_CALLEE_PACK` selects an explicit callee signature pack.
- `load_atoms()`, `load_lens()` and `list_lenses()` load the vocabulary and interpretations.
- `validate_signature_pack(data)` returns validation errors for a pack.
- `scripts/build-signature-json` regenerates JSON mirrors from the TOML packs.

## Documentation

Start with the [documentation index](docs/README.md), [SDK reference](parallax/README.md) and [architecture](ARCHITECTURE.md). The repository includes curated synthetic investigation examples; they are product examples, not results from your own code.

## License

[Apache-2.0](LICENSE). See [NOTICE](NOTICE).
