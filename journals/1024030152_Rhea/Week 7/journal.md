# Week 7 — Static Analyzer Accuracy Improvements

> **Draft note:** Written from the repository state (commits/files). Edit any line that does not match what you personally did before submitting.

## Objective

Reduce false positives and improve rule accuracy.

## Work Completed

### 1. Skip comments

Updated rules to ignore comment lines.

### 2. Tighter SQL rule

Required SQL keywords to appear inside string literals with dynamic parts.

### 3. New detections

Added checks for `eval`/`exec`, `pickle.loads`, and weak hashes like MD5.

### 4. Regression samples

Saved sample snippets to compare behaviour before and after each change.

## What I Learned

Small precision fixes matter more to users than adding many noisy rules.

## Challenges

Some constructs (multi-line statements, variable-built queries) cannot be caught line by line.

## Current Status

Fewer false positives; AST analysis is the planned next step.
