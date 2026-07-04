# XFRM.UNICODE: Unicode Representation Tricks

## Description

Uses Unicode features to alter the apparent meaning of identifiers, strings, or file extensions without changing the underlying byte sequence in ways that are immediately visible. Techniques include homoglyph substitution (replacing ASCII characters with visually identical Unicode codepoints), zero-width character insertion (U+200B, U+FEFF, U+200D), right-to-left override characters (U+202E) that reverse displayed text direction, and non-standard whitespace characters that appear identical to standard spaces but have different codepoints.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Non-ASCII codepoints in identifiers or strings where ASCII is expected, zero-width characters (byte sequences with no visible representation), RTL override characters preceding filename-like strings |
| Static Binary | Partial | Non-ASCII byte sequences in string tables, Unicode normalization differences between display and storage |
| Runtime/Dynamic | No | Unicode tricks are a static representation concern, they affect how code reads, not how it executes (with the exception of RTL filename tricks that affect file resolution) |

## Disambiguation

- **vs XFRM.RENAME**: Identifier transformation replaces names entirely with non-descriptive alternatives. Unicode tricks preserve the *apparent* name while inserting invisible characters or substituting look-alike codepoints. A function named `a1b2` is `XFRM.RENAME`. A function named `readline` where the `l` is actually a Cyrillic `l` (U+04CF) is `XFRM.UNICODE`.
- **vs AITM.INVISIBLE**: When Unicode tricks are used to embed content targeted at AI systems (invisible prompt injections via zero-width characters), the Unicode technique itself is `XFRM.UNICODE` and the AI-targeting intent is a lens interpretation. The atom describes the mechanical use of Unicode features.

## Structural Relationships

- **Often co-occurs with**: `AITM.INVISIBLE` (Unicode tricks in AI-targeted content), `ARTF.URL` / `ARTF.PATH` (Unicode-manipulated filenames or URLs)
- **May imply**: The author used a text editor or tool that supports non-ASCII character insertion

## Notes

Unicode tricks are detectable by comparing the visual rendering of code against its byte-level representation. Tools that normalize Unicode or flag non-ASCII characters in identifiers catch most variants. RTL override attacks are particularly effective against file extension display (e.g., a file named `photo_\u202Egnp.exe` displays as `photo_exe.png`).
