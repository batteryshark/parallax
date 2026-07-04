# PRST.BOOTKIT: Boot-Level Persistence

## Description

Modifies boot sectors, UEFI firmware, bootloader configuration, or Master Boot Record (MBR) to execute code before the operating system loads. Includes MBR/VBR overwrites, UEFI firmware implants (writing to EFI System Partition, modifying NVRAM boot variables, DXE driver injection), bootloader configuration modification (GRUB, Windows Boot Manager), and Secure Boot policy manipulation. Code executing at this level runs before OS-level security mechanisms (antivirus, EDR, kernel integrity checks) initialize, operating with the highest available privilege level.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Raw disk write operations targeting boot sectors (sector 0, EFI partitions), UEFI variable modification APIs, EFI System Partition file writes, bootloader configuration modification, Secure Boot policy changes |
| Static Binary | Yes | Boot sector signatures, EFI binary structures (PE32+ with EFI subsystem), UEFI protocol GUIDs, disk sector addresses as constants, bootloader path strings |
| Runtime/Dynamic | Difficult | Boot-level code executes before most monitoring tools load; detection requires firmware integrity measurement (TPM PCR values), Secure Boot violation alerts, or offline boot media analysis |

## Disambiguation

- **vs PRST.SERVICE / PRST.STARTUP**: These operate within the OS. `PRST.BOOTKIT` operates before the OS loads. The distinction is the execution layer: pre-OS (firmware/bootloader) vs. OS-managed.
- **vs FSYS.WRITE**: Writing to the EFI System Partition is `FSYS.WRITE` + `PRST.BOOTKIT`. Writing to a raw disk sector (MBR) bypasses the filesystem entirely and is `PRST.BOOTKIT` alone (no filesystem operation, direct block device access).

## Structural Relationships

- **Often co-occurs with**: `EXEC.SYSCALL` (direct disk I/O for MBR writes), `FSYS.WRITE` (EFI partition file writes), `FSYS.PERM` (elevated permissions required for boot sector access), `ENVI.SECDISABLE` (Secure Boot modification to allow unsigned boot code)
- **May imply**: Complete pre-OS execution control; all OS-level security mechanisms can be subverted before they initialize; persistence survives OS reinstallation (firmware implants) or disk formatting (NVRAM-based persistence)

## Notes

Boot-level persistence is the deepest persistence mechanism in the hierarchy. MBR/VBR modifications survive OS reinstallation if the disk is not fully reformatted. UEFI firmware implants stored in SPI flash survive disk replacement entirely. The required privilege level for boot-level modification (typically kernel/root with raw disk access, or physical access for firmware flashing) means this atom generally appears in late-stage attack chains, after privilege escalation has already been achieved. Detection is inherently difficult because the malicious code executes before the monitoring stack is operational.
