# MCD Lens: TIME (Temporal Operations) Verification

Investigation questions for TIME findings. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## TIME.CMP: Activation Condition

1. **What is the exact comparison threshold, and is it hardcoded or derived?** Identify the specific date, timestamp, epoch value, or time range used in the comparison. A hardcoded date literal embedded in source is structurally different from a threshold read from configuration, computed at runtime, or retrieved from a server. Hardcoded values are forensic artifacts; derived values indicate configurable behavior. `[lens-neutral]`

2. **What executes after the time check passes?** Trace the true-branch (and false-branch) of the comparison. The gated behavior determines the significance of the temporal condition. A time check gating a deprecation warning is fundamentally different from one gating shell execution or network exfiltration. Map the complete set of operations reachable from both branches. `[lens-neutral]`

## TIME.DELAY: Duration and Proportionality

3. **Is the delay duration consistent with a legitimate operational requirement?** Identify the stated or inferable purpose of the delay (retry backoff, rate limiting, polling interval, initialization wait) and assess whether the duration is proportional. A 100ms retry delay in a network client is proportional. A 300-second delay in an install hook before a network call is not. Document both the duration and the operational context. `[lens-neutral]`

## Provenance and Introduction

4. **When was this time-dependent code introduced, and by whom?** Diff against prior versions to determine which commit introduced the temporal logic. Identify the author, the PR/commit context, and whether the change was reviewed. Time-based logic added in a version bump by a new contributor or compromised maintainer account is a different finding than logic present since initial release by the primary author. `[lens-neutral]`

## Dependency Context

5. **Does the time logic appear in a dependency rather than first-party code?** Time comparisons in application code may be product features (trial expiration, scheduled maintenance). Time comparisons in library or dependency code, especially transitive dependencies, have far fewer legitimate justifications. A dependency with a hardcoded activation date is a supply chain logic bomb until proven otherwise. `[MCD]`

## Reachability

6. **Is the time check reachable from normal execution paths?** Trace call chains from public API entry points, import-time execution, and install hooks to determine whether the time comparison is reachable during normal use. Dead code containing time checks may be staged for future activation or residual from removed functionality. Unreachable time logic in a new version warrants investigation even if it cannot currently fire. `[lens-neutral]`

## Convergence

7. **Are multiple independent time constraints present?** Look for combinations: date range AND time-of-day window, calendar check AND elapsed-time delay, multiple distinct timestamp comparisons gating different behaviors. Converging temporal conditions narrow the activation window and indicate deliberate operational scheduling rather than simple feature toggles. Multiple independent time gates in dependency code are a strong MCD signal. `[MCD]`

## Survivability

8. **Does the scheduled execution survive process termination?** For `TIME.SCHED` findings, determine whether the scheduling mechanism is in-process (dies with the process) or has been paired with OS-level persistence (`PRST.SCHED`). Test by terminating the host process and observing whether the scheduled callback still fires. If the scheduled execution survives, the finding is `PRST.SCHED`, not `TIME.SCHED`, and severity escalates accordingly. `[lens-neutral]`
