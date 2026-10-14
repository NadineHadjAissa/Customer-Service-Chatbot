
import re
import unicodedata

OUT_OF_SCOPE_PATTERNS = [
    "billet d'avion",
    "prix d'un billet",
    "vol pour paris",
    "hotel a paris",
    "prix du gaz en algérie",
    "cours du gaz",
    "prix du gaz naturel sur le marché",
]

def is_explicitly_out_of_scope(text):
    normalized = normalize_for_domain_check(text)

    return any(
        normalize_for_domain_check(phrase) in normalized
        for phrase in OUT_OF_SCOPE_PATTERNS
    )

# Common terms related to Sonelgaz services.
DOMAIN_TERMS = [
    # French
    "sonelgaz",
    "facture",
    "electricite",
    "gaz",
    "compteur",
    "index",
    "consommation",
    "raccordement",
    "branchement",
    "panne",
    "coupure",
    "courant",
    "tension",
    "disjoncteur",
    "paiement",
    "payer",
    "impaye",
    "reglement",
    "regularisation",
    "rattrapage",
    "reclamation",
    "releve",
    "montant",
    "agence commerciale",
    "abonnement",
    "kwh",
    "kilowattheure",
    "electricite coupee",
    "facture trop chere",
    "facture elevee",
    "facture trop elevee",
    "nouveau compteur",
    "nouveau branchement",
    "nouvelle connexion",
    "installer un compteur",
    "payer en ligne",
    "baridimob",
    "edahabia",
    "coupure de courant",
    "panne electrique",
    "fuite de gaz",

    # Common Darja / Arabizi expressions
    "daw",
    "dou",
    "kahraba",
    "khallas",
    "khalast",
    "ma khallastch",
    "ma kayench daw",
    "houma",
    "ra9em compteur",
    "facture ta3i",
    "compteur ta3i",
]


GREETINGS = {
    "bonjour",
    "bonsoir",
    "salut",
    "salam",
    "salam alikoum",
    "salam alaikum",
    "assalamu alaikum",
    "hello",
    "hi",
    "saha",
}


def normalize_for_domain_check(text):
    """Normalize accents, casing and extra whitespace."""
    text = text.lower().strip()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    text = re.sub(r"\s+", " ", text)

    return text
def is_explicitly_out_of_scope(text):
    normalized = normalize_for_domain_check(text)

    return any(
        normalize_for_domain_check(phrase) in normalized
        for phrase in OUT_OF_SCOPE_PATTERNS
    )


def is_greeting(text):
    """Return True for a standalone greeting."""
    normalized = normalize_for_domain_check(text)

    # Remove common final punctuation.
    normalized = re.sub(r"[.!?,;]+$", "", normalized)

    return normalized in GREETINGS


def is_sonelgaz_related(text):
    """
    First-pass keyword filter.

    This is a heuristic, not a definitive domain classifier.
    """
    normalized = normalize_for_domain_check(text)

    for term in DOMAIN_TERMS:
        term_normalized = normalize_for_domain_check(term)

        pattern = (
            r"(?<!\w)"
            + re.escape(term_normalized)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized):
            return True

    return False
