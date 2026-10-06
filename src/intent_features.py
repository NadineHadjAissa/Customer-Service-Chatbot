import re
import numpy as np


# ============================================================
# INTENT SIGNALS
# ============================================================

SIGNALS = {

    # --------------------------------------------------------
    # HOW TO PAY / PAYMENT METHODS
    # --------------------------------------------------------

    "how_to_pay": [

        # French / English
        r"\bcomment\b.*\b(payer|paie|paiement|rÃ©gler|regler)\b",
        r"\bcomment\b.*\b(faire)\b.*\b(payer|rÃ©gler|regler)\b",
        r"\bhow\b.*\b(pay|payment)\b",
        r"\bwhere\b.*\b(pay|payer)\b",
        r"\bou\b.*\bpayer\b",
        r"\boÃ¹\b.*\bpayer\b",

        # Darja / Arabizi
        r"\bkifach\b.*\b(nkhalas|nkhlas|n9der|payer|paye)\b",
        r"\bkifeh\b.*\b(nkhalas|nkhlas|n9der)\b",
        r"\bwin\b.*\b(nkhalas|nkhlas|payer|paye)\b",
        r"\bfin\b.*\b(nkhalas|nkhlas|payer|paye)\b",

        r"ÙƒÙŠÙØ§Ø´.*(Ù†Ø®Ù„Øµ|Ù†Ù‚Ø¯Ø± Ù†Ø®Ù„Øµ|Ù†Ø¯ÙŠØ±)",
        r"ÙƒÙŠÙ.*(Ù†Ø®Ù„Øµ|Ù†Ù‚Ø¯Ø± Ù†Ø®Ù„Øµ)",
        r"ÙˆÙŠÙ†.*(Ù†Ø®Ù„Øµ|Ù†Ù‚Ø¯Ø± Ù†Ø®Ù„Øµ)",
        r"ÙÙŠÙ†.*(Ù†Ø®Ù„Øµ|Ù†Ù‚Ø¯Ø± Ù†Ø®Ù„Øµ)",

        # Payment-method questions
        r"\b(bwach|b[ae]ch)\b.*\b(nkhalas|nkhlas|payer)\b",
        r"\b(way|ways|means|method|methods)\b.*\b(pay|payment)\b",
        r"\b(moyens|mÃ©thodes|methodes|faÃ§ons|facons)\b.*\b(paiement|payer)\b",

        r"Ø¨ÙˆØ§Ø´.*(Ù†Ø®Ù„Øµ|Ø§Ù„Ø¯ÙØ¹)",
        r"ÙˆØ´.*(Ø·Ø±Ù‚|ÙˆØ³Ø§Ø¦Ù„).*Ø§Ù„Ø¯ÙØ¹",
        r"ÙˆØ§Ø´.*(Ø·Ø±Ù‚|ÙˆØ³Ø§Ø¦Ù„).*Ø§Ù„Ø¯ÙØ¹",
        r"Ø¨Ø£ÙŠ Ø·Ø±ÙŠÙ‚Ø©.*(Ù†Ø®Ù„Øµ|Ø§Ù„Ø¯ÙØ¹)",
    ],


        # --------------------------------------------------------
    # ONLINE / REMOTE PAYMENT
    # --------------------------------------------------------

    "online_payment": [

        # French / English
        r"\ben ligne\b",
        r"\bonline\b",
        r"\binternet\b",
        r"\bplateforme\b",
        r"\bsite\b",
        r"\bapplication\b",
        r"\bapp\b",
        r"\btÃ©lÃ©phone\b",
        r"\btelephone\b",
        r"\bÃ  distance\b",
        r"\ba distance\b",
        r"\bpar tÃ©lÃ©phone\b",
        r"\bpar internet\b",

        # Darja / Arabizi
        r"\bonline\b",
        r"\bplateforme\b",
        r"\bsite\b",
        r"\bapplication\b",
        r"\btÃ©lÃ©phone\b",
        r"\btelephone\b",
        r"\binternet\b",

        # Arabic
        r"Ù…ÙˆÙ‚Ø¹",
        r"Ù…Ù†ØµØ©",
        r"Ø§Ù„Ù‡Ø§ØªÙ",
        r"ØªÙ„ÙÙˆÙ†",
        r"Ø§Ù„ØªÙ„ÙÙˆÙ†",
        r"Ø§Ù„Ø¥Ù†ØªØ±Ù†Øª",
        r"Ø§Ù†ØªØ±Ù†Øª",
        r"Ø¥Ù„ÙƒØªØ±ÙˆÙ†ÙŠ",
        r"\u062a\u0637\u0628\u064a\u0642",
        r"\u0627\u0644\u062a\u0637\u0628\u064a\u0642",
        r"Ø¹Ù† Ø¨Ø¹Ø¯",
    ],


    # --------------------------------------------------------
    # PAYMENT PROBLEM
    # --------------------------------------------------------

    # IMPORTANT:
    # Generic words such as "payment", "paiement", or "Ø§Ù„Ø®Ù„Ø§Øµ"
    # are intentionally NOT enough to trigger this feature.
    #
    # We require an actual problem/failure/refusal/error signal.

    "payment_problem": [

        # Explicit problem words
        r"\bproblem\b",
        r"\bproblÃ¨me\b",
        r"\bprobleme\b",
        r"\bmochkil\b",
        r"\bmochkel\b",

        r"Ù…Ø´ÙƒÙ„",
        r"Ù…Ø´ÙƒÙ„Ø©",
        r"Ù…Ø´Ø§ÙƒÙ„",

        # Failure / refusal / error
        r"\berreur\b",
        r"\berror\b",
        r"\bfailed\b",
        r"\bfail\b",
        r"\brefused\b",
        r"\brefuse\b",
        r"\brejected\b",
        r"\breject\b",
        r"\bblocked\b",
        r"\bblocage\b",
        r"\bbloquÃ©\b",
        r"\nbloque\b",
        r"\bÃ©chouÃ©\b",
        r"\bechoue\b",

        # French expressions
        r"paiement.*(Ã©chouÃ©|echoue|refusÃ©|refuse|bloquÃ©|bloque)",
        r"paiement.*ne fonctionne pas",
        r"paiement.*ne marche pas",
        r"paiement.*impossible",
        r"transaction.*(refusÃ©e|refusee|Ã©choue|echoue)",
        r"transaction.*ne passe pas",
        r"n.?arrive pas.*payer",
        r"ne peux pas.*payer",
        r"impossible.*payer",

        # Darja / Arabizi
        r"Ù…Ø§.*(Ù‚Ø¯Ø±ØªØ´|Ù†Ù‚Ø¯Ø±Ø´).*Ø®Ù„Øµ",
        r"Ù…Ø§.*(Ù…Ø´Ø§Ø´|Ù†Ø¬Ø­Ø´|ØªÙ‚Ø¨Ù„Ø´|ØªØ¯ÙˆØ²Ø´).*Ø§Ù„Ø¯ÙØ¹",
        r"Ù…Ø§.*(Ù…Ø´Ø§Ø´|Ù†Ø¬Ø­Ø´|ØªÙ‚Ø¨Ù„Ø´|ØªØ¯ÙˆØ²Ø´).*Ø§Ù„Ø®Ù„Ø§Øµ",

        r"Ø§Ù„Ø¯ÙØ¹.*(Ù…Ø§ Ù…Ø´Ø§Ø´|Ù…Ø§ Ù†Ø¬Ø­Ø´|Ù…Ø¨Ù„ÙˆÙƒÙŠ|Ù…Ø±ÙÙˆØ¶|ØªØ±ÙØ¶)",
        r"Ø§Ù„Ø®Ù„Ø§Øµ.*(Ù…Ø§ Ù…Ø´Ø§Ø´|Ù…Ø§ Ù†Ø¬Ø­Ø´|Ù…Ø¨Ù„ÙˆÙƒÙŠ|Ù…Ø±ÙÙˆØ¶|ØªØ±ÙØ¶)",

        r"Ù…Ø§ Ù‚Ø¯Ø±ØªØ´.*(Ù†Ø®Ù„Øµ|Ù†ÙƒÙ…Ù„).*Ø§Ù„Ø¯ÙØ¹",
        r"Ù…Ø§ Ù‚Ø¯Ø±ØªØ´.*(Ù†Ø®Ù„Øµ|Ù†ÙƒÙ…Ù„).*paiement",
        r"Ù…Ø§ Ù†Ù‚Ø¯Ø±Ø´.*(Ù†Ø®Ù„Øµ|Ù†ÙƒÙ…Ù„).*Ø§Ù„Ø¯ÙØ¹",

        r"Ø¹Ù†Ø¯ÙŠ.*(Ù…Ø´ÙƒÙ„|Ù…Ø´ÙƒÙ„Ø©).*Ø§Ù„Ø¯ÙØ¹",
        r"ÙƒØ§ÙŠÙ†.*(Ù…Ø´ÙƒÙ„|Ù…Ø´ÙƒÙ„Ø©).*Ø§Ù„Ø¯ÙØ¹",
        r"Ø¹Ù†Ø¯ÙŠ.*(Ù…Ø´ÙƒÙ„|Ù…Ø´ÙƒÙ„Ø©).*Ø§Ù„Ø®Ù„Ø§Øµ",
        r"ÙƒØ§ÙŠÙ†.*(Ù…Ø´ÙƒÙ„|Ù…Ø´ÙƒÙ„Ø©).*Ø§Ù„Ø®Ù„Ø§Øµ",

        r"\bmochkil\b.*\b(paiement|payment|khlas|khla[st]|nkhalas)\b",
        r"\bproblem\b.*\b(paiement|payment|khlas|nkhalas)\b",

        r"\bma\b.*\b(mchach|naj7ch|trefed|tdouzch)\b.*\b(paiement|payment|nkhalas)\b",

        # "payment doesn't work"
        r"paiement.*marche pas",
        r"paiement.*marche[p ]?pas",
        r"payment.*doesn.?t work",
        r"payment.*not working",
    ],


    # --------------------------------------------------------
    # BILL NOT RECEIVED
    # --------------------------------------------------------

    "bill_not_received": [

        # French
        r"pas reÃ§u.*facture",
        r"pas recue.*facture",
        r"n.?ai pas reÃ§u.*facture",
        r"n.?ai pas recue.*facture",
        r"facture.*pas reÃ§ue",
        r"facture.*pas recue",
        r"facture.*n.?est pas arrivÃ©e",
        r"facture.*n.?est pas arrivee",

        # English
        r"not received.*bill",
        r"didn.?t receive.*bill",
        r"have not received.*bill",
        r"haven.?t received.*bill",
        r"bill.*not received",

        # Darja / Arabizi â€” common forms
        r"ma jatnich.*facture",
        r"ma jatnich.*facture",
        r"ma wslatlich.*facture",
        r"ma waslatnich.*facture",
        r"ma wslatch.*facture",
        r"ma wasletlich.*facture",
        r"ma wslatlich.*facture",

        r"facture.*ma jatnich",
        r"facture.*ma wslatlich",
        r"facture.*ma waslatnich",
        r"facture.*ma wslatch",

        # "I didn't find / see my bill"
        r"ma l9itch.*facture",
        r"ma l9it.*facture",
        r"facture.*ma banetlich",
        r"ma banetlich.*facture",

        # Arabizi spelling of "mal79tnich"
        # Common informal spelling meaning the bill wasn't received/found.
        r"mal79tnich.*facture",
        r"mal9tnich.*facture",
        r"mal9itnich.*facture",

        # Darja Arabic
        r"Ù…Ø§ Ø¬Ø§ØªÙ†ÙŠØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§ ÙˆØµÙ„ØªØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§ ÙˆØµÙ„ØªÙ†ÙŠØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§ Ù„Ù‚ÙŠØªØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ø§Ù„ÙØ§ØªÙˆØ±Ø©.*Ù…Ø§ Ø¬Ø§ØªÙ†ÙŠØ´",
        r"Ø§Ù„ÙØ§ØªÙˆØ±Ø©.*Ù…Ø§ ÙˆØµÙ„ØªØ´",
        r"Ø§Ù„ÙØ§ØªÙˆØ±Ø©.*Ù…Ø§ ÙˆØµÙ„ØªÙ†ÙŠØ´",
        r"Ø§Ù„ÙØ§ØªÙˆØ±Ø©.*Ù…Ø§ Ù„Ù‚ÙŠØªØ´",

        # General "still waiting for the bill"
        r"mazal.*(n?stanna|n?tsenna).*facture",
        r"mazal.*(n?stanna|n?tsenna).*facture",
        r"mazal.*facture.*ma.*(jat|wsl|wasl)",

        r"Ù…Ø§Ø²Ø§Ù„.*(Ù†Ø³ØªÙ†Ù‰|Ù†Ø³ØªÙ†Ø§).*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§Ø²Ø§Ù„.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©.*Ù…Ø§.*(Ø¬Ø§Øª|ÙˆØµÙ„Øª)",
    ],


    # --------------------------------------------------------
    # UNPAID BILL
    # --------------------------------------------------------

    "unpaid_bill": [

        # French
        r"facture.*impayÃ©e",
        r"facture.*impayee",
        r"pas payÃ©.*facture",
        r"pas paye.*facture",
        r"n.?ai pas.*payÃ©.*facture",
        r"n.?ai pas.*paye.*facture",
        r"pas encore payÃ©.*facture",
        r"pas encore paye.*facture",

        # English
        r"bill.*not paid",
        r"bill.*unpaid",
        r"not paid.*bill",
        r"haven.?t paid.*bill",
        r"didn.?t pay.*bill",

        # Darja / Arabizi
        r"ma khlastch.*facture",
        r"ma khlasthech.*facture",
        r"ma khlastch.*facture",
        r"mazal.*ma.*khlastch.*facture",
        r"mazal.*ma.*khlasthech.*facture",

        r"mazal.*(khla|khlas|pay).*facture",
        r"mazal.*3liya.*facture",
        r"ba9i.*3liya.*facture",
        r"ba9i.*(nkhalas|nkhalles).*facture",

        # Arabic
        r"Ù…Ø§ Ø®Ù„ØµØªØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§ Ø®Ù„ØµØªÙ‡Ø§Ø´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§Ø²Ø§Ù„.*Ù…Ø§ Ø®Ù„ØµØªØ´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§Ø²Ø§Ù„.*Ù…Ø§ Ø®Ù„ØµØªÙ‡Ø§Ø´.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ù…Ø§Ø²Ø§Ù„.*Ø¹Ù„ÙŠØ§.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",
        r"Ø¨Ø§Ù‚ÙŠ.*Ø¹Ù„ÙŠØ§.*Ø§Ù„ÙØ§ØªÙˆØ±Ø©",

        # Explicit unpaid status
        r"\bimpayÃ©e\b",
        r"\bimpayee\b",
        r"\bunpaid\b",
        r"\bnon.?payÃ©e\b",
        r"\bnon.?payee\b",
    ],
}


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_intent_features(texts):
    """
    Create explicit binary-style intent features.

    Each matched intent signal receives a value of 3.0.
    Otherwise the feature receives 0.0.

    Feature order:
        1. how_to_pay
        2. payment_problem
        3. bill_not_received
        4. unpaid_bill
    """

    features = []

    for text in texts:

        text = str(text).lower().strip()

        row = []

        for patterns in SIGNALS.values():

            matched = any(
                re.search(
                    pattern,
                    text,
                    flags=re.IGNORECASE
                )
                for pattern in patterns
            )

            row.append(
                3.0 if matched else 0.0
            )

        features.append(row)

    return np.asarray(
        features,
        dtype=np.float32
    )
