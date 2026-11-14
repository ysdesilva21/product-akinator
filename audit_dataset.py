from pathlib import Path
import pandas as pd

path = Path("data/product_akinator_100.csv")
df = pd.read_csv(path)

features = [
    col for col in df.columns
    if col not in ["product_id", "product_name", "category"]
]

print("\n=== PRODUCT AKINATOR QUALITY AUDIT ===")

# Check how informative each question is
stats = []

for feature in features:
    yes = int(df[feature].sum())
    no = len(df) - yes
    balance = min(yes, no) / len(df)

    stats.append({
        "question": feature,
        "yes": yes,
        "no": no,
        "balance": round(balance, 2)
    })

report = pd.DataFrame(stats).sort_values(
    "balance", ascending=False
)

print("\nQUESTION BALANCE:")
print(report.to_string(index=False))

print("\nWEAK QUESTIONS (less than 5% balance):")
weak = report[report["balance"] < 0.05]
print(weak.to_string(index=False) if not weak.empty else "None")

# Check average number of YES attributes
df["yes_count"] = df[features].sum(axis=1)

print("\nPRODUCT FEATURE COUNTS:")
print(df[["product_name", "yes_count"]].sort_values(
    "yes_count"
).to_string(index=False))

print("\nAVERAGE YES FEATURES:",
      round(df["yes_count"].mean(), 2))

# Check uniqueness
collisions = df.duplicated(
    subset=features, keep=False
).sum()

print("\nDUPLICATE ANSWER PATTERNS:", collisions)

# Save report
output = Path("data/question_quality_report.csv")
report.to_csv(output, index=False)

print("\nReport saved:", output)
