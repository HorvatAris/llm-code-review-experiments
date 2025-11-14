import os
from src.evaluate import evaluate_dataframe


def main():
    os.makedirs("results", exist_ok=True)
    in_path = "results/summaries.csv"
    out_path = "results/evaluated_summaries.csv"
    df = evaluate_dataframe(in_path, out_csv=out_path)
    print(f"Saved evaluated results to {out_path}")
    print(df[["pr_number", "rougeL"]].head())


if __name__ == "__main__":
    main()
