from pathlib import Path
import re


# ============================================================
# CONFIGURATION
# ============================================================

RAG_DOCUMENTS_DIR = Path("rag_documents")


# ============================================================
# INTENT → KNOWLEDGE MAPPING
# ============================================================

INTENT_DOCUMENTS = {

    "bill_not_received": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    "bill_payment_methods": [
        Path("rag_documents/facture/paiement.md"),
    ],

    "online_bill_payment": [
        Path("rag_documents/facture/paiement.md"),
    ],

    "understand_bill": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    "update_customer_information": [
        Path("rag_documents/facture/faq_facture.md"),
    ],

    "electricity_outage": [
        Path("rag_documents/panne/faq_panne.md"),
    ],

    "payment_problem": [],

    "bill_payment_deadline": [],

    "unpaid_bill": [],

        "damaged_appliance": [
        Path("rag_documents/panne/faq_panne.md"),
    ],

    "meter_problem": [
        Path("rag_documents/panne/compteur.md"),
    ],
}


# ============================================================
# INTENT → SECTION MAPPING
# ============================================================

INTENT_SECTIONS = {

    "bill_not_received": [
        "Non-réception de la facture",
    ],

    "bill_payment_methods": [
        "Paiement selon la FAQ Sonelgaz",
    ],

    "online_bill_payment": [
        "Paiement électronique — BaridiMob",
    ],

    "understand_bill": [
        "Problème concernant la facture",
    ],

    "update_customer_information": [
        "Modification des informations client",
    ],

    "electricity_outage": [
        "Perturbation de l'alimentation électrique",
    ],

    "payment_problem": [],

    "bill_payment_deadline": [],

    "unpaid_bill": [],

    "damaged_appliance": [
        "Dommages aux appareils après une perturbation de tension",
    ],

    "meter_problem": [
        "Compteur défectueux ou problème de fonctionnement",
    ],
}


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():
    """
    Load all Markdown documents from rag_documents/.

    Returns:
        dict:
            {
                Path(...): "document content"
            }
    """

    documents = {}

    if not RAG_DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"RAG documents directory not found: "
            f"{RAG_DOCUMENTS_DIR}"
        )

    for file_path in RAG_DOCUMENTS_DIR.rglob("*.md"):

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            documents[file_path] = content

        except Exception as error:

            print(
                f"Warning: could not read "
                f"{file_path}: {error}"
            )

    return documents


# ============================================================
# PARSE DOCUMENT METADATA
# ============================================================

def extract_metadata(content):
    """
    Extract simple key/value metadata from the beginning
    of a Markdown document.
    """

    metadata = {}

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        # Stop once the first Markdown heading begins.
        if line.startswith("#"):
            break

        match = re.match(
            r"^([A-Za-z_]+):\s*(.+)$",
            line
        )

        if match:

            key = match.group(1).strip()
            value = match.group(2).strip()

            metadata[key] = value

    return metadata


# ============================================================
# SPLIT DOCUMENT INTO SECTIONS
# ============================================================

def extract_sections(content):
    """
    Split a Markdown document into ## sections.

    Returns:
        list of dictionaries:
            {
                "title": "...",
                "content": "..."
            }
    """

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

            sections.append(
                {
                    "title": title,
                    "content": section_content,
                }
            )

    return sections


# ============================================================
# BUILD KNOWLEDGE BASE
# ============================================================

def build_knowledge_base():
    """
    Load all RAG documents and convert them into structured
    knowledge sections.
    """

    documents = load_documents()

    knowledge_base = {}

    for file_path, content in documents.items():

        metadata = extract_metadata(content)
        sections = extract_sections(content)

        knowledge_base[file_path] = {
            "metadata": metadata,
            "sections": sections,
        }

    return knowledge_base


# ============================================================
# FIND DOCUMENTS FOR INTENT
# ============================================================

def get_documents_for_intent(intent):
    """
    Return the RAG documents associated with an intent.
    """

    return INTENT_DOCUMENTS.get(
        intent,
        []
    )


# ============================================================
# RETRIEVE KNOWLEDGE
# ============================================================

def retrieve_response(intent, knowledge_base=None):
    """
    Retrieve only the verified knowledge sections
    associated with the predicted intent.

    No response is invented by this function.
    """

    if knowledge_base is None:
        knowledge_base = build_knowledge_base()

    document_paths = get_documents_for_intent(intent)

    # No document mapped to this intent
    if not document_paths:

        return {
            "intent": intent,
            "found": False,
            "source": None,
            "source_url": None,
            "response": (
                "Aucune information vérifiée n'est "
                "actuellement disponible dans la base "
                "de connaissances pour cette intention."
            ),
            "sections": [],
        }

    # Sections allowed for this intent
    allowed_sections = INTENT_SECTIONS.get(
        intent,
        []
    )

    results = []

    # --------------------------------------------------------
    # Search mapped documents
    # --------------------------------------------------------

    for document_path in document_paths:

        document = knowledge_base.get(
            document_path
        )

        if document is None:
            continue

        metadata = document["metadata"]

        # ----------------------------------------------------
        # Search sections inside the document
        # ----------------------------------------------------

        for section in document["sections"]:

            title = section["title"]

            # Never return the question-list section
            if title.lower().startswith("questions"):
                continue

            # If the intent has specific sections,
            # only retrieve those sections.
            if title not in allowed_sections:
                continue

            results.append(
                {
                    "title": title,
                    "content": section["content"],
                    "source": metadata.get("source"),
                    "source_url": metadata.get("source_url"),
                    "file": document_path,
                }
            )

    # --------------------------------------------------------
    # Nothing relevant found
    # --------------------------------------------------------

    if not results:

        return {
            "intent": intent,
            "found": False,
            "source": None,
            "source_url": None,
            "response": (
                "Aucune information pertinente "
                "n'a été trouvée dans la base "
                "de connaissances."
            ),
            "sections": [],
        }

    # --------------------------------------------------------
    # Build readable response
    # --------------------------------------------------------

    response_parts = []

    for result in results:

        response_parts.append(
            f"{result['content']}"
        )

    response = "\n\n".join(
        response_parts
    )

    # --------------------------------------------------------
    # Return structured result
    # --------------------------------------------------------

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

    print(
        f"Loaded {len(knowledge_base)} documents."
    )

    print("\nAvailable documents:")

    for file_path in sorted(knowledge_base):

        sections = knowledge_base[
            file_path
        ]["sections"]

        print(
            f"  - {file_path} "
            f"({len(sections)} sections)"
        )

    print("\nTest retrieval:")

    test_intents = [
        "bill_not_received",
        "how_to_pay",
        "payment_problem",
        "unpaid_bill",
    ]

    for test_intent in test_intents:

        result = retrieve_response(
            test_intent,
            knowledge_base,
        )

        print(
            f"\nIntent: {test_intent}"
        )

        print(
            f"Found: {result['found']}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Response:\n{result['response']}"
        )