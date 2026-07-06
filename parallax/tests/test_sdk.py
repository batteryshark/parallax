"""SDK smoke + behavior tests. Run from the taxonomy repo (or with
PRLX_TAXONOMY_ROOT set) so the real data resolves."""

from __future__ import annotations

import copy
import json

import parallax


def test_classify_callee_child_process_exec():
    pack_path = parallax.resolve_source_callee_pack()
    assert pack_path is not None, "could not resolve the real source-callees.json"
    pack = parallax.load_signature_pack(pack_path)

    result = pack.classify_callee("child_process.exec", "javascript")
    assert result is not None
    atom, confidence, summary = result
    assert atom == "EXEC.SHELL"
    assert 0 < confidence <= 1
    assert summary


def test_classify_callee_known_mappings():
    # These are the mappings the reference engine ships in the real pack.
    pack = parallax.load_signature_pack(parallax.resolve_source_callee_pack())
    assert pack.classify_callee("exec.Command", "go") == (
        "EXEC.PROC",
        0.82,
        "child process via os/exec",
    )
    assert pack.classify_callee("Net::HTTP.get", "ruby") == (
        "NETW.HTTP",
        0.72,
        "outbound HTTP request",
    )


def test_load_atoms_is_populated():
    atoms = parallax.load_atoms()
    assert atoms, "load_atoms() returned nothing"
    assert "EXEC.SHELL" in atoms
    assert "NETW.HTTP" in atoms

    shell = atoms["EXEC.SHELL"]
    assert shell.category == "EXEC"
    assert shell.name == "SHELL"
    assert shell.title  # human title from the H1
    assert shell.description  # the Description section is non-empty
    # Every atom should carry the five authored sections.
    assert set(shell.sections) >= {
        "Description",
        "Detection Surface",
        "Disambiguation",
        "Structural Relationships",
        "Notes",
    }
    assert shell.relationships  # bullets pulled from Structural Relationships


def test_validate_signature_pack_accepts_real_pack():
    pack_path = parallax.resolve_source_callee_pack()
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    errors = parallax.validate_signature_pack(data)
    assert errors == [], f"real pack should validate cleanly, got: {errors}"


def test_validate_signature_pack_rejects_broken_pack():
    # Missing required keys.
    assert parallax.validate_signature_pack({"schema_version": "parallax-signature-pack/v1"})

    # Structurally present but internally broken: bad atom + bad surface/match combo.
    pack_path = parallax.resolve_source_callee_pack()
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    broken = copy.deepcopy(data)
    broken["signatures"][0]["atom"] = "not-an-atom"
    broken["signatures"][0]["surface"] = "callee"
    broken["signatures"][0].pop("match", None)
    broken["signatures"][0]["regex"] = "oops"
    errors = parallax.validate_signature_pack(broken)
    assert errors, "broken pack should not validate"
    assert any("atom" in e for e in errors)


def test_lenses():
    lenses = parallax.list_lenses()
    assert "mcd" in lenses

    mcd = parallax.load_lens("mcd")
    assert mcd is not None
    assert mcd.id == "mcd"
    assert mcd.title
    assert mcd.question  # the *"Is this malicious?"* core question
    # mcd is the richest lens: it carries several component families.
    assert mcd.has("indicators")
    assert mcd.has("compositions")
    assert mcd.has("response")
    assert "EXEC" in mcd.components["indicators"]

    # An unknown lens resolves to None, not an error.
    assert parallax.load_lens("does-not-exist") is None


def test_imports_no_tooling():
    # The SDK source itself must import no parser / tree-sitter / subprocess.
    # We inspect the shipped module source (not sys.modules, which the test
    # runner pollutes with subprocess et al. before this test even runs).
    import pathlib
    import re

    pkg_dir = pathlib.Path(parallax.__file__).parent
    forbidden = ("tree_sitter", "tree-sitter", "subprocess", "yaml", "jsonschema")
    offenders = []
    for py in sorted(pkg_dir.glob("*.py")):
        src = py.read_text(encoding="utf-8")
        for line in src.splitlines():
            stripped = line.strip()
            if not (stripped.startswith("import ") or stripped.startswith("from ")):
                continue
            for token in forbidden:
                if re.search(rf"\b{re.escape(token)}\b", stripped):
                    offenders.append(f"{py.name}: {stripped}")
    assert not offenders, f"SDK imports forbidden tooling: {offenders}"
