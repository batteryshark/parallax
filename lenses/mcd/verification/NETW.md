# MCD Lens: NETW (Network Communication) Verification

Investigation questions for NETW findings, organized for MCD triage. Questions tagged `[lens-neutral]` are applicable across multiple lenses. Questions tagged `[MCD]` assume an MCD evaluation context.

## General: Any NETW Atom

1. **Does the package's documentation or stated purpose include network functionality?** If not, why does this code make network calls? `[MCD]`

2. **When is the network call triggered?** Install time, import/module load, first use of any function, or only when the user explicitly invokes a network-facing feature? Earlier in the lifecycle is more significant. `[lens-neutral]`

3. **What data is included in the outbound payload?** Can the full payload be reconstructed statically, or does it require dynamic analysis? Does it include credentials, environment variables, or system identifiers? `[lens-neutral]`

4. **Who owns the destination endpoint?** Is the domain hardcoded, dynamically constructed, or user-supplied? What is the domain registration date and registrar? Does it share infrastructure with known actors? `[MCD]`

5. **Is there an inbound component?** Does the code receive and act on data returned from the network call? Is received data executed, written to disk, or passed to a deserializer? `[lens-neutral]`

## NETW.HTTP

6. **Does the HTTP request include headers or URL structures that mimic a trusted service?** Check for deliberate mimicry of legitimate API traffic patterns. `[MCD]`

7. **Is TLS certificate validation disabled?** Skipping certificate verification disables the primary protection against interception. `[lens-neutral]`

## NETW.DNS

8. **Does the code use the system resolver or a hardcoded alternative?** A hardcoded resolver IP bypasses system DNS configuration and monitoring. `[lens-neutral]`

9. **Are hostnames or query parameters constructed by encoding data into subdomain labels?** Extract and decode any such construction to determine what data is being transmitted via DNS. `[lens-neutral]`

## NETW.SOCKET

10. **After the socket is established, is there a loop reading from the socket and passing data to an execution function?** This is the structural pattern of a remote shell. `[lens-neutral]`

## NETW.LISTEN

11. **What interface does the listener bind to, and what happens to accepted connections?** `0.0.0.0` vs loopback. Are connections handed to a shell, a file server, or a command dispatcher? `[lens-neutral]`

## NETW.WEBHOOK

12. **What platform is the webhook for, and can the webhook URL be inspected?** The URL itself identifies receiving infrastructure. Identify the platform and, where possible, determine creation context. `[MCD]`

## NETW.DECENTRAL

13. **What is the specific decentralized address, canister ID, contract address, or IPFS CID?** Decentralized identifiers persist indefinitely. Document them in full as permanent evidence regardless of investigation outcome. `[MCD]`

## Cross-Cutting

14. **Does the network behavior match a known real-world attack pattern?** Compare the combination of NETW atoms, payload content, and trigger timing against documented supply chain incidents (Axios npm, LiteLLM/TeamPCP). Pattern matching against known campaigns increases MCD confidence. `[MCD]`

15. **Can the network destination be reached and inspected safely?** If the endpoint is still live, what does it serve? If it's down, is there archived content or DNS history? Destination investigation often resolves ambiguity more efficiently than deeper code analysis. `[MCD]`
