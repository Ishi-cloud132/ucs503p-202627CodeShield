# Code Guardian Shield

Build a complete, polished frontend for a university software engineering project called "CodeShield".

CodeShield is an ML-Based Code Vulnerability Detection and Risk Assessment Platform. Users can paste Python source code into the application, scan it for security vulnerabilities, and view a detailed risk assessment report.

IMPORTANT DESIGN DIRECTION:

The website should look like a realistic, professionally designed cybersecurity developer tool built by a human development team. Do NOT make it look like a generic AI-generated SaaS landing page.

Avoid:

- Excessive gradients

- Neon colours everywhere

- Glassmorphism

- Floating random shapes

- Huge rounded pill components

- Excessive animations

- Overuse of icons

- Generic AI chatbot-style design

- Marketing-heavy landing page sections

Use a clean, structured, practical developer-tool interface similar to a real cybersecurity dashboard.

TECH STACK:

- React

- TypeScript

- Tailwind CSS

- Component-based architecture

- Lucide icons where appropriate

COLOR STYLE:

Use a professional dark cybersecurity/developer theme.

Main background: very dark navy or charcoal

Secondary background: slightly lighter dark panels

Primary accent: muted blue

High severity: red

Medium severity: amber/orange

Low severity: green

Text: off-white and muted gray

Do not use bright purple or excessive gradients.

==================================================

APPLICATION STRUCTURE

==================================================

Create a single-page application with the following sections:

1. TOP NAVIGATION BAR

2. CODE SCANNER WORKSPACE

3. SECURITY SUMMARY

4. VULNERABILITY RESULTS

5. SCAN HISTORY / DASHBOARD SECTION

==================================================

1. TOP NAVIGATION BAR

==================================================

Create a professional fixed or sticky top navigation bar.

Left side:

- Simple shield icon

- "CodeShield" logo text

- Small subtitle: "Vulnerability Detection Platform"

Right side:

- Dashboard navigation item

- Scanner navigation item

- Reports navigation item

- Small GitHub icon button

The navigation should be minimal and practical, not overly decorative.

==================================================

2. CODE SCANNER WORKSPACE

==================================================

This should be the main section of the application.

Page heading:

"Code Security Scanner"

Subheading:

"Analyze Python source code for potential security vulnerabilities using static analysis and machine learning."

Create a large two-column layout on desktop.

LEFT SIDE:

A realistic code editor interface.

Include:

- Header showing "Python"

- Small file name such as "main.py"

- Line numbers

- Dark monospace code editor

- Syntax-highlighted sample Python code

- Ability to paste and edit code

- A "Load Vulnerable Example" button

- A prominent "Scan Code" button

Use a realistic vulnerable Python example by default, such as code containing:

- A hardcoded password

- An SQL query built using string concatenation

- A potentially dangerous command execution pattern

Example visual structure:

┌─────────────────────────────────────┐

│ main.py                    Python   │

├─────────────────────────────────────┤

│ 1  import os                        │

│ 2                                  │

│ 3  password = "admin123"            │

│ 4  user_id = input("Enter ID")      │

│ 5  query = "SELECT..." + user_id    │

│ 6  os.system(...)                   │

└─────────────────────────────────────┘

RIGHT SIDE:

A "Scan Summary" panel.

Before scanning, display:

- Ready to scan

- Supported language: Python

- Detection engine status: Active

After scanning, display statistics:

Total Issues: 3

High Risk: 2

Medium Risk: 1

Low Risk: 0

Also show an overall security status indicator such as:

"Security Risk: HIGH"

Use a clean severity indicator, not a huge circular gauge.

==================================================

3. SCANNING LOADING STATE

==================================================

When the user clicks "Scan Code", show a realistic scanning state.

Display:

"Analyzing source code..."

Show the following steps progressively:

✓ Parsing source code

✓ Performing static analysis

✓ Running vulnerability classifier

✓ Calculating risk assessment

Use subtle loading animations only.

After approximately 1–2 seconds, display the results.

==================================================

4. VULNERABILITY RESULTS

==================================================

Create a detailed results section below the scanner.

Heading:

"Detected Vulnerabilities"

Each vulnerability should be displayed as a professional expandable card or structured row.

Example vulnerability:

SQL Injection

HIGH SEVERITY

Line 5

Confidence: 94%

Description:

User-controlled input appears to be directly concatenated into an SQL query.

Recommendation:

Use parameterized queries instead of directly inserting user input into SQL statements.

Include these sample vulnerabilities:

1. SQL Injection

Severity: HIGH

Confidence: 94%

Line: 5

2. Command Injection

Severity: HIGH

Confidence: 91%

Line: 6

3. Hardcoded Credentials

Severity: MEDIUM

Confidence: 86%

Line: 3

Use clear colour-coded severity badges, but keep the overall UI professional and restrained.

==================================================

5. DASHBOARD / SCAN HISTORY

==================================================

Below the scanner results, create a compact security dashboard.

Include four statistic cards:

Total Scans

24

Vulnerabilities Detected

37

High-Risk Issues

8

Average Scan Time

1.8s

Below this, add a "Recent Scans" table.

Columns:

- File Name

- Scan Date

- Issues Found

- Highest Severity

- Status

Example rows:

authentication.py | Today, 10:42 AM | 3 | HIGH | Completed

database.py | Yesterday | 1 | MEDIUM | Completed

utils.py | Sep 2, 2026 | 0 | LOW | Completed

Do not make this dashboard overly complex. It should look like a realistic MVP prototype.

==================================================

INTERACTIONS

==================================================

Implement frontend interactions:

1. User can edit or paste Python code into the editor.

2. "Load Vulnerable Example" fills the editor with sample vulnerable code.

3. "Scan Code" triggers a scanning animation.

4. After scanning, display the vulnerability results.

5. Clicking a vulnerability expands it to show:

   - Description

   - Recommendation

   - Risk score

   - Confidence score

6. Add an API service layer prepared to connect to a FastAPI backend.

The frontend should expect an endpoint:

POST http://127.0.0.1:8000/scan

Request body:

{

  "code": "user source code"

}

Expected response:

{

  "total_vulnerabilities": 3,

  "vulnerabilities": [

    {

      "type": "SQL Injection",

      "severity": "HIGH",

      "line": 5,

      "confidence": 0.94,

      "risk_score": 9,

      "description": "User-controlled input is directly concatenated into an SQL query.",

      "recommendation": "Use parameterized queries."

    }

  ]

}

IMPORTANT:

For now, if the backend is unavailable, gracefully use mock vulnerability data so the frontend can still be demonstrated independently.

==================================================

RESPONSIVE DESIGN

==================================================

Desktop:

- Two-column scanner layout

- Structured dashboard

Mobile:

- Stack the code editor and scan summary vertically

- Make tables horizontally scrollable if necessary

==================================================

FINAL DESIGN REQUIREMENT

==================================================

The final application should feel like a genuine cybersecurity analysis tool built for developers.

It should be:

- Clean

- Practical

- Structured

- Professional

- Modern but not trendy

- Suitable for a university project presentation

- Visually impressive without looking artificially generated

Prioritize usability and information hierarchy over decorative design.

Do not create a marketing landing page.

Build the actual working CodeShield application interface.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/8c872b96-860b-4508-b8b6-71f67720805c).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
