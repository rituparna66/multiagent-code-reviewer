import subprocess
import json
from schemas.issue_schema import Issue, AgentOutput


def run_bandit(file_path: str) -> dict:

    result = subprocess.run(
        ["python", "-m", "bandit", "-f", "json", file_path],
        capture_output=True,
        text=True
    )

    # If Bandit fails or returns empty output
    if not result.stdout:
        return {"results": []}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"results": []}


def map_severity(bandit_severity: str) -> int:

    if bandit_severity == "HIGH":
        return 5
    elif bandit_severity == "MEDIUM":
        return 4
    elif bandit_severity == "LOW":
        return 3
    else:
        return 2


def analyze_security(file_path: str) -> AgentOutput:
    """
    Security Agent:
    - Runs Bandit
    - Converts findings into structured Issue objects
    - Returns AgentOutput
    """
    bandit_output = run_bandit(file_path)

    issues = []

    for item in bandit_output.get("results", []):
        severity = map_severity(item.get("issue_severity", "LOW"))

        issue = Issue(
            issue_type="security",
            severity=severity,
            file_path=file_path,
            line_number=item.get("line_number"),
            description=item.get("issue_text"),
            suggested_fix="Review and apply secure coding practices."
        )

        issues.append(issue)

    return AgentOutput(
        agent_name="SecurityAgent",
        issues=issues
    )
