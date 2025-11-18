import pandas as pd
from rouge_score import rouge_scorer


def compute_rouge_l(references: list, predictions: list):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = [scorer.score(r, p)["rougeL"].fmeasure for r, p in zip(references, predictions)]
    return scores


def evaluate_dataframe(df_path: str, out_csv: str = None):
    df = pd.read_csv(df_path)
    refs = df["description_original"].fillna("").tolist()
    preds = df["description_generated"].fillna("").tolist()

    rouge_scores = compute_rouge_l(refs, preds)

    df["rougeL"] = rouge_scores

    if out_csv:
        df.to_csv(out_csv, index=False)
    return df
