from github import Github
import os


def analyze_pull_request(repo_name, pr_number, graph):
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    all_results = []

    for file in pr.get_files():
        if file.filename.endswith(".py"):
            contents = repo.get_contents(file.filename, ref=pr.head.sha)
            code = contents.decoded_content.decode("utf-8")

            result = graph.invoke({
                "file_path": file.filename,
                "results": []
            })

            if isinstance(result, dict):
                all_results.append(result)

    return all_results
