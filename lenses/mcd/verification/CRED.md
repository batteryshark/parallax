# MCD Lens: CRED (Credential and Secret Access) Verification

## General: Any CRED Atom

1. **Where in the lifecycle does credential access occur?** Install, import, or explicit function call? `[lens-neutral]`

2. **Is the credential material transmitted over the network?** Trace the variable holding credential data through the codebase to any network call, file write, or encoded output. `[lens-neutral]`

3. **What is the package's stated purpose, and does it explain this credential access?** Justification must be specific. `[MCD]`

4. **Was credential access present in previous versions?** Newly introduced credential access in a maintenance update is high-confidence supply chain compromise. `[lens-neutral]`

5. **How many distinct credential stores or types are accessed?** Single targeted access vs. multi-store sweep. `[lens-neutral]`

## CRED.CLOUD

6. **Does the package have documented cloud provider integration?** `[MCD]`

7. **Is access via official SDK credential chain or direct file reads?** `[lens-neutral]`

## CRED.BROWSER

8. **What specific browser database is targeted?** `Login Data`, `Cookies`, `Web Data`, `Local State`? `[lens-neutral]`

9. **Does the package have documented browser integration?** `[MCD]`

## CRED.ENV

10. **Specific named variables or scanning all env vars?** Bulk scanning with pattern matching = systematic harvesting. `[lens-neutral]`

11. **What happens to the value after read?** Used locally vs. transmitted. `[lens-neutral]`

## CRED.SSH

12. **Is SSH key access combined with network reconnaissance or non-C2 connections?** Suggests lateral movement intent. `[MCD]`
