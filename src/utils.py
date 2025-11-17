import json
import pandas as pd
from typing import List, Dict


def save_prs_to_csv(prs: List[Dict], path="data/pull_requests.csv"):
    rows = []
    for p in prs:
        rows.append({
            "pr_number": p.get("pr_number"),
            "title": p.get("title"),
            "description_original": p.get("description_original", ""),
            "created_at": p.get("created_at"),
            "merged": p.get("merged"),
            "diff": p.get("diff", ""),
            "comments": json.dumps(p.get("comments", []))
        })
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return path


def load_prs_csv(path="data/pull_requests.csv"):
    return pd.read_csv(path)
