import joblib

from sentence_transformers import SentenceTransformer


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
    Convert a user sentence into a MiniLM embedding
    and predict its intent.
    """

    embedding = embedding_model.encode(
        [text]
    )

    prediction = classifier.predict(
        embedding
    )

    return prediction[0]


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

        intent = predict_intent(
            text
        )

        print(
            "Predicted intent:",
            intent
        )

        print()