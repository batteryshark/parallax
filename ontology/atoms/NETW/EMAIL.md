# NETW.EMAIL: Email Transmission

## Description

Sends email programmatically via SMTP, IMAP (for drafts/sent folder manipulation), or email service APIs (SendGrid, SES, Mailgun). Encompasses direct SMTP connection setup, authentication, and message transmission, as well as API-mediated email delivery.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | SMTP library imports (`smtplib`, `nodemailer`, `javax.mail`), email service SDK usage, SMTP server addresses and port numbers (25, 465, 587), email construction (To, From, Subject, Body) |
| Static Binary | Partial | SMTP library imports, email-related string constants, server address literals |
| Runtime/Dynamic | Yes | SMTP connections on ports 25/465/587, email protocol handshakes, message content on the wire (if not TLS) |

## Disambiguation

- **vs NETW.HTTP**: Email service APIs (SendGrid, SES) use HTTP as transport. If the code uses a dedicated email SDK or constructs email-specific payloads (MIME, RFC 5322), it's `NETW.EMAIL`. If it makes a generic HTTP POST to an API endpoint that happens to send email, it's both `NETW.HTTP` and `NETW.EMAIL`.
- **vs NETW.WEBHOOK**: Webhooks POST data to messaging platforms. Email sends structured messages via SMTP or email APIs. The protocol and message format distinguish them.

## Structural Relationships

- **Often co-occurs with**: `CRED.*` (SMTP authentication credentials), `ARTF.URL` / `ARTF.IP` (SMTP server addresses), `FSYS.READ` (reading data to include in email body or attachments)
- **May imply**: SMTP credentials exist somewhere (hardcoded, environment, configuration)

## Notes

SMTP authentication credentials (username, password, API key) are required for most email transmission. The location and protection of these credentials is a structural observation. Direct SMTP on port 25 without authentication is unusual in modern environments and typically only works from servers with specific network configurations.
