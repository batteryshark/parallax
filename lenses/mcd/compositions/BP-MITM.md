# BP-MITM: Traffic Interception / Man-in-the-Middle Setup

Positions to intercept, inspect, modify, or redirect network traffic between victim and legitimate services. Typically involves two coordinated actions: degrading the trust model (CA cert, disable TLS verification) and redirecting traffic (proxy, DNS modification).

Interception can be passive (recording for credential harvest) or active (modifying for content injection or binary replacement).

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required (one+)** | `CRPT.CERT` | Trust store manipulation: installing CA, disabling TLS verification |
| **Required (one+)** | `ENVI.SECDISABLE` | Weakening network security: firewall rules, HSTS disabling, proxy config |
| Supporting (strong) | `NETW.LISTEN` | Local proxy or transparent interceptor |
| Supporting (strong) | `CRPT.KEYGEN` | Generating interception certificates on-the-fly |
| Supporting (strong) | `CRPT.CUSTOM` | Custom TLS handling avoiding standard crypto libraries |
| Supporting | `PRST.*` | Persistent interception surviving reboot |
| Supporting | `ENVI.MASQ` | Proxy/cert named to resemble legitimate component |
| Supporting | `ARTF.IP` or `ARTF.DOMAIN` | Hardcoded proxy/relay destination |
| Supporting | `FSYS.WRITE` | Writing PAC files, modifying `/etc/hosts`, system proxy settings |
| Supporting | `SYSI.NET` | Network recon to identify target traffic before interception |
| Supporting | `XFRM.*` | Concealing interception infrastructure |

## Real-World Analogues

Superfish/Lenovo (2015): pre-installed CA with extractable private key. Malicious browser extensions injecting CA certs. Supply chain packages disabling cert verification (converts HTTPS to de facto HTTP).

## Investigation Guidance

- **Verify:** What cert/trust store operation? Scope: system-wide or application-scoped? CA private key embedded, local, or remote? Transparent or requires explicit config?
- **Escalates:** System trust store (affects all apps). Extractable CA private key. PAC files in system locations. Combined with persistence. Cert/proxy named like legitimate vendor. Targets specific high-value domains.
- **De-escalates:** Scoped to package's own HTTPS client for documented purpose. TLS disabled only for specific test endpoint behind opt-in. Package is documented inspection tool (mitmproxy, Charles).
