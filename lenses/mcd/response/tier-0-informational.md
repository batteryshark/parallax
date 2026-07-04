# Tier 0: Informational / Close

## When to Use

The finding has been investigated and is confirmed benign. The observations that triggered the finding have a clear, legitimate explanation consistent with the code's stated purpose. There is no proximity to harm: the code is not "one change away" from matching a malicious composition.

## Actions

1. **Document the finding and the investigation outcome.** Record what was observed, what was investigated, and why it was closed. This creates an audit trail and prevents the same finding from consuming investigation time in future cycles.
2. **Close the finding.** Remove it from active tracking.
3. **No monitoring required.** The finding does not warrant ongoing attention.

## Examples

- A `NETW.HTTP` observation in a package whose documented purpose is making HTTP requests.
- An `ARTF.URL` pointing to the package's own documented API endpoint.
- A `CRPT.HASH` in a package that provides integrity verification as a stated feature.
- A `XFRM.ENCODE` triggered by standard frontend JavaScript minification.

## Escalation Trigger

If a future code change materially alters the context around a closed finding (for example, the HTTP request target changes from a documented API to an unknown IP), the finding should be reopened and reassessed. This is not automatic monitoring; it is triggered by re-scanning after code changes.
