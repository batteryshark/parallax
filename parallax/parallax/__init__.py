"""parallax — the pure code-understanding SDK.

Vocabulary + matching, nothing else. This package defines the taxonomy
(atoms, lenses), the signature-pack schema and its validator, and the pure
callee-matching logic. It parses no code, spawns no subprocess, imports no
tree-sitter and no parser. Skills that reason about code depend on *this*;
they do the parsing and emit atoms/signatures conforming to the schema here.
"""

from __future__ import annotations

from .atoms import Atom, load_atoms
from .lenses import Lens, list_lenses, load_lens
from .model import Observation, confidence_label
from .paths import taxonomy_root
from .signatures import (
    ObservationGate,
    SignaturePack,
    SignaturePackError,
    SignatureRule,
    load_signature_pack,
    resolve_source_callee_pack,
)
from .validators import validate_signature_pack

__version__ = "0.1.0"

__all__ = [
    "Atom",
    "SignaturePack",
    "SignatureRule",
    "ObservationGate",
    "SignaturePackError",
    "Observation",
    "confidence_label",
    "Lens",
    "load_signature_pack",
    "resolve_source_callee_pack",
    "load_atoms",
    "load_lens",
    "list_lenses",
    "validate_signature_pack",
    "taxonomy_root",
    "__version__",
]
