# Week 11 — Extended Multi-Source Dataset


## Objective

Extend ML support to more diverse code by building a larger, cleaner dataset.

## Work Completed

### 1. Sourced public datasets

Evaluated SecurityEval, Semgrep rule test-suites and Bandit examples; all are on GitHub and carry CWE or rule metadata. Wrote `scripts/fetch_external_data.sh`.

### 2. Dataset builder

Wrote `scripts/build_extended_dataset.py`: maps CWEs to 12 classes, extracts the statement/function behind every `# ruleid` / `# ok` marker, labels Bandit examples by running Bandit, and adds a benign library-code corpus.

### 3. Removed leakage

Stripped marker comments, licence headers, docstrings and all comments; normalised names such as `ok_1`; de-duplicated; added a group id per row (found that the v1 OWASP rows shared one licence header).

### 4. Result

2,438 samples, 13 classes, 1,069 independent groups; audit saved to `data/processed/extended_audit.json`.

## What I Learned

Evaluation is only as honest as the dataset: leakage and near-duplicates can make a small model look far better than it is.

## Challenges

Rule-derived labels contain noise; rare classes (Weak Authentication, 20 samples) remain weak.

## Current Status

Extended dataset ready for training.
