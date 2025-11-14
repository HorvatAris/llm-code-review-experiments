import os
from src.github_client import collect_prs_full
from src.utils import save_prs_to_csv


def main():
    os.makedirs("data", exist_ok=True)
    print("Collecting PRs ...")
    prs = collect_prs_full(n=50)
    csv_path = save_prs_to_csv(prs, path="data/pull_requests.csv")
    print(f"Saved PRs to {csv_path}")


if __name__ == "__main__":
    main()
