
import os
import joblib
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.preprocessing import load_and_clean_data, split_data
from src.intent_features import extract_intent_features


# ============================================================
# 1. CONFIGURATION
# ============================================================

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

MODEL_PATH = "models/intent_classifier_merged_test.joblib"


C_VALUES = [0.1, 0.5, 1, 3, 5, 10, 20, 50]

RANDOM_STATE = 42

CUSTOM_FEATURE_NAMES = [
    "how_to_pay",
    "online_payment",
    "payment_problem",
    "bill_not_received",
    "unpaid_bill",
    "voltage_problem",
    "wrong_meter_reading",
    "neighborhood_outage",
]


# ============================================================
# 2. LOAD DATA
# ============================================================

data = load_and_clean_data()

print("=" * 65)
print("DATASET OVERVIEW")
print("=" * 65)

print("Total examples:", len(data))
print("Number of intents:", data["Intent"].nunique())

print("\nExamples per intent:")
print(data["Intent"].value_counts().sort_index())

print("\nIntent x Language:")
print(pd.crosstab(data["Intent"], data["Language"]))


# ============================================================
# 3. DATASET QUALITY AUDIT
# ============================================================

print("\n" + "=" * 65)
print("DATA QUALITY AUDIT")
print("=" * 65)

# Find normalized phrases assigned to multiple intents.
conflicts = data.groupby("Phrase")["Intent"].nunique()
conflicting_phrases = conflicts[conflicts > 1].index

print(
    "Phrases assigned to multiple intents:",
    len(conflicting_phrases),
)

if len(conflicting_phrases) > 0:
    print("\nConflicting examples:")
    print(
        data[data["Phrase"].isin(conflicting_phrases)]
        .sort_values("Phrase")
        .to_string(index=False)
    )

# Find identical phrase/intent pairs with multiple language labels.
cross_language = (
    data.groupby(["Phrase", "Intent"])["Language"].nunique()
)

print(
    "\nPhrase/intent pairs with multiple language labels:",
    int((cross_language > 1).sum()),
)


# ============================================================
# 4. TRAIN / VALIDATION / TEST SPLIT
# ============================================================

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_data(data)

print("\n" + "=" * 65)
print("DATA SPLIT")
print("=" * 65)

print("Training:", len(X_train))
print("Validation:", len(X_val))
print("Test:", len(X_test))


# ============================================================
# 5. CREATE MINILM EMBEDDINGS
# ============================================================

print("\nLoading MiniLM...")

embedding_model = SentenceTransformer(MODEL_NAME)

print("\nEncoding training messages...")

E_train = embedding_model.encode(
    X_train,
    show_progress_bar=True,
    convert_to_numpy=True,
)

print("\nEncoding validation messages...")

E_val = embedding_model.encode(
    X_val,
    show_progress_bar=True,
    convert_to_numpy=True,
)

print("\nEncoding test messages...")

E_test = embedding_model.encode(
    X_test,
    show_progress_bar=True,
    convert_to_numpy=True,
)


# ============================================================
# 6. EXTRACT CUSTOM FEATURES
# ============================================================

F_train = extract_intent_features(X_train)
F_val = extract_intent_features(X_val)
F_test = extract_intent_features(X_test)

print("\nEmbedding shape:", E_train.shape)
print("Custom feature shape:", F_train.shape)

print(
    "Training examples with at least one matched feature:",
    int((F_train.sum(axis=1) > 0).sum()),
    "/",
    len(F_train),
)

print("\nCustom feature activation counts:")

for index, name in enumerate(CUSTOM_FEATURE_NAMES):
    print(f"{name}: {int(F_train[:, index].sum())}")


# ============================================================
# 7. BUILD TWO REPRESENTATIONS
# ============================================================

representations = {
    "embeddings_only": (
        E_train,
        E_val,
        E_test,
    ),

    "embeddings_plus_features": (
        np.hstack([E_train, F_train]),
        np.hstack([E_val, F_val]),
        np.hstack([E_test, F_test]),
    ),
}


# ============================================================
# 8. COMPARE REPRESENTATIONS AND TUNE C
# ============================================================

results = []
best_models = {}

for representation_name, (Xtr, Xv, Xt) in representations.items():

    print("\n" + "=" * 65)
    print("EXPERIMENT:", representation_name)
    print("=" * 65)

    best_f1 = -1.0
    best_C = None
    best_model = None
    best_val_accuracy = 0.0

    for C in C_VALUES:

        classifier = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=C,
                max_iter=3000,
                random_state=RANDOM_STATE,
            ),
        )

        classifier.fit(Xtr, y_train)

        val_predictions = classifier.predict(Xv)

        val_accuracy = accuracy_score(
            y_val,
            val_predictions,
        )

        val_macro_f1 = f1_score(
            y_val,
            val_predictions,
            average="macro",
            zero_division=0,
        )

        results.append({
            "representation": representation_name,
            "C": C,
            "validation_accuracy": val_accuracy,
            "validation_macro_f1": val_macro_f1,
        })

        print(
            f"C={C:<5} "
            f"accuracy={val_accuracy:.4f} "
            f"macro_f1={val_macro_f1:.4f}"
        )

        # Choose hyperparameters using validation macro F1 only.
        if val_macro_f1 > best_f1:
            best_f1 = val_macro_f1
            best_C = C
            best_model = classifier
            best_val_accuracy = val_accuracy

    best_models[representation_name] = {
        "classifier": best_model,
        "C": best_C,
        "validation_macro_f1": best_f1,
        "validation_accuracy": best_val_accuracy,
    }


