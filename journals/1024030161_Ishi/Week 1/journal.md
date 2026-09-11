Week 1 : Project Understanding and Backend Planning
Objective
The objective of Week 1 was to understand the overall requirements of CodeShield and plan the backend architecture for the vulnerability detection system.
Work Completed
1. Understood the CodeShield Workflow
Studied the overall workflow of CodeShield and divided the system into the main components: frontend, backend, static code analysis, machine learning and risk assessment.
The initial flow was planned so that Python source code entered by the user would be sent to the backend for analysis and the detected vulnerabilities would be returned to the frontend.
2. Identified Initial Vulnerability Categories
Reviewed common Python security vulnerabilities that could be targeted in the initial version of the project.
The initial categories included:
SQL Injection
Command Injection
Hardcoded Credentials
Insecure File Handling
These categories were selected as the starting point for the static analysis component.
3. Planned the FastAPI Backend
Planned FastAPI as the backend framework for handling communication between the frontend and the vulnerability detection components.
The backend was designed to provide API endpoints through which the frontend could submit Python code for scanning.
4. Planned Risk Assessment
Discussed how the detected vulnerabilities could be assigned severity levels and how these severity levels could be used to calculate an overall risk level for a scan.
5. Discussed ML Integration
Started planning how the machine learning component would later work alongside static analysis.
The initial idea was to keep static analysis and ML as separate detection components so that their results could eventually be combined by the backend.
Challenges / Observations
One of the main considerations was deciding how to structure the backend so that the static analysis component and future ML model could be added without changing the complete API architecture.
It was also important to define a consistent response structure that could later contain vulnerability type, severity, confidence and risk information.
Learning
This week helped me understand the overall architecture of CodeShield and how the different components of the project would communicate with each other.
I also gained a clearer understanding of the role of FastAPI as the interface between the frontend and the vulnerability detection system.
Week 1 Outcome
The initial CodeShield architecture and backend requirements were planned. The main vulnerability categories, API structure and future ML integration approach were identified.
