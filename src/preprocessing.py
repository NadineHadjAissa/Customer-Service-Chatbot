import pandas as pd
from sklearn.model_selection import train_test_split

import re
import unicodedata

# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize a user message before prediction.
    """

    text = str(text).strip().lower()

    # Normalize Unicode characters
    text = unicodedata.normalize(
        "NFC",
        text
    )

    # Normalize common apostrophe variants
    text = text.replace("’", "'")
    text = text.replace("`", "'")

    # --------------------------------------------------------
    # Common French typing variations
    # --------------------------------------------------------

    text = re.sub(
        r"\bje\s+nest\s+pas\b",
        "je n'ai pas",
        text
    )

    text = re.sub(
        r"\brecu\b",
        "reçu",
        text
    )

    text = re.sub(
        r"\barrivee\b",
        "arrivée",
        text
    )

    # --------------------------------------------------------
    # Collapse repeated whitespace
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# CONFIGURATION
# ============================================================

DATASETS = [
    "data/dataset_facture.xlsx",
    "data/dataset_panne.xlsx",
    "data/dataset_raccordement.xlsx",
]


# ============================================================
# LOAD AND CLEAN DATA
# ============================================================

def load_and_clean_data():
    """
    Load all datasets, keep the required columns,
    clean the text, normalize language labels,
    remove empty rows and duplicates.
    """

    dataframes = []

    for file in DATASETS:

        df = pd.read_excel(file)

        # The Excel files use "Langue"
        df = df[["Phrase", "Intent", "Langue"]]

        # Rename internally to "Language"
        df = df.rename(
            columns={"Langue": "Language"}
        )

        dataframes.append(df)

    # --------------------------------------------------------
    # Combine all datasets
    # --------------------------------------------------------

    data = pd.concat(
        dataframes,
        ignore_index=True,
    )

    # --------------------------------------------------------
    # Clean Phrase
    # --------------------------------------------------------

    data["Phrase"] = (
        data["Phrase"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Clean Intent
    # --------------------------------------------------------

    data["Intent"] = (
        data["Intent"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Clean Language
    # --------------------------------------------------------

    data["Language"] = (
        data["Language"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Standardize language labels
    # --------------------------------------------------------

    # FR -> French
    data.loc[
        data["Language"].str.lower() == "fr",
        "Language"
    ] = "French"

    # Arabizi -> Daridja written in Latin script
    data.loc[
        data["Language"].str.lower() == "arabizi",
        "Language"
    ] = "Daridja_Latin"

    # Mixed stays Mixed
    data.loc[
        data["Language"].str.lower() == "mixed",
        "Language"
    ] = "Mixed"

    # --------------------------------------------------------
    # Detect Arabic script
    # --------------------------------------------------------

    arabic_mask = data["Phrase"].str.contains(
        r"[\u0600-\u06FF]",
        regex=True,
        na=False,
    )

    # --------------------------------------------------------
    # Split Darja into Arabic-script / Latin-script
    # --------------------------------------------------------

    darja_mask = (
        data["Language"].str.lower() == "darja"
    )

    # Darja written in Arabic script
    data.loc[
        darja_mask & arabic_mask,
        "Language"
    ] = "Daridja_Arabic"

    # Darja written using Latin transliteration
    data.loc[
        darja_mask & ~arabic_mask,
        "Language"
    ] = "Daridja_Latin"

    # --------------------------------------------------------
    # Infer missing language labels
    # --------------------------------------------------------

    missing_language = data["Language"] == ""

    # Missing + Arabic script -> Daridja Arabic
    data.loc[
        missing_language & arabic_mask,
        "Language"
    ] = "Daridja_Arabic"

    # Missing + Latin script -> Daridja Latin
    data.loc[
        missing_language & ~arabic_mask,
        "Language"
    ] = "Daridja_Latin"

    # --------------------------------------------------------
    # Remove empty rows
    # --------------------------------------------------------

    data = data[
        (data["Phrase"] != "")
        & (data["Intent"] != "")
        & (data["Language"] != "")
    ]

    # --------------------------------------------------------
    # Remove exact duplicate rows
    # --------------------------------------------------------

    data = data.drop_duplicates(
        subset=["Phrase", "Intent", "Language"]
    )

    return data


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

def split_data(data):
    """
    Split the dataset into:

        80% training
        10% validation
        10% test

    Stratification uses Intent.

    This avoids failures caused by very small
    Intent + Language groups.
    """

    X = data["Phrase"].astype(str).tolist()
    y = data["Intent"].astype(str).tolist()

    # --------------------------------------------------------
    # First split:
    # 80% training
    # 20% temporary
    # --------------------------------------------------------

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------------
    # Second split:
    # 10% validation
    # 10% test
    # --------------------------------------------------------

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp,
    )

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    )
