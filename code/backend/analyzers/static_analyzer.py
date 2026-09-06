import re


def analyze_code(code: str):
    issues = []

    lines = code.split("\n")

    for line_number, line in enumerate(lines, start=1):

        # SQL Injection Detection
        if (
            re.search(
                r"(SELECT|INSERT|UPDATE|DELETE).*(\+|%|\.format|f['\"])",
                line,
                re.IGNORECASE
            )
        ):
            issues.append({
                "type": "SQL Injection",
                "severity": "HIGH",
                "line": line_number,
                "confidence": 90,
                "description": "Potential SQL query constructed using dynamic input.",
                "recommendation": "Use parameterized queries instead of string concatenation."
            })

        # Command Injection Detection
        if re.search(
            r"(os\.system|subprocess\.call|subprocess\.run)\s*\(",
            line
        ):
            issues.append({
                "type": "Command Injection",
                "severity": "HIGH",
                "line": line_number,
                "confidence": 85,
                "description": "Potentially unsafe system command execution detected.",
                "recommendation": "Validate user input and avoid directly executing user-controlled commands."
            })

        # Hardcoded Credentials Detection
        if re.search(
            r"(password|passwd|secret|api_key|apikey|token)\s*=\s*['\"]",
            line,
            re.IGNORECASE
        ):
            issues.append({
                "type": "Hardcoded Credentials",
                "severity": "MEDIUM",
                "line": line_number,
                "confidence": 95,
                "description": "Potential hardcoded credential detected in source code.",
                "recommendation": "Store sensitive credentials in environment variables or a secure secret manager."
            })

        # Insecure File Handling
        if re.search(
            r"open\s*\(.+,\s*['\"]w['\"]",
            line
        ):
            issues.append({
                "type": "Potential Insecure File Handling",
                "severity": "LOW",
                "line": line_number,
                "confidence": 70,
                "description": "File write operation detected. Input validation may be required.",
                "recommendation": "Validate file paths and ensure user-controlled input cannot access unauthorized files."
            })

    return issues