def calculate_overall_risk(issues):

    if not issues:
        return "LOW"

    severity_scores = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }

    highest_score = max(
        severity_scores.get(issue["severity"], 1)
        for issue in issues
    )

    if highest_score == 3:
        return "HIGH"
    elif highest_score == 2:
        return "MEDIUM"

    return "LOW"