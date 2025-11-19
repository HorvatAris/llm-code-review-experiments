import os
import pandas as pd
from src.evaluate import evaluate_dataframe


def main():
    os.makedirs("results", exist_ok=True)

    in_path = "results/summaries.csv"
    out_path = "results/evaluated_summaries.csv"

    df = evaluate_dataframe(in_path, out_csv=out_path)

    table = df[["pr_number", "generated_preview", "rougeL"]]

    print("\n=== Evaluation Summary ===")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
