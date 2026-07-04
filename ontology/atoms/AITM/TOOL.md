# AITM.TOOL: AI Tool / Schema Definition

## Description

Tool definitions, MCP server configurations, or API schemas that are provided for use by AI agent systems. The atom describes the presence of tool definitions, their structure, declared capabilities, parameter requirements, and implementation routing. Includes MCP servers, function-calling tool definitions, plugin manifests, and API schemas designed for AI agent consumption.

Tool definitions specify what an AI agent can do through the tool (name, description, parameters), what the tool claims to do (human-readable descriptions), and where the tool routes its implementation (server endpoints, local executables, shell commands). The definition may be declared in JSON, YAML, TOML, or language-native configuration structures. The tool may be registered in a local agent configuration, distributed via a package, or fetched from a remote registry.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | MCP server configuration files (`mcp.json`, `claude_desktop_config.json`), tool definition schemas with `name`/`description`/`parameters`/`inputSchema` structures, function-calling definitions (`tools` arrays with JSON Schema), AI plugin manifests (`ai-plugin.json`, `.well-known/ai-plugin.json`), OpenAPI specs with `x-ai-*` extensions |
| Static Binary | Partial | Embedded JSON/YAML tool definition structures in data sections, less common because tool definitions are typically in configuration files rather than compiled code |
| Runtime/Dynamic | Yes | Tool registration API calls, MCP server startup and tool listing responses, dynamic tool schema generation, agent tool registry population at runtime |

## Disambiguation

- **vs normal API schemas**: `AITM.TOOL` applies to schemas and definitions specifically structured for AI agent consumption, they contain the metadata (natural language descriptions, parameter schemas, capability declarations) that AI systems use to decide when and how to invoke the tool. A standard REST API with OpenAPI documentation is not `AITM.TOOL` unless the schema includes AI-agent-specific extensions or is packaged as a tool definition for an agent framework.
- **vs AITM.INJECT**: `AITM.TOOL` describes the structural presence of tool definitions. `AITM.INJECT` describes embedded directives targeting AI behavior. A tool definition that also contains injected instructions in its description fields carries both atoms, `AITM.TOOL` for the tool structure and `AITM.INJECT` for the embedded directives.
- **vs NETW.\***: Tool definitions that route to network endpoints describe a declared communication path. The declaration is `AITM.TOOL`; actual network communication at runtime is `NETW.*`. Both may apply when a tool definition is observed and the tool is also invoked.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` / `NETW.WS` (tool implementation routes to network endpoint), `EXEC.SHELL` / `EXEC.PROC` (tool implementation executes local commands), `FSYS.READ` / `FSYS.WRITE` (tool implementation accesses filesystem), `AITM.INJECT` (directive content embedded in tool descriptions), `AITM.CONTEXT` (misleading documentation about tool behavior)
- **May imply**: The package or project is designed to interact with AI agent systems; the tool definitions provide the interface through which agents operate
- **Commonly part of idioms**: MCP server package (tool definitions + server implementation + transport layer), AI agent plugin (manifest + tool schemas + implementation routing), proxy tool (tool definition that re-routes agent actions through an intermediary)

## Notes

`AITM.TOOL` applies to ALL AI tool definitions as a structural observation. The atom describes what is present in the code: tool definitions with their declared capabilities, parameter schemas, and routing. The MCD lens and other analytical lenses determine which tool definitions are suspicious based on factors like parameter scope exceeding stated function, implementation routing to unexpected infrastructure, description content that manipulates agent behavior, or capability declarations inconsistent with the package's purpose. A legitimate MCP server and a malicious MCP proxy both carry `AITM.TOOL`; the difference is in the co-occurring atoms and the interpretive lens applied.
