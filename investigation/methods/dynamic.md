# Dynamic Analysis

Observation of software behavior during execution: what the code actually does at runtime.

## Capabilities

- **Actual behavior:** Which code paths execute, what functions are called, what data flows where
- **Resolved targets:** Runtime-computed URLs, file paths, hostnames, command arguments
- **Decoded payloads:** Obfuscated or encrypted content resolved to its operational form
- **System interaction:** File creation/modification/deletion, registry changes, process creation, network connections
- **Memory contents:** Runtime state, decrypted secrets, unpacked code, heap/stack contents
- **Timing behavior:** Actual delays, time-check outcomes, scheduled operations
- **Environment interaction:** Which environment variables are read, what system properties are queried
- **Triggered conditions:** Environment gates, time bombs, and conditional branches that activate during execution

## Blind Spots

- **Dormant paths:** Code paths that don't trigger under the analysis conditions remain invisible
- **Time-bombed behavior:** If the time condition hasn't been met, the payload doesn't execute
- **Environment-specific branches:** Behavior gated on conditions not present in the analysis environment
- **Anti-analysis:** Code that detects dynamic analysis environments and suppresses malicious behavior (`ENVI.SANDBOX`, `ENVI.DEBUG`)
- **Rare triggers:** Behaviors activated by specific input, network responses, or external signals not reproduced during analysis
- **Scale-dependent behavior:** Resource consumption patterns that only manifest under production load

## Tools

Debuggers (gdb, lldb, WinDbg, x64dbg), sandboxes (Cuckoo/CAPE, ANY.RUN, Joe Sandbox), system call tracers (strace, dtrace, procmon), API monitors, memory forensics (Volatility), runtime instrumentation (Frida, DynamoRIO, Pin), container-based execution environments.

## When to Use

- **Opaque code:** When static analysis (source or binary) reveals obfuscated, packed, or dynamically-generated code
- **Behavioral confirmation:** When static analysis identifies a suspicious pattern and you need to confirm it actually executes
- **Install-time analysis:** When package lifecycle hooks (`PKGM.INSTALL`) need to be observed in action
- **Payload recovery:** When encoded/encrypted payloads need to be captured in their decoded form
- **Trigger identification:** When time-gated or environment-gated behavior needs to be activated under controlled conditions

## When to Transition Away

- **Unexpected network targets:** When dynamic analysis reveals connections to unknown destinations → transition to **OSINT** + **network analysis**
- **Anti-analysis detected:** When code detects the analysis environment and changes behavior → transition to **environment scaffolding** (build a less detectable environment)
- **Persistence artifacts:** When code installs persistence mechanisms → transition to **static source/binary analysis** of the persisted artifacts
- **Build concerns:** When the dynamic behavior doesn't match expected behavior from source → transition to **build & CI analysis**

## Relationship to Environment Scaffolding

Dynamic analysis is only as good as the environment it runs in. The **scaffolding** method prepares the execution context: what OS, what architecture, what environment variables, what network access, what time the clock reports. Scaffolding choices directly determine which behaviors dynamic analysis can observe.

## Atom Categories Most Visible

NETW (actual connections), EXEC (actual process creation), FSYS (actual file operations), CRED (actual credential access), PRST (actual persistence installation), PRIV (actual privilege changes), RSRC (actual resource consumption), TIME (actual timing behavior)

## Atom Categories Least Visible

XFRM (the transformation itself may not be visible, only its input and output), ARTF (embedded artifacts are source-level; dynamic analysis sees their *use*, not their *presence*)
