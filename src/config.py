import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
REPO = os.getenv("REPO", "scikit-learn/scikit-learn")
PRS_PER_PAGE = int(os.getenv("PRS_PER_PAGE", "30"))

if GITHUB_TOKEN is None:
    raise ValueError("GITHUB_TOKEN not found in environment (.env).")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in environment (.env).")
if GEMINI_KEY is None:
    raise ValueError("GEMINI_API_KEY missing from .env")