import os
import ast
import pandas as pd
from datasets import load_dataset


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OWASP_DIR = os.path.join(
    PROJECT_ROOT,
    "code",
    "backend",
    "data",
    "raw",
    "owasp"
)

OWASP_CSV = os.path.join(
    OWASP_DIR,
    "expectedresults-0.1.csv"
)

OWASP_TESTCODE_DIR = os.path.join(
    OWASP_DIR,
    "testcode"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "code",
    "backend",
    "data",
    "processed"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "codeshield_dataset.csv"
)


# ============================================================
# CODE SHIELD LABEL MAPPING
# ============================================================

CWE_TO_LABEL = {
    "CWE-89": "SQL Injection",

    "CWE-78": "Command Injection",
    "CWE-77": "Command Injection",

    "CWE-798": "Hardcoded Credentials",

    "CWE-22": "Insecure File Handling",

    "CWE-79": "Cross-Site Scripting",
}


# OWASP category mapping
OWASP_CATEGORY_TO_CWE = {
    "sqli": "CWE-89",
    "cmdi": "CWE-78",
    "xss": "CWE-79",
    "pathtraver": "CWE-22",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_code(code):
    """Normalize source code whitespace."""

    if not isinstance(code, str):
        return ""

    code = code.replace("\r\n", "\n")
    code = code.replace("\r", "\n")

    return code.strip()


def get_remediation_cwe(metadata):
    """Extract CWE from remediation dataset metadata."""

    if not isinstance(metadata, dict):
        return None

    cwe = metadata.get("cwe")

    if not cwe:
        return None

    cwe = str(cwe).strip().upper()

    if not cwe.startswith("CWE-"):
        return None

    return cwe


def is_valid_python(code):
    """
    Check whether the example is syntactically valid Python.
    """

    if not code:
        return False

    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# ============================================================
# LOAD OWASP
# ============================================================

def load_owasp():

    print("\n========== OWASP BENCHMARK ==========")

    df = pd.read_csv(OWASP_CSV)

    # Remove accidental spaces from CSV column names
    df.columns = df.columns.str.strip()

    records = []

    for _, row in df.iterrows():

        category = str(row["category"]).strip().lower()

        if category not in OWASP_CATEGORY_TO_CWE:
            continue

        cwe = OWASP_CATEGORY_TO_CWE[category]

        test_name = str(row["# test name"]).strip()

        # OWASP filenames have .py
        file_path = os.path.join(
            OWASP_TESTCODE_DIR,
            test_name + ".py"
        )

        if not os.path.exists(file_path):
            print(f"WARNING: Missing {file_path}")
            continue

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            code = clean_code(f.read())

        if not is_valid_python(code):
            continue

        real_vulnerability = bool(row["real vulnerability"])

        if real_vulnerability:
            label = CWE_TO_LABEL[cwe]
        else:
            label = "SAFE"

        records.append({
            "code": code,
            "label": label,
            "cwe": cwe,
            "source": "OWASP"
        })

    print(f"OWASP examples collected: {len(records)}")

    return records


# ============================================================
# LOAD PYTHON VULNERABILITY REMEDIATION DATASET
# ============================================================

def load_remediation():

    print("\n========== REMEDIATION DATASET ==========")

    dataset = load_dataset(
        "cmonplz/Python_Vulnerability_Remediation",
        split="train"
    )

    records = []

    for example in dataset:

        metadata = example.get("metadata", {})

        cwe = get_remediation_cwe(metadata)

        # Only keep our target CWEs
        if cwe not in CWE_TO_LABEL:
            continue

        # We only want Python examples
        language = str(
            metadata.get("language", "")
        ).strip().lower()

        if language != "python":
            continue

        code = clean_code(
            example.get("input", "")
        )

        if not is_valid_python(code):
            continue

        label = CWE_TO_LABEL[cwe]

        records.append({
            "code": code,
            "label": label,
            "cwe": cwe,
            "source": "Python_Vulnerability_Remediation"
        })

    print(
        f"Remediation examples collected: {len(records)}"
    )

    return records


# ============================================================
# COMBINE DATASETS
# ============================================================

def combine_datasets():

    print("\n========== COMBINING DATASETS ==========")

    owasp_records = load_owasp()

    remediation_records = load_remediation()

    all_records = (
        owasp_records +
        remediation_records
    )

    df = pd.DataFrame(all_records)

    print(
        f"Total before deduplication: {len(df)}"
    )

    # --------------------------------------------------------
    # Remove exact duplicate code + label combinations
    # --------------------------------------------------------

    df = df.drop_duplicates(
        subset=["code", "label"]
    ).reset_index(drop=True)

    print(
        f"Total after deduplication: {len(df)}"
    )

    # --------------------------------------------------------
    # Remove empty code
    # --------------------------------------------------------

    df = df[
        df["code"].str.strip() != ""
    ].reset_index(drop=True)

    # --------------------------------------------------------
    # Create unique ID
    # --------------------------------------------------------

    df.insert(
        0,
        "id",
        range(1, len(df) + 1)
    )

    return df


# ============================================================
# DATASET SUMMARY
# ============================================================

def print_summary(df):

    print("\n========== FINAL DATASET ==========")

    print(
        f"Total examples: {len(df)}"
    )

    print("\nClass distribution:")

    print(
        df["label"].value_counts().to_string()
    )

    print("\nCWE distribution:")

    print(
        df["cwe"].value_counts().to_string()
    )

    print("\nSource distribution:")

    print(
        df["source"].value_counts().to_string()
    )


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df = combine_datasets()

    print_summary(df)

    # Save dataset

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nDataset saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()