"""Lenses: interpretive frames over the judgment-free ontology.

A lens asks one question of the same atoms ("is this malicious?" for mcd,
"what's the blast radius?" for capability, ...). Each lens is a directory under
``lenses/<id>/`` with a ``README.md`` and, depending on maturity, component
files or subdirectories: ``indicators``, ``compositions``, ``response`` tiers,
``signals``, ``verification``.

These are *data models*, not execution. ``load_lens`` reads a lens's README
(title + core question + intro) and enumerates its components as file listings.
Actually applying a lens to observations is a skill/product concern, not the
pure SDK's. Pure stdlib markdown parsing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Optional

from .paths import taxonomy_root

# The "core question" appears in one of two authored forms:
#   *"..."*
#   > **Core question:** *...*
_QUESTION_QUOTE_RE = re.compile(r'^\*"(.+?)"\*\s*$')
_QUESTION_CORE_RE = re.compile(r'^>\s*\*\*Core question:\*\*\s*\*(.+?)\*\s*$')

# Component subdirectories/files a lens may carry.
_COMPONENT_KINDS = (
    "indicators",
    "compositions",
    "response",
    "signals",
    "verification",
    "confidence",
)


@dataclass
class Lens:
    id: str
    title: str
    question: str
    description: str
    path: Path
    # component kind -> sorted list of member stems (file names without .md)
    components: dict[str, list[str]] = field(default_factory=dict)

    def has(self, kind: str) -> bool:
        return bool(self.components.get(kind))


def _parse_readme(text: str) -> tuple[str, str, str]:
    """Return ``(title, question, description)`` from a lens README body."""
    lines = text.splitlines()
    title = ""
    question = ""
    desc_lines: list[str] = []
    for line in lines:
        if not title:
            m = re.match(r"^#\s+(.+?)\s*$", line)
            if m:
                title = m.group(1).strip()
                continue
        if not question:
            mq = _QUESTION_QUOTE_RE.match(line.strip()) or _QUESTION_CORE_RE.match(line.strip())
            if mq:
                question = mq.group(1).strip()
                continue
        # First real paragraph after the question is the description.
        if title and line.strip() and not line.startswith("#") and not line.startswith(">"):
            desc_lines.append(line.strip())
            # Stop the description at the first blank line / next heading.
            break
    return title, question, "\n".join(desc_lines).strip()


def _collect_components(lens_dir: Path) -> dict[str, list[str]]:
    """Enumerate a lens's component members (subdir files or flat ``kind.md``)."""
    components: dict[str, list[str]] = {}
    for kind in _COMPONENT_KINDS:
        sub = lens_dir / kind
        if sub.is_dir():
            members = sorted(
                p.stem for p in sub.glob("*.md") if p.stem.upper() != "README"
            )
            if members:
                components[kind] = members
            continue
        flat = lens_dir / f"{kind}.md"
        if flat.is_file():
            components[kind] = [kind]
    return components


def lenses_dir(root: Optional[Path] = None) -> Optional[Path]:
    root = root or taxonomy_root()
    if root is None:
        return None
    d = root / "lenses"
    return d if d.is_dir() else None


def list_lenses(root: Optional[Path] = None) -> list[str]:
    """Return the sorted ids of all lenses (directories with a ``README.md``)."""
    d = lenses_dir(root)
    if d is None:
        return []
    return sorted(
        p.name for p in d.iterdir() if p.is_dir() and (p / "README.md").is_file()
    )


def load_lens(lens_id: str, root: Optional[Path] = None) -> Optional[Lens]:
    """Load a single lens by id, or ``None`` if it does not exist."""
    d = lenses_dir(root)
    if d is None:
        return None
    lens_dir = d / lens_id
    readme = lens_dir / "README.md"
    if not readme.is_file():
        return None
    title, question, description = _parse_readme(readme.read_text(encoding="utf-8"))
    return Lens(
        id=lens_id,
        title=title,
        question=question,
        description=description,
        path=lens_dir,
        components=_collect_components(lens_dir),
    )
