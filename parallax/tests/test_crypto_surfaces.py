"""Crypto lifecycle mapping regressions; no live keys or crypto dependencies.

Run with pytest, or with stdlib unittest discovery. These tests exercise the
pack/SDK contract, not scanner-owned value flow or entropy assessment.
"""

from __future__ import annotations

import copy
import json
import re
import tomllib
import unittest

import parallax


class CryptoSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = parallax.taxonomy_root()
        cls.pack = parallax.load_signature_pack(parallax.resolve_source_callee_pack())

    def test_selected_material_is_loading_not_generation(self):
        cases = [
            ("ec.derive_private_key", "python"),
            ("cryptography.hazmat.primitives.asymmetric.ec.derive_private_key", "python"),
            ("serialization.load_pem_private_key", "python"),
            ("serialization.load_der_public_key", "python"),
            ("crypto.createSecretKey", "javascript"),
            ("crypto.createPrivateKey", "typescript"),
            ("crypto.createPublicKey", "tsx"),
            ("window.crypto.subtle.importKey", "javascript"),
            ("webcrypto.subtle.unwrapKey", "typescript"),
            ("PEM_read_bio_PrivateKey_ex", "c"),
            ("d2i_AutoPrivateKey", "cpp"),
        ]
        for callee, language in cases:
            with self.subTest(callee=callee, language=language):
                self.assertEqual(self.pack.classify_callee(callee, language)[0], "CRPT.KEYLOAD")

    def test_generation_and_randomness_remain_distinct(self):
        cases = [
            ("ec.generate_private_key", "python", "CRPT.KEYGEN"),
            ("crypto.generateKeyPairSync", "javascript", "CRPT.KEYGEN"),
            ("crypto.subtle.generateKey", "typescript", "CRPT.KEYGEN"),
            ("secrets.token_bytes", "python", "CRPT.RNG"),
            ("os.urandom", "python", "CRPT.RNG"),
            ("crypto.randomBytes", "javascript", "CRPT.RNG"),
            ("window.crypto.getRandomValues", "typescript", "CRPT.RNG"),
        ]
        for callee, language, atom in cases:
            with self.subTest(callee=callee):
                self.assertEqual(self.pack.classify_callee(callee, language)[0], atom)

    def test_validation_surface_does_not_claim_entropy_or_enforcement(self):
        for name in (
            "EVP_PKEY_check", "EVP_PKEY_param_check_quick",
            "EVP_PKEY_public_check", "EVP_PKEY_public_check_quick",
            "EVP_PKEY_private_check", "EVP_PKEY_pairwise_check",
        ):
            with self.subTest(name=name):
                atom, confidence, summary = self.pack.classify_callee(name, "c")
                self.assertEqual(atom, "CRPT.KEYCHECK")
                self.assertGreater(confidence, 0)
                self.assertNotRegex(summary, r"secure|entropy|enforced|approved")

    def test_unqualified_unrelated_and_wrong_language_calls_do_not_claim_crypto(self):
        # Aliases require engine binding resolution. Generic import/validation
        # names and general-purpose RNGs must not acquire crypto guarantees.
        cases = [
            ("derive_private_key", "python"),
            ("app.importKey", "javascript"),
            ("createSecretKey", "javascript"),
            ("validate", "python"),
            ("entropy", "python"),
            ("random.random", "python"),
            ("Math.random", "javascript"),
            ("crypto.createSecretKey", "python"),
            ("ec.derive_private_key", "javascript"),
            ("ec.derive_private_key_backup", "python"),
            ("notcrypto.createSecretKey", "javascript"),
            ("crypto.createsecretkey", "javascript"),
            ("EVP_PKEY_check_init", "c"),
            ("my_EVP_PKEY_check", "c"),
            ("EVP_PKEY_check", "python"),
        ]
        for callee, language in cases:
            with self.subTest(callee=callee, language=language):
                match = self.pack.classify_callee(callee, language)
                self.assertTrue(match is None or not match[0].startswith("CRPT."), match)

    def test_content_surfaces_match_api_names_without_secret_arguments(self):
        data = json.loads((self.root / "signatures/packs/content-surfaces.json").read_text())
        rules = {row["id"]: row for row in data["signatures"]}
        load = re.compile(rules["sig.content.crpt-keyload"]["regex"])
        check = re.compile(rules["sig.content.crpt-keycheck"]["regex"])
        # Public synthetic example; the captured surface excludes its value.
        self.assertEqual(load.search("ec.derive_private_key(4, curve)").group(), "ec.derive_private_key")
        self.assertEqual(load.search("crypto.createSecretKey(Buffer.alloc(32))").group(), "crypto.createSecretKey")
        self.assertEqual(check.search("if (EVP_PKEY_private_check(ctx) != 1)").group(), "EVP_PKEY_private_check")
        for text in ("ec.derive_private_key_backup", "my_EVP_PKEY_check", "EVP_PKEY_check_init", "importKey", "00:00:04", "entropy(data)"):
            with self.subTest(text=text):
                self.assertIsNone(load.search(text))
                self.assertIsNone(check.search(text))

    def test_binary_rules_are_exact_normalized_symbols(self):
        data = json.loads((self.root / "signatures/packs/binary-imports.json").read_text())
        rows = {row["atom"]: row for row in data["signatures"] if row["atom"] in {"CRPT.KEYLOAD", "CRPT.KEYCHECK"}}
        for atom, symbol in (("CRPT.KEYLOAD", "PEM_read_bio_PrivateKey"), ("CRPT.KEYCHECK", "EVP_PKEY_private_check")):
            with self.subTest(atom=atom):
                match = rows[atom]["match"]
                self.assertEqual(match["mode"], "exact")
                self.assertIn("lowercase", match["normalize"])
                self.assertIn(symbol.lower(), match["values"])
                self.assertNotIn(symbol.lower() + "_init", match["values"])

    def test_authored_packs_validate_and_equal_generated_mirrors(self):
        for name in ("source-callees", "content-surfaces", "binary-imports"):
            with self.subTest(pack=name):
                base = self.root / "signatures/packs" / name
                authored = tomllib.loads(base.with_suffix(".toml").read_text())
                generated = json.loads(base.with_suffix(".json").read_text())
                self.assertEqual(authored, generated)
                self.assertEqual(parallax.validate_signature_pack(generated), [])
                ids = [row["id"] for row in generated["signatures"]]
                self.assertEqual(len(ids), len(set(ids)))

    def test_new_atoms_and_lens_composition_load(self):
        atoms = parallax.load_atoms()
        for atom_id in ("CRPT.KEYLOAD", "CRPT.KEYCHECK"):
            with self.subTest(atom=atom_id):
                atom = atoms[atom_id]
                self.assertTrue(atom.description)
                self.assertTrue(atom.detection_surfaces)
                self.assertTrue(atom.disambiguation)
                self.assertTrue(atom.relationships)
                self.assertTrue(atom.notes)
        mcd = parallax.load_lens("mcd")
        self.assertIn("BP-CRYPTOWEAK", mcd.components["compositions"])
        self.assertIn("cryptographic-material", mcd.components["signals"])
        architecture = parallax.load_lens("architecture")
        self.assertIn("cryptographic-controls", architecture.components["indicators"])

    def test_validator_requires_binary_match_and_rejects_content_regex(self):
        data = json.loads((self.root / "signatures/packs/binary-imports.json").read_text())
        broken = copy.deepcopy(data)
        broken["signatures"][0].pop("match")
        self.assertTrue(any("requires 'match'" in e for e in parallax.validate_signature_pack(broken)))
        broken = copy.deepcopy(data)
        broken["signatures"][0]["regex"] = "EVP_PKEY_check"
        self.assertTrue(any("must not carry 'regex'" in e for e in parallax.validate_signature_pack(broken)))


if __name__ == "__main__":
    unittest.main()
