# Week 7 — Improved Model: Calibrated SVM and AST Features


## Objective

Improve the classifier and add calibrated confidence scores.

## Work Completed

### 1. Calibrated Linear SVM

Wrote `scripts/train_codeshield_est.py`: word 1–2 gram TF-IDF with class-balanced Linear SVM and sigmoid calibration (5-fold) so confidence values are meaningful.

### 2. Tuned C on validation

Compared C = 0.5 to 2.5 on the validation set and picked C = 2.0 (validation macro-F1 about 0.85).

### 3. AST structural features

Added `codeshield_ml/features.py` extracting counts such as subprocess/os.system calls, open calls, SQL keywords and f-strings, with safe handling of unparsable code.

### 4. Final test results

Test accuracy 0.90, macro-F1 about 0.92; confusion matrix and classification report saved under `codeshield_ml/models/`.

## What I Learned

Calibration gives usable confidence scores, and tuning on validation (not test) keeps the final figures fair.

## Challenges

Excluding `id`, `cwe` and `source` from features was necessary to avoid the model learning dataset artefacts instead of code patterns.

## Current Status

Model artifact `codeshield_vulnerability_model.joblib` is ready for backend integration.
