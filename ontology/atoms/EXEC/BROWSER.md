# EXEC.BROWSER: Browser Automation

## Description

Code that drives a real web browser through an automation framework: Puppeteer, Playwright, Selenium / WebDriver, ChromeDriver, pyppeteer, or a direct `chromium` / `firefox` `launch`. A controlled browser is a distinct capability from spawning an arbitrary process. It can navigate, scrape rendered pages, fill and submit forms, intercept and replay network traffic, execute arbitrary script in page context, download files, and, if pointed at the user's real profile, act inside already-authenticated sessions. The structural observation is the use of a browser-automation entry point; what it then does is the reach.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | An import or call into a browser-automation framework (`puppeteer.launch`, `playwright.chromium.launch`, `webdriver.Chrome`, `selenium`, `chromedriver`, `pyppeteer.launch`). |
| Static Binary | Partial | Bundled browser binaries or driver executables, and framework strings, show up in binary triage. |
| Runtime/Dynamic | Yes | A spawned browser process plus the pages it navigates and the network it generates. |

## Disambiguation

- **vs EXEC.PROC**: `EXEC.PROC` is spawning an arbitrary process. `EXEC.BROWSER` is the narrower, higher-context act of driving a browser. They are kept as separate capability surfaces so a pure automation tool is not mislabeled as general command execution, and a tool that does both shows both.
- **vs NETW.HTTP**: A browser makes network requests, but its reach is broader than an HTTP client: it renders, runs page scripts, and can carry the user's session. Treat it as its own surface, not just network.
- **vs a test harness**: Browser automation in a test suite is usually benign. The capability is real either way; intent is a lens judgment, and the guardrail (throwaway profile, allowlisted origins) is what de-escalates it.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (the traffic it generates), `FSYS.WRITE` (downloads / screenshots), `AITM.*` (an agent tool that exposes a browser), `CRED.*` (reaching authenticated sessions)
- **May imply**: Steerable data exfiltration and authenticated-session access when an agent can influence where the browser goes

## Notes

For agentic systems this is a high-reach surface: an agent that can be steered (prompt injection, tool poisoning) and that holds a browser tool can be driven to navigate to attacker pages, read authenticated content, and exfiltrate through ordinary-looking web traffic. The capability lens names it as `CAP-BROWSER`; the agentic profile treats it as reachable-if-steered alongside command execution and network.
