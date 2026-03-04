import sys
import os
from graph.workflow import build_graph

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    # Change this to any .py file you want to test
    file_path = "agents/security_agent.py"

    print(f"Running multi-agent review on: {file_path}")
    print("-" * 50)

    graph = build_graph()
    result = graph.invoke({
        "file_path": file_path,
        "results": []
    })

    print("Summary:")
    print(result.get("summary"))
    print("\nIssues:")
    for issue in result.get("final_issues", []):
        print(f"  [{issue.severity}] {issue.issue_type} — {issue.description[:80]}")


if __name__ == "__main__":
    main()
