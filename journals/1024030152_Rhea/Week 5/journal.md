# Week 5 — Recent Scans and Dashboard Data

> **Draft note:** Written from the repository state (commits/files). Edit any line that does not match what you personally did before submitting.

## Objective

Connect the dashboard to real scan results instead of mock data.

## Work Completed

### 1. Scan history state

Designed how each completed scan (time, risk, count) is stored and shown under Recent Scans.

### 2. Dashboard statistics

Planned computing totals and severity distribution from actual scan results.

### 3. Frontend data flow

Reviewed `scan-api.ts` and the Dashboard component for the data needed.

### 4. Persistence options

Compared browser storage with a backend database such as PostgreSQL from the proposal.

## What I Learned

Dashboards need real data flow; visual completeness is not enough.

## Challenges

No persistence layer exists yet in the backend.

## Current Status

Design finished; implementation of history follows.
