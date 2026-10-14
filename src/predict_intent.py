import os
import re
import joblib
import numpy as np

from sentence_transformers import SentenceTransformer
from src.preprocessing import normalize_text
from src.intent_features import extract_intent_features
from src.domain_filter import (
    is_sonelgaz_related,
    is_greeting,
    is_explicitly_out_of_scope,
)


# ============================================================
# CONFIGURATION
# ============================================================

CLASSIFIER_PATH = os.environ.get(
    "INTENT_CLASSIFIER_PATH",
    "models/intent_classifier_merged_test.joblib",
)


# ============================================================
# LOAD MODEL
# ============================================================

artifact = joblib.load(CLASSIFIER_PATH)

classifier = artifact["classifier"]
representation = artifact["representation"]

embedding_model = SentenceTransformer(
    artifact["embedding_model_name"]
)


# ============================================================
# TEXT NORMALIZATION FOR RULES
# ============================================================

def normalize_for_rules(text):
    text = normalize_text(text)
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    replacements = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "î": "i",
        "ï": "i",
        "ô": "o",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ç": "c",
        "œ": "oe",
        "'": " ",
        "’": " ",
        "-": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return re.sub(r"\s+", " ", text).strip()


def matches_any(text, patterns):
    return any(re.search(pattern, text) for pattern in patterns)


# ============================================================
# RULE-BASED INTENT CORRECTIONS
# ============================================================

