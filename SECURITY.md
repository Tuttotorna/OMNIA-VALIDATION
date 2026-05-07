# Security Policy

OMNIA-VALIDATION currently uses a minimal dependency surface and relies mainly on the Python standard library.

## Reporting Security Issues

Do not publish exploit details in public issues.

Report suspected security problems to the repository maintainer.

## Scope

Security-relevant issues include:

```text
unsafe file handling
path traversal
secret exposure
malicious artifact generation
hash-validation bypass
dependency-risk introduction

Boundary

OMNIA-VALIDATION does not certify production safety.

measurement != inference != decision

Dopo questo abbiamo completato il **primo blocco di industrializzazione**:

```text
pyproject.toml
requirements-dev.txt
omnia_validation/
tests/
.github/workflows/ci.yml
docs/CONSOLIDATION_ROADMAP_V0.md
CONTRIBUTING.md
SECURITY.md
