# Satellite Backbone Integration Order

This document defines the recommended order for aligning satellite repositories to the OMNIA backbone contract.

## Already stabilized

OMNIA
omnia-limit
OMNIA-VALIDATION

These form the current backbone:

OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validation API
  -> OMNIA-VALIDATION ValidationEnvelope
  -> GitHub Actions CI regression

## Next integration order

1. OMNIAMIND
2. OMNIA-RADAR
3. OMNIA-INVARIANCE
4. OMNIA-CRYPTO
5. OMNIA-SECURITY
6. OMNIA-CONSTANT
7. OMNIA-THREE-BODY
8. OMNIABASE
9. lon-mirror

## Reasoning

### 1. OMNIAMIND

OMNIAMIND should be integrated first because it is the orchestration layer.

It must learn to orchestrate the existing backbone rather than inventing a parallel one.

### 2. OMNIA-RADAR

OMNIA-RADAR likely acts as an observer or detection layer.

It should consume certificates/envelopes rather than redefine measurement boundaries.

### 3. OMNIA-INVARIANCE

OMNIA-INVARIANCE should be stabilized before OMNIA-CRYPTO because it owns generic invariance primitives.

### 4. OMNIA-CRYPTO

OMNIA-CRYPTO should become a domain adapter over OMNIA-INVARIANCE and the backbone contract.

### 5. OMNIA-SECURITY

OMNIA-SECURITY should consume validated backbone artifacts for security-oriented interpretation or reporting.

### 6. OMNIA-CONSTANT

OMNIA-CONSTANT should align once the invariant/crypto overlap is resolved.

### 7. OMNIA-THREE-BODY

OMNIA-THREE-BODY should be treated as a domain-specific producer or experiment repository.

### 8. OMNIABASE

OMNIABASE should later expose base-invariance outputs as BoundaryCertificate-compatible artifacts or upstream measurement inputs.

### 9. lon-mirror

lon-mirror should remain the conceptual/root reference unless and until it needs direct software participation.

## Rule

Do not integrate satellites randomly.

Do not add more surface area before each repository has a declared backbone role.

Every satellite must answer:

Producer, Adapter, Consumer, or Observer?
