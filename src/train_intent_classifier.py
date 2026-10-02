import joblib
import pandas as pd

from sentence_transformers import SentenceTransformer

from src.preprocessing import (
    load_and_clean_data,
    split_data,
)
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. CONFIGURATION
# ============================================================

DATASETS = [
    "data/dataset_facture.xlsx",
    "data/dataset_panne.xlsx",
    "data/dataset_raccordement.xlsx",
]

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

C_VALUES = [
    0.1,
    0.5,
    1,
    3,
    5,
    10,
    15,
    20,
    30,
    50,
    100,
]

# ============================================================
# 2. LOAD AND PREPROCESS DATA
# ============================================================

data = load_and_clean_data()

print("=" * 60)
print("DATASET")
print("=" * 60)

print("Total examples:", len(data))
print("Number of intents:", data["Intent"].nunique())

print("\nExamples per intent:")
print(
    data["Intent"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 3. TRAIN / VALIDATION / TEST SPLIT
# ============================================================

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_data(data)


print("\n" + "=" * 60)
print("DATA SPLIT")
print("=" * 60)

print("Training:", len(X_train))
print("Validation:", len(X_val))
print("Test:", len(X_test))

# ============================================================
# 4. LOAD MULTILINGUAL MINILM
# ============================================================

print("\nLoading MiniLM...")

model = SentenceTransformer(
    MODEL_NAME
)


# ============================================================
# 5. CREATE EMBEDDINGS
# ============================================================

print("\nCreating embeddings...")

X_train_embeddings = model.encode(
    X_train,
    show_progress_bar=True,
)

X_val_embeddings = model.encode(
    X_val,
    show_progress_bar=True,
)

X_test_embeddings = model.encode(
    X_test,
    show_progress_bar=True,
)


print(
    "\nEmbedding shape:",
    X_train_embeddings.shape
)


# ============================================================
# 6. EXPERIMENT 1 — COMPARE CLASSIFIER FAMILIES
# ============================================================

classifiers = {

    # --------------------------------------------------------
    # Logistic Regression
    # --------------------------------------------------------

    "LogisticRegression_C1": Pipeline([
        (
            "classifier",
            LogisticRegression(
                C=1,
                max_iter=3000,
            ),
        )
    ]),

    "LogisticRegression_C3": Pipeline([
        (
            "classifier",
            LogisticRegression(
                C=3,
                max_iter=3000,
            ),
        )
    ]),

    "LogisticRegression_C10": Pipeline([
        (
            "classifier",
            LogisticRegression(
                C=10,
                max_iter=3000,
            ),
        )
    ]),


    # --------------------------------------------------------
    # Linear SVM
    # --------------------------------------------------------

    "SVM_linear_C1": Pipeline([
        (
            "classifier",
            SVC(
                kernel="linear",
                C=1,
            ),
        )
    ]),

    "SVM_linear_C3": Pipeline([
        (
            "classifier",
            SVC(
                kernel="linear",
                C=3,
            ),
        )
    ]),


    # --------------------------------------------------------
    # RBF SVM
    # --------------------------------------------------------

    "SVM_rbf_C1": Pipeline([
        (
            "classifier",
            SVC(
                kernel="rbf",
                C=1,
            ),
        )
    ]),

    "SVM_rbf_C3": Pipeline([
        (
            "classifier",
            SVC(
                kernel="rbf",
                C=3,
            ),
        )
    ]),


    # --------------------------------------------------------
    # KNN
    # --------------------------------------------------------

    "KNN_3": Pipeline([
        (
            "classifier",
            KNeighborsClassifier(
                n_neighbors=3,
            ),
        )
    ]),

    "KNN_5": Pipeline([
        (
            "classifier",
            KNeighborsClassifier(
                n_neighbors=5,
            ),
        )
    ]),
}


classifier_results = []


print("\n" + "=" * 60)
print("EXPERIMENT 1 — CLASSIFIER COMPARISON")
print("=" * 60)


for name, classifier in classifiers.items():

    print(f"\nTraining: {name}")


    # Train
    classifier.fit(
        X_train_embeddings,
        y_train,
    )


    # Training predictions
    train_predictions = classifier.predict(
        X_train_embeddings
    )


    # Validation predictions
    val_predictions = classifier.predict(
        X_val_embeddings
    )


    # Accuracies
    train_accuracy = accuracy_score(
        y_train,
        train_predictions,
    )

    val_accuracy = accuracy_score(
        y_val,
        val_predictions,
    )


    # Training / validation gap
    gap = train_accuracy - val_accuracy


    classifier_results.append({
        "model": name,
        "train_accuracy": train_accuracy,
        "validation_accuracy": val_accuracy,
        "train_val_gap": gap,
    })


    print(
        f"Training accuracy:   {train_accuracy:.4f}"
    )

    print(
        f"Validation accuracy: {val_accuracy:.4f}"
    )

    print(
        f"Train/val gap:       {gap:.4f}"
    )


# Convert results to DataFrame
classifier_results_df = pd.DataFrame(
    classifier_results
)


classifier_results_df = (
    classifier_results_df
    .sort_values(
        "validation_accuracy",
        ascending=False,
    )
)


print("\n" + "=" * 60)
print("CLASSIFIER COMPARISON RESULTS")
print("=" * 60)

print(
    classifier_results_df.to_string(
        index=False,
        formatters={
            "train_accuracy": "{:.4f}".format,
            "validation_accuracy": "{:.4f}".format,
            "train_val_gap": "{:.4f}".format,
        },
    )
)


# ============================================================
# 7. EXPERIMENT 2 — LOGISTIC REGRESSION C SWEEP
# ============================================================

c_results = []


print("\n" + "=" * 60)
print("EXPERIMENT 2 — LOGISTIC REGRESSION C SWEEP")
print("=" * 60)


for C in C_VALUES:

    print(f"\nTesting C = {C}")


    classifier = LogisticRegression(
        C=C,
        max_iter=3000,
    )


    # Train
    classifier.fit(
        X_train_embeddings,
        y_train,
    )


    # Training predictions
    train_predictions = classifier.predict(
        X_train_embeddings
    )


    # Validation predictions
    val_predictions = classifier.predict(
        X_val_embeddings
    )


    # Accuracies
    train_accuracy = accuracy_score(
        y_train,
        train_predictions,
    )

    val_accuracy = accuracy_score(
        y_val,
        val_predictions,
    )


    # Training / validation gap
    gap = train_accuracy - val_accuracy


    c_results.append({
        "C": C,
        "train_accuracy": train_accuracy,
        "validation_accuracy": val_accuracy,
        "train_val_gap": gap,
    })


    print(
        f"Training accuracy:   {train_accuracy:.4f}"
    )

    print(
        f"Validation accuracy: {val_accuracy:.4f}"
    )

    print(
        f"Train/val gap:       {gap:.4f}"
    )


# Convert results to DataFrame
c_results_df = pd.DataFrame(
    c_results
)


c_results_df = (
    c_results_df
    .sort_values(
        "validation_accuracy",
        ascending=False,
    )
)


print("\n" + "=" * 60)
print("LOGISTIC REGRESSION C RESULTS")
print("=" * 60)

print(
    c_results_df.to_string(
        index=False,
        formatters={
            "train_accuracy": "{:.4f}".format,
            "validation_accuracy": "{:.4f}".format,
            "train_val_gap": "{:.4f}".format,
        },
    )
)


# ============================================================
# 8. SELECT FINAL CONFIGURATION
# ============================================================

best_c_row = c_results_df.iloc[0]

best_C = best_c_row["C"]
best_validation_accuracy = (
    best_c_row["validation_accuracy"]
)
best_train_accuracy = (
    best_c_row["train_accuracy"]
)
best_gap = (
    best_c_row["train_val_gap"]
)


print("\n" + "=" * 60)
print("SELECTED CONFIGURATION")
print("=" * 60)

print("Embedding model:", MODEL_NAME)
print("Classifier: Logistic Regression")
print("C:", best_C)

print(
    f"Training accuracy: "
    f"{best_train_accuracy:.4f}"
)

print(
    f"Validation accuracy: "
    f"{best_validation_accuracy:.4f}"
)

print(
    f"Train/validation gap: "
    f"{best_gap:.4f}"
)


# ============================================================
# 9. FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL TEST EVALUATION")
print("=" * 60)


# Train the selected configuration
final_classifier = LogisticRegression(
    C=best_C,
    max_iter=3000,
)


final_classifier.fit(
    X_train_embeddings,
    y_train,
)


# Predict on the untouched test set
test_predictions = final_classifier.predict(
    X_test_embeddings
)


test_accuracy = accuracy_score(
    y_test,
    test_predictions,
)


print(
    f"Test accuracy: {test_accuracy:.4f}"
)

# ============================================================
# 10. SAVE FINAL CLASSIFIER
# ============================================================

MODEL_PATH = "models/intent_classifier.joblib"

joblib.dump(
    final_classifier,
    MODEL_PATH,
)

print("\nFinal classifier saved to:")
print(MODEL_PATH)

# ============================================================
# 11. CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("FINAL CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        test_predictions,
        zero_division=0,
    )
)

