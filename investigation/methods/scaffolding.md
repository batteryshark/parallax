# Environment Scaffolding

Construction of controlled execution environments tailored to activate specific behaviors or test specific hypotheses. Scaffolding is a meta-method: it enables other methods (primarily dynamic and network analysis) by preparing the conditions under which they operate.

## Capabilities

- **Condition manipulation:** Set specific environment variables, hostnames, time values, network configurations to trigger environment-gated behavior
- **Anti-analysis evasion:** Build environments that don't trigger sandbox/VM/debugger detection (`ENVI.SANDBOX`, `ENVI.DEBUG`)
- **Time manipulation:** Set system clocks to future dates to trigger time-bombed behavior (`TIME.CMP`)
- **Network simulation:** Provide fake DNS responses, mock API endpoints, simulated C2 servers to observe interaction protocols
- **Isolation:** Prevent actual damage (network isolation, filesystem snapshots, credential honeypots) while allowing behavior to proceed
- **Credential honeypots:** Plant synthetic credentials in expected locations to detect credential harvesting without exposing real secrets
- **Platform simulation:** Match target platform characteristics (OS version, installed software, user accounts) to trigger platform-specific branches

## Blind Spots

- **Unknown triggers:** Cannot scaffold conditions you don't know about; if the code checks for a specific hostname you haven't identified, the behavior won't trigger
- **Fidelity gaps:** Simulated environments never perfectly match production; sophisticated anti-analysis may detect the simulation
- **Observer effect:** Any instrumentation or monitoring added to the scaffold is itself detectable by code that looks for it
- **Combinatorial explosion:** The space of possible environment configurations is vast; you can't test every combination

## Tools

Virtual machines (VMware, VirtualBox, QEMU), containers (Docker, Podman), sandbox platforms (Cuckoo/CAPE), network simulation (FakeNet-NG, INetSim), time manipulation (libfaketime, Windows time service), configuration management (Ansible, Terraform for repeatable environments), snapshot/restore tools.

## When to Use

- **Environment-gated behavior:** When static analysis reveals `ENVI.ENVCHECK` or `ENVI.SANDBOX` gates and you need to trigger the gated path
- **Time-bombed behavior:** When `TIME.CMP` with a future date is detected and you need to observe the post-trigger payload
- **Anti-analysis resistance:** When initial dynamic analysis was detected (behavior changed in sandbox) and you need a more convincing environment
- **Safe detonation:** When you want to observe potentially destructive behavior without risk to real systems
- **Hypothesis testing:** When you have a specific theory about what triggers a behavior and need to test it

## When to Transition Away

Scaffolding doesn't transition away; it enables transitions *to* other methods:
- Scaffold built → **dynamic analysis** executed within it
- Scaffold includes network monitoring → **network analysis** captures traffic
- Scaffold produces artifacts → **static source/binary analysis** examines them
- Scaffold reveals destinations → **OSINT** investigates them

## Scaffolding Design Principles

**Start from the hypothesis.** Every scaffold should test a specific theory: "I think this code activates when `CI=true` is set" or "I think this contacts a C2 server after January 2027." Design the environment to test that theory specifically.

**Layer instrumentation carefully.** Every monitoring tool added is a potential detection vector. Balance observation capability against detection risk. Sometimes less instrumentation yields more authentic behavior.

**Document the scaffold.** The environment configuration is part of the observation provenance. What was set, what was simulated, what was monitored: all affect interpretation of results.

**Iterate.** First scaffold may not trigger the behavior. Refine based on what static analysis and initial dynamic runs reveal about the trigger conditions.

## Atom Categories Most Enabled

ENVI (scaffolding directly addresses environment gates), TIME (clock manipulation activates time bombs), NETW (network simulation enables safe observation of C2/exfiltration), PRST (isolated environments allow persistence to install without risk)

## Atom Categories Least Relevant

ARTF (embedded artifacts are visible in source, no scaffolding needed), XFRM (transformation patterns are visible statically), PKGM (package metadata is visible through registry APIs)
