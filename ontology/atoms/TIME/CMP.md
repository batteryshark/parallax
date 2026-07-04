# TIME.CMP: Time Comparison

## Description

Compares the current time against a specific date, timestamp, time range, or temporal threshold. The conditional logic that enables "activate after date X" or "only run during time window Y." The comparison target may be a hardcoded literal value (embedded date string, epoch constant), a computed value (current time minus duration), or a value retrieved from an external source (config file, server response, environment variable). The comparison produces a boolean outcome that gates subsequent behavior.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Comparison operators against time values (`if date > datetime(2026, 6, 1)`, `if (Date.now() > 1717200000000)`), date/time parsing functions feeding conditionals, hardcoded date strings or epoch constants near comparison logic |
| Static Binary | Yes | Comparison instructions following time retrieval calls, hardcoded timestamp constants in data sections, date string literals adjacent to conditional branch targets |
| Runtime/Dynamic | Yes | Conditional branches taken or not taken based on temporal values, time retrieval followed by comparison instruction, divergent execution paths depending on system clock |

## Disambiguation

- **vs TIME.GET**: `TIME.GET` retrieves a temporal value without conditional logic. `TIME.CMP` requires a comparison operation, the time value is tested against a threshold and the result gates a branch. If data-flow analysis shows a retrieved time value flowing into a comparison, the finding is `TIME.CMP`, not `TIME.GET`.
- **vs ENVI.TIMING**: `TIME.CMP` checks calendar/clock time, dates, deadlines, time-of-day windows. `ENVI.TIMING` measures execution duration, how long something takes, how long to wait. "If today is after June 1st" is `TIME.CMP`. "If this function took longer than 200ms" is `ENVI.TIMING`. The distinction is clock time vs. elapsed time.
- **vs ENVI.ENVCHECK**: When a time comparison targets a CI/CD environment's build timestamp or checks whether code is running during business hours to avoid analysis, the behavior bridges `TIME.CMP` (the temporal comparison) and `ENVI.ENVCHECK` (the environment-aware gating). Both may apply.

## Structural Relationships

- **Often co-occurs with**: `TIME.GET` (retrieves the time value being compared), `ARTF.TIMESTAMP` (hardcoded date or epoch constant used as comparison target), conditional branches gating any subsequent behavior
- **May imply**: A hardcoded comparison target is an embedded artifact (`ARTF.TIMESTAMP`), and the gated behavior is the payload or feature that activates on the condition

## Notes

The comparison target is the key structural data. A hardcoded future date literal is the canonical logic bomb signature. A configurable threshold read from a config file or API is a feature toggle or trial expiration. A relative comparison ("more than 30 days since install") is a time-delayed activation. The comparison operator matters too: greater-than implies "activate after," less-than implies "active until," and range checks imply a time window. The gated behavior, what executes when the comparison passes, determines the significance of the finding.
