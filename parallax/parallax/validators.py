"""Validate signature packs against ``signatures/schema.json``.

Hand-rolled, stdlib-only. We do not pull in ``jsonschema``: the pack format is
small and stable, so a focused validator covering its real constraints (the
ones the schema actually enforces) is enough and keeps the SDK dependency-free.

``validate_signature_pack(data)`` returns a list of human-readable error
strings; an empty list means the pack is valid.
"""

from __future__ import annotations

import re
from typing import Any

# Patterns mirror signatures/schema.json.
_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_ATOM_RE = re.compile(r"^[A-Z][A-Z0-9]*\.[A-Z][A-Z0-9_]*$")
_LANG_RE = re.compile(r"^(\*|[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*)$")
_SIG_ID_RE = re.compile(r"^sig\.[a-z0-9][a-z0-9_.-]*$")
_GATE_ID_RE = re.compile(r"^gate\.[a-z0-9][a-z0-9_.-]*$")

_STATUS = {"draft", "experimental", "stable", "deprecated"}
_SURFACE = {"callee", "content"}
_METHOD = {"static-source", "static-binary", "package-metadata"}
_MATCH_MODE = {"exact", "base", "suffix", "exact_or_suffix", "substring", "regex"}
_ON_MISSING = {"drop", "downweight", "tag"}


