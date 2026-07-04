# ARTF.URL: Embedded URL / URI

## Description

HTTP(S), FTP, or other protocol URLs present as string literals in source or binary. Includes full URLs with protocol scheme, optional authority (host, port, credentials), path components, query parameters, and fragment identifiers. The artifact is the complete resource locator, a structured reference to a network-accessible or local resource. URI schemes include `http://`, `https://`, `ftp://`, `ftps://`, `file://`, `ws://`, `wss://`, custom protocol handlers, and data URIs.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals matching URL patterns with protocol prefix, URL construction via string concatenation or template literals, URL objects (`new URL("...")`, `urllib.parse`), API endpoint constants |
| Static Binary | Yes | URL strings in data sections, protocol scheme prefixes (`http://`, `https://`) in string tables, URL-encoded sequences |
| Runtime/Dynamic | Yes | URLs passed to HTTP clients, fetch/request calls, browser navigation APIs, URL strings in network payloads |

## Disambiguation

- **vs ARTF.DOMAIN**: A URL includes protocol, path, and possibly query/fragment components (`https://example.com/api/v1/data?key=val`). A domain is a hostname only (`example.com`). A URL always contains a hostname or IP, but carries additional structural information beyond the host identifier.
- **vs ARTF.IP**: A URL may contain an IP address instead of a hostname (`http://203.0.113.50:8080/path`). In this case both `ARTF.URL` and `ARTF.IP` apply. The IP is the network identifier; the URL is the full resource locator.
- **vs NETW.HTTP / NETW.***: `ARTF.URL` is the static presence of a URL string. `NETW.*` atoms describe runtime network operations. A URL embedded in code may serve as documentation, a default, a template, or an actual connection target.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (URL used as request target), `XFRM.ENCODE` (URL encoded to avoid string detection), `XFRM.STRCON` (URL assembled from fragments at runtime), `ARTF.IP` or `ARTF.DOMAIN` (host component of the URL)
- **May imply**: The code references an external resource, whether for data retrieval, command-and-control, update checking, analytics, or configuration

## Notes

URL structure carries contextual information. Path components may indicate API endpoints, file downloads, or webhook receivers. Query parameters may carry tokens, identifiers, or encoded data. The protocol scheme indicates the transport mechanism. Non-standard ports in the authority component indicate custom services. These are structural properties of the URL, useful for characterization regardless of analytical lens.
