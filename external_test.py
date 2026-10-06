from sentence_transformers import SentenceTransformer
from joblib import load

TEST_DATA = [
    ("bill_payment_methods", "Comment payer ma facture ?"),
    ("bill_payment_methods", "كيفاش نخلص الفاتورة؟"),
    ("bill_payment_methods", "كيفاش نخلص la facture؟"),
    ("bill_payment_methods", "kifach nkhalas la facture"),
    ("bill_payment_methods", "Où puis-je payer ma facture ?"),
    ("bill_payment_methods", "وين نقدر نخلص الفاتورة؟"),
    ("bill_payment_methods", "وين نقدر نخلص la facture؟"),
    ("bill_payment_methods", "win n9der nkhalas la facture"),

    ("payment_problem", "Mon paiement a échoué."),
    ("payment_problem", "الدفع ما مشاش"),
    ("payment_problem", "Le paiement ما نجحش"),
    ("payment_problem", "le paiement ma najahch"),
    ("payment_problem", "J'ai un problème avec mon paiement."),
    ("payment_problem", "كاين مشكل في الخلاص تاعي"),
    ("payment_problem", "كاين problème في le paiement"),
    ("payment_problem", "3andi mochkil fel paiement"),

    ("unpaid_bill", "J'ai une facture impayée."),
    ("unpaid_bill", "عندي فاتورة ما خلصتهاش"),
    ("unpaid_bill", "عندي une facture impayée"),
    ("unpaid_bill", "3andi facture ma khlasthech"),
    ("unpaid_bill", "Je n'ai pas encore payé ma facture."),
    ("unpaid_bill", "مازال عليا فاتورة"),
    ("unpaid_bill", "مازال ما خلصتش la facture"),
    ("unpaid_bill", "mazal ma khlastch la facture"),

    ("bill_not_received", "Je n'ai pas reçu ma facture."),
    ("bill_not_received", "ما وصلتنيش الفاتورة"),
    ("bill_not_received", "مازال ما جاتنيش la facture"),
    ("bill_not_received", "mazal ma jatnich la facture"),
    ("bill_not_received", "Ma facture n'est pas arrivée."),
    ("bill_not_received", "الفاتورة ما جاتنيش"),
    ("bill_not_received", "La facture ما جاتنيش"),
    ("bill_not_received", "la facture ma jatnich"),
]

model = load("models/intent_classifier.joblib")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

phrases = [x[1] for x in TEST_DATA]
expected = [x[0] for x in TEST_DATA]

X = embedder.encode(phrases, show_progress_bar=False)
predicted = model.predict(X)

correct = 0

for i, (exp, phrase, pred) in enumerate(zip(expected, phrases, predicted), 1):
    status = "✓" if exp == pred else "✗"
    if exp == pred:
        correct += 1
    else:
        print(f"{status} {i}. Expected: {exp} | Predicted: {pred} | {phrase}")

print()
print(f"External accuracy: {correct}/{len(TEST_DATA)} = {correct/len(TEST_DATA):.2%}")
