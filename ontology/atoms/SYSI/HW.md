# SYSI.HW: Hardware Information Query

## Description

Queries hardware identifiers and physical system properties: MAC addresses, serial numbers, CPU model and ID, GPU information, disk identifiers (serial numbers, volume IDs), BIOS/UEFI information (vendor, version, date), total RAM, screen resolution, motherboard serial, and TPM state. APIs and mechanisms include `wmic` queries (`Win32_BIOS`, `Win32_Processor`, `Win32_DiskDrive`, `Win32_BaseBoard`), `dmidecode` (Linux), `system_profiler` (macOS), `lshw` / `lspci` / `lscpu` (Linux), `IOKit` framework (macOS), `GetSystemInfo` / `GlobalMemoryStatusEx` (Windows API), `CPUID` instruction, `/sys/class/dmi/id/` reads (Linux), and `sysctl hw.*` (BSD/macOS). Combined hardware identifiers can produce machine-unique fingerprints.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `wmic` subprocess calls with hardware classes, `dmidecode` / `system_profiler` invocations, `CPUID` inline assembly, `/sys/class/dmi/` reads, `IOKit` framework calls, hardware attribute concatenation for fingerprinting |
| Static Binary | Yes | WMI class name strings, `dmidecode` command strings, CPUID instruction sequences, hardware identifier path strings, hash function applied to concatenated hardware values |
| Runtime/Dynamic | Yes | WMI queries, `dmidecode` execution, CPUID instruction execution, file reads from `/sys/class/dmi/`, hardware attribute collection across multiple subsystems |

## Disambiguation

- **vs ENVI.SANDBOX**: `SYSI.HW` queries hardware information generally: CPU model, RAM size, disk serial, MAC address. When specific hardware fields are queried to detect virtualization (CPUID hypervisor bit, low core/RAM counts as VM heuristics, MAC address OUI prefixes associated with VMware/VirtualBox/Hyper-V virtual NICs, DMI strings containing "Virtual" or "QEMU"), `ENVI.SANDBOX` also applies. The mechanical query is `SYSI.HW`; the interpretive use for VM detection is `ENVI.SANDBOX`. Both co-occur when hardware queries serve as sandbox detection primitives.
- **vs SYSI.NET**: MAC addresses appear in both contexts. When collected as part of network interface configuration alongside IP addresses and routes, `SYSI.NET` applies. When collected as hardware identifiers alongside serial numbers and CPU IDs for machine fingerprinting, `SYSI.HW` applies. Both may apply simultaneously.

## Structural Relationships

- **Often co-occurs with**: `SYSI.OS` (combined system fingerprint), `ENVI.SANDBOX` (hardware fields as VM detection primitives), `CRPT.HASH` (hashing combined hardware values to produce fingerprint), `NETW.*` (transmitting hardware fingerprint), other `SYSI.*` subtypes (aggregated system profile)
- **May imply**: The code needs hardware identity information, for licensing, telemetry, fingerprinting, or environment detection

## Notes

Hardware information queries serve legitimate purposes in licensing (machine-locked keys), telemetry (aggregated hardware demographics), and diagnostics (hardware compatibility checks). The key structural observations are: which specific attributes are collected, whether they are combined into a composite fingerprint (typically by concatenation and hashing), and where the fingerprint goes. Collecting a single attribute (e.g., total RAM for resource allocation) differs structurally from collecting MAC + CPU ID + disk serial + BIOS serial and hashing them together.
