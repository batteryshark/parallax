# Confidence Algebra

Structural rules for how evidence composes into assessments. These mechanics are shared across all lenses; each lens parameterizes them differently, but the underlying algebra is the same.

## Severity

Severity reflects how noteworthy an observation is **in isolation**, before considering combinations or context. It is a property of the observation relative to the lens, not a property of the code.

| Level | Meaning |
|---|---|
| **Informational** | Commonly seen in software. Only meaningful in combination with other observations. |
| **Low** | Unusual in the specific context but has common benign explanations. |
| **Medium** | Warrants investigation. Multiple plausible interpretations exist; additional evidence needed to distinguish. |
| **High** | Rarely benign in the observed context. Should trigger active investigation. |
| **Critical** | Almost never benign. Immediate attention warranted regardless of confidence level. |

Severity is lens-defined. The same atom at the same severity level means different things to different lenses. `EXEC.INJECT` is Critical through the MCD lens (code injection is almost never benign in a dependency) but might be Medium through an architecture lens (DI frameworks use injection legitimately, but it's worth flagging).

## Confidence

Confidence reflects certainty that an interpretation is **actually correct**, considering all available evidence. It is not about the observation; it's about the lens's claim.

| Level | Meaning |
|---|---|
| **Low** | Interpretation partially supported. Some expected observations present but required elements may be ambiguous or missing. |
| **Medium** | All required observations present with plausible reachability. Supporting observations may or may not be present. |
| **High** | All required observations present with confirmed reachability. Multiple supporting observations present. Enrichment aligns. |

Confidence is always a spectrum, not a category. The levels above are convenient shorthand for communication, but the underlying assessment is continuous.

## Composition Rules

### Reachability

Observations must be connected through plausible execution flow to compose into an idiom or pattern. Co-location is not composition.

Two atoms in the same file are structurally proximate. Two atoms connected by data flow and control flow are reachable. Only reachable combinations contribute to confidence in a composition. Co-location without reachability is suggestive but not evidentiary.

**Reachability sources (strongest to weakest):**
1. Confirmed execution trace (dynamic analysis)
2. Verified control flow path (static analysis with resolved branches)
3. Plausible control flow path (static analysis, unresolved branches)
4. Same function/method scope
5. Same module, connected through call graph
6. Same package, no demonstrated connection

### Cross-Category Accumulation

Corroborating observations from different ontology categories are more significant than multiple observations from the same category.

Three `FSYS.*` atoms in the same scope tell you the code does a lot of filesystem work. `FSYS.READ` + `CRED.SSH` + `NETW.HTTP` in the same scope tells you the code reads files, accesses SSH credentials, and makes HTTP requests: a cross-category combination that is structurally more informative regardless of which lens is interpreting it.

**Accumulation principle:** Each additional category represented in a reachable composition adds more interpretive weight than additional atoms from an already-represented category.

### Idiom Recognition

Atoms that form a recognized idiom carry more weight than disconnected atoms.

When a set of observations matches an idiom's constituent atoms with appropriate structural relationships, the idiom match subsumes the individual atom observations for interpretive purposes. The lens interprets the idiom as a unit rather than interpreting each atom independently.

Idiom matches are probabilistic. Partial matches (most but not all constituent atoms present) are valid observations at reduced confidence. The confidence spectrum for idiom matching:
- **Strong match:** All constituent atoms present with confirmed reachability and expected structural relationships
- **Probable match:** Most constituent atoms present; missing atoms are plausibly present but unobserved (method blind spot) or ambiguous
- **Partial match:** Some constituent atoms present in expected relationships; others absent or substituted
- **Structural similarity:** Atom composition resembles an idiom but with significant deviations

### Provenance Weighting

Observations confirmed by multiple methods are stronger than single-method observations.

Each method of observation has structural capabilities and blind spots. An observation from static source analysis is one data point. The same observation confirmed by dynamic analysis is two independent data points from methods with different blind spots, substantially stronger evidence.

**Provenance rules:**
- Multi-method confirmation increases confidence in the observation itself
- A method's blind spots define what it *cannot* disprove: absence of evidence from a method that cannot see the relevant behavior is not evidence of absence
- Contradictory observations from different methods demand investigation: one method is seeing something the other cannot, or one is producing a false signal

### Enrichment Integration

Enrichment data modifies confidence in structured ways. Enrichment is facts; interpretation is the lens's job.

**Enrichment effects on confidence:**
- **Amplifying:** Enrichment aligns with the lens's interpretation, increasing confidence. (MCD example: domain registered 28 days ago amplifies confidence in a suspicious `NETW.HTTP` finding)
- **Attenuating:** Enrichment provides alternative explanation, decreasing confidence. (MCD example: package maintainer is a known contributor to the parent project attenuates suspicion of a new dependency)
- **Neutral:** Enrichment is irrelevant to this lens's interpretation. (Architecture lens: domain age is neutral; the architecture concern is the external dependency itself, not who owns it)

Each lens defines which enrichment data is amplifying, attenuating, or neutral for its interpretations. The same enrichment datum can have different effects across lenses.

### Disproof Handling

Evidence against a hypothesis reduces confidence. The framework explicitly tracks what would disprove a current assessment.

**Disproof principles:**
- Every composition and idiom match should have identifiable disproof criteria: observations or enrichment that, if found, would invalidate or substantially weaken the interpretation
- Confidence is not monotonically increasing. New evidence can and should reduce confidence when it contradicts the current assessment
- A lens that cannot articulate what would disprove its interpretation is making an unfalsifiable claim; treat with appropriate skepticism
- Disproof from one lens does not automatically disprove other lenses' interpretations of the same observations

## Severity Modifiers

Certain observation categories act as severity modifiers: their presence changes how other co-occurring observations are assessed.

This is a structural property of the algebra, but **which categories are modifiers and in which direction is lens-defined.** The shared mechanic is: some observations don't just add to the picture, they change how the rest of the picture is interpreted.

**Modifier mechanics:**
- A modifier amplifies or attenuates severity of co-occurring observations
- Modifiers apply to reachable observations only (same reachability rules as composition)
- Multiple modifiers compound but do not stack linearly; diminishing returns apply
- A modifier without anything to modify is itself just an observation at its own baseline severity

## Assessment Lifecycle

Assessments are not static. They evolve as new evidence arrives.

1. **Initial assessment:** First observations interpreted through active lenses, producing initial severity and confidence
2. **Refinement:** Verification produces new observations; all lenses re-evaluate; confidence adjusts up or down
3. **Stabilization:** Assessment converges as available evidence saturates; further verification yields diminishing returns
4. **Reassessment trigger:** New observations (code change, new enrichment, environmental change) reopen the assessment

The algebra does not prescribe when to stop investigating. That is a lens-specific threshold decision combined with practitioner judgment.
