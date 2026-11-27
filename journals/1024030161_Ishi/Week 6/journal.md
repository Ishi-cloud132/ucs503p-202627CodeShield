# Week 6 — Dataset Split and Baseline Model


## Objective

Create leakage-free splits and train a first baseline model.

## Work Completed

### 1. Split the data

Wrote `scripts/split_dataset.py` producing train (278), validation (60) and test (60) CSVs, stratified by label.

### 2. Checked leakage

Verified no identical code snippet appears in more than one split.

### 3. Trained baseline

Wrote `scripts/train_codeshield_ml.py` using TF-IDF plus a linear classifier; saved model and metrics to `backend/models/`.

### 4. Reviewed first results

Baseline metrics were saved in `metrics.json`; errors were mostly between similar classes such as Command Injection and Insecure File Handling.

## What I Learned

Splitting before any tuning prevents leakage and keeps test results honest.

## Challenges

Very small test set (60) means a single misclassification moves accuracy noticeably, so metrics must be read cautiously.

## Current Status

Baseline pipeline works end to end; improvement and model selection come next.
