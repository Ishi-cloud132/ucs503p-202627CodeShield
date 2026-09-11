# Week 2 — React Frontend Implementation

## Objective

The objective of Week 2 was to implement the frontend planned during Week 1. The focus was on developing the main React components, building the CodeShield dashboard and creating the interface for code submission and vulnerability results.

## Work Completed

### 1. Developed the Main React Interface

Started implementing the CodeShield frontend using React based on the planned component structure.

The application was divided into reusable sections rather than keeping all functionality within a single component.

### 2. Built the Code Submission Interface

Implemented the main code input section where users can enter the source code that will eventually be analyzed by CodeShield.

The interface was designed to make the code submission and scanning process straightforward, with a clearly identifiable area for entering code and initiating a scan.

### 3. Developed the Dashboard

Implemented the main CodeShield dashboard and its supporting UI elements.

The dashboard was designed to give users a quick overview of the security analysis, while also providing access to the detailed scan results.

The interface included sections for:

* Security overview
* Vulnerability statistics
* Risk information
* Recent scan information
* Navigation to the scanning interface

### 4. Implemented Vulnerability Cards / Results

Developed reusable components for displaying individual vulnerability findings.

The components were designed to display information such as:

* Vulnerability type
* Severity
* Affected line
* Confidence
* Description
* Recommendation

The layout was designed so that multiple findings could be displayed in a consistent and readable manner.

### 5. Implemented Risk Summary Elements

Developed the UI components required to display the overall risk level of a scan.

The purpose was to provide a quick visual summary while still allowing the user to inspect the individual vulnerabilities in detail.

### 6. Added Sample Scan Results

Used sample vulnerability data during frontend development to test how the interface would behave when different types and numbers of vulnerabilities were returned.

This helped in testing the layout of vulnerability cards, severity indicators and risk summaries before the complete backend workflow was available.

### 7. Worked on Styling and User Experience

Refined the visual appearance of the application and worked on consistency between the different frontend sections.

Attention was given to spacing, typography, component layout and the visual distinction between different types of security information.

## Challenges

One challenge was designing the frontend around data that would eventually come from the backend while the backend functionality was still under development.

Another challenge was making the results interface flexible enough to display different vulnerability types and different numbers of findings without breaking the overall layout.

## What I Learned

This week gave me practical experience in building a multi-component React application.

I learned how reusable components can simplify development and how frontend interfaces can be developed independently using structured sample data while the backend is being developed in parallel.

I also gained experience in designing interfaces where information hierarchy is important, particularly when displaying security-related information such as severity and risk.

## Week 2 Outcome

The primary CodeShield frontend was implemented, including the dashboard, code submission interface, vulnerability result components, risk summary and navigation.

The frontend was functional with sample scan data and was prepared for further refinement and connection with the backend.
