# Week 3 — Static Analysis and Frontend Improvement

## Work Done This Week

This week, I focused on reviewing the existing static analysis and identifying improvements while also reviewing the frontend components that were still using basic or mock functionality.

### 1. Reviewed Existing Static Analyzer

Reviewed the current rule-based static analyzer and the patterns used to identify vulnerabilities.

The existing implementation provides the initial detection for:

- **Hardcoded Credentials**
- **Command Injection**
- **SQL Injection**
- **Insecure File Handling**

### 2. Planned Static Analysis Improvements

Identified areas where the existing rules can be improved to detect more variations of vulnerable code.

The aim is to reduce dependence on very simple pattern matching and eventually introduce more structured code analysis where appropriate.

### 3. Reviewed Dashboard Functionality

Checked the existing dashboard and recent scan sections.

Some of these sections currently use predefined or mock information and therefore do not automatically reflect the scans performed by the user.

### 4. Planned Recent Scan Integration

Planned how the recent scans/checks section can be connected to actual scan results so that newly performed scans can appear in the dashboard.

### 5. Reviewed Frontend Interactions

Started identifying frontend buttons and sections that currently provide mainly visual functionality and need to be connected to actual application logic.

## What I Learned

This week helped me understand the difference between a frontend that is visually complete and one where all components are connected to actual application data.

I also learned that improving static analysis requires considering different ways the same vulnerability can appear in source code rather than checking only one fixed pattern.

## Challenges

The main challenge was improving the static analysis while keeping it compatible with the existing backend response structure.

For the frontend, the main issue was that some dashboard and recent-scan information was not yet connected to persistent scan data.

## Current Status

The basic scanner is already connected to the FastAPI backend, while the dashboard and recent scan functionality still require further implementation.

The static analyzer is also being improved to provide broader and more reliable vulnerability detection.