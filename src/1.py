
import pandas as pd

path = "data/processed/merged_intents_augmented.xlsx"
df = pd.read_excel(path)

targets = [
    "understand_bill",
    "amount_breakdown",
    "bill_amount_issue",
    "bill_payment_methods",
]

keywords = [
    "montant", "total", "frais", "détail", "detail",
    "facture", "expliquer", "comprendre", "taxe",
    "مبلغ", "الفاتورة", "المصاريف",
]

for intent in targets:
    subset = df[df["Intent"] == intent].copy()
    phrase_col = "Phrase"

    mask = subset[phrase_col].fillna("").apply(
        lambda text: any(
            word in text.lower() for word in keywords
        )
    )

    print(f"\n{'=' * 60}")
    print(f"{intent}: matching examples")
    print("=" * 60)

    print(
        subset.loc[mask, phrase_col]
        .drop_duplicates()
        .head(30)
        .to_string(index=False)
    )
