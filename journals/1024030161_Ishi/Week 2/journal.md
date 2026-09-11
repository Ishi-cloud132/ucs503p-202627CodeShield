Week 2 — FastAPI Backend and Static Analysis Foundation
Work Done This Week
This week, I focused on implementing the initial FastAPI backend and creating the first version of the static vulnerability analysis component.
1. Created FastAPI Backend
Created the initial FastAPI application for CodeShield and configured the basic project structure.
The backend was designed to receive Python code through an API and process it using the vulnerability analysis module.
2. Configured Uvicorn
Configured Uvicorn as the development server for running the FastAPI application locally.
The backend was tested to make sure that the application starts correctly and can be accessed through the local development environment.
3. Implemented Basic API Endpoints
Implemented the initial:
/
/health
/scan
endpoints.
The health endpoint was used to verify that the backend is running correctly, while the scan endpoint was created for submitting source code for analysis.
4. Implemented Static Analyzer
Created the initial rule-based static analyzer for detecting common vulnerability patterns in Python code.
The analyzer currently checks for hardcoded credentials, command execution, dynamically constructed SQL queries and potentially unsafe file handling.
5. Implemented Risk Assessment
Added a basic risk assessment component that determines the overall risk level based on the highest severity vulnerability detected.
The initial severity mapping uses HIGH, MEDIUM and LOW categories.
6. Tested the Backend
Tested the API locally using the FastAPI Swagger interface.
Sample vulnerable code was submitted to verify that the backend correctly identifies vulnerabilities and returns structured results.
What I Learned
This week helped me gain practical experience with FastAPI, API endpoints and connecting different backend modules together.
I also learned how rule-based static analysis can be used as an initial approach for detecting security issues in source code.
Challenges
One challenge was designing the response structure so that it would contain enough information for the frontend while remaining compatible with the future ML component.
Another consideration was keeping the static analyzer separate from the API logic so that its rules can be improved independently.
Current Status
The basic FastAPI backend and static analyzer are working locally. The /scan endpoint can receive Python code, analyze it and return detected vulnerabilities along with severity and risk information.