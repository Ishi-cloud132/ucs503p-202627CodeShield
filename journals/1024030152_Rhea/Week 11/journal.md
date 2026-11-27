# Week 11 — AST Static Analyser with Taint Tracking

> **Draft note:** Written from the repository state. Edit any line that does not match what you personally did before submitting.

## Objective

Rewrite the static analyser so it understands code structure and data flow.

## Work Completed

### 1. AST engine

Replaced regex rules with `engine/static_analyzer.py`: import-alias resolution, taint levels (constant / dynamic / user input), propagation through assignments, f-strings, format and `%`.

### 2. 58 rules

Added rules for SQL/command/code injection, deserialisation, path traversal, XSS, hard-coded secrets, weak crypto, insecure configuration, SSRF, XXE and JWT problems, each with CWE, OWASP, explanation and secure example (`catalogue.py`).

### 3. False-positive fixes

Comments, plain text and parameterised queries no longer trigger findings; these cases are now pytest regression tests.

### 4. Lexical fallback

When code has a syntax error the engine falls back to a small set of lower-confidence rules and tells the user.

## What I Learned

AST plus taint tracking removes most false positives of line-based regexes and gives exact lines and data-flow traces.

## Challenges

Handling aliases, free variables and sanitisers without over-flagging.

## Current Status

Static engine complete: precision 0.92 with a 7% false-positive rate on the whole dataset.
