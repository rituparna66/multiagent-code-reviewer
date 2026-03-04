import os
import requests
import tempfile
from dotenv import load_dotenv
from tools.patch_parser import extract_patch_metadata
from graph.workflow import build_graph

load_dotenv()


def fetch_pr_files(owner: str, repo: str, pr_number: int):
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise ValueError("GITHUB_TOKEN not found in environment variables")

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    return response.json()


def review_pr(owner: str, repo: str, pr_number: int) -> dict:
    """
    Fetch PR files and run full multi-agent review on each changed file.
    Returns combined results across all files.
    """
    files = fetch_pr_files(owner, repo, pr_number)
    graph = build_graph()

    all_final_issues = []
    combined_summary = {
        "total_issues": 0,
        "critical": 0,
        "serious": 0,
        "moderate": 0,
        "low": 0,
    }

    for pr_file in files:
        filename = pr_file.get("filename", "")
        patch = pr_file.get("patch", "")

        # Only review Python files
        if not filename.endswith(".py") or not patch:
            continue

        # Write patch content to a temp file for the graph
        added_lines = [
            line[1:]
            for line in patch.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]

        if not added_lines:
            continue

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
            tmp.write("\n".join(added_lines))
            file_path = tmp.name

        try:
            result = graph.invoke({
                "file_path": file_path,
                "results": []
            })

            if isinstance(result, dict) and "final_issues" in result:
                all_final_issues.extend(result["final_issues"])
                summary = result.get("summary", {})
                for key in combined_summary:
                    combined_summary[key] += summary.get(key, 0)

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return {
        "pr": f"{owner}/{repo}#{pr_number}",
        "summary": combined_summary,
        "issues": [issue.model_dump() for issue in all_final_issues]
    }


# ── CLI usage ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 4:
        print("Usage: python github_bot.py <owner> <repo> <pr_number>")
        sys.exit(1)

    owner, repo, pr_number = sys.argv[1], sys.argv[2], int(sys.argv[3])
    result = review_pr(owner, repo, pr_number)
    print(json.dumps(result, indent=2))
