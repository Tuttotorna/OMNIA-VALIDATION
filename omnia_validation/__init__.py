"""OMNIA-VALIDATION package.

Reusable validation utilities for the OMNIA-VALIDATION repository.

Boundary:
    measurement != inference != decision

This package exposes submodules such as:

- omnia_validation.hashing
- omnia_validation.io
- omnia_validation.metrics
- omnia_validation.metadata
- omnia_validation.schemas
- omnia_validation.manifest
- omnia_validation.cli

The package initializer intentionally avoids importing every helper eagerly.

Reason:
    submodules may evolve independently.
    package import should remain stable.
    validation logic should be imported from the specific module that defines it.

This package does not validate semantic truth.
It does not certify production safety.
It does not make final decisions.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = [
    "__version__",
]