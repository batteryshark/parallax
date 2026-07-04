# SYSI.REGISTRY: Windows Registry Access

## Description

Reads or writes the Windows registry, the hierarchical configuration database holding operating-system and application settings. Mechanisms include the `RegOpenKeyEx` / `RegQueryValueEx` / `RegSetValueEx` / `RegCreateKeyEx` / `RegDeleteKey` Win32 APIs, the `winreg` Python module, `reg.exe` and PowerShell `Get-ItemProperty` / `Set-ItemProperty` over `HKLM:` / `HKCU:`, and direct hive references (`HKEY_LOCAL_MACHINE`, `HKEY_CURRENT_USER`, `HKLM\`, `HKCU\`). The access may read configuration for profiling or write keys that change system or application behavior.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `RegOpenKeyEx` / `RegSetValueEx` / `RegCreateKeyEx` / `RegQueryValueEx` / `RegDeleteKey` calls, `winreg.` use, hive path strings (`HKEY_*`, `HKLM\`, `HKCU\`) |
| Static Binary | Yes | Registry API imports, hive path string literals, registry key path strings |
| Runtime/Dynamic | Yes | Registry open / query / set / delete events, hive access |

## Disambiguation

- **vs PRST.STARTUP / PRST.SERVICE**: Reading or writing a registry key is `SYSI.REGISTRY`. Writing specifically to an autostart key (`...\CurrentVersion\Run`, `RunOnce`) or a service key to gain persistence also implies the relevant `PRST.*` atom. The mechanical registry access is `SYSI.REGISTRY`; the persistence intent lives in `PRST.*`.
- **vs SYSI.SW / SYSI.OS**: When the registry is read to enumerate installed software or operating-system configuration, `SYSI.SW` / `SYSI.OS` describe what is being profiled; `SYSI.REGISTRY` describes the mechanism. They co-occur when registry reads feed a system profile.
- **vs ENVI.SANDBOX**: Reading registry keys that reveal a virtual machine or analysis environment (VMware / VirtualBox artifact keys) and branching on the result also implies `ENVI.SANDBOX`.

## Structural Relationships

- **Often co-occurs with**: `PRST.STARTUP` / `PRST.SERVICE` (autostart and service keys), `ENVI.SANDBOX` (VM-artifact key checks), `SYSI.SW` / `SYSI.OS` (system profiling), `PRIV.*` (writes under `HKLM` typically require elevation)
- **May imply**: Reading system or application configuration, or persisting changes to it

## Notes

The specific key path is the primary structural data point: autostart keys, service keys, and security-product keys carry far more signal than generic application-settings reads. Read versus write, and the hive (`HKLM` is machine-wide and usually privileged; `HKCU` is per-user), further shape the observation. Registry access is structurally common in Windows installers, configuration tools, and system utilities.
