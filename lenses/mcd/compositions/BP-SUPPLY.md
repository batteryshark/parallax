# BP-SUPPLY: Supply Chain Payload

A package executes a malicious payload during installation or first use. The dominant attack pattern in modern software supply chains: a package runs code at install time that downloads a second stage, exfiltrates credentials, or establishes persistence, before the developer has written a single line of code using the package.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `PKGM.INSTALL` | Install-time execution is the entry point |
| **Required** | `EXEC.SHELL` or `NETW.*` or `FSYS.WRITE` | The payload must do something: execute commands, phone home, or drop files |
| Supporting | `XFRM.*` | Transformation of install-time code strongly escalates |
| Supporting | `ARTF.URL` or `ARTF.IP` | Hardcoded remote targets in install scripts |
| Supporting | `PKGM.BINDOWN` | Downloading binaries during install |
| Supporting | `ENVI.ENVCHECK` | Checking whether environment is CI/sandbox before activating |
| Supporting | `PKGM.PHANTOM` | Payload delivered via dependency never imported in source |
| Supporting | `ENVI.FORENSIC` | Self-destruction or evidence replacement after payload execution |
| Supporting | `ENVI.MASQ` | Payload artifacts masquerading as legitimate system components |

## Real-World Analogues

The `ua-parser-js` hijack (2021), the `event-stream` attack (2018), the Axios npm compromise (2026), phantom dependency `plain-crypto-js` with `postinstall` hook deploying cross-platform RAT.

## Investigation Guidance

- **Verify:** What does the install script actually do? Trace the full execution path from the install hook.
- **Escalates:** Install script is transformed/encoded. Contacts a remote host. Writes outside package directory. Package is new or has anomalous metadata.
- **De-escalates:** Install script compiles native extensions from included source. Runs a standard build tool. Package has long history and many maintainers.
