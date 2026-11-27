# Week 4 — Extending Static Analysis Rules

> **Draft note:** Written from the repository state (commits/files). Edit any line that does not match what you personally did before submitting.

## Objective

Extend the static analyzer beyond the first four categories.

## Work Completed

### 1. Added XSS rule

Added detection for unsafe rendering such as `render_template_string` and `Markup`.

### 2. Added Weak Authentication rule

Added a rule for direct password comparison against literals.

### 3. Reviewed false positives

Identified that the SQL rule fires on comments and normal text containing words like SELECT.

### 4. Collected test snippets

Prepared vulnerable and safe snippets per category for later testing.

## What I Learned

Regex rules are quick to write but need safe test cases as well as vulnerable ones.

## Challenges

Balancing detection of variants against false alarms.

## Current Status

Six categories now have at least a basic rule; precision work is next.
