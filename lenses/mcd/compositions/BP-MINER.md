# BP-MINER: Resource Hijacking

Uses host compute resources for unauthorized purposes. Classic: cryptocurrency mining. Evolving: unauthorized AI training, distributed computing, proxy/relay networks.

## Constituent Atoms

| Role | Atom | Notes |
|---|---|---|
| **Required** | `RSRC.CPU` or `RSRC.GPU` | Significant resource consumption |
| **Required** | `NETW.*` | Communication with pool, coordinator, or beneficiary |
| Supporting | `ENVI.*` | Throttling when user active, activating when idle |
| Supporting | `XFRM.*` | Concealing the mining/compute logic |
| Supporting | `SYSI.HW` | Profiling hardware capabilities (CPU cores, GPU model) |
| Supporting | `ARTF.CRYPTO_ADDR` | Mining pool address or wallet |

## Investigation Guidance

- **Verify:** What computation? What network destination? Proportional to stated functionality?
- **Escalates:** Mining pool addresses/protocols identified. GPU in non-ML code. Hidden behind evasion.
- **De-escalates:** Proportional to documented functionality (image processing, ML in ML library).
