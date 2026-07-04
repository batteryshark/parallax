# Execution Context

Facts about where and how code runs: the lifecycle phase, the privilege and
orchestration around it, and whether the environment is an analysis context.
Sourced from configuration, the runtime environment, and dynamic observation.

| Id | Data point | What it factually states | Primary source |
|---|---|---|---|
| `ENR.EXEC.PHASE` | Lifecycle phase | The phase the code runs in: install, build, test, or runtime | config, dynamic |
| `ENR.EXEC.PRIVILEGE` | Privilege and orchestration | The privilege level and orchestration around execution: CI runner, root, container, or an unprivileged user | environment, config |
| `ENR.EXEC.TOOLING` | Analysis-environment awareness | Whether the surrounding environment is a security, sandbox, or scanning context that code could detect | environment, dynamic |

Judgment-free: this records the context facts. Whether running at install time on
a privileged CI runner, or behaving differently when it detects a sandbox, is
significant is a lens call. The MCD lens's weighting is in
[`../lenses/mcd/signals/execution-context.md`](../lenses/mcd/signals/execution-context.md).
