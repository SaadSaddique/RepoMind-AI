import requests
from urllib.parse import quote

GITHUB_API_URL = "https://api.github.com"


def get_repo_details(repo_url):
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


def fetch_file_content(download_url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(download_url, headers=headers)
    response.raise_for_status()
    return response.text


def fetch_files_recursively(owner, repo, path="", token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{quote(path)}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json()

    documents = []

    for item in items:
        if item["type"] == "file":
            if item["name"].endswith((".py", ".md", ".txt", ".js")):
                content = fetch_file_content(item["download_url"], token)
                documents.append(content)
        elif item["type"] == "dir":
            documents.extend(fetch_files_recursively(owner, repo, item["path"], token))

    return documents


def load_github_repo(repo_url, token=None):
    owner, repo = get_repo_details(repo_url)
    documents = fetch_files_recursively(owner, repo, token=token)
    return documents
