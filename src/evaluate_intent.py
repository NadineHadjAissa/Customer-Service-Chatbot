import joblib
from sentence_transformers import SentenceTransformer
from collections import defaultdict

CLASSIFIER_PATH = "models/intent_classifier.joblib"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# ============================================================
# Evaluation dataset
# ============================================================

TEST_DATA = [

    # --------------------------------------------------------
    # bill_payment_methods
    # --------------------------------------------------------

    ("bill_payment_methods", "Comment payer ma facture ?"),
    ("bill_payment_methods", "كيفاش نخلص الفاتورة؟"),
    ("bill_payment_methods", "كيفاش نخلص la facture؟"),
    ("bill_payment_methods", "kifach nkhalas la facture"),

    ("bill_payment_methods", "Où puis-je payer ma facture ?"),
    ("bill_payment_methods", "وين نقدر نخلص الفاتورة؟"),
    ("bill_payment_methods", "وين نقدر نخلص la facture؟"),
    ("bill_payment_methods", "win n9der nkhalas la facture"),


    # --------------------------------------------------------
    # payment_problem
    # --------------------------------------------------------

    ("payment_problem", "Mon paiement a échoué."),
    ("payment_problem", "الدفع ما مشاش"),
    ("payment_problem", "Le paiement ما نجحش"),
    ("payment_problem", "le paiement ma najahch"),

    ("payment_problem", "J'ai un problème avec mon paiement."),
    ("payment_problem", "كاين مشكل في الخلاص تاعي"),
    ("payment_problem", "كاين problème في le paiement"),
    ("payment_problem", "3andi mochkil fel paiement"),


    # --------------------------------------------------------
    # unpaid_bill
    # --------------------------------------------------------

    ("unpaid_bill", "J'ai une facture impayée."),
    ("unpaid_bill", "عندي فاتورة ما خلصتهاش"),
    ("unpaid_bill", "عندي une facture impayée"),
    ("unpaid_bill", "3andi facture ma khlasthech"),

    ("unpaid_bill", "Je n'ai pas encore payé ma facture."),
    ("unpaid_bill", "مازال عليا فاتورة"),
    ("unpaid_bill", "مازال ما خلصتش la facture"),
    ("unpaid_bill", "mazal ma khlastch la facture"),


    # --------------------------------------------------------
    # bill_not_received
    # --------------------------------------------------------

    ("bill_not_received", "Je n'ai pas reçu ma facture."),
    ("bill_not_received", "ما وصلتنيش الفاتورة"),
    ("bill_not_received", "مازال ما جاتنيش la facture"),
    ("bill_not_received", "mazal ma jatnich la facture"),

    ("bill_not_received", "Ma facture n'est pas arrivée."),
    ("bill_not_received", "الفاتورة ما جاتنيش"),
    ("bill_not_received", "La facture ما جاتنيش"),
    ("bill_not_received", "la facture ma jatnich"),
]


# ============================================================
# Load models
# ============================================================

print("Loading classifier...")
classifier = joblib.load(CLASSIFIER_PATH)

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# ============================================================
# Prediction
# ============================================================

sentences = [sentence for _, sentence in TEST_DATA]
expected = [intent for intent, _ in TEST_DATA]

embeddings = embedding_model.encode(sentences)
predictions = classifier.predict(embeddings)


# ============================================================
# Overall results
# ============================================================

correct = 0

print("\n" + "=" * 80)
print("BASELINE EVALUATION")
print("=" * 80)

for sentence, expected_intent, predicted_intent in zip(
    sentences,
    expected,
    predictions
):
    is_correct = expected_intent == predicted_intent

    if is_correct:
        correct += 1

    symbol = "✓" if is_correct else "✗"

    print(f"\n{symbol}")
    print(f"Sentence : {sentence}")
    print(f"Expected : {expected_intent}")
    print(f"Predicted: {predicted_intent}")


accuracy = correct / len(TEST_DATA)

print("\n" + "=" * 80)
print(f"Overall accuracy: {correct}/{len(TEST_DATA)} = {accuracy:.2%}")
print("=" * 80)


# ============================================================
# Results by intent
# ============================================================

results = defaultdict(lambda: {"correct": 0, "total": 0})

for expected_intent, predicted_intent in zip(expected, predictions):
    results[expected_intent]["total"] += 1

    if expected_intent == predicted_intent:
        results[expected_intent]["correct"] += 1


print("\nAccuracy by intent:")
print("-" * 50)

for intent, result in results.items():
    intent_accuracy = result["correct"] / result["total"]

    print(
        f"{intent:25s} "
        f"{result['correct']}/{result['total']} "
        f"= {intent_accuracy:.2%}"
    )