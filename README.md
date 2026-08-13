# CodeShield — ML-Based Code Vulnerability Detection and Risk Assessment Platform

CodeShield is a software-security platform designed to automatically identify selected vulnerabilities in source code using a combination of **static code analysis and machine learning**.

The platform aims to help developers detect security issues early in the development cycle by identifying the vulnerability type, affected location, severity, confidence, and providing a clear security report.

## Project

This project is being developed as part of the **UCS503P Project (2026–27 ODD)** at **Thapar Institute of Engineering and Technology**.

### Team Members

| Name             | Roll Number | Email                                                               |
| ---------------- | ----------- | ------------------------------------------------------------------- |
| Rhea Balamurugan | 1024030152  | [rbalamurugan_be24@thapar.edu](mailto:rbalamurugan_be24@thapar.edu) |
| Ishi Govil       | 1024030161  | [igovil_be24@thapar.edu](mailto:igovil_be24@thapar.edu)             |
| Shreya Kush      | 1024030718  | [skush_be24@thapar.edu](mailto:skush_be24@thapar.edu)               |

## Key Features

* Source-code submission for security scanning
* Source-code preprocessing and structural analysis
* Static analysis using predefined security rules
* ML-based vulnerability classification
* Risk and severity assessment
* Confidence scoring
* File and line-level vulnerability identification
* Plain-language security explanations
* Security reports and dashboard
* Scan history and issue tracking
* CI/CD-based automated testing and deployment workflow

## Supported Vulnerability Categories

The initial version of CodeShield focuses on selected vulnerability categories:

* SQL Injection
* Command Injection
* Hardcoded Credentials
* Insecure File Handling
* Cross-Site Scripting (XSS)
* Weak Authentication

The project intentionally limits its initial scope to selected vulnerability categories so that detection performance can be evaluated realistically.

## Core Workflow

```text
Source Code
     |
     v
Code Preprocessing
     |
     v
+-------------------------+
| Static Analysis + ML    |
| Vulnerability Detection |
+-------------------------+
     |
     v
Risk Assessment
     |
     v
Security Report
     |
     v
Developer Dashboard
```

## Technology Stack

| Layer            | Technologies                                          |
| ---------------- | ----------------------------------------------------- |
| Frontend         | React.js, HTML/CSS, JavaScript                        |
| Backend          | Python, FastAPI                                       |
| Machine Learning | Python, scikit-learn / PyTorch                        |
| Code Analysis    | Python AST, Tree-sitter                               |
| Database         | PostgreSQL                                            |
| Version Control  | Git, GitHub                                           |
| CI/CD            | Automated testing, validation and deployment pipeline |

Optional technologies such as Docker, Redis, GitHub API, and Celery/RQ may be considered for future extensions.

## CI/CD Pipeline

CodeShield uses a CI/CD workflow to maintain code quality and support reliable deployment.

```text
Developer
    |
    v
Code Push to GitHub
    |
    v
CI Pipeline
    |
    +--> Install Dependencies
    |
    +--> Run Unit Tests
    |
    +--> Code Quality Checks
    |
    +--> Build Validation
    |
    v
CD Pipeline
    |
    v
Deployment
```

The CI pipeline automatically validates new changes before they are integrated. After successful checks, the application can be built and prepared for deployment.

## Evaluation

The ML component will be evaluated using:

* Precision
* Recall
* F1-score
* Accuracy

System-level evaluation will include:

* Average code scanning time
* Number of files successfully analyzed
* Detection coverage for supported vulnerability categories
* API response time
* Successful scan completion rate

Precision and recall are particularly important because both false positives and missed vulnerabilities affect the usefulness of a security-analysis system.

## Repository Structure

```text
CodeShield/
│
├── project-proposal/
│   ├── main.tex
│   └── main.pdf
│
├── journals/
│   ├── rhea/
│   ├── ishi/
│   └── shreya/
│
├── code/
│   ├── frontend/
│   ├── backend/
│   └── ml/
│
├── docs/
│
└── README.md
```

The exact source-code organization may evolve as development progresses.

## Documentation

Project documentation is maintained under the `docs` directory.

The documentation may include:

* Project requirements
* System design
* Architecture
* Development notes
* Testing documentation
* User documentation
* Team journals

## Project Proposal

The project proposal is available in the `project-proposal` directory.

```text
project-proposal/
├── main.tex
└── main.pdf
```

The `.tex` file contains the LaTeX source, while the `.pdf` file contains the compiled project proposal.

## Development

The project will be developed incrementally, beginning with the core Python code-analysis pipeline and expanding toward the complete web-based platform.

The initial development focuses on:

1. Python source-code parsing
2. Static vulnerability rules
3. Initial ML vulnerability classifier
4. FastAPI backend
5. PostgreSQL database
6. Code submission interface
7. Vulnerability reporting
8. Basic dashboard
9. Unit testing and CI/CD

## Future Extensions

Planned extensions include:

* GitHub repository scanning
* Additional programming-language support
* Improved ML models
* Severity prioritization
* Code-level remediation suggestions
* Scan history and comparison
* Background/asynchronous scanning
* Docker-based isolated analysis

## Project Status

**Current Stage:** Project Proposal / Initial Development

The initial implementation will focus on establishing a reliable vulnerability-analysis pipeline and a measurable minimum viable version of CodeShield before adding advanced features.

## Academic Information

**Course:** UCS503P Project
**Academic Year:** 2026–27 ODD
**Institute:** Thapar Institute of Engineering and Technology
**Project:** CodeShield — ML-Based Code Vulnerability Detection and Risk Assessment Platform
