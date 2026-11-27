# Week 8 — AST-Based Analysis Prototype

> **Draft note:** Written from the repository state (commits/files). Edit any line that does not match what you personally did before submitting.

## Objective

Prototype Python AST analysis for better structure awareness.

## Work Completed

### 1. AST walker

Wrote a prototype using Python `ast` to find calls to `os.system`, `subprocess` and `cursor.execute`.

### 2. Argument inspection

Checked whether arguments are string concatenations, f-strings or `.format` calls.

### 3. Comparison

Compared AST results with regex results on the same snippets.

### 4. Integration plan

Planned running AST rules alongside existing regex rules with the same output format.

## What I Learned

AST analysis ignores comments and strings automatically and gives exact line numbers.

## Challenges

Code with syntax errors cannot be parsed, so a regex fallback must remain.

## Current Status

Prototype works on test snippets; integration pending.
