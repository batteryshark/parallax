"""Atoms: the ontology vocabulary of observable software behaviors.

An atom is the smallest judgment-free unit of description (``EXEC.SHELL``,
``NETW.HTTP``, ...). Each is authored as a markdown file under
``ontology/atoms/<CATEGORY>/<NAME>.md`` with a fixed five-section shape:

    # CAT.NAME: Human Title
    ## Description
    ## Detection Surface
    ## Disambiguation
    ## Structural Relationships
    ## Notes

``load_atoms()`` reads those files into ``Atom`` records. Pure stdlib markdown
parsing: split on the ``## `` headers, keep section bodies as text. No markdown
library, no parser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Optional

from .paths import taxonomy_root

# ``# CAT.NAME: Title`` — id must match the schema's atom pattern.
_H1_RE = re.compile(r"^#\s+([A-Z][A-Z0-9]*\.[A-Z][A-Z0-9_]*)\s*:\s*(.+?)\s*$")


@dataclass
class Atom:
    id: str
    category: str
    name: str
    title: str
    description: str
    detection_surfaces: str
    disambiguation: str
    relationships: list[str]
    notes: str
    path: Optional[Path] = None
    sections: dict[str, str] = field(default_factory=dict)


def _split_sections(body: str) -> dict[str, str]:
    """Split a markdown body into ``{h2_title: section_text}``."""
    sections: dict[str, str] = {}
    current: Optional[str] = None
    buf: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def _relationship_bullets(text: str) -> list[str]:
    """Pull the top-level ``- `` bullets out of a section as clean strings."""
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            out.append(stripped[2:].strip())
    return out


def parse_atom(text: str, path: Optional[Path] = None) -> Optional[Atom]:
    """Parse one atom markdown document. Returns ``None`` if it has no atom H1."""
    lines = text.splitlines()
    header = None
    header_idx = 0
    for i, line in enumerate(lines):
        m = _H1_RE.match(line)
        if m:
            header = m
            header_idx = i
            break
    if header is None:
        return None

    atom_id = header.group(1)
    title = header.group(2).strip()
    category, _, name = atom_id.partition(".")

    body = "\n".join(lines[header_idx + 1 :])
    sections = _split_sections(body)

    return Atom(
        id=atom_id,
        category=category,
        name=name,
        title=title,
        description=sections.get("Description", ""),
        detection_surfaces=sections.get("Detection Surface", ""),
        disambiguation=sections.get("Disambiguation", ""),
        relationships=_relationship_bullets(sections.get("Structural Relationships", "")),
        notes=sections.get("Notes", ""),
        path=path,
        sections=sections,
    )


def atoms_dir(root: Optional[Path] = None) -> Optional[Path]:
    root = root or taxonomy_root()
    if root is None:
        return None
    d = root / "ontology" / "atoms"
    return d if d.is_dir() else None


def load_atoms(root: Optional[Path] = None) -> dict[str, Atom]:
    """Load every atom under ``ontology/atoms/**`` into ``{atom_id: Atom}``.

    ``root`` overrides taxonomy-root resolution. Returns an empty dict if the
    ontology directory cannot be found.
    """
    d = atoms_dir(root)
    if d is None:
        return {}
    out: dict[str, Atom] = {}
    for md in sorted(d.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        atom = parse_atom(text, path=md)
        if atom is not None:
            out[atom.id] = atom
    return out
