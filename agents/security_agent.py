from openai import OpenAI
from dotenv import load_dotenv
from schemas.issue_schema import AgentOutput, Issue
import os

load_dotenv()

client = OpenAI()


def analyze_security(file_path: str) -> AgentOutput:
    """Used by workflow.py graph — reads file directly."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return AgentOutput(agent_name="SecurityAgent", issues=[])

    lines = code.splitlines()
    parsed_patch = {
        "file": file_path,
        "start_line": 1,
        "added_lines": lines
    }

    raw_result = review_security(parsed_patch)

    # Parse raw text into structured AgentOutput
    issues = []
    current_severity = None
    current_line = None
    current_desc = None
    current_fix = None

    severity_map = {
        "CRITICAL": 5,
        "HIGH": 4,
        "MEDIUM": 3,
        "LOW": 2,
        "SAFE": 1
    }

    for line in raw_result.splitlines():
        line = line.strip()

        for sev in severity_map:
            if line.startswith(f"[{sev}]"):
                # Save previous issue
                if current_severity and current_severity != "SAFE" and current_desc:
                    issues.append(Issue(
                        issue_type="security",
                        severity=severity_map[current_severity],
                        file_path=file_path,
                        line_number=None,
                        description=current_desc,
                        suggested_fix=current_fix
                    ))
                current_severity = sev
                current_desc = line.split("]", 1)[-1].strip()
                current_line = None
                current_fix = None
                break

        if line.startswith("Line :"):
            current_line = line.replace("Line :", "").strip()
            if current_desc:
                current_desc = f"{current_desc} | Line: {current_line}"

        if line.startswith("Fix  :") or line.startswith("Fix:"):
            current_fix = line.split(":", 1)[-1].strip()

        if line.startswith("Risk :"):
            risk = line.replace("Risk :", "").strip()
            if current_desc:
                current_desc = f"{current_desc} | Risk: {risk}"

    # Save last issue
    if current_severity and current_severity != "SAFE" and current_desc:
        issues.append(Issue(
            issue_type="security",
            severity=severity_map.get(current_severity, 2),
            file_path=file_path,
            line_number=None,
            description=current_desc,
            suggested_fix=current_fix
        ))

    return AgentOutput(agent_name="SecurityAgent", issues=issues)


def review_security(parsed_patch):
    """Used for raw patch-based review (original interface)."""
    review_input = f"""
You are a strict security code reviewer. You must flag EVERY potential issue, even LOW severity ones.
Do NOT skip any line. Treat every line as suspicious until proven safe.

Respond ONLY in this exact format for EACH line of code:

[SEVERITY] Issue Title
  Line : <the exact problematic line>
  Risk : <why it is dangerous>
  Fix  : <concrete remediation step>

If a line has NO issues, still report it as:
[SAFE] Line Reviewed
  Line : <the line>
  Note : <why it is considered safe>

Severity levels: CRITICAL / HIGH / MEDIUM / LOW / SAFE

Rules:
- CRITICAL : hardcoded secrets, credentials, tokens, passwords, PAN numbers, SWIFT/IBAN codes
- HIGH     : insecure storage, unencrypted file writes, exposed paths, unencrypted financial data
- MEDIUM   : missing access controls, unsafe defaults, weak configurations, missing audit logs
- LOW      : potential info leakage, unvalidated inputs, risky patterns

End your response with exactly this line:
Summary: X Critical, X High, X Medium, X Low | <Action Required / No Action Required>

---
File: {parsed_patch['file']}
Starting line: {parsed_patch['start_line']}

New Code:
{chr(10).join(parsed_patch['added_lines'])}

Check every line for:
- Hardcoded secrets, API keys, tokens, passwords
- PAN/card numbers, SWIFT codes, IBAN patterns (fintech specific)
- PCI-DSS violations
- Unsafe environment variable usage
- Injection vulnerabilities (SQL, shell, prompt)
- Insecure local file or index storage
- Unprotected paths or world-readable files
- Exposed credentials or tokens in logs or storage
- Missing encryption on saved financial data
- Overly permissive file operations
- Missing audit trail for financial transactions
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a paranoid senior security engineer performing a strict fintech audit. Flag everything. Never skip a line. No prose, no extra explanation outside the format."},
            {"role": "user", "content": review_input}
        ]
    )

    return response.choices[0].message.content