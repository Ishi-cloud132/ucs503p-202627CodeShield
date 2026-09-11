# Week 2 : FastAPI Backend and Static Analysis Foundation

## Objective

The objective of Week 2 was to implement the initial FastAPI backend for CodeShield and develop the first working version of the static vulnerability analysis component. The focus was on creating the basic API structure, connecting the backend modules and testing the initial vulnerability detection workflow.

## Work Completed

### 1. Created FastAPI Backend

Created the initial FastAPI application for CodeShield and configured the basic backend project structure.

The backend was designed to receive Python source code through an API and process it using the vulnerability analysis module. This provided the foundation for connecting the backend with the frontend in the following stages.

### 2. Configured Uvicorn

Configured Uvicorn as the development server for running the FastAPI application locally.

The backend was tested to make sure that the application starts successfully and can be accessed through the local development environment.

### 3. Implemented Basic API Endpoints

Implemented the initial API endpoints:

- `/`
- `/health`
- `/scan`

The `/` endpoint was used to verify the basic availability of the application, while the `/health` endpoint was implemented to check whether the backend service is running correctly.

The `/scan` endpoint was created to receive Python source code and send it to the vulnerability analysis component for processing.

### 4. Implemented Static Analyzer

Created the initial rule-based static analyzer for detecting common vulnerability patterns in Python source code.

The analyzer currently checks for:

- Hardcoded Credentials
- Command Injection
- SQL Injection
- Potential Insecure File Handling

The initial implementation uses code patterns to identify potentially unsafe operations and returns details about the detected vulnerability.

### 5. Implemented Risk Assessment

Added a basic risk assessment component for determining the overall risk level of the submitted code.

The detected vulnerabilities are assigned severity levels such as HIGH, MEDIUM and LOW. The overall risk is then calculated based on the highest severity vulnerability found during the analysis.

### 6. Tested the Backend

Tested the FastAPI backend locally using the Swagger API interface.

Sample vulnerable Python code was submitted through the `/scan` endpoint to verify that the static analyzer correctly identifies security issues and that the backend returns the expected structured information.

The testing also helped verify that the vulnerability type, severity, affected line and risk information were being returned correctly.

## What I Learned

This week helped me gain practical experience with FastAPI, Uvicorn and API endpoint development.

I also learned how different backend modules can be separated according to their responsibilities. Keeping the static analyzer and risk assessment logic separate from the main API makes it easier to improve individual components later.

Working with rule-based static analysis also helped me understand how common security vulnerabilities can initially be identified by analyzing patterns in source code.

## Challenges

One of the main challenges was designing the backend response structure so that it contained enough information for the frontend while also remaining suitable for the future machine learning component.

Another consideration was keeping the static analyzer independent from the API logic. This allows the vulnerability detection rules to be improved or expanded later without having to restructure the complete FastAPI application.

Testing different vulnerable code samples was also important to make sure that the initial detection rules were producing meaningful results.

## Current Status

The basic FastAPI backend and initial static analyzer are working successfully in the local development environment.

The `/scan` endpoint can receive Python source code, pass it to the static analyzer and return the detected vulnerabilities along with their severity and risk information.

The backend is now ready for the next stage, which includes improving the static analysis, connecting the frontend with the API and preparing the machine learning component for later integration.