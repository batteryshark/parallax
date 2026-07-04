# FSYS.CLIPBOARD: Clipboard Access

## Description

Reads from or writes to the system clipboard. The clipboard is a shared data surface that crosses application boundaries: any process can read what a user copied from any other application, and any process can replace the clipboard contents. Reading retrieves whatever the user (or another application) last copied. Writing replaces the current clipboard contents with new data.

On most operating systems, clipboard access requires no special permissions, making it a low-friction cross-application data access mechanism.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Clipboard API calls (`pyperclip`, `clipboard`, `navigator.clipboard`, `GetClipboardData()`, `SetClipboardData()`, `pbcopy`/`pbpaste` invocations) |
| Static Binary | Yes | Clipboard function imports, clipboard format constants |
| Runtime/Dynamic | Yes | Clipboard access events (on platforms that log them), clipboard content changes, clipboard monitoring loops |

## Disambiguation

- **vs other FSYS atoms**: Clipboard access is categorized under FSYS as an OS resource access mechanism, but it is behaviorally distinct from file-based FSYS operations. It does not involve file paths, file handles, or disk I/O. It accesses an in-memory OS resource shared across applications.
- **Read vs. Write**: Clipboard reads retrieve data from other applications. Clipboard writes replace the current clipboard contents. Both directions are structurally significant but represent different capabilities (passive data access vs. active content substitution).

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (transmitting clipboard contents), `TIME.*` (polling clipboard on a timer), `CRED.*` (clipboard may contain copied credentials)
- **May imply**: The code interacts with user-copied data across application boundaries

## Notes

Clipboard contents are inherently transient and user-controlled: they change with each copy operation. Clipboard monitoring (repeated reads on a timer or event) captures a stream of user-copied content. Clipboard replacement (writes) substitutes attacker-controlled content for user-copied content. The trigger mechanism (explicit function call, background timer, import-time hook) and direction (read vs. write) are the key structural observations. This atom may be relocated to a better-fitting category in future ontology revisions.
