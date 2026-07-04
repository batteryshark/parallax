# ARTF.TIMESTAMP: Embedded Date/Time Value

## Description

Specific timestamps, dates, or datetime values embedded in source or binary as string literals, numeric constants, or structured date objects. Includes ISO 8601 strings (`2025-06-15T00:00:00Z`), Unix epoch values (integer or float seconds since 1970-01-01), date component literals (year/month/day integers in date construction), RFC 2822 formatted dates, and locale-specific date strings. The artifact is the temporal value itself, a fixed point in time or date range embedded in the code.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | ISO 8601 date strings, Unix epoch integer constants (10-digit or 13-digit for milliseconds), `datetime(2025, 6, 15)` constructors, `Date.parse("...")` arguments, date comparison constants, cron expressions with specific dates |
| Static Binary | Yes | Date-format strings in data sections, large integer constants consistent with Unix epoch ranges, structured date bytes |
| Runtime/Dynamic | Yes | Timestamp constants used in date comparisons, time-based conditional branches, expiration checks, scheduled activation logic |

## Disambiguation

- **vs TIME.CMP**: `ARTF.TIMESTAMP` is the static presence of a temporal value in code or binary. `TIME.CMP` is the runtime operation of comparing the current time against a value. When code checks `if datetime.now() > datetime(2025, 6, 15)`, the embedded date is `ARTF.TIMESTAMP` and the comparison operation is `TIME.CMP`. The timestamp is the artifact; the comparison is the behavior.
- **vs generic integer constants**: Unix epoch timestamps are large integers (e.g., `1718409600` for 2024-06-15). Not all large integers are timestamps. Context determines classification, assignment to time-related variables, use in date construction or comparison functions, or proximity to time API calls disambiguates.

## Structural Relationships

- **Often co-occurs with**: `TIME.CMP` (timestamp used in temporal comparison), `ENVI.TIMING` (timestamp as part of timing-based behavior), `XFRM.ENCODE` (timestamp encoded to avoid detection), `NETW.*` (timestamp-gated network activity)
- **May imply**: The code contains time-dependent logic, activation dates, expiration checks, or scheduling constraints that depend on the current time relative to the embedded value

## Notes

The temporal relationship between the embedded value and the present carries structural information. Past dates may represent version markers, build timestamps, or epoch boundaries. Future dates in comparison logic indicate activation or expiration thresholds. Date ranges define operational windows. The granularity of the timestamp (date-only vs. second-precision vs. millisecond-precision) indicates the temporal precision of the dependent logic. These are factual properties of the embedded value, useful for analysis regardless of lens.
