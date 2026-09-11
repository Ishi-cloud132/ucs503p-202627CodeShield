import re


def analyze_code(code: str):
    issues = []

    lines = code.split("\n")

    for line_number, line in enumerate(lines, start=1):

        # SQL Injection Detection
        if re.search(
            r"(SELECT|INSERT|UPDATE|DELETE).*(\+|%|\.format|f['\"])",
            line,
            re.IGNORECASE
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
            r"(os\.system|subprocess\.(call|run|Popen))\s*\(",
            line,
            re.IGNORECASE
        ):
            if re.search(
                r"(shell\s*=\s*True|\+|\.format|f['\"]|%s|%d)",
                line,
                re.IGNORECASE
            ):
                issues.append({
                    "type": "Command Injection",
                    "severity": "HIGH",
                    "line": line_number,
                    "confidence": 90,
                    "description": "Potential command injection through dynamically constructed system commands.",
                    "recommendation": "Avoid shell execution with user-controlled input. Validate inputs and use argument lists instead of dynamically constructed commands."
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

        # Insecure File Handling Detection
        if re.search(
            r"open\s*\(.+,\s*['\"]w['\"]",
            line,
            re.IGNORECASE
        ):
            issues.append({
                "type": "Potential Insecure File Handling",
                "severity": "LOW",
                "line": line_number,
                "confidence": 70,
                "description": "File write operation detected. Input validation may be required.",
                "recommendation": "Validate file paths and ensure user-controlled input cannot access unauthorized files."
            })

        # Cross-Site Scripting (XSS) Detection
        if re.search(
            r"(render_template_string|Markup)\s*\(",
            line,
            re.IGNORECASE
        ):
            issues.append({
                "type": "Cross-Site Scripting (XSS)",
                "severity": "HIGH",
                "line": line_number,
                "confidence": 80,
                "description": "Potentially unsafe rendering of dynamic content detected.",
                "recommendation": "Escape and sanitize user-controlled input before rendering it."
            })

        # Weak Authentication Detection
        if re.search(
            r"(password\s*==\s*['\"]|if\s+password\s*==|authenticate\s*=\s*['\"])",
            line,
            re.IGNORECASE
        ):
            issues.append({
                "type": "Weak Authentication",
                "severity": "MEDIUM",
                "line": line_number,
                "confidence": 75,
                "description": "Potentially weak authentication logic detected.",
                "recommendation": "Use secure authentication mechanisms and properly hashed passwords."
            })

    return issues