# PKGM.BINDOWN: Binary Download During Build

## Description

Downloads pre-compiled binary artifacts during package installation or build rather than building from source. The downloaded binary is opaque to source-level analysis performed on the package's own code. Common in packages with native extensions that distribute pre-built binaries for supported platforms, the package selects and downloads the appropriate binary for the target platform at install time.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | HTTP/fetch calls in install scripts, URL construction targeting binary download endpoints (GitHub Releases, CDN paths, custom hosting), platform detection logic selecting binary URLs, binary extraction/placement after download, checksum verification (or absence thereof) |
| Static Binary | N/A | The detection target is the install-time download mechanism, not the downloaded binary itself |
| Runtime/Dynamic | Yes | HTTP requests during `npm install` / `pip install` / build phase, binary files appearing on disk that were not in the package distribution, file permission changes (chmod +x) on downloaded artifacts |

## Disambiguation

- **vs NETW.HTTP**: `PKGM.BINDOWN` is specifically a binary download during the build or install phase. `NETW.HTTP` is general HTTP communication at any lifecycle phase. A package that downloads a `.so`/`.dll`/`.dylib` during `postinstall` is `PKGM.BINDOWN`. A package that makes API calls at runtime is `NETW.HTTP`. Both may technically use the same HTTP primitives, but the lifecycle phase and what is downloaded distinguish them.
- **vs PKGM.INSTALL**: `PKGM.INSTALL` identifies the hook mechanism that triggers code at install time. `PKGM.BINDOWN` identifies the specific behavior of downloading a binary during that phase. A package with a `postinstall` script that downloads a native binary carries both `PKGM.INSTALL` (the hook) and `PKGM.BINDOWN` (the binary download behavior).

## Structural Relationships

- **Often co-occurs with**: `PKGM.INSTALL` (binary download triggered by install hook), `NETW.HTTP` (the HTTP mechanism used for the download), `ENVI.*` (platform detection to select the correct binary), `EXEC.PROC` (executing the downloaded binary), `FSYS.WRITE` (placing the downloaded binary on disk)
- **May imply**: The package contains native code or platform-specific compiled components; source-level analysis of the package is incomplete without analyzing the downloaded binary

## Notes

Binary downloads during build are structurally significant because they introduce opaque executable content that cannot be assessed through source-level analysis of the package itself. The downloaded binary may be a legitimate compiled native extension, or it may be an arbitrary payload. The structural observation is that the package's installed footprint includes executable content not present in or derivable from the package's source code. Integrity verification (checksums, signatures) against the downloaded binary is an observable structural property, its presence or absence is a meaningful detection surface detail.
