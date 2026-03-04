from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from schemas.issue_schema import AgentOutput, Issue
from agents.code_analyzer import analyze_code
from agents.security_agent import analyze_security
from tools.file_reader import read_file
from tools.aggregator import aggregate_results
from agents.performance_agent import analyze_performance


class ReviewState(TypedDict):
    file_path: str
    code: str
    results: List[AgentOutput]
    final_issues: List[Issue]
    summary: dict  # ← add this


def load_code(state: ReviewState):
    code = read_file(state["file_path"])
    return {"code": code}


def run_code_agent(state: ReviewState):
    previous_findings = state.get("results", [])

    result = analyze_code(
        state["code"],
        state["file_path"],
        previous_findings
    )

    return {"results": previous_findings + [result]}


def run_security_agent(state: ReviewState):
    result = analyze_security(state["file_path"])
    return {"results": state.get("results", []) + [result]}


def aggregate(state: ReviewState):
    all_results = state.get("results", [])

    # Flatten issues
    all_issues = []
    for agent_result in all_results:
        all_issues.extend(agent_result.issues)

    # Deduplicate similar issues (based on description + line)
    unique = {}
    for issue in all_issues:
        key = (issue.issue_type, issue.line_number, issue.description)
        if key not in unique:
            unique[key] = issue
        else:
            # Keep higher severity if duplicate
            if issue.severity > unique[key].severity:
                unique[key] = issue

    final_issues = list(unique.values())

    # Sort by severity descending
    final_issues.sort(key=lambda x: x.severity, reverse=True)

    # Summary stats
    summary = {
        "total_issues": len(final_issues),
        "critical": len([i for i in final_issues if i.severity == 5]),
        "serious": len([i for i in final_issues if i.severity == 4]),
        "moderate": len([i for i in final_issues if i.severity == 3]),
        "low": len([i for i in final_issues if i.severity <= 2]),
    }

    return {
        "final_issues": final_issues,
        "summary": summary
    }


def run_performance_agent(state: ReviewState):
    result = analyze_performance(state["code"], state["file_path"])
    return {"results": state.get("results", []) + [result]}


def build_graph():
    builder = StateGraph(ReviewState)

    def check_critical(state: ReviewState):
        for result in state["results"]:
            for issue in result.issues:
                if issue.severity >= 4:
                    return "halt"
        return "continue"

    builder.add_node("load_code", load_code)
    builder.add_node("code_agent", run_code_agent)
    builder.add_node("security_agent", run_security_agent)
    builder.add_node("aggregate", aggregate)
    builder.add_node("performance_agent", run_performance_agent)

    builder.set_entry_point("load_code")

    builder.add_edge("load_code", "code_agent")
    builder.add_edge("code_agent", "security_agent")
    builder.add_edge("security_agent", "performance_agent")
    builder.add_edge("performance_agent", "aggregate")

    builder.add_edge("aggregate", END)

    return builder.compile()