def rule_based_intent(text):
    text = normalize_for_rules(text)

    if not text:
        return None

    # --------------------------------------------------------
    # 1. GAS EMERGENCY
    # --------------------------------------------------------

    gas_smell_patterns = [
        r"\brihet gaz\b",
        r"\briha ta3 gaz\b",
        r"\brihet ta3 gaz\b",
        r"\bkayen rihet gaz\b",
        r"\bodeur de gaz\b",
        r"\bsmell of gas\b",
        r"\bgas leak\b",
        r"\bfuite de gaz\b",
        r"\bfuite gaz\b",
        r"\bje sens le gaz\b",
        r"\bca sent le gaz\b",
        r"\bsent le gaz\b",
        r"\bgaz leak\b",
    ]

    if matches_any(text, gas_smell_patterns):
        return "gas_emergency"

    # --------------------------------------------------------
    # 2. PAYMENT MADE BUT STATUS NOT UPDATED
    # --------------------------------------------------------

    payment_made_patterns = [
        r"\bpaye\b",
        r"\bpaiement effectue\b",
        r"\bpaid\b",
        r"\bi paid\b",
        r"\bkhalest\b",
        r"\bkhellest\b",
        r"\bkhalasst\b",
    ]

    payment_problem_patterns = [
        r"\bpas apparu\b",
        r"\bn apparait pas\b",
        r"\bnot showing\b",
        r"\bnot reflected\b",
        r"\bpayment.*not.*appear\b",
        r"\btoujours impaye\b",
        r"\btoujours unpaid\b",
        r"\bma banach\b",
        r"\bma banlich\b",
        r"\bmazal.*impaye\b",
        r"\bpayment.*pending\b",
        r"\bstill unpaid\b",
    ]

    if (
        matches_any(text, payment_made_patterns)
        and matches_any(text, payment_problem_patterns)
    ):
        return "paid_but_unpaid_status"

    # --------------------------------------------------------
    # 3. ONLINE BILL PAYMENT
    # --------------------------------------------------------

    online_payment_patterns = [
        r"\bpay online\b",
        r"\bpay my bill online\b",
        r"\bhow can i pay.*online\b",
        r"\bhow do i pay.*online\b",
        r"\bhow to pay.*online\b",
        r"\bonline bill payment\b",
        r"\bpaiement en ligne\b",
        r"\bpayer en ligne\b",
        r"\bkhaless en ligne\b",
        r"\bnkhaless en ligne\b",
        r"\bpayment online\b",
    ]

    if matches_any(text, online_payment_patterns):
        return "online_bill_payment"

    # --------------------------------------------------------
    # 4. BILL PAYMENT METHODS
    # --------------------------------------------------------

    payment_method_patterns = [
        r"\bkifach nkhaless\b",
        r"\bkifach nkhalas\b",
        r"\bkifach nkhalles\b",
        r"\bkifach nkhelles\b",
        r"\bwin nkhaless\b",
        r"\bwin nkhalas\b",
        r"\bou payer\b",
        r"\bcomment payer\b",
        r"\bhow can i pay\b",
        r"\bhow do i pay\b",
        r"\bhow to pay\b",
        r"\bpayment methods\b",
        r"\bwach n9der nkhaless\b",
        r"\bn9der nkhaless\b",
        r"\bpayer ma facture\b",
        r"\bkhaless la facture\b",
    ]

    if matches_any(text, payment_method_patterns):
        return "bill_payment_methods"

    # --------------------------------------------------------
    # 5. DUPLICATE BILLS
    # --------------------------------------------------------

    duplicate_bill_patterns = [
        r"\bdeux factures pour la meme periode\b",
        r"\bdouble facture\b",
        r"\bfacture en double\b",
        r"\bduplicate bills?\b",
        r"\btwo bills for the same period\b",
        r"\btwo invoices for the same period\b",
        r"\bdeux factures pour la meme periode\b",
    ]

    if matches_any(text, duplicate_bill_patterns):
        return "bill_amount_issue"

    # --------------------------------------------------------
    # 6. METER PROBLEMS
    # --------------------------------------------------------

    meter_problem_patterns = [
        r"\ble compteur affiche\b",
        r"\bcompteur affiche des chiffres\b",
        r"\bcompteur tourne trop vite\b",
        r"\bmon compteur tourne vite\b",
        r"\bcompteur defectueux\b",
        r"\bcompteur ne fonctionne pas\b",
        r"\bmeter is running too fast\b",
        r"\bmeter displays strange numbers\b",
        r"\bmeter shows strange numbers\b",
        r"\bfaulty meter\b",
        r"\bcompteur tourne anormalement\b",
        r"\bchiffres bizarres\b",
    ]

    if matches_any(text, meter_problem_patterns):
        return "meter_problem"

    # --------------------------------------------------------
    # 7. GAS AVAILABLE IN NEIGHBORHOOD BUT NOT AT HOME
    # --------------------------------------------------------

    gas_local_supply_patterns = [
        r"\bgaz kayen fel houma mais machi fel dar\b",
        r"\blgaz kayen fel houma mais machi fel dar\b",
        r"\bgaz.*disponible.*quartier.*pas.*maison\b",
        r"\bgas.*available.*neighborhood.*not.*home\b",
    ]

    if matches_any(text, gas_local_supply_patterns):
        return "gas_outage"

    # --------------------------------------------------------
    # 8. POWER RESTORATION QUESTIONS
    # --------------------------------------------------------

    restoration_patterns = [
        r"\bimta yarja3 daw\b",
        r"\bimta yerja3 daw\b",
        r"\bimta yarja3.*courant\b",
        r"\bwhen will the power return\b",
        r"\bwhen will electricity return\b",
        r"\bwhen will the electricity come back\b",
        r"\bwhen will power be restored\b",
        r"\bwhen is the power coming back\b",
        r"\bquand revient le courant\b",
        r"\bquand le courant revient\b",
        r"\bquand sera retabli le courant\b",
        r"\bquand est ce que le courant revient\b",
    ]

    if matches_any(text, restoration_patterns):
        return "restoration"

    # --------------------------------------------------------
    # 9. VOLTAGE / INTERMITTENT ELECTRICITY
    # --------------------------------------------------------

    voltage_patterns = [
        r"\byroho w yji\b",
        r"\byrouh w yji\b",
        r"\bdaw.*yroho.*yji\b",
        r"\bdaw.*yrouh.*yji\b",
        r"\byet9ata3 w yerja3\b",
        r"\bvoltage problem\b",
        r"\blow voltage\b",
        r"\bbaisse de tension\b",
        r"\btension instable\b",
        r"\bcourant instable\b",
        r"\bkeeps going on and off\b",
        r"\blights keep flickering\b",
        r"\bcourant.*coupe.*revient\b",
        r"\bdaw yched w ykheli\b",
    ]

    if matches_any(text, voltage_patterns):
        return "voltage_problem"

    # --------------------------------------------------------
    # 10. NEIGHBORHOOD OUTAGE
    # --------------------------------------------------------

    neighborhood_outage_patterns = [
        r"\btout le quartier\b.*\b(courant|electricite|gaz)\b",
        r"\b(courant|electricite|gaz)\b.*\btout le quartier\b",
        r"\bwhole neighborhood\b",
        r"\bwhole neighbourhood\b",
        r"\bentire neighborhood\b",
        r"\bentire neighbourhood\b",
        r"\bhouma kamla\b",
        r"\bfel houma kamla\b",
        r"\bma kayench daw fel houma\b",
        r"\bma kaynch daw fel houma\b",
        r"\bma kayench gaz fel houma\b",
    ]

    if matches_any(text, neighborhood_outage_patterns):
        return "neighborhood_outage"

    # --------------------------------------------------------
    # 11. ELECTRICITY OUTAGE
    # --------------------------------------------------------

    electricity_outage_patterns = [
        r"\bdaw makanch\b",
        r"\bmakanch daw\b",
        r"\bma kayench daw\b",
        r"\bma kaynch daw\b",
        r"\bma kayenchi daw\b",
        r"\bcoupure d electricite\b",
        r"\bplus d electricite\b",
        r"\bpas d electricite\b",
        r"\bno electricity\b",
        r"\belectricity outage\b",
        r"\bpower outage\b",
        r"\bpower is out\b",
        r"\bno power\b",
        r"\bthe electricity is gone\b",
        r"\bthe electricity is off\b",
        r"\bthere is no electricity\b",
        r"\bthere is no power\b",
    ]

    if matches_any(text, electricity_outage_patterns):
        return "electricity_outage"

    # --------------------------------------------------------
    # 12. GAS OUTAGE
    # --------------------------------------------------------

    gas_outage_patterns = [
        r"\blgaz makanch\b",
        r"\bgaz makanch\b",
        r"\blgaz ma ykhdemch\b",
        r"\bgaz ma ykhdemch\b",
        r"\bma kayench gaz\b",
        r"\bma kaynch gaz\b",
        r"\bma kayench lgaz\b",
        r"\bma kaynch lgaz\b",
        r"\bplus de gaz\b",
        r"\bpas de gaz\b",
        r"\bgaz coupe\b",
        r"\bgaz est coupe\b",
        r"\bno gas\b",
        r"\bgas outage\b",
        r"\bno gas supply\b",
        r"\bthe gas is not working\b",
        r"\bchauffage.*plus de gaz\b",
        r"\bthere is no gas\b",
        r"\bthe gas stopped\b",
    ]

    if matches_any(text, gas_outage_patterns):
        return "gas_outage"

    # --------------------------------------------------------
    # 13. REPORT A BREAKDOWN
    # --------------------------------------------------------

    breakdown_patterns = [
        r"\bnbelagh\b",
        r"\bbelagh\b",
        r"\bsignaler une panne\b",
        r"\bsignaler.*probleme\b",
        r"\bdeclarer une panne\b",
        r"\breport a breakdown\b",
        r"\breport a fault\b",
        r"\breport.*outage\b",
        r"\bwho should i call.*outage\b",
        r"\bcontact.*sonelgaz.*coupure\b",
        r"\bصرح\b",
        r"\bنصرح\b",
    ]

    if matches_any(text, breakdown_patterns):
        return "report_breakdown"

    return None


