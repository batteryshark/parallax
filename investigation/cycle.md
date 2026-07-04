# Investigation Cycle

The investigation cycle is the process that turns observations into useful understanding.

It is intentionally iterative. A first scan should not pretend to know the truth. It should produce claims, confidence levels, gaps, and the next best ways to learn more.

## Inputs

- target system or repository
- active lenses
- available observation methods
- existing observations and enrichment
- practitioner context, such as "dependency review", "incident triage", "agent permission audit", or "architecture review"

## Outputs

- normalized ontology observations
- structural relationships between observations
- lens findings
- confidence assessments
- disproof criteria
- verification plan
- response or mitigation recommendation when warranted

## Loop

### 1. Scope The Question

Define why the system is being investigated.

Examples:

- Is this dependency malicious?
- Where is this generated code brittle?
- What can this agent toolchain do if abused?
- Which repos in this org have install-time side effects?

Scope determines active lenses, but it does not change the ontology. Observations remain judgment-free.

### 2. Gather Observations

Run one or more methods of observation:

- static source
- static binary
- dynamic
- OSINT
- build/CI
- network
- scaffolding

Each method produces observations with its own strengths and blind spots.

### 3. Normalize To Ontology

Convert raw evidence into atoms and idioms.

The normalization step should not decide whether behavior is good or bad. It should only say what behavior was observed, where, how, and with what confidence.

### 4. Build Relationships

Record structural relationships:

- same scope
- calls
- called by
- dataflow
- manifest entrypoint
- runtime confirmation
- package dependency relationship

This step determines whether observations are merely near each other or actually compose.

### 5. Interpret Through Active Lenses

Each active lens evaluates the same observations independently.

One observation can produce multiple findings:

- `NETW.HTTP` in an install script can be an MCD supply-chain signal.
- The same observation can be an architecture build-fragility signal.
- The same observation can be a capability external-communication surface.

### 6. Assess Confidence

For each lens claim, assess:

- required evidence present
- supporting evidence present
- reachability strength
- method provenance
- enrichment alignment
- missing evidence
- contradictory evidence
- disproof criteria

Confidence applies to the lens claim, not to the raw observation.

### 7. Select Verification

Generate verification tasks that can change confidence.

A good verification task includes:

- the question being answered
- the method that can answer it
- why the current method cannot answer it
- what observation would increase confidence
- what observation would decrease or disprove confidence
- expected cost or risk of the method

### 8. Execute Verification

Run the selected method manually or automatically.

Examples:

- dynamic sandbox run to confirm install-time network traffic
- OSINT lookup for a destination domain
- build reproducibility check
- static dataflow trace
- network capture
- CI workflow review

### 9. Re-Evaluate

Feed new observations and enrichment back into the ontology layer. Re-run all active lenses.

Confidence can go up or down. A finding that cannot be disproved is not a good finding.

### 10. Respond Or Monitor

When confidence is sufficient, move from investigation to response.

Response is lens-specific:

- MCD: close, monitor, refer to engineering, alert, or contain
- Architecture: refactor, test, document, isolate, or simplify
- Capability: restrict, sandbox, gate, monitor, or remove permission

If confidence is not sufficient and additional methods are not available, record the residual uncertainty explicitly.

## Stop Conditions

An investigation can stop when:

- confidence reaches a response threshold
- a claim is disproved
- available methods are exhausted
- the expected value of more investigation is lower than the response cost
- a practitioner decides the residual uncertainty is acceptable

Stopping should preserve the current state: what is known, what is inferred, what is unknown, and what would reopen the assessment.

## Finding States

Tooling should track finding lifecycle states:

| State | Meaning |
|---|---|
| `observed` | Raw behavior has been identified. |
| `hypothesized` | A lens has produced an initial interpretation. |
| `verified` | Additional evidence supports the interpretation. |
| `disproved` | Evidence contradicts or invalidates the interpretation. |
| `monitored` | Finding is not actionable now but could change. |
| `actioned` | Response or mitigation has been taken. |

## Tooling Implication

Parallax should optimize for better next questions, not just louder alerts.

Every report should make the investigation state visible:

- what was found
- what it suggests
- how sure the tool is
- what evidence is missing
- what would change the assessment
- what should happen next

