# ARTF.EMAIL: Embedded Email Address

## Description

Email addresses present as string literals in source or binary. The artifact is the address itself, a `local-part@domain` identifier conforming to RFC 5321 addressing. Includes addresses in code comments, string constants, configuration defaults, contact information, and SMTP envelope parameters. May appear as full addresses or as components assembled at runtime.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals matching `*@*.*` patterns, email validation regex containing test addresses, SMTP envelope construction (`MAIL FROM:`, `RCPT TO:`), `mailto:` URI schemes |
| Static Binary | Yes | Email-format strings in data sections, `@` followed by domain-format strings |
| Runtime/Dynamic | Yes | Email addresses passed to SMTP libraries, used in HTTP form submissions, included in notification payloads |

## Disambiguation

- **vs ARTF.DOMAIN**: An email address contains a domain component after the `@`. Both `ARTF.EMAIL` and `ARTF.DOMAIN` may apply if the domain is independently significant. The email is the complete mailbox identifier; the domain is the host component.
- **vs NETW.EMAIL**: `ARTF.EMAIL` is the static presence of an email address string. `NETW.EMAIL` is the runtime behavior of sending email via SMTP or email API. An embedded address may be used for notification, error reporting, contact display, or as a recipient in a send operation.

## Structural Relationships

- **Often co-occurs with**: `NETW.EMAIL` (address used as SMTP recipient), `NETW.HTTP` (address submitted via HTTP API), `ARTF.DOMAIN` (domain component of the address), `XFRM.ENCODE` (email address encoded to avoid detection)
- **May imply**: The code has a fixed contact point, notification target, or registration identity

## Notes

The domain portion of the email address indicates the mail provider or organization. Free providers (gmail.com, outlook.com, protonmail.com) versus organizational domains carry different contextual weight. The local-part may contain identifiers, role names, or generated strings. These are structural properties of the address useful for characterization.
