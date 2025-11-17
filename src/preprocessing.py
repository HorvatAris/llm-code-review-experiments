import re
from typing import List


def trim_diff(diff: str, max_chars: int = 15000) -> str:
    """
    Trim diff nicely: keep file headers and first/last parts.
    """
    if len(diff) <= max_chars:
        return diff
    parts = diff.split("\n@@")
    kept = []
    for p in parts:
        if len("\n".join(kept)) > max_chars - 2000:
            break
        kept.append(p if p.startswith("@@") else p)
    text = "\n@@".join(kept)
    return text[:max_chars]


def normalize_text(text: str) -> str:
    t = re.sub(r"\s+\n", "\n", text)
    t = re.sub(r"\r", "", t)
    return t.strip()
