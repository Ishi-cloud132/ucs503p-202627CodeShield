# Week 10 — Backend Hardening and Test Suite


## Objective

Make the backend more reliable and testable.

## Work Completed

### 1. Request validation

Planned replacing the raw `dict` input in `/scan` with a Pydantic model and a maximum code size.

### 2. Unified risk format

Aligned `overall_risk` as a label (NONE/LOW/MEDIUM/HIGH/CRITICAL) across `/scan` and `/ml/scan`.

### 3. Tests

Started a pytest suite with safe and vulnerable samples per category plus API tests via FastAPI TestClient.

### 4. Dependency pinning

Reviewed the scikit-learn version warning when loading the model and planned to pin the training version in requirements.

## What I Learned

Automated tests make it safe to change rules without breaking earlier behaviour.

## Challenges

Model artifacts trained on one scikit-learn version emit warnings on another, so versions must be pinned and documented.

## Current Status

Hardening is in progress; AST-based analyzer and CI tests are the next steps.