# ============================================================
# 9. DISPLAY VALIDATION RESULTS
# ============================================================

results_df = pd.DataFrame(results)

print("\n" + "=" * 65)
print("ALL VALIDATION RESULTS")
print("=" * 65)

print(
    results_df.sort_values(
        ["representation", "validation_macro_f1"],
        ascending=[True, False],
    ).to_string(index=False)
)

print("\nBest configuration per representation:")

for name, info in best_models.items():
    print(
        f"{name}: C={info['C']}, "
        f"validation accuracy={info['validation_accuracy']:.4f}, "
        f"validation macro F1={info['validation_macro_f1']:.4f}"
    )


# ============================================================
# 10. FINAL TEST EVALUATION AND ERROR ANALYSIS
# ============================================================

os.makedirs("reports", exist_ok=True)

test_results = []

for representation_name, (Xtr, Xv, Xt) in representations.items():

    info = best_models[representation_name]
    classifier = info["classifier"]

    predictions = classifier.predict(Xt)

    y_true = np.asarray(y_test)
    y_pred = np.asarray(predictions)
    test_messages = np.asarray(X_test, dtype=object)

    accuracy = accuracy_score(y_true, y_pred)

    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    test_results.append({
        "representation": representation_name,
        "C": info["C"],
        "test_accuracy": accuracy,
        "test_macro_f1": macro_f1,
    })

    print("\n" + "=" * 65)
    print("TEST REPORT:", representation_name)
    print("=" * 65)

    print(f"Test accuracy: {accuracy:.4f}")
    print(f"Test macro F1: {macro_f1:.4f}")

    print(
        classification_report(
            y_true,
            y_pred,
            zero_division=0,
        )
    )

    # --------------------------------------------------------
    # Save individual misclassified messages
    # --------------------------------------------------------

    error_mask = y_true != y_pred

    errors = pd.DataFrame({
        "message": test_messages[error_mask],
        "true_intent": y_true[error_mask],
        "predicted_intent": y_pred[error_mask],
    })

    error_file = (
        f"reports/misclassified_{representation_name}.csv"
    )

    errors.to_csv(error_file, index=False)

    print(
        f"Saved {len(errors)} misclassified messages to "
        f"{error_file}"
    )

    # --------------------------------------------------------
    # Save summary of intent confusions
    # --------------------------------------------------------

    if not errors.empty:
        confusion_summary = (
            errors.groupby(
                ["true_intent", "predicted_intent"]
            )
            .size()
            .reset_index(name="count")
            .sort_values(
                "count",
                ascending=False,
            )
        )
    else:
        confusion_summary = pd.DataFrame(
            columns=[
                "true_intent",
                "predicted_intent",
                "count",
            ]
        )

    confusion_file = (
        f"reports/confusions_{representation_name}.csv"
    )

    confusion_summary.to_csv(confusion_file, index=False)

    print(f"Saved confusion summary to {confusion_file}")


# ============================================================
# 11. FINAL COMPARISON
# ============================================================

test_results_df = pd.DataFrame(test_results)

print("\n" + "=" * 65)
print("FINAL COMPARISON")
print("=" * 65)

print(test_results_df.to_string(index=False))


# ============================================================
# 12. SELECT MODEL USING VALIDATION PERFORMANCE
# ============================================================

# Do not select the production model based on test performance.
best_representation = max(
    best_models,
    key=lambda name: best_models[name]["validation_macro_f1"],
)

selected = best_models[best_representation]

print("\nSelected representation:", best_representation)
print("Selected C:", selected["C"])


# ============================================================
# 13. RETRAIN SELECTED MODEL ON TRAIN + VALIDATION
# ============================================================

X_train_val_texts = X_train + X_val
y_train_val = y_train + y_val

E_train_val = np.vstack([E_train, E_val])
F_train_val = np.vstack([F_train, F_val])

if best_representation == "embeddings_only":
    X_train_val = E_train_val
else:
    X_train_val = np.hstack([
        E_train_val,
        F_train_val,
    ])

production_classifier = make_pipeline(
    StandardScaler(),
    LogisticRegression(
        C=selected["C"],
        max_iter=3000,
        random_state=RANDOM_STATE,
    ),
)

production_classifier.fit(
    X_train_val,
    y_train_val,
)


# ============================================================
# 14. SAVE MODEL AND CONFIGURATION
# ============================================================

os.makedirs("models", exist_ok=True)

artifact = {
    "classifier": production_classifier,
    "embedding_model_name": MODEL_NAME,
    "representation": best_representation,
    "custom_feature_names": CUSTOM_FEATURE_NAMES,
    "C": selected["C"],
}

joblib.dump(artifact, MODEL_PATH)

print("\nProduction model saved to:", MODEL_PATH)
print("Training complete.")
