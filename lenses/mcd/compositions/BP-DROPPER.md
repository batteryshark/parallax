# BP-DROPPER: Dropper / Downloader

Retrieves a secondary payload from a remote source and executes it locally. The dropper itself may appear benign; its purpose is to be small, inconspicuous, and serve as the delivery vehicle for the real payload, which is never present in the analyzed artifact.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `NETW.HTTP` or `NETW.FTP` | Downloading the payload |
| **Required** | `FSYS.WRITE` | Writing the payload to disk |
| **Required** | `EXEC.SHELL` or `EXEC.PROC` or `LOAD.EVAL` | Executing the downloaded payload |
| Supporting | `FSYS.PERM` | Making the downloaded file executable |
| Supporting | `FSYS.TEMP` | Staging in temp directory |
| Supporting | `XFRM.*` | Concealing the download URL or execution logic |
| Supporting | `ENVI.*` | Only downloading when not under analysis |

## Investigation Guidance

- **Verify:** What URL? Is the payload still available? What does it contain?
- **Escalates:** Downloaded file is binary. URL is IP or shortener. Download at install time. Immediate execution with elevated privileges.
- **De-escalates:** Downloaded file is documented resource. From well-known CDN. Not executed.
