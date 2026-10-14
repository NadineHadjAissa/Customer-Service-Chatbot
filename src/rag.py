
from pathlib import Path
import re


# ============================================================
# CONFIGURATION
# ============================================================

RAG_DOCUMENTS_DIR = Path("rag_documents")


# ============================================================
# INTENT -> DOCUMENT MAPPING
# ============================================================

INTENT_DOCUMENTS = {
    # FACTURE
    "bill_not_received": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "understand_bill": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "consumption_calculation": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "amount_breakdown": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "rem_r_meaning": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "catch_up_bill": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "bill_amount_issue": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "wrong_meter_reading": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "dispute_estimated_reading": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "paid_but_unpaid_status": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    # PAIEMENT
    "bill_payment_methods": [
        Path("rag_documents/facture/faq_facture.md"),
        Path("rag_documents/facture/paiement.md"),
    ],
    "bill_payment_deadline": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "online_bill_payment": [
        Path("rag_documents/facture/faq_facture.md"),
        Path("rag_documents/facture/paiement.md"),
    ],
    "payment_problem": [
        Path("rag_documents/facture/faq_facture.md"),
        Path("rag_documents/facture/paiement.md"),
    ],
    "unpaid_bill": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    # DISCONNECTION / RESTORATION
    "disconnection": [
        Path("rag_documents/facture/faq_facture.md"),
    ],
    "restoration": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "restoration_after_payment": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    # CUSTOMER INFORMATION
    "update_customer_information": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    # GENERIC BILL QUESTION
    "amount_question": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    # PANNE / DÉPANNAGE
    "electricity_outage": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "neighborhood_outage": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "gas_outage": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "voltage_problem": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "damaged_appliance": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "report_breakdown": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "electrical_danger": [
        Path("rag_documents/panne/faq_panne.md"),
    ],
    "gas_emergency": [
        Path("rag_documents/panne/faq_panne.md"),
    ],

    # COMPTEUR
    "meter_problem": [
        Path("rag_documents/panne/compteur.md"),
    ],

    # RACCORDEMENT
    "connection_procedure": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "new_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "new_construction_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "electricity_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "low_voltage_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "gas_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "electricity_gas_connection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_documents": [
        Path("rag_documents/raccordement/documents_raccordement.md"),
    ],
    "missing_connection_document": [
        Path("rag_documents/raccordement/documents_raccordement.md"),
    ],
    "connection_eligibility": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "network_availability": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "technical_study": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_works": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_cost": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_payment": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_cost_dispute": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_status": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_delay": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_rejection": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_not_completed": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
    "connection_problem": [
        Path("rag_documents/raccordement/procedure_raccordement.md"),
    ],
}


# ============================================================
# INTENT -> SECTION MAPPING
# ============================================================

