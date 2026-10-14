import os
import joblib
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

from src.preprocessing import normalize_text
from src.intent_features import extract_intent_features

ORIGINAL_FILE = "data/processed/merged_intents.xlsx"
AUGMENTED_FILE = "data/processed/merged_intents_augmented.xlsx"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
OUTPUT_MODEL = "models/intent_classifier_augmented_experiment.joblib"
REPORT_FILE = "reports/augmented_experiment_results.csv"
RANDOM_STATE = 42
C_VALUES = [0.1, 0.5, 1, 3, 10]

def load_dataset(path):
    df = pd.read_excel(path)[["Phrase", "Intent", "Langue"]].copy()
    df = df.rename(columns={"Langue": "Language"})
    df["Phrase"] = df["Phrase"].fillna("").astype(str).str.strip()
    df["Phrase"] = df["Phrase"].apply(normalize_text)
    df["Intent"] = df["Intent"].fillna("").astype(str).str.strip()
    df = df[(df["Phrase"] != "") & (df["Intent"] != "")]
    return df.reset_index(drop=True)

original = load_dataset(ORIGINAL_FILE)
augmented = load_dataset(AUGMENTED_FILE)

# Keep only rows that are new relative to the original phrase/intent pairs.
original_pairs = set(zip(original["Phrase"], original["Intent"]))
extra = augmented[
    ~augmented.apply(
        lambda r: (r["Phrase"], r["Intent"]) in original_pairs,
        axis=1,
    )
].copy()

print("Original examples:", len(original))
print("Additional examples detected:", len(extra))
print("Additional examples by intent:")
print(extra["Intent"].value_counts().to_string())

# Split original data first. The test set is never augmented.
train_df, temp_df = train_test_split(
    original,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=original["Intent"],
)
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=temp_df["Intent"],
)

# Avoid exact normalized phrase overlap between training and held-out data.
heldout_phrases = set(val_df["Phrase"]) | set(test_df["Phrase"])
before = len(train_df)
train_df = train_df[~train_df["Phrase"].isin(heldout_phrases)].copy()
print("Original training examples removed to avoid exact phrase leakage:", before - len(train_df))

# Add extra examples only to training; remove exact phrases already in held-out sets.
extra = extra[~extra["Phrase"].isin(heldout_phrases)].copy()
train_df = pd.concat([train_df, extra], ignore_index=True)

# Ensure every test label is represented in training.
missing = set(test_df["Intent"]) - set(train_df["Intent"])
if missing:
    raise ValueError(f"Test intents missing from training: {sorted(missing)}")

X_train = train_df["Phrase"].tolist()
y_train = train_df["Intent"].tolist()
X_val = val_df["Phrase"].tolist()
y_val = val_df["Intent"].tolist()
X_test = test_df["Phrase"].tolist()
y_test = test_df["Intent"].tolist()

print("\nSplit sizes:")
print("Train (including added examples):", len(X_train))
print("Validation:", len(X_val))
print("Test:", len(X_test))

print("\nLoading MiniLM...")
embedder = SentenceTransformer(MODEL_NAME)

def build_features(texts):
    embeddings = embedder.encode(
        texts, show_progress_bar=True, convert_to_numpy=True
    )
    custom = extract_intent_features(texts)
    return embeddings, custom

E_train, F_train = build_features(X_train)
E_val, F_val = build_features(X_val)
E_test, F_test = build_features(X_test)

representations = {
    "embeddings_only": (E_train, E_val, E_test),
    "embeddings_plus_features": (
        np.hstack([E_train, F_train]),
        np.hstack([E_val, F_val]),
        np.hstack([E_test, F_test]),
    ),
}

results = []
best_models = {}

for name, (Xtr, Xv, Xt) in representations.items():
    best = None

    print(f"\n--- {name} ---")
    for C in C_VALUES:
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=C,
                max_iter=3000,
                random_state=RANDOM_STATE,
            ),
        )
        model.fit(Xtr, y_train)
        pred = model.predict(Xv)
        acc = accuracy_score(y_val, pred)
        macro = f1_score(y_val, pred, average="macro", zero_division=0)

        results.append({
            "representation": name,
            "C": C,
            "validation_accuracy": acc,
            "validation_macro_f1": macro,
        })
        print(f"C={C:<4} validation accuracy={acc:.4f} macro F1={macro:.4f}")

        if best is None or macro > best["validation_macro_f1"]:
            best = {
                "classifier": model,
                "C": C,
                "validation_macro_f1": macro,
                "validation_accuracy": acc,
            }

    best_models[name] = best

print("\n--- Held-out test results ---")
test_results = []

for name, (Xtr, Xv, Xt) in representations.items():
    model = best_models[name]["classifier"]
    pred = model.predict(Xt)
    acc = accuracy_score(y_test, pred)
    macro = f1_score(y_test, pred, average="macro", zero_division=0)

    print(f"\n{name}: C={best_models[name]['C']}")
    print(f"Test accuracy: {acc:.4f}")
    print(f"Test macro F1: {macro:.4f}")
    print(classification_report(y_test, pred, zero_division=0))

    test_results.append({
        "representation": name,
        "C": best_models[name]["C"],
        "test_accuracy": acc,
        "test_macro_f1": macro,
    })

    os.makedirs("reports", exist_ok=True)
    errors = pd.DataFrame({
        "message": X_test,
        "true_intent": y_test,
        "predicted_intent": pred,
    })
    errors = errors[errors["true_intent"] != errors["predicted_intent"]]
    errors.to_csv(f"reports/augmented_errors_{name}.csv", index=False)

# Select only using validation macro F1.
selected_name = max(
    best_models,
    key=lambda n: best_models[n]["validation_macro_f1"],
)
selected = best_models[selected_name]

# Save a model compatible with src/predict_intent.py.
# Fit it on training + validation texts using the selected representation.
X_train_val_text = X_train + X_val
y_train_val = y_train + y_val
E_train_val = np.vstack([E_train, E_val])
F_train_val = np.vstack([F_train, F_val])

if selected_name == "embeddings_only":
    X_train_val = E_train_val
else:
    X_train_val = np.hstack([E_train_val, F_train_val])

final_classifier = make_pipeline(
    StandardScaler(),
    LogisticRegression(C=selected["C"], max_iter=3000, random_state=RANDOM_STATE),
)
final_classifier.fit(X_train_val, y_train_val)

os.makedirs("models", exist_ok=True)
joblib.dump({
    "classifier": final_classifier,
    "embedding_model_name": MODEL_NAME,
    "representation": selected_name,
    "custom_feature_names": [
        "how_to_pay",
        "online_payment",
        "payment_problem",
        "bill_not_received",
        "unpaid_bill",
        "voltage_problem",
        "wrong_meter_reading",
        "neighborhood_outage",
    ],
    "C": selected["C"],
}, OUTPUT_MODEL)

os.makedirs("reports", exist_ok=True)
summary = pd.DataFrame(test_results)
summary.to_csv(REPORT_FILE, index=False)

print("\nSelected using validation macro F1:", selected_name)
print("Selected C:", selected["C"])
print("Experimental model saved to:", OUTPUT_MODEL)
print("Test summary saved to:", REPORT_FILE)
print("Original model files were not changed.")
