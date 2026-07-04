# XFRM.STRCON: String Construction

## Description

Assembles strings from individual characters, character codes, array joins, format string substitution, or concatenation of scattered fragments. The resulting string is not present as a contiguous literal in the artifact, requiring reconstruction to determine its value. Construction may draw fragments from hardcoded sources, runtime data, environment variables, or decoded/decrypted content.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `String.fromCharCode()` arrays, `chr()` calls in loops, array `.join('')` patterns, format string abuse, repeated concatenation building a single value |
| Static Binary | Partial | Character-by-character construction patterns in disassembly, char arrays assembled at runtime, format string references with scattered arguments |
| Runtime/Dynamic | Yes | String materialization, the fully constructed string appears in memory, as a function argument, or in network/file output |

## Disambiguation

- **vs XFRM.ENCODE**: Encoding transforms an entire data blob through a standardized scheme. String construction assembles a value from discrete fragments. An encoded string is one contiguous encoded literal; a constructed string is many pieces joined at runtime.
- **vs normal string formatting**: Constructing URLs from base + path + query parameters, building SQL queries, or assembling log messages are standard programming patterns. `XFRM.STRCON` applies when the construction specifically prevents the resulting value from appearing as a searchable literal, the mechanical effect is that static string extraction will not find the value.

## Structural Relationships

- **Often co-occurs with**: `ARTF.URL` / `ARTF.IP` / `ARTF.CMD` (the constructed string resolves to a recognizable artifact), `EXEC.SHELL` (constructed command string executed), `NETW.HTTP` (constructed URL used as request target)
- **May imply**: The final string value has significance; construction from fragments is not typically applied to arbitrary data
- **Commonly part of idioms**: Decode-and-execute chain (string assembly as the "decode" step, where fragments are the encoded form)

## Notes

The distinction between `XFRM.STRCON` and normal string building is the mechanical effect on static analysis: if the complete string value cannot be recovered without executing or simulating the construction logic, it's `XFRM.STRCON`. If the value is trivially readable from the source (e.g., `"https://" + domain + "/api"`), it's normal string formatting.
