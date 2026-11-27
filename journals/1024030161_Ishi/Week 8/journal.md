# Week 8 — Backend ML Integration and Hybrid Scanning


## Objective

Integrate the trained model with FastAPI and combine it with static analysis.

## Work Completed

### 1. ML package

Created `codeshield_ml` with `model.py` (loads artifact, returns type, confidence, severity, CWE, risk score) and `scan_service.py` (merges static and ML findings).

### 2. Updated /scan

Updated `main.py` so `/scan` runs static analysis, then ML, adds an ML finding only if the model predicts a vulnerability, and avoids duplicate types.

### 3. Router and integration

Added `/ml/scan` router and `integration.py` for optional registration.

### 4. Risk handling

SAFE predictions stay in `ml_assessment` but do not inflate the vulnerability count; overall risk takes the higher of static and ML scores.

## What I Learned

Combining two detectors needs clear rules for duplicates and risk, otherwise results become confusing.

## Challenges

ML findings have no line number, and the static and ML routes return overall risk in different formats (label versus number), which needs unifying.

## Current Status

Hybrid scanning works through `/scan`; cleanup and testing remain.
