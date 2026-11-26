import csv
import json
from collections import Counter
from pathlib import Path
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "code/backend/data/processed"

FILES = {
    "dataset": DATA_DIR / "codeshield_dataset.csv",
    "train": DATA_DIR / "train.csv",
    "validation": DATA_DIR / "validation.csv",
    "test": DATA_DIR / "test.csv",
}

def load_csv(path):
    if not path.exists():
        print(f"\nMissing file: {path}")
        return []

    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def fingerprint(code):
    normalized = " ".join((code or "").split())
    return sha256(normalized.encode("utf-8")).hexdigest()

report = {}

print("\n========== CODESHIELD DATASET AUDIT ==========")

split_hashes = {}

for name, path in FILES.items():
    rows = load_csv(path)

    if not rows:
        continue

    labels = Counter()
    missing_code = 0
    missing_label = 0
    hashes = []

    for row in rows:
        code = (row.get("code") or "").strip()
        label = (row.get("label") or "").strip()

        if not code:
            missing_code += 1

        if not label:
            missing_label += 1

        if code:
            hashes.append(fingerprint(code))

        if label:
            labels[label] += 1

    duplicates = len(hashes) - len(set(hashes))
    split_hashes[name] = set(hashes)

    report[name] = {
        "rows": len(rows),
        "class_distribution": dict(labels),
        "missing_code": missing_code,
        "missing_label": missing_label,
        "duplicate_code_rows": duplicates,
    }

    print(f"\n--- {name.upper()} ---")
    print("Rows:", len(rows))
    print("Classes:", dict(labels))
    print("Missing code:", missing_code)
    print("Missing labels:", missing_label)
    print("Duplicate code rows:", duplicates)

print("\n========== CROSS-SPLIT OVERLAP ==========")

split_names = ["train", "validation", "test"]

for i, first in enumerate(split_names):
    for second in split_names[i + 1:]:
        if first in split_hashes and second in split_hashes:
            overlap = split_hashes[first] & split_hashes[second]

            print(
                f"{first} vs {second}: "
                f"{len(overlap)} identical code samples"
            )

report_path = DATA_DIR / "dataset_audit_report.json"
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("\nAudit report saved to:", report_path)
print("\nDATASET AUDIT COMPLETED")
