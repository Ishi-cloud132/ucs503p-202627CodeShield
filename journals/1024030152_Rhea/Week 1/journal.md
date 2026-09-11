# Week 1 — Frontend Planning and Project Understanding

## Objective

The objective of Week 1 was to understand the CodeShield user interface requirements and plan the frontend structure for the vulnerability scanning workflow.

## Work Done This Week

### 1. Studied the User Workflow

I reviewed how a user would interact with CodeShield, from entering source code to viewing the security analysis results.

The basic frontend workflow was identified as:

**Open CodeShield → Enter Source Code → Start Scan → View Vulnerabilities → View Risk Summary**

### 2. Planned the Dashboard

I worked on identifying the main sections required for the CodeShield dashboard.

The dashboard needs to provide:

- A clear area for code input
- A separate area for displaying scan results
- A risk summary section for quickly understanding the overall security status

### 3. Planned the Results Interface

I identified the information that would be useful to display after a scan:

- **Vulnerability Type**
- **Severity**
- **Line Number**
- **Confidence**
- **Description**
- **Recommendation**

### 4. Planned Component Structure

The frontend was divided into reusable components so that individual parts of the interface can be developed and modified independently.

## Challenges / Observations

One important consideration was avoiding an interface that becomes too complicated when multiple vulnerabilities are detected.

The results therefore need to be organized clearly so that users can quickly understand which issues are more serious.

## Learning

This week helped me understand how UI structure should follow the actual workflow of the application.

I also learned the importance of reusable components when developing a larger frontend.

## Week 1 Outcome

The initial CodeShield frontend structure and dashboard requirements were identified, providing the foundation for frontend implementation.