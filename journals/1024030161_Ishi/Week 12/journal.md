# Week 12 — Model Training, Hybrid Evaluation and Integration


## Objective

Train the extended model, evaluate it honestly and integrate it with the new backend.

## Work Completed

### 1. Training script

Wrote `scripts/train_extended_model.py`: word+char TF-IDF plus 26 AST features into a calibrated Linear SVM; 5-fold grouped CV, leave-one-source-out and a held-out group split; saved model card, confusion matrix and figures.

### 2. Results

Selected model: macro-F1 0.798 +/- 0.037 (CV); held-out accuracy 0.768; detection F1 0.872.

### 3. Hybrid evaluation

Wrote `scripts/evaluate_hybrid.py` comparing static-only, ML-only and hybrid; chose the ML-only threshold 0.70 (precision 0.919, recall 0.845, FPR 11.5%).

### 4. Backend integration

Built `app/engine/ml.py` (chunking, probabilities, evidence tokens, line localisation), `pipeline.py` (fusion, risk score), SQLite history, report export and 43 pytest tests.

## What I Learned

Calibration and group-aware splits matter; adding benign code removed false alarms on ordinary functions.

## Challenges

The model confused ordinary code with vulnerable code until a benign corpus was added.

## Current Status

Backend and ML complete; final report and demo remain.
