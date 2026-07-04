# PRST.EXTENSION: Browser / Application Extension Installation

## Description

Installs or modifies browser extensions, IDE plugins, or application add-ons that execute within the context of a host application. Includes Chromium extension installation (unpacked extension directories, CRX files, extension registry/preferences manipulation, managed policy-based installation), Firefox add-on deployment, VS Code extension installation, and other application plugin mechanisms. The extension gains access to the host application's capabilities: browser extensions can access page content, cookies, network requests, and browsing history; IDE extensions can access source code, terminals, and stored credentials.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Extension manifest creation (`manifest.json` with permissions), writes to browser extension directories, browser preferences/registry manipulation for extension installation, IDE extension packaging or installation commands |
| Static Binary | Yes | Extension directory path strings, browser profile path strings, extension manifest structures, CRX/VSIX packaging patterns |
| Runtime/Dynamic | Yes | New extensions appearing in browser extension lists, new IDE plugins in extension directories, extension processes spawned by the host application, extension-initiated network requests |

## Disambiguation

- **vs FSYS.WRITE**: Writing files is `FSYS.WRITE`. Writing files that constitute a browser extension into the browser's extension directory is `FSYS.WRITE` + `PRST.EXTENSION`. The persistence atom describes the semantic consequence: the written files will execute within the host application's privileged context.
- **vs PRST.HOOK**: `PRST.HOOK` intercepts execution at the OS/loader/runtime level (shared library injection, PATH shadowing). `PRST.EXTENSION` installs code within a specific application's plugin framework using that application's documented extension mechanism. The distinction is the interception layer: OS/loader vs. application plugin API.
- **vs PRST.STARTUP**: Browser extensions persist across browser restarts and system reboots (the browser loads them on every launch), but they are not OS-level startup items. `PRST.EXTENSION` persists via the application's own extension management, not via OS boot/login mechanisms.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing extension files to disk), `NETW.HTTP` (extension making network requests from the browser context), `CRED.BROWSER` (extension accessing browser-stored credentials or cookies), `FSYS.SENSITIVE` (extension reading browser profile data)
- **May imply**: The installed extension has access to the host application's full capability set as defined by its requested permissions (or all capabilities if installed via developer mode or policy override)
- **Commonly part of idioms**: Browser credential harvester (extension captures credentials from page forms or cookie stores), browsing surveillance (extension monitors and exfiltrates browsing activity), session hijacker (extension extracts session cookies for replay)

## Notes

The extension's declared permissions are the key structural data point. A browser extension requesting `<all_urls>`, `cookies`, `webRequest`, and `webRequestBlocking` has full visibility into and control over all browser network traffic. The gap between the installing package's stated purpose and the extension's requested permissions is the primary structural observation. Force-installed extensions (via managed policies or registry manipulation) bypass user consent entirely.
