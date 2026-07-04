# Build & CI Analysis

Examination of build pipelines, CI/CD configurations, and the process that transforms source into distributed artifacts.

## Capabilities

- **Build reproducibility:** Can the published artifact be reproduced from the published source using the documented build process?
- **Source-to-artifact drift:** Differences between expected build output and actual distributed artifact: extra files, modified binaries, injected code
- **Pipeline integrity:** CI/CD configuration review: who can trigger builds, what secrets are accessible, what steps execute, what has changed recently
- **Build-time execution:** What runs during the build: install scripts, pre/post-build hooks, code generation, asset downloads
- **Artifact provenance:** Signing chains, attestation documents (SLSA, Sigstore), build environment metadata
- **Dependency resolution:** What actually gets installed during build vs. what's declared: resolution of version ranges, platform-specific dependencies
- **Secret exposure:** Whether build logs, artifacts, or intermediate outputs leak credentials, tokens, or internal infrastructure details

## Blind Spots

- **Runtime behavior:** Build analysis sees how artifacts are produced, not how they behave when deployed
- **Post-distribution modification:** Cannot detect if artifacts are modified between the build system and the end user (distribution chain attacks)
- **Legitimate build complexity:** Complex build systems (multi-stage Docker, cross-compilation, generated code) make reproducibility verification genuinely difficult; irreproducibility is not proof of tampering
- **Build environment opacity:** Hosted CI/CD runners are controlled by the platform; build environment integrity depends on platform trust

## Tools

Build system analysis (Makefile/CMake/Gradle inspection), CI/CD configuration review (GitHub Actions, GitLab CI, Jenkins), container image analysis (dive, docker inspect), reproducible build frameworks (reprotest, diffoscope), provenance verification (cosign, slsa-verifier), dependency lock file auditing.

## When to Use

- **Source-to-binary drift detection:** When static binary analysis reveals differences from expected source-compiled output
- **Supply chain investigation:** When the question is "was this built from the source it claims?", particularly for pre-compiled dependencies
- **Pipeline compromise assessment:** When maintainer account compromise or CI/CD targeting is suspected
- **Post-incident analysis:** When a compromise has been confirmed and you need to determine the injection point in the build pipeline

## When to Transition Away

- **Code-level concerns:** When build analysis reveals unexpected build steps that produce suspicious code → transition to **static source/binary analysis** of the produced artifacts
- **Runtime verification:** When build output looks clean but runtime behavior is suspicious → transition to **dynamic analysis**
- **Infrastructure investigation:** When build configuration references unknown infrastructure → transition to **OSINT**

## MCD Relevance

Build & CI analysis is the primary method for detecting source-to-binary drift, one of the MCD lens's six signal categories. It also provides evidence for the package metadata signal category (publication pipeline anomalies) and is the method most relevant to `PKGM.*` atom verification.

The CI/CD environment is also a high-value target (`ENVI.ENVCHECK` for CI variables); build analysis can reveal whether code specifically targets the build environment as an operating context.

## Atom Categories Most Visible

PKGM (build hooks, dependency manipulation, publication metadata), ARTF (embedded in build outputs), LOAD (build-time code generation), ENVI (CI/CD environment targeting)

## Atom Categories Least Visible

CRED (credential access is runtime), PRST (persistence is runtime), NETW (actual network behavior is runtime, though build-time network access is visible)
