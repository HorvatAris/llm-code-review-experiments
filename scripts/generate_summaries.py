import os
import pandas as pd
from src.preprocessing import trim_diff, normalize_text
from src.llm_client import safe_generate
from tqdm import tqdm


def main():
    os.makedirs("results", exist_ok=True)
    df = pd.read_csv("data/pull_requests.csv")
    df["diff_clean"] = df["diff"].fillna("").apply(lambda d: normalize_text(trim_diff(d)))
    df["description_generated"] = ""

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        diff = row["diff_clean"]
        if not diff:
            df.at[idx, "description_generated"] = ""
            continue
        try:
            gen = safe_generate(diff)
        except Exception as e:
            gen = f"[ERROR_GENERATING] {e}"
        df.at[idx, "description_generated"] = gen

    out_path = "results/summaries.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated summaries saved to {out_path}")


if __name__ == "__main__":
    main()
