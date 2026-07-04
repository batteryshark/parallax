# ENVI.SANDBOX: VM / Container / Sandbox Detection

## Description

Detects whether code is executing inside a virtual machine, container, or sandboxed analysis environment. Techniques include hardware fingerprinting (CPUID hypervisor bit, DMI/SMBIOS strings), checking for known VM artifacts (VMware Tools, VirtualBox Guest Additions, Hyper-V integration services), inspecting MAC address prefixes associated with virtual NICs, querying resource profiles (low RAM/CPU count as heuristic for analysis sandboxes), checking for sandbox-specific registry keys or files, and detecting container environments (/.dockerenv, cgroup namespace indicators).

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | VM artifact path checks, CPUID queries, MAC address prefix comparisons, resource threshold checks, container indicator file reads |
| Static Binary | Yes | Strings referencing VM vendor names, hardware fingerprint constants, known sandbox artifact paths |
| Runtime/Dynamic | Yes | CPUID instruction execution, registry/filesystem queries for VM artifacts, WMI queries for hardware model |

## Disambiguation

- **vs ENVI.DEBUG**: Debugger detection checks for attached analysis tooling. Sandbox detection checks the execution environment infrastructure. A debugger can be attached inside or outside a VM; a VM can run with or without a debugger attached.
- **vs ENVI.ENVCHECK**: Sandbox detection targets analysis infrastructure specifically, VM hypervisors, container runtimes, sandbox products. Environment fingerprinting (`ENVI.ENVCHECK`) targets operational environment characteristics, CI variables, hostnames, usernames, geographic indicators. When a check targets a specific sandbox product by name (Cuckoo, Any.Run, Joe Sandbox), use ENVI.SANDBOX. When a check targets a named hostname or CI variable, use ENVI.ENVCHECK.

## Structural Relationships

- **Often co-occurs with**: `ENVI.DEBUG` (layered analysis detection), `ENVI.ENVCHECK` (combined environment profiling), `ENVI.TIMING` (timing as additional sandbox indicator)
- **May imply**: The code has different behavior paths for virtualized vs. bare-metal execution

## Notes

Sandbox detection techniques vary in sophistication. Simple artifact checks (file existence, registry key presence) are detectable in static analysis. Hardware fingerprinting (CPUID timing, cache behavior) may require dynamic analysis. The mechanical behavior is: query execution environment properties and compare against known virtualization/containerization indicators.
