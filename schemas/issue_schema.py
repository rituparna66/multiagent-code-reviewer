from pydantic import BaseModel
from typing import Optional, List

class Issue(BaseModel):
    issue_type: str
    severity: int
    file_path: str
    line_number: Optional[int]
    description: str
    suggested_fix: Optional[str]

class AgentOutput(BaseModel):
    agent_name: str
    issues: List[Issue]
