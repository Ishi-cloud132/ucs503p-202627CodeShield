# Week 11 — Front-End Redesign


## Objective

Rebuild the front end so it looks professional and is honest about results.

## Work Completed

### 1. New stack

Vite + React 18 + TypeScript + Tailwind, CodeMirror editor, Recharts, React Router.

### 2. Scanner page

Hero section, example loader, file open and drag-and-drop, animated scan overlay, severity-highlighted editor lines, risk gauge, expandable finding cards with data flow, fix and ML evidence, filters and search.

### 3. Other pages

Dashboard (severity donut, category bars, trend), history (search, delete, reports), scan detail, model card with confusion matrix; dark/light themes.

### 4. Removed mock data

The old fallback that showed fake findings when the backend was down was replaced by a clear error banner.

## What I Learned

A security tool must never show fake results; good UI also means clear empty, loading and error states.

## Challenges

Keeping the types in sync with the API; getting CodeMirror line decorations right.

## Current Status

Front end complete and verified with browser screenshots.
