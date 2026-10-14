
import re
import unicodedata

import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize a user message without changing its meaning."""

    text = str(text).strip().lower()

    # Normalize Unicode characters
    text = unicodedata.normalize("NFC", text)

    # Normalize apostrophe variants
    text = text.replace("’", "'")
    text = text.replace("`", "'")
    text = text.replace("´", "'")

    # Common French typing variations
    text = re.sub(r"\brecu\b", "reçu", text)
    text = re.sub(r"\barrivee\b", "arrivée", text)

    # Collapse repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text


# ============================================================
# CONFIGURATION
# ============================================================
DATASETS = [
    "data/processed/merged_intents_augmented.xlsx",
]

VALID_LANGUAGES = {
    "fr": "French",
    "french": "French",
    "darja": "Darja",
    "darija": "Darja",
    "arabizi": "Arabizi",
    "mixed": "Mixed",
}


# ============================================================
# LOAD AND CLEAN DATA
# ============================================================

def load_and_clean_data():
    """Load, normalize and combine all intent datasets."""

    dataframes = []

    for file in DATASETS:
        df = pd.read_excel(file)

        required_columns = ["Phrase", "Intent", "Langue"]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file} is missing columns: {missing_columns}"
            )

        df = df[required_columns].copy()
        df = df.rename(columns={"Langue": "Language"})

        dataframes.append(df)

    # Combine datasets
    data = pd.concat(dataframes, ignore_index=True)

    # Clean text and intent
    data["Phrase"] = (
        data["Phrase"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    data["Intent"] = (
        data["Intent"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Normalize language labels
    data["Language"] = (
        data["Language"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .map(VALID_LANGUAGES)
        .fillna("")
    )

    # Normalize phrases consistently
    data["Phrase"] = data["Phrase"].apply(normalize_text)

    # Remove empty phrases, intents and unknown language labels
    data = data[
        (data["Phrase"] != "")
        & (data["Intent"] != "")
        & (data["Language"] != "")
    ].copy()

    # Remove exact duplicates within the same intent and language
    data = data.drop_duplicates(
        subset=["Phrase", "Intent", "Language"]
    ).reset_index(drop=True)

    return data


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

def split_data(data):
    """
    Split into 80% training, 10% validation and 10% test.

    Stratify by intent so each split represents the intent classes.
    """

    X = data["Phrase"].astype(str).to_numpy()
    y = data["Intent"].astype(str).to_numpy()

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp,
    )

    return (
        X_train.tolist(),
        X_val.tolist(),
        X_test.tolist(),
        y_train.tolist(),
        y_val.tolist(),
        y_test.tolist(),
    )


# ============================================================
# OPTIONAL DATASET DIAGNOSTICS
# ============================================================

if __name__ == "__main__":
    data = load_and_clean_data()

    print("Dataset loaded successfully.")
    print(f"Total examples: {len(data)}")

    print("\nIntent distribution:")
    print(data["Intent"].value_counts())

    print("\nLanguage distribution:")
    print(data["Language"].value_counts())

    print("\nIntent x Language:")
    print(pd.crosstab(data["Intent"], data["Language"]))

    print("\nDuplicate phrases with different intents:")
    conflicts = (
        data.groupby("Phrase")["Intent"]
        .nunique()
    )
    print((conflicts > 1).sum())
