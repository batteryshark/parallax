# NETW.WEBHOOK: Webhook / Messaging API

## Description

Sends data to messaging platform webhook endpoints via HTTP POST to platform-provided callback URLs. Target platforms include Discord (webhook URLs), Telegram (Bot API), Slack (incoming webhooks), Microsoft Teams (connectors), and similar services. The defining characteristic is the use of a platform-specific webhook URL pattern as the destination, which routes the data to a channel or conversation controlled by whoever created the webhook.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Webhook URL patterns (`https://discord.com/api/webhooks/...`, `https://api.telegram.org/bot.../sendMessage`, `https://hooks.slack.com/services/...`), HTTP POST to these endpoints, message payload construction matching platform schema |
| Static Binary | Partial | Webhook URL string literals or fragments, platform API endpoint patterns |
| Runtime/Dynamic | Yes | HTTP POST requests to known webhook URL patterns, JSON payloads matching platform message schemas |

## Disambiguation

- **vs NETW.HTTP**: `NETW.WEBHOOK` is a specialized form of `NETW.HTTP`. The transport is HTTP POST, but the destination is specifically a messaging platform webhook endpoint. The distinction matters because the webhook URL itself identifies the receiving infrastructure: whoever created the webhook controls where data goes.
- **vs NETW.EMAIL**: Both deliver messages, but via different mechanisms. Webhooks use HTTP to platform APIs. Email uses SMTP or email service APIs.

## Structural Relationships

- **Often co-occurs with**: `CRED.*` (credentials included in webhook payload), `ARTF.URL` (the webhook URL itself), `XFRM.ENCODE` (encoded payload content), `SYSI.*` (system information gathered and sent via webhook)
- **May imply**: The webhook URL is controlled by someone with access to the target platform channel/workspace

## Notes

Webhook URLs are self-contained credentials: the URL itself provides write access to the target channel without additional authentication. The URL pattern identifies both the platform and the specific destination. Discord webhooks contain a numeric ID and token. Telegram Bot API URLs contain the bot token. Slack webhook URLs contain workspace and channel identifiers.
