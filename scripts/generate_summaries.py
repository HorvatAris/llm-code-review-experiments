import os
import pandas as pd
from src.preprocessing import trim_diff, normalize_text
from src.llm_client import safe_generate
from tqdm import tqdm


def main():
    os.makedirs("results", exist_ok=True)

    df = pd.read_csv("data/pull_requests.csv")
    df["diff_clean"] = df["diff"].fillna("").apply(
        lambda d: normalize_text(trim_diff(d))
    )

    df["description_generated"] = ""
    df["generated_preview"] = ""
    df["generation_status"] = ""

    summaries_clean_list = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        pr_number = row.get("pr_number", idx)
        diff = row["diff_clean"]

        if not diff.strip():
            df.at[idx, "generation_status"] = "no_diff"
            summaries_clean_list.append({
                "pr_number": pr_number,
                "summary": "",
                "status": "no_diff"
            })
            continue

        try:
            summary = safe_generate(diff)
            df.at[idx, "description_generated"] = summary
            df.at[idx, "generated_preview"] = summary[:160]
            df.at[idx, "generation_status"] = "ok"

            summaries_clean_list.append({
                "pr_number": pr_number,
                "summary": summary,
                "status": "ok"
            })

        except Exception as e:
            df.at[idx, "generation_status"] = f"error: {e}"
            summaries_clean_list.append({
                "pr_number": pr_number,
                "summary": "",
                "status": f"error: {e}"
            })

    # Save full CSV
    out_path = "results/summaries.csv"
    df.to_csv(out_path, index=False)
    print(f"\nFull CSV saved to {out_path}")

    # Save CLEAN summaries only
    clean_df = pd.DataFrame(summaries_clean_list)
    clean_path = "results/summaries_clean.csv"
    clean_df.to_csv(clean_path, index=False)
    print(f"Clean summaries saved to {clean_path}")

    # Save pretty text file
    txt_path = "results/summaries_readable.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for item in summaries_clean_list:
            f.write(f"=== PR {item['pr_number']} ===\n")
            f.write(f"STATUS: {item['status']}\n\n")
            f.write(item["summary"] if item["summary"] else "[NO SUMMARY]\n")
            f.write("\n" + "-"*60 + "\n\n")
    print(f"Readable text file saved to {txt_path}")

    print("\n---- SAMPLE OF FIRST 5 GENERATED SUMMARIES ----")
    for item in summaries_clean_list[:5]:
        print(f"\nPR {item['pr_number']}:\n{item['summary']}\n")


if __name__ == "__main__":
    main()
