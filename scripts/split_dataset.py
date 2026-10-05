import os
import pandas as pd

from sklearn.model_selection import train_test_split


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "code",
    "backend",
    "data",
    "processed",
    "codeshield_dataset.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "code",
    "backend",
    "data",
    "processed"
)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATASET_PATH)

print("Original dataset:", df.shape)

print("\nOriginal class distribution:")
print(df["label"].value_counts())


# ============================================================
# FIRST SPLIT
# 70% TRAIN
# 30% TEMPORARY
# ============================================================

train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    stratify=df["label"],
    random_state=42
)


# ============================================================
# SECOND SPLIT
# TEMPORARY → VALIDATION + TEST
#
# 50% / 50%
# Therefore:
# 15% validation
# 15% test
# ============================================================

validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    stratify=temp_df["label"],
    random_state=42
)


# ============================================================
# SAVE
# ============================================================

train_path = os.path.join(
    OUTPUT_DIR,
    "train.csv"
)

validation_path = os.path.join(
    OUTPUT_DIR,
    "validation.csv"
)

test_path = os.path.join(
    OUTPUT_DIR,
    "test.csv"
)


train_df.to_csv(
    train_path,
    index=False
)

validation_df.to_csv(
    validation_path,
    index=False
)

test_df.to_csv(
    test_path,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n========== SPLIT RESULTS ==========")

print(
    f"Training:   {len(train_df)} examples"
)

print(
    f"Validation: {len(validation_df)} examples"
)

print(
    f"Test:       {len(test_df)} examples"
)


print("\n========== TRAIN DISTRIBUTION ==========")
print(train_df["label"].value_counts())


print("\n========== VALIDATION DISTRIBUTION ==========")
print(validation_df["label"].value_counts())


print("\n========== TEST DISTRIBUTION ==========")
print(test_df["label"].value_counts())


print("\nFiles saved:")
print(train_path)
print(validation_path)
print(test_path)