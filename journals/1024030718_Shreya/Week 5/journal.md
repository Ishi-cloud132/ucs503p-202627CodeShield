# Week 5 — Handling ML Findings in the UI


## Objective

Update results display for combined static and ML findings.

## Work Completed

### 1. Detection method badge

Added a badge showing whether a finding came from static analysis or ML.

### 2. Null line numbers

Displayed 'whole snippet' instead of a missing line.

### 3. ML assessment panel

Added a section showing label, confidence and CWE from `ml_assessment`.

### 4. Confidence display

Shown as a percentage with consistent rounding.

## What I Learned

Users trust results more when they can see how each was produced.

## Challenges

ML findings lack descriptions, so the UI needs fallback text.

## Current Status

Results view supports both detection types.
