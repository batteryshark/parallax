"""Locate the parallax taxonomy root (schema + ontology + lenses + packs).

The pure SDK ships *inside* the ``parallax-taxonomy`` repo, so the taxonomy
data (``signatures/schema.json``, ``ontology/atoms/**``, ``lenses/<id>/`` ...)
lives one directory up from this package. This module is the single place that
resolves that root; ``PRLX_TAXONOMY_ROOT`` pins it for downstream tools.

Pure stdlib. No parsers, no tooling.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

# A checkout is a taxonomy root iff this marker file exists under it.
_MARKER = os.path.join("signatures", "schema.json")


def _is_root(path: Path) -> bool:
    return (path / _MARKER).is_file()


def taxonomy_root(start: Optional[Path] = None) -> Optional[Path]:
    """Return the parallax-taxonomy repo root, or ``None`` if not found.

    Resolution order:
      1. ``PRLX_TAXONOMY_ROOT`` (if it points at a valid checkout).
      2. Walk upward from this file (the SDK lives inside the repo).
      3. Walk upward from ``start`` (if given) and from the cwd.
    """
    env = os.environ.get("PRLX_TAXONOMY_ROOT")
    if env:
        root = Path(env).expanduser().resolve()
        return root if _is_root(root) else None

    candidates = []
    if start is not None:
        candidates.append(Path(start).resolve())
    candidates.append(Path(__file__).resolve())
    candidates.append(Path.cwd().resolve())

    for c in candidates:
        for d in [c, *c.parents]:
            if _is_root(d):
                return d
    return None
