import os
import pandas as pd

FILES = [
    "data/dataset_facture.xlsx",
    "data/dataset_panne.xlsx",
    "data/dataset_raccordement.xlsx",
]

INTENT_MAPPING = {
    "catch_up_bill": "catch_up_bill",
    "dispute_catch_up_bill": "catch_up_bill",
    "dispute_bill": "bill_amount_issue",
    "high_or_abnormal_amount": "bill_amount_issue",
}

# Load and combine the original datasets.
data = pd.concat(
    [pd.read_excel(file) for file in FILES],
    ignore_index=True
)

# Keep the original labels for verification.
original_intents = data["Intent"].copy()

# Merge the selected intents.
data["Intent"] = data["Intent"].replace(INTENT_MAPPING)

# Verify that only the intended labels changed.
changed = original_intents != data["Intent"]
print("Rows relabeled:", int(changed.sum()))
print("\nRelabeling summary:")
print(
    pd.DataFrame({
        "old": original_intents[changed],
        "new": data.loc[changed, "Intent"],
    }).groupby(["old", "new"]).size().to_string()
)

print("\nNew billing intent counts:")
print(
    data[data["Intent"].isin(["catch_up_bill", "bill_amount_issue"])]
    ["Intent"].value_counts().to_string()
)

# Save to a separate file; original Excel files remain unchanged.
os.makedirs("data/processed", exist_ok=True)
output = "data/processed/merged_intents.xlsx"
data.to_excel(output, index=False)

print(f"\nSaved cleaned dataset to: {output}")
print("Original Excel files were not modified.")
