# Week 3 : Frontend-Backend Integration and Scan API

## Objective

The objective of Week 3 was to connect the existing React frontend with the FastAPI backend and verify the complete code scanning workflow. The focus was on making the frontend communicate with the actual backend vulnerability detection service and ensuring that the scan results are displayed correctly.

## Work Completed

### 1. Connected Frontend with FastAPI

Integrated the React frontend with the FastAPI `/scan` endpoint.

The frontend was updated so that the Python code entered by the user in the code editor is sent to the backend for analysis. This replaced the dependency on only predefined frontend results and allowed the actual static analyzer to process the submitted code.

### 2. Configured CORS

Updated the FastAPI CORS configuration to allow requests from the frontend development server running on port 8080.

This configuration allowed the React frontend and FastAPI backend to communicate correctly during local development.

### 3. Matched API Response Structure

Updated the backend response structure to match the format expected by the frontend.

The scan response was structured to include:

- Vulnerability type
- Severity
- Line number
- Confidence
- Risk score
- Description
- Recommendation
- Overall risk

This ensured that the frontend could correctly display the information returned by the backend.

### 4. Tested End-to-End Scanning

Tested the complete scanning workflow by entering vulnerable Python code into the frontend and using the scan functionality.

For example, a hardcoded password such as `password = "admin123"` was submitted through the frontend. The backend processed the code using the static analyzer and correctly identified it as a medium-severity vulnerability.

### 5. Verified Scan Results

Verified that the detected vulnerability was displayed correctly on the frontend.

The result included the vulnerability type, affected line number, confidence level and risk information. This confirmed that the frontend, backend and static analysis components were communicating correctly.

### 6. Prepared for ML Integration

With the basic scanning pipeline working, the backend was prepared for the next stage of development.

The planned next step is to integrate the machine learning model with the existing static analysis system and eventually combine the outputs from both approaches to provide a more comprehensive vulnerability assessment.

## What I Learned

This week helped me understand the practical process of integrating a React frontend with a FastAPI backend.

I also learned the importance of maintaining a consistent API response structure between the frontend and backend. Fields such as confidence, severity and risk score need to be formatted correctly so that the frontend can interpret and display them as intended.

The end-to-end testing also gave me a better understanding of how individual backend components come together to produce the final result shown to the user.

## Challenges

The main challenge was matching the backend response format with the structure expected by the existing frontend components.

Another important issue was configuring CORS because the frontend and backend were running on different local ports. Without the correct CORS configuration, the frontend would not be able to make requests to the FastAPI service.

Ensuring that the confidence and risk values were returned in the correct format was also important for displaying the scan results correctly.

## Current Status

The basic frontend-to-backend scanning pipeline is working successfully.

Python code entered through the frontend is sent to the FastAPI `/scan` endpoint, processed by the static analyzer and returned to the frontend with vulnerability and risk information.

The next stage of development is to improve the static analysis rules, develop and integrate the machine learning model and connect both detection approaches into the final CodeShield scanning workflow.