def _string_list_errors(value: Any, where: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{where}: must be a non-empty array of strings"]
    errs = []
    for i, v in enumerate(value):
        if not isinstance(v, str) or not v:
            errs.append(f"{where}[{i}]: must be a non-empty string")
    if len(set(value)) != len(value):
        errs.append(f"{where}: items must be unique")
    return errs


def _validate_match(match: Any, where: str) -> list[str]:
    if not isinstance(match, dict):
        return [f"{where}: match must be an object"]
    errs = []
    mode = match.get("mode")
    if mode not in _MATCH_MODE:
        errs.append(f"{where}.mode: {mode!r} not one of {sorted(_MATCH_MODE)}")
    if "values" not in match:
        errs.append(f"{where}: missing required key 'values'")
    else:
        errs += _string_list_errors(match["values"], f"{where}.values")
    if "case_sensitive" in match and not isinstance(match["case_sensitive"], bool):
        errs.append(f"{where}.case_sensitive: must be a boolean")
    return errs


def _validate_context_gate(ctx: Any, where: str) -> list[str]:
    if not isinstance(ctx, dict):
        return [f"{where}: requires_context must be an object"]
    errs = []
    on_missing = ctx.get("on_missing")
    if on_missing not in _ON_MISSING:
        errs.append(f"{where}.on_missing: {on_missing!r} not one of {sorted(_ON_MISSING)}")
    predicate_keys = (
        "all_text",
        "any_text",
        "none_text",
        "imports_any",
        "imports_all",
        "path_any",
        "path_none",
    )
    if not any(k in ctx for k in predicate_keys):
        errs.append(f"{where}: must specify at least one of {list(predicate_keys)}")
    if on_missing == "downweight" and "downweight_multiplier" not in ctx:
        errs.append(f"{where}: on_missing 'downweight' requires 'downweight_multiplier'")
    return errs


def _validate_signature(sig: Any, where: str) -> list[str]:
    if not isinstance(sig, dict):
        return [f"{where}: must be an object"]
    errs = []
    required = ("id", "atom", "surface", "method", "languages", "confidence", "summary")
    for key in required:
        if key not in sig:
            errs.append(f"{where}: missing required key {key!r}")

    if isinstance(sig.get("id"), str) and not _SIG_ID_RE.match(sig["id"]):
        errs.append(f"{where}.id: {sig['id']!r} must match sig.<slug>")
    if isinstance(sig.get("atom"), str) and not _ATOM_RE.match(sig["atom"]):
        errs.append(f"{where}.atom: {sig['atom']!r} is not a valid atom id")

    surface = sig.get("surface")
    if surface not in _SURFACE:
        errs.append(f"{where}.surface: {surface!r} not one of {sorted(_SURFACE)}")
    if sig.get("method") not in _METHOD:
        errs.append(f"{where}.method: {sig.get('method')!r} not one of {sorted(_METHOD)}")

    langs = sig.get("languages")
    errs += _string_list_errors(langs, f"{where}.languages")
    if isinstance(langs, list):
        for i, lang in enumerate(langs):
            if isinstance(lang, str) and not _LANG_RE.match(lang):
                errs.append(f"{where}.languages[{i}]: {lang!r} is not a valid language token")

    conf = sig.get("confidence")
    if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not (0 <= conf <= 1):
        errs.append(f"{where}.confidence: must be a number in [0, 1]")
    if not sig.get("summary"):
        errs.append(f"{where}.summary: must be a non-empty string")

    # surface-conditional: callee needs match (not regex); content needs regex (not match)
    if surface == "callee":
        if "match" not in sig:
            errs.append(f"{where}: surface 'callee' requires 'match'")
        else:
            errs += _validate_match(sig["match"], f"{where}.match")
        if "regex" in sig:
            errs.append(f"{where}: surface 'callee' must not carry 'regex'")
    elif surface == "content":
        if not sig.get("regex"):
            errs.append(f"{where}: surface 'content' requires a non-empty 'regex'")
        if "match" in sig:
            errs.append(f"{where}: surface 'content' must not carry 'match'")

    if "requires_context" in sig:
        errs += _validate_context_gate(sig["requires_context"], f"{where}.requires_context")
    return errs


def _validate_observation_gate(gate: Any, where: str) -> list[str]:
    if not isinstance(gate, dict):
        return [f"{where}: must be an object"]
    errs = []
    for key in ("id", "atom", "languages", "requires_context"):
        if key not in gate:
            errs.append(f"{where}: missing required key {key!r}")
    if isinstance(gate.get("id"), str) and not _GATE_ID_RE.match(gate["id"]):
        errs.append(f"{where}.id: {gate['id']!r} must match gate.<slug>")
    if isinstance(gate.get("atom"), str) and not _ATOM_RE.match(gate["atom"]):
        errs.append(f"{where}.atom: {gate['atom']!r} is not a valid atom id")
    if "languages" in gate:
        errs += _string_list_errors(gate["languages"], f"{where}.languages")
    if "requires_context" in gate:
        errs += _validate_context_gate(gate["requires_context"], f"{where}.requires_context")
    return errs


def validate_signature_pack(data: Any) -> list[str]:
    """Validate a signature-pack mapping. Returns a list of error strings
    (empty means valid). Does not raise on invalid input."""
    if not isinstance(data, dict):
        return ["pack: top-level document must be an object"]

    errs: list[str] = []
    for key in ("schema_version", "id", "name", "version", "status", "signatures"):
        if key not in data:
            errs.append(f"pack: missing required key {key!r}")

    if data.get("schema_version") != "parallax-signature-pack/v1":
        errs.append(
            f"pack.schema_version: {data.get('schema_version')!r} must be "
            "'parallax-signature-pack/v1'"
        )
    if isinstance(data.get("id"), str) and not _ID_RE.match(data["id"]):
        errs.append(f"pack.id: {data['id']!r} does not match the id pattern")
    if isinstance(data.get("name"), str) and not data["name"]:
        errs.append("pack.name: must be a non-empty string")
    if isinstance(data.get("version"), str) and not _VERSION_RE.match(data["version"]):
        errs.append(f"pack.version: {data['version']!r} must be semver-like")
    if data.get("status") not in _STATUS:
        errs.append(f"pack.status: {data.get('status')!r} not one of {sorted(_STATUS)}")

    sigs = data.get("signatures")
    if not isinstance(sigs, list) or not sigs:
        errs.append("pack.signatures: must be a non-empty array")
    else:
        for i, sig in enumerate(sigs):
            errs += _validate_signature(sig, f"signatures[{i}]")

    gates = data.get("observation_gates")
    if gates is not None:
        if not isinstance(gates, list):
            errs.append("pack.observation_gates: must be an array")
        else:
            for i, gate in enumerate(gates):
                errs += _validate_observation_gate(gate, f"observation_gates[{i}]")

    return errs
