# Week 9 — Mid-Semester Prototype Report and Testing

> **Draft note:** Written from the repository state (commits/files). Edit any line that does not match what you personally did before submitting.

## Objective

Document the prototype and test the full pipeline.

## Work Completed

### 1. Prototype report

Contributed backend, ML pipeline, dataset and metrics sections to `mst_codeshield_report.pdf`.

### 2. End-to-end testing

Tested sample snippets for each category through Swagger and the frontend, noting true and false positives.

### 3. Found issues

Noted false positives on comments and plain strings, and misses on f-string SQL, dict-style credentials, `eval` and `pickle`.

### 4. Planned fixes

Listed AST-based rules, input validation and automated tests as the next priorities.

## What I Learned

Writing the report forced us to explain every design choice and to be honest about limits such as dataset size.

## Challenges

Regex rules are fast but cannot tell code from comments or strings; ML confidence on short snippets can be low.

## Current Status

Prototype is documented and demonstrable; hardening is the focus for the coming weeks.
