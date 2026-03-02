import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "rituparna66"
REPO = "sebi-rbi-kyc-compliance"
PR_NUMBER = 1  # change to your PR number

url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/files"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

files = response.json()

for file in files:
    print("FILE:", file["filename"])
    print("PATCH:")
    print(file["patch"])
    print("-" * 80)