INTENT_SECTIONS = {
    # FACTURE
    "bill_not_received": ["bill_not_received"],
    "understand_bill": ["understand_bill"],
    "consumption_calculation": ["consumption_calculation"],
    "amount_breakdown": ["amount_breakdown"],
    "rem_r_meaning": ["rem_r_meaning"],
    "catch_up_bill": [
        "catch_up_bill",
        "dispute_catch_up_bill",
    ],
    "bill_amount_issue": [
        "dispute_bill",
        "high_or_abnormal_amount",
    ],
    "wrong_meter_reading": ["wrong_meter_reading"],
    "dispute_estimated_reading": ["dispute_estimated_reading"],
    "paid_but_unpaid_status": ["paid_but_unpaid_status"],

    # PAIEMENT
    "bill_payment_methods": ["bill_payment_methods"],
    "bill_payment_deadline": ["bill_payment_deadline"],
    "online_bill_payment": ["online_bill_payment"],
    "payment_problem": ["payment_problem"],
    "unpaid_bill": ["unpaid_bill"],

    # DISCONNECTION / RESTORATION
    "disconnection": ["disconnection"],
    "restoration": ["restoration"],
    "restoration_after_payment": ["restoration_after_payment"],

    # CUSTOMER INFORMATION
    "update_customer_information": ["update_customer_information"],

    # GENERIC BILL QUESTION
    "amount_question": ["amount_question"],

    # PANNE / DÉPANNAGE
    "electricity_outage": ["electricity_outage"],
    "neighborhood_outage": ["neighborhood_outage"],
    "gas_outage": ["gas_outage"],
    "voltage_problem": ["voltage_problem"],
    "damaged_appliance": ["damaged_appliance"],
    "report_breakdown": ["report_breakdown"],
    "electrical_danger": ["electrical_danger"],
    "gas_emergency": ["gas_emergency"],

    # COMPTEUR
    "meter_problem": ["meter_problem"],

    # RACCORDEMENT
    "connection_procedure": ["connection_procedure"],
    "new_connection": ["new_connection"],
    "new_construction_connection": ["new_construction_connection"],
    "electricity_connection": ["electricity_connection"],
    "low_voltage_connection": ["low_voltage_connection"],
    "gas_connection": ["gas_connection"],
    "electricity_gas_connection": ["electricity_gas_connection"],
    "connection_documents": ["connection_documents"],
    "missing_connection_document": ["missing_connection_document"],
    "connection_eligibility": ["connection_eligibility"],
    "network_availability": ["network_availability"],
    "technical_study": ["technical_study"],
    "connection_works": ["connection_works"],
    "connection_cost": ["connection_cost"],
    "connection_payment": ["connection_payment"],
    "connection_cost_dispute": ["connection_cost_dispute"],
    "connection_status": ["connection_status"],
    "connection_delay": ["connection_delay"],
    "connection_rejection": ["connection_rejection"],
    "connection_not_completed": ["connection_not_completed"],
    "connection_problem": ["connection_problem"],
}


# ============================================================
# QUESTION-AWARE SECTION SELECTION
# ============================================================

def select_sections_for_intent(intent, user_message=""):
    """
    Select the most appropriate section for an intent.
    """

    if intent == "bill_amount_issue":
        text = user_message.lower()

        high_bill_terms = [
            "trop chère",
            "trop cher",
            "trop elevee",
            "trop élevé",
            "trop eleve",
            "anormalement élevé",
            "anormalement eleve",
            "facture élevée",
            "facture elevee",
            "montant élevé",
            "montant eleve",
            "facture chère",
            "facture cher",
            "ghalia",
            "ghali",
        ]

        dispute_terms = [
            "contester",
            "conteste",
            "réclamation",
            "reclamation",
            "erreur sur ma facture",
            "facture incorrecte",
            "montant incorrect",
            "pas correct",
        ]

        if any(term in text for term in high_bill_terms):
            return ["high_or_abnormal_amount"]

        if any(term in text for term in dispute_terms):
            return ["dispute_bill"]

        return ["high_or_abnormal_amount"]

    return INTENT_SECTIONS.get(intent, [])


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():
    """Load all Markdown files from the knowledge directory."""

    documents = {}

    if not RAG_DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"RAG documents directory not found: {RAG_DOCUMENTS_DIR}"
        )

    for file_path in RAG_DOCUMENTS_DIR.rglob("*.md"):
        try:
            content = file_path.read_text(encoding="utf-8")
            documents[file_path] = content
        except Exception as error:
            print(f"Warning: could not read {file_path}: {error}")

    return documents


# ============================================================
# PARSE DOCUMENT METADATA
# ============================================================

def extract_metadata(content):
    """Extract simple key/value metadata from document text."""

    metadata = {}

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        match = re.match(r"^([A-Za-z_]+):\s*(.+)$", line)

        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()

    return metadata


# ============================================================
# SPLIT DOCUMENT INTO SECTIONS
# ============================================================