# ============================================================
# EXPERIMENT RESULTS — 2026-09-26
# ============================================================
#
# Dataset:
# - 1000 examples
# - 51 intents
# - Train: 800
# - Validation: 100
# - Test: 100
#
# Embedding model:
# sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
# Embedding dimension: 384
#
# Classifier comparison (validation accuracy):
# - Logistic Regression C=10: 96%
# - Linear SVM C=3:            95%
# - Logistic Regression C=3:   94%
# - Linear SVM C=1:            94%
# - Logistic Regression C=1:   93%
# - RBF SVM C=3:               93%
# - RBF SVM C=1:               80%
# - KNN k=3:                   79%
# - KNN k=5:                   72%
#
# Logistic Regression C sweep:
# - C=0.1: 76%
# - C=0.5: 92%
# - C=1:   93%
# - C=3:   94%
# - C=5:   95%
# - C=10:  96%
# - C=15:  96%
# - C=20:  96%
# - C=30:  96%
# - C=50:  96%
# - C=100: 95%
#
# Selected configuration:
# - MiniLM + Logistic Regression
# - C=10
#
# Final evaluation:
# - Training accuracy:   100%
# - Validation accuracy: 96%
# - Test accuracy:       96%
# - Train/validation gap: 4%
#
# Note:
# The test set was kept separate from model selection.
# ============================================================