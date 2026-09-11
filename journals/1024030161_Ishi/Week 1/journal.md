# Week 1 : Project Understanding and Backend Planning

## Objective

The objective of Week 1 was to understand the overall requirements of CodeShield and establish the initial technical direction for the backend, vulnerability detection and machine learning components. The focus was on understanding how the different modules of the project would work together to form a complete code vulnerability detection system.

## Work Completed

### 1. Understood the CodeShield Workflow

Studied the overall workflow of CodeShield and divided the system into its major components: frontend, backend, static code analysis, machine learning and risk assessment.

The initial workflow was planned so that Python source code entered by the user through the frontend would be sent to the backend for analysis. The backend would then process the code through the vulnerability detection components and return structured results to the frontend.

### 2. Identified Initial Vulnerability Categories

Reviewed common security vulnerabilities that could be targeted in the initial version of CodeShield.

The initial categories identified were:

- SQL Injection
- Command Injection
- Hardcoded Credentials
- Potential Insecure File Handling

These categories were selected as the initial focus for the static analysis component, as they provide a practical starting point for detecting common security issues in Python source code.

### 3. Planned the FastAPI Backend

Planned FastAPI as the backend framework for CodeShield.

The backend was designed to act as the communication layer between the frontend and the vulnerability detection modules. An API-based approach was selected so that the frontend could submit Python code for scanning and receive the analysis results in a structured format.

The backend structure was also planned to keep the static analyzer, risk assessment and future ML components separate so that each part could be developed and improved independently.

### 4. Planned the Static Analysis Component

Studied how rule-based static analysis could be used to identify potentially vulnerable patterns directly from Python source code.

The initial approach was based on identifying recognizable code patterns associated with the selected vulnerability categories. This provided a simple starting point for implementing the first working version of the vulnerability scanner.

### 5. Planned Risk Assessment

Discussed how the vulnerabilities detected by the system could be assigned different severity levels such as HIGH, MEDIUM and LOW.

These severity levels would then be used to determine an overall risk level for the submitted code. This was planned to give users a simpler summary of the security condition of their code in addition to the individual vulnerability details.

### 6. Discussed ML Integration

Started planning the role of machine learning in the overall vulnerability detection pipeline.

The initial approach was to keep the ML model separate from the static analysis component. This would allow both approaches to independently analyze the code, after which their results could eventually be combined by the backend to provide a more comprehensive vulnerability assessment.

## Challenges / Observations

One of the main considerations during the initial planning was deciding how to structure the backend so that new components could be added without requiring major changes to the existing architecture.

Since both static analysis and machine learning are expected to contribute to the final detection system, it was important to keep these components modular.

Another consideration was defining a consistent result structure that could contain information such as vulnerability type, severity, affected line, confidence, risk score, description and recommendation. This would make it easier to connect the backend results with the frontend later.

## Learning

This week helped me understand the overall architecture of CodeShield and how the frontend, backend, static analysis and machine learning components would communicate with each other.

I also gained a better understanding of how FastAPI can be used to create an API-based backend for a software project and how separating different processing components can make the system easier to extend and maintain.

The initial planning also helped me understand that the static analysis and ML components can work as complementary parts of the vulnerability detection pipeline.

## Week 1 Outcome

The initial technical architecture of CodeShield was planned, including the frontend-backend workflow, FastAPI backend structure, static analysis approach, initial vulnerability categories and risk assessment mechanism.

The role of the future ML component was also defined, providing a clear foundation for backend implementation and further development in the following weeks.