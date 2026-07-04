# LOAD.KERNEL_MODULE: Kernel Module Loading

## Description

Loads or unloads a kernel module (device driver) into the running operating-system kernel via `insmod`, `modprobe`, `rmmod` (Linux userspace utilities), `init_module` / `finit_module` (Linux syscalls), or `kextload` / `kextunload` (macOS kernel extensions). The loaded code runs in kernel space with full ring-0 privileges, outside the isolation that constrains user-space processes. The module may or may not be signed, and may or may not be present in the system's distribution.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `insmod` / `modprobe` / `rmmod` / `kextload` / `kextunload` subprocess calls, `init_module` / `finit_module` syscall use, `.ko` / `.kext` path arguments |
| Static Binary | Yes | Module-loader API imports, module-utility command strings, `.ko` / `.kext` path strings |
| Runtime/Dynamic | Yes | Module load/unload events, kernel ring-buffer log entries, newly registered kernel symbols |

## Disambiguation

- **vs LOAD.DYLIB**: `LOAD.DYLIB` loads a shared library into a user-space process's address space. `LOAD.KERNEL_MODULE` loads code into the kernel itself. The privilege boundary is different: a user-space library runs in ring 3 under the process's privileges, a kernel module runs in ring 0 with full control of the host.
- **vs PRIV.EXPLOIT**: Loading a module through the supported module interface is `LOAD.KERNEL_MODULE`. Subverting the kernel by writing its memory directly (`/dev/kmem`, exploiting a vulnerable driver) is `PRIV.EXPLOIT`. The mechanical act of invoking the module loader is `LOAD.KERNEL_MODULE`.
- **vs PRST.\***: Loading a module is the load. Arranging for it to load on every boot (`/etc/modules-load.d`, a launch daemon, a registry/service entry) is a persistence atom.

## Structural Relationships

- **Often co-occurs with**: `FSYS.WRITE` (writing the module file before loading it), `NETW.HTTP` (downloading a module), `PRIV.SUDO` (module loading requires elevated privileges), `PRST.*` (boot-time module loading)
- **May imply**: Code execution in kernel space, the highest privilege level on the host

## Notes

The module path, whether the module is signed, and whether it is present in the package's distribution are the primary structural data points. Module loading is legitimate in driver installers, virtualization tooling, and hardware-support packages; the structural signal is the module's origin and whether it is bundled, downloaded, or written by a prior stage. A module loaded from a temp or writable directory is a stronger structural observation than one loaded from a canonical system path.
