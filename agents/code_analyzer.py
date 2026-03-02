import os
from dotenv import load_dotenv
from openai import OpenAI
from schemas.issue_schema import AgentOutput

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
token = os.getenv("GITHUB_TOKEN")


def analyze_code(code: str, file_path: str, previous_findings=None) -> AgentOutput:
    # 🔹 Build context section (THIS is what you were asking about)
    context_section = ""

    if previous_findings:
        context_section = f"""
Previous agent findings:
{[r.model_dump() for r in previous_findings]}
"""

    # 🔹 Now build the prompt including that context
    prompt = f"""
You are a strict code reviewer.

Analyze the following Python code for:
- Code smells
- Bad naming
- Missing docstrings
- Structural problems

Avoid duplicating issues already identified by other agents.

{context_section}

Return output strictly in JSON format:

{{
  "agent_name": "CodeAnalyzer",
  "issues": [
    {{
      "issue_type": "code_smell",
      "severity": 1-5,
      "file_path": "{file_path}",
      "line_number": number or null,
      "description": "explanation",
      "suggested_fix": "fix suggestion"
    }}
  ]
}}

Here is the code:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise and structured code reviewer."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )

    data = response.choices[0].message.content

    return AgentOutput.model_validate_json(data)


print("DEBUG_TOKEN:", os.getenv("GITHUB_TOKEN"))