def extract_sections(content):
    """Split Markdown into sections beginning with ##."""

    sections = []

    pattern = re.compile(
        r"^##\s+(.+?)\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    for match in pattern.finditer(content):
        title = match.group(1).strip()
        section_content = match.group(2).strip()

        if section_content:
            sections.append({
                "title": title,
                "content": section_content,
            })

    return sections


# ============================================================
# BUILD KNOWLEDGE BASE
# ============================================================

def build_knowledge_base():
    """Load documents and organize their sections."""

    documents = load_documents()
    knowledge_base = {}

    for file_path, content in documents.items():
        knowledge_base[file_path] = {
            "metadata": extract_metadata(content),
            "sections": extract_sections(content),
        }

    return knowledge_base


# ============================================================
# FIND DOCUMENTS FOR INTENT
# ============================================================

def get_documents_for_intent(intent):
    """Return the document paths associated with an intent."""

    return INTENT_DOCUMENTS.get(intent, [])


# ============================================================
# RETRIEVE KNOWLEDGE
# ============================================================

def retrieve_response(
    intent,
    knowledge_base=None,
    user_message="",
):
    """
    Retrieve knowledge sections mapped to an intent.

    The original user message is used to choose the most
    appropriate section when an intent has multiple sections.
    """

    if knowledge_base is None:
        knowledge_base = build_knowledge_base()

    document_paths = get_documents_for_intent(intent)

    if not document_paths:
        return {
            "intent": intent,
            "found": False,
            "source": None,
            "source_url": None,
            "response": (
                "Aucune information vérifiée n'est actuellement "
                "disponible dans la base de connaissances pour "
                "cette intention."
            ),
            "sections": [],
        }

    allowed_sections = select_sections_for_intent(
        intent,
        user_message,
    )

    results = []

    for document_path in document_paths:
        document = knowledge_base.get(document_path)

        if document is None:
            continue

        metadata = document["metadata"]

        for section in document["sections"]:
            title = section["title"]

            if title.lower().startswith("questions"):
                continue

            if title not in allowed_sections:
                continue

            results.append({
                "title": title,
                "content": section["content"],
                "source": metadata.get("source"),
                "source_url": metadata.get("source_url"),
                "file": document_path,
            })

    if not results:
        return {
            "intent": intent,
            "found": False,
            "source": None,
            "source_url": None,
            "response": (
                "Aucune information pertinente n'a été trouvée "
                "dans la base de connaissances."
            ),
            "sections": [],
        }

    # Remove duplicate section contents while preserving order.
    response_parts = []
    seen_contents = set()

    for result in results:
        content = result["content"].strip()

        if content and content not in seen_contents:
            response_parts.append(content)
            seen_contents.add(content)

    response = "\n\n".join(response_parts)

    # Remove Markdown heading markers from the final answer.
    response = re.sub(
        r"^#{1,6}\s+",
        "",
        response,
        flags=re.MULTILINE,
    )

    return {
        "intent": intent,
        "found": True,
        "source": results[0]["source"],
        "source_url": results[0]["source_url"],
        "response": response,
        "sections": results,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("\nLoading RAG knowledge base...")

    knowledge_base = build_knowledge_base()

    print(f"Loaded {len(knowledge_base)} documents.")

    print("\nAvailable documents:")

    for file_path in sorted(knowledge_base):
        sections = knowledge_base[file_path]["sections"]
        print(f"  - {file_path} ({len(sections)} sections)")

    print("\nTest high-bill response:")

    test_cases = [
        (
            "bill_amount_issue",
            "Pourquoi ma facture est trop chère ?",
        ),
        (
            "bill_amount_issue",
            "Je conteste le montant de ma facture.",
        ),
    ]

    for test_intent, message in test_cases:
        result = retrieve_response(
            test_intent,
            knowledge_base=knowledge_base,
            user_message=message,
        )

        print(f"\nQuestion: {message}")
        print(f"Intent: {result['intent']}")
        print(f"Found: {result['found']}")
        print(f"Sections: {[s['title'] for s in result['sections']]}")
        print(f"Response:\n{result['response']}")
