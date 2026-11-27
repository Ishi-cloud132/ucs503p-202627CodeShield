# Week 4 — ML Planning and Dataset Sources


## Objective

Plan the machine learning component and identify data sources for vulnerability classification.

## Work Completed

### 1. Defined ML problem

Framed the task as multi-class classification of Python snippets into SQL Injection, Command Injection, Hardcoded Credentials, Insecure File Handling, Cross-Site Scripting and SAFE.

### 2. Identified data sources

Reviewed OWASP-style vulnerable/safe examples and the Python Vulnerability Remediation dataset as sources, with CWE labels for each class.

### 3. Chose model approach

Decided on TF-IDF text features with a linear classifier as an explainable baseline suited to a small dataset, keeping ML separate from static rules.

### 4. Planned evaluation

Planned a train/validation/test split and macro-F1 as the main metric because classes are imbalanced.

## What I Learned

Small datasets limit model choice, so a simple, explainable baseline is a better starting point than a deep model.

## Challenges

Raw datasets use different formats and labels, so they cannot be merged directly. Deciding which CWE maps to which CodeShield category needed care.

## Current Status

ML approach and data sources finalised; dataset construction is next.
