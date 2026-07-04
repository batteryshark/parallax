# LOAD.CODEGEN: Runtime Code Generation

## Description

Generates and executes new code at runtime: JIT compilation, AST manipulation and compilation, bytecode generation, writing and importing temporary modules, or constructing callable objects from runtime data. Distinguished from `LOAD.EVAL` in that codegen CREATES new executable content rather than interpreting an existing string, the generated code may have no direct textual representation in the source.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `compile()` + `exec()`, AST manipulation (`ast.parse()`, node construction), bytecode assembly, `types.CodeType()` construction, template engine compilation |
| Static Binary | Partial | Code generation API imports, compiler/assembler function references |
| Runtime/Dynamic | Yes | New code objects appearing in memory, dynamically compiled modules, JIT compilation events |

## Disambiguation

- **vs LOAD.EVAL**: Eval interprets an existing string. Codegen creates new executable artifacts (bytecode, native code, AST nodes) that may not have a simple string representation. `eval("1+1")` is EVAL. `compile(ast_tree, ...)` followed by `exec()` is CODEGEN.
- **vs normal compilation**: Compilers and build tools generate code as their core function. `LOAD.CODEGEN` applies when application-level or library-level code generates executable content at runtime, not when a build tool does so at build time.

## Structural Relationships

- **Often co-occurs with**: `LOAD.EVAL` (codegen output passed to eval), `NETW.*` (generated code incorporating network-sourced data), `XFRM.*` (generated code assembled from transformed inputs)
- **May imply**: The actual executable code is created at runtime and is not present in the distributed artifact

## Notes

Template engines (Jinja2, Handlebars, ERB), ORMs that generate SQL or query objects, and JIT compilers are common legitimate users of runtime code generation. The structural data points are: what inputs feed the generation, whether the generated code is executable (vs. data like SQL queries), and whether the generator is a well-known framework or ad-hoc logic.
