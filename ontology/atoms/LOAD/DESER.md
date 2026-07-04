# LOAD.DESER: Unsafe Deserialization

## Description

Deserializes data into executable objects using formats that support code execution during reconstruction: Python `pickle`/`shelve`, Java `ObjectInputStream`, Ruby `Marshal`, PHP `unserialize()`, YAML `load()` (with code execution), .NET `BinaryFormatter`. Code execution occurs as a side effect of the deserialization process via lifecycle hooks (`__reduce__` in pickle, `readObject()` in Java). There is no explicit eval call; execution is implicit in the object reconstruction.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | `pickle.loads()`, `ObjectInputStream.readObject()`, `Marshal.load()`, `yaml.load()` (vs `yaml.safe_load()`), `BinaryFormatter.Deserialize()`, `unserialize()` |
| Static Binary | Yes | Deserialization function imports, serialized data format markers |
| Runtime/Dynamic | Yes | Object reconstruction, lifecycle hook execution, new objects created from serialized data |

## Disambiguation

- **vs LOAD.EVAL**: Eval explicitly executes code strings. Deserialization achieves code execution implicitly through object graph reconstruction. The mechanism is different, no `eval` call appears in the code path.
- **vs safe deserialization**: JSON, `yaml.safe_load()`, `RestrictedUnpickler`, `ObjectInputFilter` with a strict allowlist, these constrain or eliminate the code execution surface. The atom applies specifically when the deserialization format and configuration permit arbitrary code execution.

## Structural Relationships

- **Often co-occurs with**: `NETW.*` (serialized data from network), `FSYS.READ` (serialized data from file), `XFRM.ENCODE` (serialized data also encoded), `LOAD.REFLECT` (deserialization gadget chains use reflection)
- **May imply**: Data from some source is being reconstructed into live objects with potential side effects

## Notes

The serialization format, the source of the serialized data, and the presence/absence of class restrictions are the key structural data. `pickle.loads(untrusted_data)` with no restricted unpickler is the highest-risk configuration. The same data through `json.loads()` has no code execution surface. Format choice is the primary structural differentiator.
