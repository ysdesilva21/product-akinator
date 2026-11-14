import pandas as pd
from pathlib import Path

df = pd.read_csv("data/product_akinator_100.csv")

features = [
    c for c in df.columns
    if c not in ["product_id", "product_name", "category"]
]

results = []

for _, target in df.iterrows():
    candidates = df.copy()
    remaining = features.copy()
    questions_asked = 0

    while len(candidates) > 1 and remaining:
        # Select question with most balanced split
        scores = {}

        for feature in remaining:
            yes = candidates[feature].sum()
            no = len(candidates) - yes
            scores[feature] = min(yes, no)

        best = max(scores, key=scores.get)

        answer = target[best]

        candidates = candidates[
            candidates[best] == answer
        ]

        remaining.remove(best)
        questions_asked += 1

    results.append({
        "product": target["product_name"],
        "questions": questions_asked,
        "correct": (
            len(candidates) == 1
            and candidates.iloc[0]["product_name"]
            == target["product_name"]
        )
    })

report = pd.DataFrame(results)

print("\n=== GUESSING EFFICIENCY REPORT ===")
print("Accuracy:", round(report["correct"].mean()*100, 2), "%")
print("Average questions:", round(report["questions"].mean(), 2))
print("Maximum questions:", report["questions"].max())
print("Minimum questions:", report["questions"].min())

print("\nHARDEST PRODUCTS:")
print(
    report.sort_values(
        "questions", ascending=False
    ).head(15).to_string(index=False)
)

Path("data").mkdir(exist_ok=True)
report.to_csv(
    "data/guessing_efficiency_report.csv",
    index=False
)
