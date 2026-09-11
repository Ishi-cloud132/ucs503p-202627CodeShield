# Week 1 — Frontend Planning and UI/UX Design

## Objective

The objective of Week 1 was to understand the CodeShield requirements from a frontend perspective and plan the user interface for the vulnerability detection platform. The main focus was on deciding how the scanning workflow, vulnerability information and risk assessment would be presented to the user.

## Work Completed

### 1. Studied the Project Requirements

Reviewed the CodeShield proposal and understood the intended user workflow and the information that would need to be presented through the web application.

The main workflow identified was:

**Code Submission → Code Analysis → Vulnerability Detection → Risk Assessment → Security Report**

The frontend needed to provide a simple interface through which a developer could submit code and understand the results of the analysis.

### 2. Planned the Overall UI Structure

Planned the major sections of the frontend, including:

* Main dashboard
* Code input/editor section
* Scan controls
* Risk summary
* Vulnerability results
* Recent scans
* Navigation and supporting interface elements

The goal was to keep the interface organized so that detailed security information could be displayed without overwhelming the user.

### 3. Planned the Dashboard

Designed the initial structure of the CodeShield dashboard.

The dashboard was planned to provide an overview of the security status of scanned code, including information such as:

* Overall risk level
* Number of vulnerabilities
* Severity distribution
* Recent scans
* Scan-related statistics

### 4. Planned the Vulnerability Results Interface

Identified the information that should be displayed for each detected vulnerability.

The planned result structure included:

* **Vulnerability Type**
* **Severity**
* **Affected Line**
* **Confidence**
* **Risk Score**
* **Description**
* **Recommendation**

The results were planned as separate reusable UI elements so that multiple vulnerabilities could be displayed consistently.

### 5. Planned React Component Structure

Planned the frontend as a collection of reusable React components instead of developing the application as a single large page.

Major components were planned for the navigation, dashboard, code input, scan interface, risk summary and vulnerability results.

This structure would make it easier to modify individual sections as the project developed.

### 6. Considered Sample Data and Future API Data

Since the backend and frontend were being developed in parallel, the frontend was planned so that sample vulnerability data could initially be used for development and testing.

The data structure was kept consistent with the information expected from the backend so that the interface could later display actual scan results.

## Challenges / Observations

A major consideration was designing the interface without having the final scanning functionality available yet.

The frontend therefore needed to be flexible enough to work with sample data initially while still being suitable for the actual analysis results that would be provided later.

Another challenge was deciding how to present multiple vulnerabilities and their severity levels clearly.

## Learning

This week helped me understand how application requirements can be translated into a structured frontend design.

I also gained a better understanding of React component planning and the importance of designing reusable components when building a larger application.

## Week 1 Outcome

The overall CodeShield frontend structure and UI requirements were planned. The dashboard, code submission interface, vulnerability results and risk assessment sections were defined, providing a clear foundation for frontend implementation.
