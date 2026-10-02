import pandas as pd
from sklearn.model_selection import train_test_split


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
    clean the text, remove empty rows and duplicates.
    """

    dataframes = []

    for file in DATASETS:

        df = pd.read_excel(file)

        # Keep only the columns needed for intent classification
        df = df[["Phrase", "Intent"]]

        dataframes.append(df)

    # Combine all datasets
    data = pd.concat(
        dataframes,
        ignore_index=True,
    )

    # Clean Phrase
    data["Phrase"] = (
        data["Phrase"]
        .astype(str)
        .str.strip()
    )

    # Clean Intent
    data["Intent"] = (
        data["Intent"]
        .astype(str)
        .str.strip()
    )

    # Remove empty rows
    data = data[
        (data["Phrase"] != "")
        & (data["Intent"] != "")
    ]

    # Remove exact duplicate phrase/intent pairs
    data = data.drop_duplicates(
        subset=["Phrase", "Intent"]
    )

    return data


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

def split_data(data):
    """
    Split the dataset into training, validation and test sets.

    80% training
    10% validation
    10% test
    """

    X = data["Phrase"].astype(str).tolist()
    y = data["Intent"].astype(str).tolist()

    # First split:
    # 80% training
    # 20% temporary
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # Second split:
    # 10% validation
    # 10% test
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