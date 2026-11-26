
import os
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    ROOT, "code", "backend", "data", "processed",
    "codeshield_dataset.csv"
)

OUTPUT_DIR = os.path.join(
    ROOT, "code", "backend", "data", "processed"
)

# 1. Load original dataset
df = pd.read_csv(DATASET_PATH)

print("Original dataset:", len(df))

# 2. Normalize code for duplicate detection
df["normalized_code"] = (
    df["code"].fillna("").astype(str).str.split().str.join(" ")
)

# 3. Check for conflicting labels before removing duplicates
label_counts = df.groupby("normalized_code")["label"].nunique()
conflicts = label_counts[label_counts > 1]

if not conflicts.empty:
    raise ValueError(
        "Duplicate code samples have conflicting labels. "
        "Resolve these manually before splitting."
    )

# 4. Remove normalized duplicates
df = df.drop_duplicates(
    subset=["normalized_code"],
    keep="first"
).copy()

df = df.drop(columns=["normalized_code"])

print("After deduplication:", len(df))
print("\nClass distribution:")
print(df["label"].value_counts())

# 5. Split: 70% training, 15% validation, 15% testing
train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    stratify=df["label"],
    random_state=42
)

validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    stratify=temp_df["label"],
    random_state=42
)

# 6. Save splits
os.makedirs(OUTPUT_DIR, exist_ok=True)

train_df.to_csv(
    os.path.join(OUTPUT_DIR, "train.csv"), index=False
)

validation_df.to_csv(
    os.path.join(OUTPUT_DIR, "validation.csv"), index=False
)

test_df.to_csv(
    os.path.join(OUTPUT_DIR, "test.csv"), index=False
)

# 7. Report
print("\n========== NEW SPLIT RESULTS ==========")
print("Training:", len(train_df))
print("Validation:", len(validation_df))
print("Testing:", len(test_df))

for name, split in [
    ("TRAIN", train_df),
    ("VALIDATION", validation_df),
    ("TEST", test_df)
]:
    print(f"\n{name} DISTRIBUTION")
    print(split["label"].value_counts())

print("\nNew splits saved successfully.")
