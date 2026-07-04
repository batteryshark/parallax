# AITM.INVISIBLE: Invisible Content Embedding

## Description

Content embedded using encoding techniques that make it invisible or difficult to see in standard text rendering but processable by LLMs and other text-processing systems. The content is present in the file's byte sequence but does not produce visible output in standard editors, terminals, or documentation renderers.

Techniques include zero-width Unicode characters (U+200B Zero Width Space, U+200C Zero Width Non-Joiner, U+200D Zero Width Joiner, U+FEFF Byte Order Mark used mid-text), homoglyphs (visually identical characters from different Unicode scripts that encode information through script selection), right-to-left override characters (U+202E that reverses displayed text direction, hiding true content ordering), tag characters (U+E0001-U+E007F, a Unicode block designed for language tagging that produces no visible output), variation selectors used outside their defined combining contexts, and adversarial token sequences that exploit tokenizer behavior in specific LLM architectures.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Non-printable Unicode codepoints in source files (byte sequences with no visible representation), unexpected file size relative to visible content length, homoglyph characters detectable by Unicode script analysis (mixed scripts within a single identifier or string), RTL override characters in LTR-language source files, tag character byte sequences (F3 A0 80 81 through F3 A0 81 BF in UTF-8) |
| Static Binary | Partial | Non-printable byte sequences in string tables, file size anomalies relative to visible string content |
| Runtime/Dynamic | No | Invisible content is a static embedding concern, the content targets AI systems that process the text, not the language runtime. Detection is at the source/file level, not at execution time |

## Disambiguation

- **vs XFRM.UNICODE**: `XFRM.UNICODE` describes the broad use of Unicode features to alter apparent meaning, including homoglyphs in identifiers, RTL tricks on filenames, and non-standard whitespace. `AITM.INVISIBLE` specifically describes invisible content embedding that targets AI text processing, content that has no visible representation but is present in the byte stream and processed by LLMs. When Unicode tricks are used to embed invisible AI-targeted content, both atoms apply. When Unicode tricks alter visible identifiers (e.g., Cyrillic homoglyphs in function names), only `XFRM.UNICODE` applies.
- **vs AITM.INJECT**: `AITM.INVISIBLE` describes the embedding technique, how the content is hidden. `AITM.INJECT` describes the content type, directives targeting AI behavior. Invisible content may or may not contain injected instructions. When it does, both atoms apply: `AITM.INVISIBLE` for the invisibility mechanism and `AITM.INJECT` for the directive content.
- **vs XFRM.STEG**: Steganography hides content within non-text media (images, audio, video). `AITM.INVISIBLE` hides content within text using Unicode and encoding properties of the text itself. Both are concealment techniques but in different media.

## Structural Relationships

- **Often co-occurs with**: `AITM.INJECT` (invisible directives targeting AI systems), `XFRM.UNICODE` (Unicode-based embedding technique), `AITM.CONTEXT` (invisible content that alters the apparent meaning of visible documentation)
- **May imply**: The content author anticipated that both human reviewers (who would not see the content) and AI systems (which would process it) would encounter the file; the invisibility is meaningful only when different readers have different visibility
- **Commonly part of idioms**: Invisible prompt injection (zero-width encoded directives in README/docstring), dual-audience attack (visible documentation for humans + invisible instructions for AI), invisible payload delivery (encoded instructions that survive copy-paste and text processing)

## Notes

The gap between what is visible and what is processable is the core structural property. A human reviewing a README in a browser or terminal sees rendered text. An LLM processing the same file as a token sequence sees all bytes, including non-printable characters. This visibility gap exists in every tool that renders Unicode text. The gap is a property of the rendering pipeline, not of any specific AI system. Detection requires byte-level analysis that compares the visible content length against the actual byte sequence length, or that flags the presence of specific non-printable codepoint ranges that have no legitimate reason to appear in source code or documentation.
