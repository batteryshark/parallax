# MCD Lens: RSRC (Resource Consumption) Verification

Investigation questions for RSRC findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any RSRC Atom

1. **Where does the output of the computation go?** Is the result returned to the calling application for its own use, stored locally, or transmitted to an external endpoint? The recipient of the computation's output determines who benefits from the resource consumption. `[lens-neutral]`

2. **Is the resource acquisition conditioned on environment, time, or feature flags?** Does the resource-intensive code path activate based on environment detection (`ENVI`), time-of-day checks (`TIME`), CI/production differentiation, or dynamically-fetched configuration? Conditional activation suggests the code avoids consuming resources during review or testing. `[MCD]`

3. **Does the package's stated purpose explain this level of resource consumption?** Assess whether the observed resource usage is proportional to and necessary for what the package claims to do. A logging library has no reason for sustained CPU computation; a video encoder does. `[lens-neutral]`

## RSRC.CPU / RSRC.GPU

4. **Are cryptocurrency wallet addresses, mining pool hostnames, or stratum protocol URLs present anywhere in the codebase or its dependencies?** Search for `ARTF.CRYPTO_ADDR` patterns: Base58/Bech32 addresses, `stratum+tcp://` URLs, pool domain names, coin algorithm identifiers. Their presence alongside compute consumption is the canonical cryptojacking signature. `[MCD]`

5. **Is the GPU compute capability reachable from the package's documented public API?** Trace the call path from public API surface to GPU dispatch. GPU compute accessible only through internal/undocumented paths, not reachable from any function a user would call intentionally, indicates the capability is hidden from the consumer. `[lens-neutral]`

## RSRC.FORK

6. **Is there an enforced upper bound on process or thread creation?** Identify whether a pool size limit, iteration cap, or resource limit (`ulimit`, `setrlimit`, thread pool max) constrains creation count. Determine whether the bound is enforced programmatically or only documented. An unenforced "recommended limit" is not a bound. `[lens-neutral]`

## Cross-Cutting

7. **What is the network traffic profile during resource consumption?** Monitor outbound connections during active resource consumption. Identify whether traffic correlates with computation cycles (result submission), runs continuously (relay/proxy), or is absent (local-only resource use). The presence, timing, and destination of network traffic during resource consumption is the primary signal for determining beneficiary. `[lens-neutral]`

8. **Is the resource behavior present in the published artifact but absent from the source repository?** Compare the published package (npm tarball, PyPI wheel, Maven JAR) against the source repository at the tagged release. Resource-consuming code injected during build/publish that does not appear in auditable source is a supply chain indicator. `[MCD]`
