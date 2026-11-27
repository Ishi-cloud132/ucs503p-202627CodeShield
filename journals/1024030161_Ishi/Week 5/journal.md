# Week 5 — Dataset Construction and Audit


## Objective

Build a single clean labelled dataset and check its quality.

## Work Completed

### 1. Built dataset

Wrote `scripts/build_dataset.py` to merge the raw sources into `codeshield_dataset.csv` (id, code, label, cwe, source) with 399 samples.

### 2. Label and CWE mapping

Normalised labels and attached CWE IDs (CWE-89, 78, 79, 22, 798) to each class.

### 3. Audited the dataset

Wrote `scripts/audit_codeshield_dataset.py` to check duplicates, empty rows and class balance; output saved as `dataset_audit_report.json`.

### 4. Inspected class balance

Found SAFE (130) and Command Injection (85) dominate while Hardcoded Credentials has only 18 samples.

## What I Learned

Dataset quality matters more than model choice. An audit step catches duplicates and imbalance before they distort results.

## Challenges

Hardcoded Credentials is under-represented. Raw data is kept out of Git (`data/raw/` in `.gitignore`), so the build script must be reproducible.

## Current Status

A clean 399-row dataset and audit report exist. Next is splitting and baseline training.
