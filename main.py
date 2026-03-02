from graph.workflow import build_graph


def main():
    graph = build_graph()

    result = graph.invoke({
        "file_path": "sample.py",   # Change this to analyze any file
        "results": []
    })

    print("\nUnified Review Report:\n")

    # Safety check: ensure result is dictionary
    if not isinstance(result, dict):
        print("Unexpected result type:", type(result))
        return

    # If pipeline halted due to critical issue
    if "message" in result:
        print(result["message"])
        return

    # Print summary if available
    summary = result.get("summary")
    if summary:
        print("Summary:")
        print(f"Total Issues: {summary.get('total_issues', 0)}")
        print(f"Critical: {summary.get('critical', 0)}")
        print(f"Serious: {summary.get('serious', 0)}")
        print(f"Moderate: {summary.get('moderate', 0)}")
        print(f"Low: {summary.get('low', 0)}")
        print("-" * 50)

    # Print issues
    final_issues = result.get("final_issues", [])

    for issue in final_issues:
        print(f"[Severity {issue.severity}] {issue.issue_type}")
        print(f"File: {issue.file_path}")
        print(f"Line: {issue.line_number}")
        print(f"Description: {issue.description}")
        print(f"Suggested Fix: {issue.suggested_fix}")
        print("-" * 50)


if __name__ == "__main__":
    main()