def aggregate_results(state):
    all_results = state.get("results", [])

    all_issues = []
    for agent_result in all_results:
        all_issues.extend(agent_result.issues)

    unique = {}

    for issue in all_issues:
        key = (issue.issue_type, issue.line_number)

        if key not in unique:
            unique[key] = issue
        else:
            # Keep higher severity version
            if issue.severity > unique[key].severity:
                unique[key] = issue

    final_issues = list(unique.values())
    final_issues.sort(key=lambda x: x.severity, reverse=True)

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