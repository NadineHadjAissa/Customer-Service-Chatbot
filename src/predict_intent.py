
import joblib
import numpy as np

from sentence_transformers import SentenceTransformer
from src.preprocessing import normalize_text

from src.intent_features import extract_intent_features


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

CLASSIFIER_PATH = "models/intent_classifier.joblib"


# ============================================================
# LOAD MODELS
# ============================================================

print("Loading MiniLM...")

embedding_model = SentenceTransformer(
    MODEL_NAME
)

print("Loading intent classifier...")

classifier = joblib.load(
    CLASSIFIER_PATH
)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_intent(text):
    """
    Convert a user sentence into:
        MiniLM embedding + intent features

    Then return the top 3 predicted intents
    with their probabilities.
    """

    # --------------------------------------------------------
    # 1. MiniLM embedding
    # --------------------------------------------------------

    text = normalize_text(text)

    embedding = embedding_model.encode(
        [text]
    )

    # --------------------------------------------------------
    # 2. Intent-specific features
    # --------------------------------------------------------

    intent_features = extract_intent_features(
        [text]
    )

    # --------------------------------------------------------
    # 3. Combine both
    # --------------------------------------------------------

    embedding = np.hstack(
        [
            embedding,
            intent_features,
        ]
    )

    # --------------------------------------------------------
    # 4. Predict probabilities
    # --------------------------------------------------------

    probabilities = classifier.predict_proba(
        embedding
    )[0]

    # --------------------------------------------------------
    # 5. Get top 3
    # --------------------------------------------------------

    top_indices = probabilities.argsort()[-3:][::-1]

    results = []

    for i in top_indices:

        results.append(
            (
                classifier.classes_[i],
                probabilities[i],
            )
        )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\nIntent classifier is ready!")
    print("Type 'exit' to stop.\n")

    while True:

        text = input("Enter a message: ")

        if text.lower() == "exit":

            print("\nGoodbye!")
            break

        results = predict_intent(
            text
        )

        print("\nTop 3 predictions:")

        for rank, (intent, probability) in enumerate(
            results,
            start=1,
        ):

            print(
                f"  {rank}. {intent}: "
                f"{probability:.3f}"
            )

        print()
