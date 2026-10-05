from datasets import load_dataset
import pandas as pd
import os


print("========== OWASP ==========")

owasp_csv = "data/raw/owasp/expectedresults-0.1.csv"

owasp = pd.read_csv(owasp_csv)

print("OWASP shape:", owasp.shape)
print("\nOWASP columns:")
print(owasp.columns.tolist())

print("\nFirst 5 rows:")
print(owasp.head())


print("\n========== REMEDIATION ==========")

ds = load_dataset(
    "cmonplz/Python_Vulnerability_Remediation",
    split="train"
)

remediation = ds.to_pandas()

print("Remediation shape:", remediation.shape)

print("\nRemediation columns:")
print(remediation.columns.tolist())

print("\nFirst 5 rows:")
print(remediation.head())