Week 3 — Frontend-Backend Integration and Scan API
Work Done This Week
This week, I focused on connecting the existing frontend with the FastAPI backend and testing the complete scanning workflow.
1. Connected Frontend with FastAPI
Integrated the React frontend with the FastAPI /scan endpoint.
The frontend now sends the code entered in the code editor to the backend for analysis instead of relying only on predefined frontend results.
2. Configured CORS
Updated the FastAPI CORS configuration to allow requests from the frontend development server running on port 8080.
This allowed the React application and FastAPI service to communicate correctly during local development.
3. Matched API Response Structure
Updated the backend response structure to match the format expected by the frontend.
The response now includes:
Vulnerability type
Severity
Line number
Confidence
Risk score
Description
Recommendation
Overall risk
4. Tested End-to-End Scanning
Tested the complete workflow by entering vulnerable Python code into the frontend and running the scan.
For example, a hardcoded password was submitted through the frontend and the backend correctly detected it as a medium-severity vulnerability.
5. Verified Scan Results
Verified that the detected vulnerability was displayed correctly on the frontend, including its line number, confidence and risk level.
This confirmed that the frontend, backend and static analysis components are communicating correctly.
6. Prepared for ML Integration
With the basic scanning pipeline working, the next stage is to add the machine learning model and eventually combine ML predictions with the existing static analysis results.
What I Learned
This week helped me understand the practical process of integrating a React frontend with a FastAPI backend.
I also learned that the API response structure needs to be consistent between the frontend and backend, especially when information such as confidence and risk scores is being displayed.
Challenges
The main challenge was matching the backend response format with what the frontend components expected.
CORS configuration was another important part because the frontend and backend were running on different local ports.
Current Status
The basic frontend-to-backend scanning pipeline is working successfully. Code entered through the frontend is sent to FastAPI, analyzed by the static analyzer and returned to the frontend with vulnerability and risk information.
The next stage is to improve the static analysis and integrate the ML model.