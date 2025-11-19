from google import genai
from google.genai import types
from .config import GEMINI_KEY
import time

client = genai.Client(api_key=GEMINI_KEY)

MAX_DIFF_LENGTH = 4000


def generate_pr_description(diff_text: str, max_tokens: int = 512) -> str:
    diff_text = diff_text[:MAX_DIFF_LENGTH]
    """
    Use the LLM to generate a PR description from diff_text.
    Keep diff_text trimmed if very long.
    """
    prompt = f"""
    You are an AI assistant that summarizes GitHub Pull Requests.
    Summarize the following PR using code diff.

    === Pull Request Diff ===
    {diff_text}

    Provide a short, clear summary (4–6 sentences).
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=max_tokens
        )
    )

    return response.text.strip()


def safe_generate(diff_text, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            return generate_pr_description(diff_text)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(backoff ** attempt)
            else:
                raise
