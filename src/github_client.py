import requests
import time
from typing import List, Dict, Any
from .config import GITHUB_TOKEN, REPO, PRS_PER_PAGE

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}


def fetch_pull_requests(state: str = "closed", per_page: int = PRS_PER_PAGE) -> List[Dict[str, Any]]:
    """
    Fetch a page of pull requests for the configured repository.
    Returns a list of PR metadata (first page only).
    """
    url = f"https://api.github.com/repos/{REPO}/pulls"
    params = {"state": state, "per_page": per_page}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    pr_list = resp.json()
    return pr_list


def fetch_pr_diff(pr_number: int) -> str:
    diff_url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}"
    headers = HEADERS.copy()
    headers["Accept"] = "application/vnd.github.v3.diff"
    r = requests.get(diff_url, headers=headers)
    r.raise_for_status()
    return r.text


def fetch_pr_comments(pr_number: int) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def collect_prs_full(n: int = 50) -> List[Dict[str, Any]]:
    pr_meta = fetch_pull_requests(per_page=n)
    data = []
    for pr in pr_meta:
        num = pr["number"]
        body = pr.get("body") or ""
        title = pr.get("title") or ""
        created_at = pr.get("created_at")
        merged = pr.get("merged_at") is not None
        try:
            diff = fetch_pr_diff(num)
        except Exception as e:
            diff = ""
        try:
            comments = fetch_pr_comments(num)
        except Exception:
            comments = []
        data.append({
            "pr_number": num,
            "title": title,
            "description_original": body,
            "created_at": created_at,
            "merged": merged,
            "diff": diff,
            "comments": comments
        })
        time.sleep(0.5) 
    return data