# ============================================================
# INTENT PREDICTION
# ============================================================

def predict_intent(text):
    if not text or not text.strip():
        return [("out_of_scope", 1.0)]

    # Apply explicit intent rules first.
    rule_intent = rule_based_intent(text)

    if rule_intent is not None:
        return [(rule_intent, 1.0)]

    # Handle greetings.
    if is_greeting(text):
        return [("greeting", 1.0)]

    # Reject explicitly unrelated requests.
    if is_explicitly_out_of_scope(text):
        return [("out_of_scope", 1.0)]

    # Check whether the request relates to Sonelgaz.
    if not is_sonelgaz_related(text):
        return [("out_of_scope", 1.0)]

    normalized_text = normalize_text(text)

    embedding = embedding_model.encode(
        [normalized_text],
        convert_to_numpy=True,
    )

    if representation == "embeddings_plus_features":
        features = extract_intent_features([normalized_text])
        X = np.hstack([embedding, features])

    elif representation == "embeddings_only":
        X = embedding

    else:
        raise ValueError(
            f"Unknown model representation: {representation}"
        )

    probabilities = classifier.predict_proba(X)[0]
    top_indices = np.argsort(probabilities)[::-1][:3]

    return [
        (
            classifier.classes_[i],
            float(probabilities[i]),
        )
        for i in top_indices
    ]


# ============================================================
# INTERACTIVE TESTING
# ============================================================

if __name__ == "__main__":
    print("Sonelgaz intent classifier is ready!")
    print("Loaded model:", CLASSIFIER_PATH)
    print("Representation:", representation)
    print("Type 'exit' to stop.\n")

    while True:
        try:
            text = input("Enter a message: ").strip()

            if text.lower() in {"exit", "quit", "quitter"}:
                print("Goodbye!")
                break

            predictions = predict_intent(text)

            for rank, (intent, probability) in enumerate(
                predictions,
                start=1,
            ):
                print(f"{rank}. {intent}: {probability:.3f}")

            print()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break