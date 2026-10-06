import joblib
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer

from src.preprocessing import (
    load_and_clean_data,
    split_data,
)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from src.intent_features import extract_intent_features

# ============================================================
# 1. CONFIGURATION
# ============================================================

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

MODEL_PATH = "models/intent_classifier.joblib"


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

X_train_features = extract_intent_features(X_train)
X_val_features = extract_intent_features(X_val)
X_test_features = extract_intent_features(X_test)

X_train_embeddings = np.hstack(
    [X_train_embeddings, X_train_features]
)

X_val_embeddings = np.hstack(
    [X_val_embeddings, X_val_features]
)

X_test_embeddings = np.hstack(
    [X_test_embeddings, X_test_features]
)
print(
    "\nEmbedding shape:",
    X_train_embeddings.shape
)


# ============================================================
# 6. EXPERIMENT 1 — COMPARE CLASSIFIER FAMILIES
# ============================================================

classifiers = {

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

    classifier.fit(
        X_train_embeddings,
        y_train,
    )

    train_predictions = classifier.predict(
        X_train_embeddings
    )

    val_predictions = classifier.predict(
        X_val_embeddings
    )

    train_accuracy = accuracy_score(
        y_train,
        train_predictions,
    )

    val_accuracy = accuracy_score(
        y_val,
        val_predictions,
    )

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

    classifier.fit(
        X_train_embeddings,
        y_train,
    )

    train_predictions = classifier.predict(
        X_train_embeddings
    )

    val_predictions = classifier.predict(
        X_val_embeddings
    )

    train_accuracy = accuracy_score(
        y_train,
        train_predictions,
    )

    val_accuracy = accuracy_score(
        y_val,
        val_predictions,
    )

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


final_classifier = LogisticRegression(
    C=best_C,
    max_iter=3000,
)


final_classifier.fit(
    X_train_embeddings,
    y_train,
)


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
# 12. MOST COMMON MISCLASSIFICATIONS
# ============================================================

from collections import Counter

misclassifications = Counter()

for true_label, predicted_label in zip(
    y_test,
    test_predictions,
):
    if true_label != predicted_label:
        misclassifications[
            (true_label, predicted_label)
        ] += 1


print("\n" + "=" * 60)
print("MOST COMMON MISCLASSIFICATIONS")
print("=" * 60)

for (true_label, predicted_label), count in (
    misclassifications.most_common(30)
):
    print(
        f"{count:>3}  "
        f"{true_label}  -->  {predicted_label}"
    )

print("\n" + "=" * 60)
print("MISCLASSIFIED TEST EXAMPLES")
print("=" * 60)

for phrase, true_label, predicted_label in zip(
    X_test,
    y_test,
    test_predictions,
):
    if true_label != predicted_label:
        print(
            f"\nPhrase: {phrase}"
            f"\nTrue: {true_label}"
            f"\nPredicted: {predicted_label}"
        )