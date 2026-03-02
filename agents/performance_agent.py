from openai import OpenAI
from schemas.issue_schema import AgentOutput
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def analyze_performance(code: str, file_path: str) -> AgentOutput:
    prompt = f"""
You are a performance optimization expert.

Analyze the following Python code for:

- Inefficient loops
- Nested loops with high complexity
- Redundant computations
- Memory inefficiencies
- Poor algorithmic choices

Return output strictly in JSON format:

{{
  "agent_name": "PerformanceAgent",
  "issues": [
    {{
      "issue_type": "performance",
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
            {"role": "system", "content": "You are a strict performance reviewer."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )

    data = response.choices[0].message.content
    return AgentOutput.model_validate_json(data)
